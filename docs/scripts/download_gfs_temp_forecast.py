#!/usr/bin/env python
"""
Download NCEP GFS 0.25° 2-meter temperature (TMP at 2 m AGL),
compute 1–N-day daily mean temperature from 3-hourly instantaneous fields,
clip to a bounding box, and save as a single NetCDF file
with dims (time, lat, lon).

Notes
-----
For GFS 0.25° on NOMADS:
- 2m temperature is an *instantaneous* forecast field.
- To derive daily means, we AVERAGE the 3-hourly values within each 24-h window.

Daily window convention used here:
- Day 1 (time = init + 24h): average hours [0, 3, 6, ..., 24] if 0 is available,
  otherwise average (3, 6, ..., 24).
- Day 2 (time = init + 48h): average hours (24, 48] i.e., 27, 30, ..., 48
- ...
This avoids double-counting the boundary hour across days.

Example
-------
python download_gfs_t2m_daily.py \
    --outdir data/gfs_t2m \
    --outfile gfs_t2m_ea_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --date 2025-11-30 \
    --cycle 0
"""

import argparse
import datetime as dt
from pathlib import Path
from typing import Dict, List

import numpy as np
import requests
import xarray as xr
from urllib.parse import urlencode

NOMADS_BASE = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"


# --------------------------------------------------------------------------
# Utilities
# --------------------------------------------------------------------------
def log(msg: str) -> None:
    print(f"[info] {msg}")


def build_gfs_url_t2m(
    init_date: dt.date,
    cycle: int,
    fhour: int,
    lon_min: float,
    lon_max: float,
    lat_min: float,
    lat_max: float,
) -> str:
    """
    Build NOMADS GRIB-filter URL for GFS 0.25° 2m temperature at a given forecast hour.
    """
    date_str = init_date.strftime("%Y%m%d")
    file_name = f"gfs.t{cycle:02d}z.pgrb2.0p25.f{fhour:03d}"
    dir_path = f"/gfs.{date_str}/{cycle:02d}/atmos"

    params = {
        "file": file_name,
        # 2m temperature level + variable
        "lev_2_m_above_ground": "on",
        "var_TMP": "on",
        # spatial subset
        "subregion": "",
        "leftlon": str(lon_min),
        "rightlon": str(lon_max),
        "toplat": str(lat_max),
        "bottomlat": str(lat_min),
        "dir": dir_path,
    }

    return NOMADS_BASE + "?" + urlencode(params)


