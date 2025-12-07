#!/usr/bin/env python
"""
Download ECMWF HRES (IFS 0.25°) total precipitation (tp) from ECMWF Open Data,
compute daily 24-hour accumulations, clip to a region of interest,
and save as a single merged NetCDF file.

- Uses ECMWF Free & Open Data (IFS HRES, 0.25° resolution, GRIB2).
- Downloads accumulated total precipitation (tp) at selected lead times.
- Converts accumulated tp -> daily totals for lead days 1..N (N <= 10 for HRES).
- Clips to lat/lon bounding box.
- Writes a single NetCDF with dims (time, lat, lon) and units mm/day.

Example
-------
python download_ecmwf_hres_tp.py \
    --outdir data/ecmwf_hres_tp \
    --outfile ecmwf_hres_tp_ea_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --time 0

Notes
-----
- Daily accumulation is computed from total accumulated precipitation:
    Day 1: tp(24h) - tp(0h)
    Day 2: tp(48h) - tp(24h)
    ...
- Default forecast run: latest available (date/time inferred by ECMWF).
- HRES open-data time steps (00/12 UTC):
    0–144 by 3h, 144–240 by 6h → max 240h = 10 days.
"""

import argparse
from pathlib import Path

import numpy as np
import xarray as xr
from ecmwf.opendata import Client


# ---------------------------------------------------------------------------
# Step selection utilities
# ---------------------------------------------------------------------------

def hres_all_steps():
    """
    Full ECMWF HRES step list for 00Z/12Z in hours:
    0..144 by 3h, 144..240 by 6h
    """
    steps = list(range(0, 145, 3)) + list(range(144, 241, 6))
    # Ensure uniqueness and sorted order
    return sorted(set(steps))


def daily_steps(max_lead_days: int):
    """
    Return the list of step hours needed to compute daily 24h totals
    up to max_lead_days (1–10 for HRES).

    We need step=0 plus 24,48,..., 24*max_lead_days where each step
    actually exists in the open-data step schedule.
    """
    max_lead_days = int(max_lead_days)
    if max_lead_days < 1 or max_lead_days > 10:
        raise ValueError("max_lead_days must be between 1 and 10 for HRES.")

    steps_all = hres_all_steps()
    max_step_hours = max_lead_days * 24

    needed = {0}
    for s in steps_all:
        if 0 < s <= max_step_hours and s % 24 == 0:
            needed.add(s)

    return sorted(needed)


# ---------------------------------------------------------------------------
# Download ECMWF HRES tp from Open Data
# ---------------------------------------------------------------------------

def download_hres_tp_grib(
    target_path: Path,
    ndays: int = 10,
    date: "str | int | None" = None,
    time: "int | None" = None,
):
    """
    Download ECMWF HRES (IFS 0.25°) total precipitation (tp) GRIB2 file
    from ECMWF Free & Open Data for the requested forecast run.

    Parameters
    ----------
    target_path : Path
        Where to store the GRIB2 file.
    ndays : int, optional
        Number of forecast lead days (1–10). Default 10.
    date : str | int | None, optional
        Forecast start date. Examples:
        - '2025-11-30'
        - 0 (today), -1 (yesterday) etc.
        If None, ECMWF will choose the latest available date.
    time : int | None, optional
        Forecast start time (0, 6, 12, 18). If None, ECMWF chooses latest.

    Returns
    -------
    result : ecmwf.opendata.Result
        Result object; result.datetime is the actual forecast init time.
    """
    steps = daily_steps(ndays)

    client = Client(
        source="ecmwf",   # ECMWF Open Data servers
        model="ifs",      # IFS (physics-based HRES)
        resol="0p25",     # 0.25° resolution
    )

    request_kwargs = {
        "type": "fc",
        "param": "tp",
        "step": steps,
    }
    if date is not None:
        request_kwargs["date"] = date
    if time is not None:
        request_kwargs["time"] = time

    result = client.retrieve(
        target=str(target_path),
        **request_kwargs,
    )

    return result


# ---------------------------------------------------------------------------
# Processing GRIB -> daily totals -> clip -> NetCDF
# ---------------------------------------------------------------------------

