#!/usr/bin/env python
"""
Download NCEP GFS 0.25° accumulated precipitation (APCP),
compute 1–N-day daily totals, clip to a bounding box,
and save as a single NetCDF file with dims (time, lat, lon).

For GFS 0.25° on NOMADS:
- APCP is precipitation accumulated over the *previous interval* (3h),
  not from t0. So we SUM all 3-hourly APCP fields within each 24-h window
  instead of differencing them.

Example
-------
python download_gfs_apcp_daily.py \
    --outdir data/gfs_apcp \
    --outfile gfs_apcp_ea_10day.nc \
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


def build_gfs_url(
    init_date: dt.date,
    cycle: int,
    fhour: int,
    lon_min: float,
    lon_max: float,
    lat_min: float,
    lat_max: float,
) -> str:
    """
    Build NOMADS GRIB-filter URL for GFS 0.25° APCP at a given forecast hour.
    """
    date_str = init_date.strftime("%Y%m%d")
    file_name = f"gfs.t{cycle:02d}z.pgrb2.0p25.f{fhour:03d}"
    dir_path = f"/gfs.{date_str}/{cycle:02d}/atmos"

    params = {
        "file": file_name,
        "lev_surface": "on",
        "var_APCP": "on",
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
                    # Too many requests → small backoff
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


def open_apcp_from_grib(grib_path: Path) -> xr.DataArray:
    """
    Open a GFS APCP GRIB2 file and return a DataArray (lat, lon)
    in units of mm (kg m-2) for the 3-hour accumulation period.
    """
    backend_kwargs = {"indexpath": ""}

    # Try to restrict to accumulated fields; fall back to generic open
    try:
        ds = xr.open_dataset(
            grib_path,
            engine="cfgrib",
            backend_kwargs={
                **backend_kwargs,
                "filter_by_keys": {"stepType": "accum"},
            },
        )
    except Exception:
        ds = xr.open_dataset(grib_path, engine="cfgrib", backend_kwargs=backend_kwargs)

    if not ds.data_vars:
        raise RuntimeError(f"No data variables found in {grib_path}")

    # Pick the most likely precip variable
    var_name = None
    for name in ds.data_vars:
        lower = name.lower()
        attrs = ds[name].attrs
        long = (attrs.get("long_name", "") + attrs.get("name", "")).lower()
        if any(k in lower for k in ("apcp", "tp", "pr", "precip")) or "precip" in long:
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

    # Drop any singleton time/step dimension (one forecast hour per file)
    for dim in list(da.dims):
        if dim not in ("lat", "lon") and da.sizes[dim] == 1:
            da = da.isel({dim: 0}, drop=True)

    # Ensure lat ascending (south→north)
    if da.lat.size > 1 and float(da.lat[0]) > float(da.lat[-1]):
        da = da.sortby("lat")

    # Drop stray surface coord if present
    if "surface" in da.coords:
        da = da.reset_coords("surface", drop=True)

    da.name = "apcp"
    return da


def compute_daily_totals_from_accum(
    acc_by_hour: Dict[int, xr.DataArray],
    init_datetime: dt.datetime,
    ndays: int,
) -> xr.DataArray:
    """
    Convert 3-hourly APCP fields (mm over the last 3h) into
    24-hour totals (mm/day) by summing 3-hourly values.

    For a 00Z run:
      Day 1 (time = init+24h): sum hours 3, 6, ..., 24
      Day 2 (time = init+48h): sum hours 27, 30, ..., 48
      ...
    """
    hours = sorted(acc_by_hour.keys())

    # Basic consistency check
    if not hours or hours[0] != 3:
        raise RuntimeError(f"Expected first APCP hour to be 3, got {hours[0] if hours else 'none'}")
    if hours[-1] < 24 * ndays:
        raise RuntimeError(
            f"Need APCP up to at least hour {24*ndays}, got max hour {hours[-1]}"
        )

    daily_list: List[xr.DataArray] = []
    time_coords: List[dt.datetime] = []

    for day in range(1, ndays + 1):
        start = 24 * (day - 1)    # start of day window (in hours)
        end = 24 * day            # end of day window

        # 3-hourly forecast hours strictly inside (start, end]
        hs = [h for h in hours if (start < h <= end)]

        if not hs:
            raise RuntimeError(f"No APCP hours found for day {day}: start={start}, end={end}")

        # Sum 3-hourly APCP to get 24-h total (mm)
        stack = xr.concat([acc_by_hour[h] for h in hs], dim="step")
        daily = stack.sum(dim="step")

        # Attributes
        daily = daily.copy()
        daily.attrs["units"] = "mm/day"
        daily.attrs["long_name"] = "GFS daily total precipitation"
        daily.attrs["description"] = (
            "24-hour total precipitation computed by summing 3-hourly APCP "
            f"over ({start}h, {end}h]."
        )

        valid_time = init_datetime + dt.timedelta(hours=end)
        daily = daily.expand_dims(time=[np.datetime64(valid_time)])
        daily_list.append(daily)
        time_coords.append(valid_time)

    tp = xr.concat(daily_list, dim="time")
    tp.name = "tp"
    tp.coords["time"] = np.array(time_coords, dtype="datetime64[ns]")
    tp.attrs["units"] = "mm/day"
    tp.attrs["long_name"] = "GFS daily total precipitation"

    # Clip tiny negatives caused by numerical issues
    tp = tp.clip(min=0)

    return tp


def process_to_netcdf(
    out_nc: Path,
    init_date: dt.date,
    cycle: int,
    ndays: int,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
) -> None:
    """
    Main workflow: download GFS APCP 3-hourly fields needed for ndays,
    compute daily totals, and save to NetCDF.
    """
    if ndays < 1 or ndays > 16:
        raise ValueError("ndays must be between 1 and 16 for GFS.")

    max_fhour = 24 * ndays
    if max_fhour > 384:
        raise ValueError("Maximum forecast hour must be <= 384 for GFS.")

    init_dt = dt.datetime.combine(init_date, dt.time(cycle))
    log(f"GFS init time (UTC): {init_dt.isoformat()}")

    # 3, 6, 9, ..., 24*ndays
    fhours = list(range(3, max_fhour + 1, 3))
    acc: Dict[int, xr.DataArray] = {}

    for fh in fhours:
        url = build_gfs_url(
            init_date=init_date,
            cycle=cycle,
            fhour=fh,
            lon_min=lon_min,
            lon_max=lon_max,
            lat_min=lat_min,
            lat_max=lat_max,
        )
        grib_name = f"gfs_apcp_f{fh:03d}.grib2"
        grib_path = out_nc.parent / grib_name

        log(f"Downloading APCP fhour={fh:03d} → {grib_name}")
        download_grib(url, grib_path)

        log(f"Opening {grib_name} with xarray/cfgrib...")
        da = open_apcp_from_grib(grib_path)
        acc[fh] = da

    log("Computing daily totals from 3-hourly APCP...")
    tp = compute_daily_totals_from_accum(acc, init_dt, ndays)

    # Build final Dataset
    ds_out = xr.Dataset({"tp": tp})
    ds_out.attrs["title"] = "NCEP GFS 0.25° daily total precipitation (mm/day)"
    ds_out.attrs["source"] = "NCEP GFS 0.25-degree (APCP from NOMADS filter_gfs_0p25)"
    ds_out.attrs["history"] = (
        f"Created on {dt.datetime.utcnow().isoformat()}Z by download_gfs_apcp_daily.py; "
        "daily 24h totals computed by summing 3-hourly APCP."
    )
    ds_out.attrs["forecast_reference_time"] = init_dt.isoformat()

    # Conservative chunking; ensure chunk dims ≤ data dims
    ntime = ds_out.dims["time"]
    nlat = ds_out.dims["lat"]
    nlon = ds_out.dims["lon"]

    encoding = {
        "tp": {
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
            "Download NCEP GFS 0.25° APCP, compute daily totals (mm/day), "
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
    )


if __name__ == "__main__":
    main()