def download_grib(url: str, out_path: Path, max_retries: int = 10) -> None:
    """
    Download a single GRIB2 file with simple retry logic.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, max_retries + 1):
        try:
            with requests.get(url, stream=True, timeout=60) as r:
                if r.status_code == 429:
                    wait = min(60 * attempt, 300)
                    log(
                        f"HTTP 429 from NOMADS (attempt {attempt}/{max_retries}), "
                        f"sleeping {wait} s..."
                    )
                    import time

                    time.sleep(wait)
                    continue

                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            return
        except Exception as exc:  # noqa: BLE001
            if attempt == max_retries:
                raise RuntimeError(
                    f"Failed to download {url} after {max_retries} attempts"
                ) from exc
            wait = min(30 * attempt, 180)
            log(
                f"Error downloading {url} (attempt {attempt}/{max_retries}): "
                f"{exc}. Retrying in {wait} s..."
            )
            import time

            time.sleep(wait)


def open_t2m_from_grib(grib_path: Path) -> xr.DataArray:
    """
    Open a GFS 2m temperature GRIB2 file and return a DataArray (lat, lon).

    Tries to filter to 2m heightAboveGround first; falls back to generic open.
    """
    backend_kwargs = {"indexpath": ""}

    try:
        ds = xr.open_dataset(
            grib_path,
            engine="cfgrib",
            backend_kwargs={
                **backend_kwargs,
                "filter_by_keys": {"typeOfLevel": "heightAboveGround", "level": 2},
            },
        )
    except Exception:
        ds = xr.open_dataset(grib_path, engine="cfgrib", backend_kwargs=backend_kwargs)

    if not ds.data_vars:
        raise RuntimeError(f"No data variables found in {grib_path}")

    # Try to pick the most likely 2m temperature variable
    var_name = None
    for name in ds.data_vars:
        lower = name.lower()
        attrs = ds[name].attrs
        long = (attrs.get("long_name", "") + " " + attrs.get("name", "")).lower()
        if any(k in lower for k in ("t2m", "tmp", "2t", "temperature")) and (
            "2 m" in long or "2m" in long or "above ground" in long or "height" in long or True
        ):
            var_name = name
            break

    if var_name is None:
        var_name = list(ds.data_vars)[0]

    da = ds[var_name]

    # Unify coordinate names
    if "latitude" in da.dims:
        da = da.rename({"latitude": "lat"})
    if "longitude" in da.dims:
        da = da.rename({"longitude": "lon"})

    # Drop any singleton time/step/valid_time dimension
    for dim in list(da.dims):
        if dim not in ("lat", "lon") and da.sizes.get(dim, 0) == 1:
            da = da.isel({dim: 0}, drop=True)

    # Ensure lat ascending (south→north)
    if da.lat.size > 1 and float(da.lat[0]) > float(da.lat[-1]):
        da = da.sortby("lat")

    # Drop stray surface or height coords if present
    for c in ("surface", "heightAboveGround"):
        if c in da.coords:
            da = da.reset_coords(c, drop=True)

    da.name = "t2m"
    return da


def compute_daily_means_from_inst(
    inst_by_hour: Dict[int, xr.DataArray],
    init_datetime: dt.datetime,
    ndays: int,
    to_celsius: bool = True,
) -> xr.DataArray:
    """
    Convert 3-hourly instantaneous 2m temperature into daily means.

    Convention:
    - Day 1 uses [0, 3, ..., 24] if hour 0 exists
    - Days 2..N use hours in (start, end] to avoid double counting boundaries.
    """
    hours = sorted(inst_by_hour.keys())

    if not hours:
        raise RuntimeError("No forecast hours provided for temperature.")

    if hours[-1] < 24 * ndays:
        raise RuntimeError(
            f"Need temperature up to at least hour {24*ndays}, got max hour {hours[-1]}"
        )

    daily_list: List[xr.DataArray] = []
    time_coords: List[dt.datetime] = []

    for day in range(1, ndays + 1):
        start = 24 * (day - 1)
        end = 24 * day

        if day == 1:
            # Prefer including 0 if available
            hs = [h for h in hours if (0 <= h <= end)]
        else:
            hs = [h for h in hours if (start < h <= end)]

        # Keep only 3-hourly steps (defensive)
        hs = sorted([h for h in hs if h % 3 == 0])

        if not hs:
            raise RuntimeError(f"No temperature hours found for day {day}")

        stack = xr.concat([inst_by_hour[h] for h in hs], dim="step")
        daily = stack.mean(dim="step")

        # Unit handling
        daily = daily.copy()
        src_units = (daily.attrs.get("units") or "").lower()

        # GFS TMP is typically Kelvin
        if to_celsius:
            # If units look like K or empty, assume Kelvin
            if "k" in src_units or src_units == "":
                daily = daily - 273.15
            daily.attrs["units"] = "degC"
            daily.attrs["long_name"] = "GFS daily mean 2m air temperature"
        else:
            daily.attrs["units"] = "K"
            daily.attrs["long_name"] = "GFS daily mean 2m air temperature"

        daily.attrs["description"] = (
            "24-hour mean 2m temperature computed by averaging 3-hourly "
            f"instantaneous GFS TMP within the day window."
        )

        valid_time = init_datetime + dt.timedelta(hours=end)
        daily = daily.expand_dims(time=[np.datetime64(valid_time)])
        daily_list.append(daily)
        time_coords.append(valid_time)

    t2m = xr.concat(daily_list, dim="time")
    t2m.name = "t2m"
    t2m.coords["time"] = np.array(time_coords, dtype="datetime64[ns]")

    return t2m


def process_to_netcdf(
    out_nc: Path,
    init_date: dt.date,
    cycle: int,
    ndays: int,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    to_celsius: bool = True,
) -> None:
    """
    Main workflow: download GFS 2m temperature 3-hourly fields needed for ndays,
    compute daily means, and save to NetCDF.
    """
    if ndays < 1 or ndays > 16:
        raise ValueError("ndays must be between 1 and 16 for GFS.")

    max_fhour = 24 * ndays
    if max_fhour > 384:
        raise ValueError("Maximum forecast hour must be <= 384 for GFS.")

    init_dt = dt.datetime.combine(init_date, dt.time(cycle))
    log(f"GFS init time (UTC): {init_dt.isoformat()}")

    # 0, 3, 6, ..., 24*ndays
    fhours = list(range(0, max_fhour + 1, 3))
    inst: Dict[int, xr.DataArray] = {}

    for fh in fhours:
        url = build_gfs_url_t2m(
            init_date=init_date,
            cycle=cycle,
            fhour=fh,
            lon_min=lon_min,
            lon_max=lon_max,
            lat_min=lat_min,
            lat_max=lat_max,
        )
        grib_name = f"gfs_t2m_f{fh:03d}.grib2"
        grib_path = out_nc.parent / grib_name

        log(f"Downloading T2m fhour={fh:03d} → {grib_name}")
        download_grib(url, grib_path)

        log(f"Opening {grib_name} with xarray/cfgrib...")
        da = open_t2m_from_grib(grib_path)
        inst[fh] = da

    log("Computing daily mean temperature from 3-hourly T2m...")
    t2m = compute_daily_means_from_inst(inst, init_dt, ndays, to_celsius=to_celsius)

    # Build final Dataset
    ds_out = xr.Dataset({"t2m": t2m})
    ds_out.attrs["title"] = "NCEP GFS 0.25° daily mean 2m air temperature"
    ds_out.attrs["source"] = "NCEP GFS 0.25-degree (TMP at 2 m AGL from NOMADS filter_gfs_0p25)"
    ds_out.attrs["history"] = (
        f"Created on {dt.datetime.utcnow().isoformat()}Z by download_gfs_t2m_daily.py; "
        "daily means computed by averaging 3-hourly instantaneous 2m temperature."
    )
    ds_out.attrs["forecast_reference_time"] = init_dt.isoformat()

    # Conservative chunking
    ntime = ds_out.dims["time"]
    nlat = ds_out.dims["lat"]
    nlon = ds_out.dims["lon"]

    encoding = {
        "t2m": {
            "zlib": True,
            "complevel": 4,
            "dtype": "float32",
            "chunksizes": (
                min(ntime, 1),
                min(nlat, 200),
                min(nlon, 200),
            ),
        }
    }

    log(f"Writing NetCDF → {out_nc}")
    out_nc.parent.mkdir(parents=True, exist_ok=True)
    ds_out.to_netcdf(out_nc, encoding=encoding)
    log("Done.")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download NCEP GFS 0.25° 2m temperature (TMP), "
            "compute daily means (degC by default), "
            "clip to a region, and save NetCDF."
        )
    )

    parser.add_argument(
        "--outdir",
        type=str,
        required=True,
        help="Output directory for NetCDF + temporary GRIB2 files.",
    )
    parser.add_argument(
        "--outfile",
        type=str,
        required=True,
        help="Name of the output NetCDF file (relative to outdir).",
    )
    parser.add_argument(
        "--ndays",
        type=int,
        default=10,
        help="Number of forecast days (1–16).",
    )

    parser.add_argument("--lat-min", type=float, required=True)
    parser.add_argument("--lat-max", type=float, required=True)
    parser.add_argument("--lon-min", type=float, required=True)
    parser.add_argument("--lon-max", type=float, required=True)

    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Initial date YYYY-MM-DD for the GFS run (UTC). "
        "If omitted, uses today's UTC date.",
    )
    parser.add_argument(
        "--cycle",
        type=int,
        default=0,
        choices=[0, 6, 12, 18],
        help="GFS cycle hour (0, 6, 12, or 18 UTC).",
    )

    parser.add_argument(
        "--keep-kelvin",
        action="store_true",
        help="If set, do NOT convert to Celsius; keep output in Kelvin.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.date:
        init_date = dt.datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        init_date = dt.datetime.utcnow().date()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    out_nc = outdir / args.outfile

    process_to_netcdf(
        out_nc=out_nc,
        init_date=init_date,
        cycle=args.cycle,
        ndays=args.ndays,
        lat_min=args.lat_min,
        lat_max=args.lat_max,
        lon_min=args.lon_min,
        lon_max=args.lon_max,
        to_celsius=not args.keep_kelvin,
    )


if __name__ == "__main__":
    main()