def open_tp_from_grib(grib_path: Path) -> xr.DataArray:
    """
    Open GRIB2 file and return tp DataArray with step_hours coordinate.

    Returns
    -------
    tp : xr.DataArray
        Dimensions: (step_hours, latitude, longitude)
    """
    ds = xr.open_dataset(
        grib_path,
        engine="cfgrib",
        backend_kwargs={
            "indexpath": "",
            "filter_by_keys": {"shortName": "tp"},
        },
    )

    tp = ds["tp"]  # accumulated from forecast start

    # Drop singleton time dimension (HRES forecast run time)
    if "time" in tp.dims and tp.sizes["time"] == 1:
        tp = tp.isel(time=0, drop=True)

    # Convert 'step' (timedelta64) to integer hours as a numpy array
    step = tp["step"]
    step_hours = (step / np.timedelta64(1, "h")).astype("int32").values

    # Attach as a new coordinate using raw values, not a DataArray
    tp = tp.assign_coords(step_hours=("step", step_hours))

    # Swap dimensions: use step_hours instead of step
    tp = tp.swap_dims({"step": "step_hours"}).drop_vars("step")

    return tp


def compute_daily_totals(tp: xr.DataArray, ndays: int) -> xr.DataArray:
    """
    Compute 24h daily totals from accumulated tp (still in meters).

    tp is accumulated from step=0. We compute:
        day1 = tp(24h) - tp(0h)
        day2 = tp(48h) - tp(24h)
        ...
    """
    max_step_hours = ndays * 24
    step_hours = tp["step_hours"].values

    needed = np.arange(0, max_step_hours + 24, 24)
    missing = [s for s in needed if s not in step_hours]
    if missing:
        raise RuntimeError(
            f"Expected steps {missing} not found in tp; "
            f"got steps={step_hours.tolist()}"
        )

    daily = []
    lead_days = []
    for day in range(1, ndays + 1):
        h1 = day * 24
        h0 = (day - 1) * 24
        daily_tp = tp.sel(step_hours=h1) - tp.sel(step_hours=h0)
        daily.append(daily_tp)
        lead_days.append(day)

    daily_tp = xr.concat(daily, dim="lead_day")
    daily_tp = daily_tp.assign_coords(lead_day=("lead_day", lead_days))

    # Still in meters here; conversion to mm/day is done later
    daily_tp.name = "tp"
    daily_tp.attrs["units"] = tp.attrs.get("units", "m")
    daily_tp.attrs["long_name"] = "Daily total precipitation (24h)"

    return daily_tp


def clip_to_bbox(
    da: xr.DataArray,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
) -> xr.DataArray:
    """
    Clip DataArray to lat/lon bounding box.

    Handles both ascending and descending latitude.
    """
    lat = da.coords.get("latitude")
    lon = da.coords.get("longitude")
    if lat is None or lon is None:
        raise ValueError("Dataset must have 'latitude' and 'longitude' coords.")

    # ECMWF latitude is usually descending (90 -> -90)
    if lat[0] > lat[-1]:
        lat_slice = slice(lat_max, lat_min)
    else:
        lat_slice = slice(lat_min, lat_max)

    lon_slice = slice(lon_min, lon_max)

    return da.sel(latitude=lat_slice, longitude=lon_slice)


def process_to_netcdf(
    grib_path: Path,
    out_nc: Path,
    ndays: int,
    lat_min: float | None = None,
    lat_max: float | None = None,
    lon_min: float | None = None,
    lon_max: float | None = None,
    compress: bool = True,
    init_time=None,
):
    """
    End-to-end processing:
    - Open GRIB
    - Compute daily 24h totals 1..ndays
    - Convert from m to mm/day
    - Rename dims to time, lat, lon
    - Clip to ROI (optional)
    - Save to NetCDF
    """
    # 1) Open and compute daily totals (still in meters)
    tp = open_tp_from_grib(grib_path)
    daily = compute_daily_totals(tp, ndays)

    # 2) Clip to bounding box (still latitude/longitude dims)
    if None not in (lat_min, lat_max, lon_min, lon_max):
        daily = clip_to_bbox(daily, lat_min, lat_max, lon_min, lon_max)

    # 3) Convert from meters to mm/day
    #    (ECMWF tp is m of water equivalent over the accumulation period)
    daily = daily * 1000.0
    daily.attrs["units"] = "mm/day"
    daily.attrs["long_name"] = "Daily total precipitation (24h) [mm/day]"

    # 4) Rename spatial dims/coords to lat, lon
    rename_dims = {}
    if "latitude" in daily.dims:
        rename_dims["latitude"] = "lat"
    if "longitude" in daily.dims:
        rename_dims["longitude"] = "lon"
    if rename_dims:
        daily = daily.rename(rename_dims)


    # 4b) Drop scalar surface coordinate if present
    if "surface" in daily.coords:
        daily = daily.reset_coords("surface", drop=True)

    # 5) Create a proper time dimension (instead of lead_day)
    #    time = forecast_reference_time + lead_day (1..ndays)
    if init_time is not None:
        base = np.datetime64(init_time)
        times = base + np.arange(1, ndays + 1).astype("timedelta64[D]")
    else:
        # Fallback: just use 1..ndays as a dummy time axis
        times = np.arange(1, ndays + 1).astype("int32")

    daily = daily.assign_coords(time=("lead_day", times))
    daily = daily.swap_dims({"lead_day": "time"})
    # Optional: keep lead_day as an auxiliary coordinate or drop it.
    # If you want to drop it completely, uncomment:
    daily = daily.drop_vars("lead_day")

    # 6) Build dataset with dims (time, lat, lon)
    ds_out = daily.to_dataset(name="tp")

    # Some useful global attributes
    if init_time is not None:
        ds_out.attrs["forecast_reference_time"] = str(init_time)
    ds_out.attrs.setdefault(
        "title", "ECMWF IFS HRES (0.25°) daily total precipitation (mm/day)"
    )
    ds_out.attrs.setdefault("source", "ECMWF Open Data (IFS, param=tp)")
    ds_out.attrs.setdefault(
        "history",
        "Daily 24h totals computed from accumulated tp, "
        "converted from m to mm/day using download_ecmwf_hres_tp.py",
    )

    # 7) Safe compression: no manual chunksizes (avoid size mismatch errors)
    encoding = None
    if compress:
        encoding = {
            "tp": {
                "zlib": True,
                "complevel": 4,
                "dtype": "float32",
            }
        }

    out_nc.parent.mkdir(parents=True, exist_ok=True)
    ds_out.to_netcdf(out_nc, encoding=encoding)
    print(f"[info] Written NetCDF: {out_nc}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Download ECMWF HRES (IFS 0.25°) total precipitation, "
                    "compute daily 24h totals (mm/day) and clip to ROI."
    )
    p.add_argument(
        "--outdir",
        type=str,
        default="ecmwf_hres_tp",
        help="Output directory for GRIB & NetCDF (default: %(default)s)",
    )
    p.add_argument(
        "--outfile",
        type=str,
        default="ecmwf_hres_tp_daily.nc",
        help="Output NetCDF file name (default: %(default)s)",
    )
    p.add_argument(
        "--ndays",
        type=int,
        default=10,
        help="Number of forecast lead days (1–10, default: %(default)s)",
    )
    p.add_argument(
        "--date",
        type=str,
        default=None,
        help=(
            "Forecast start date (e.g. '2025-11-30'). "
            "If omitted, latest available is used."
        ),
    )
    p.add_argument(
        "--time",
        type=int,
        default=None,
        help="Forecast start time (0, 6, 12, 18). If omitted, latest is used.",
    )
    p.add_argument(
        "--lat-min", type=float, required=True, help="Minimum latitude"
    )
    p.add_argument(
        "--lat-max", type=float, required=True, help="Maximum latitude"
    )
    p.add_argument(
        "--lon-min", type=float, required=True, help="Minimum longitude"
    )
    p.add_argument(
        "--lon-max", type=float, required=True, help="Maximum longitude"
    )

    return p.parse_args()


def main():
    args = parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    grib_path = outdir / "ecmwf_hres_tp.grib2"
    out_nc = outdir / args.outfile

    print("[info] Downloading ECMWF HRES tp from Open Data...")
    result = download_hres_tp_grib(
        target_path=grib_path,
        ndays=args.ndays,
        date=args.date,
        time=args.time,
    )
    print(f"[info] Forecast init time (UTC): {result.datetime}")

    print("[info] Processing GRIB -> daily totals -> clip -> NetCDF...")
    process_to_netcdf(
        grib_path=grib_path,
        out_nc=out_nc,
        ndays=args.ndays,
        lat_min=args.lat_min,
        lat_max=args.lat_max,
        lon_min=args.lon_min,
        lon_max=args.lon_max,
        init_time=result.datetime,
    )


if __name__ == "__main__":
    main()