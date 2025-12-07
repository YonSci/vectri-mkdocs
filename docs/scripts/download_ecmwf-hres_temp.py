#!/usr/bin/env python
"""
Download ECMWF HRES (IFS 0.25°) 2-meter temperature (2t) from ECMWF Open Data,
compute daily mean temperature, clip to a region of interest,
and save as a single merged NetCDF file.

- Uses ECMWF Free & Open Data (IFS HRES, 0.25° resolution, GRIB2).
- Downloads instantaneous 2m temperature (2t) at selected lead times.
- Computes daily mean 2m temperature for lead days 1..N (N <= 10).
- Clips to lat/lon bounding box.
- Writes a single NetCDF with dims (time, lat, lon) and units degC.

Example
-------
python download_ecmwf_hres_2t.py \
    --outdir data/ecmwf_hres_2t \
    --outfile ecmwf_hres_2t_ea_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --time 0

Notes
-----
- 2m temperature (2t) is an instantaneous field (units K in GRIB).
- Daily mean is computed by averaging all available steps within each 24h window:
    Day 1: mean of steps in [0, 24]
    Day 2: mean of steps in (24, 48]
    ...
  This avoids double-counting boundary hours across days.
- HRES open-data step schedule for 00/12 UTC:
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
    return sorted(set(steps))


def temp_steps(max_lead_days: int):
    """
    Return the list of step hours needed to compute daily means
    up to max_lead_days (1–10 for HRES).

    For temperature daily means, we keep all available steps
    up to 24*max_lead_days.
    """
    max_lead_days = int(max_lead_days)
    if max_lead_days < 1 or max_lead_days > 10:
        raise ValueError("max_lead_days must be between 1 and 10 for HRES.")

    max_step_hours = max_lead_days * 24
    steps_all = hres_all_steps()
    needed = [s for s in steps_all if 0 <= s <= max_step_hours]

    # Ensure we have step=0
    if 0 not in needed:
        needed = [0] + needed

    return sorted(set(needed))


# ---------------------------------------------------------------------------
# Download ECMWF HRES 2t from Open Data
# ---------------------------------------------------------------------------

def download_hres_2t_grib(
    target_path: Path,
    ndays: int = 10,
    date: "str | int | None" = None,
    time: "int | None" = None,
):
    """
    Download ECMWF HRES (IFS 0.25°) 2m temperature (2t) GRIB2 file
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
    steps = temp_steps(ndays)

    client = Client(
        source="ecmwf",
        model="ifs",
        resol="0p25",
    )

    request_kwargs = {
        "type": "fc",
        "param": "2t",
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
# Processing GRIB -> daily means -> clip -> NetCDF
# ---------------------------------------------------------------------------

def open_2t_from_grib(grib_path: Path) -> xr.DataArray:
    """
    Open GRIB2 file and return 2t DataArray with step_hours coordinate.

    Returns
    -------
    t2m : xr.DataArray
        Dimensions: (step_hours, latitude, longitude)
    """
    ds = xr.open_dataset(
        grib_path,
        engine="cfgrib",
        backend_kwargs={
            "indexpath": "",
            "filter_by_keys": {"shortName": "2t"},
        },
    )

    t2m = ds["t2m"] if "t2m" in ds.data_vars else ds["2t"]

    # Drop singleton time dimension (forecast run time)
    if "time" in t2m.dims and t2m.sizes["time"] == 1:
        t2m = t2m.isel(time=0, drop=True)

    # Convert 'step' (timedelta64) to integer hours
    step = t2m["step"]
    step_hours = (step / np.timedelta64(1, "h")).astype("int32").values

    t2m = t2m.assign_coords(step_hours=("step", step_hours))
    t2m = t2m.swap_dims({"step": "step_hours"}).drop_vars("step")

    t2m.name = "t2m"
    return t2m


def compute_daily_means(t2m: xr.DataArray, ndays: int) -> xr.DataArray:
    """
    Compute daily mean 2m temperature from instantaneous steps.

    Day 1: mean of steps in [0, 24]
    Day 2: mean of steps in (24, 48]
    ...
    """
    max_step_hours = ndays * 24
    step_hours = t2m["step_hours"].values

    if step_hours.max() < max_step_hours:
        raise RuntimeError(
            f"Need steps up to at least {max_step_hours}h, "
            f"got max {int(step_hours.max())}h"
        )

    daily_list = []
    lead_days = []

    for day in range(1, ndays + 1):
        h1 = day * 24
        h0 = (day - 1) * 24

        if day == 1:
            mask = (t2m.step_hours >= 0) & (t2m.step_hours <= h1)
        else:
            mask = (t2m.step_hours > h0) & (t2m.step_hours <= h1)

        sub = t2m.where(mask, drop=True)
        if sub.step_hours.size == 0:
            raise RuntimeError(f"No temperature steps found for day {day}")

        daily_mean = sub.mean(dim="step_hours", skipna=True)
        daily_list.append(daily_mean)
        lead_days.append(day)

    daily = xr.concat(daily_list, dim="lead_day")
    daily = daily.assign_coords(lead_day=("lead_day", lead_days))

    daily.name = "t2m"
    daily.attrs["units"] = t2m.attrs.get("units", "K")
    daily.attrs["long_name"] = "Daily mean 2m temperature"

    return daily


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
    to_celsius: bool = True,
):
    """
    End-to-end processing:
    - Open GRIB
    - Compute daily means 1..ndays
    - Convert from K to degC (optional)
    - Rename dims to time, lat, lon
    - Clip to ROI (optional)
    - Save to NetCDF
    """
    # 1) Open and compute daily means (still in Kelvin)
    t2m = open_2t_from_grib(grib_path)
    daily = compute_daily_means(t2m, ndays)

    # 2) Clip to bounding box (still latitude/longitude dims)
    if None not in (lat_min, lat_max, lon_min, lon_max):
        daily = clip_to_bbox(daily, lat_min, lat_max, lon_min, lon_max)

    # 3) Convert units
    if to_celsius:
        daily = daily - 273.15
        daily.attrs["units"] = "degC"
        daily.attrs["long_name"] = "Daily mean 2m temperature [degC]"
    else:
        daily.attrs["units"] = "K"
        daily.attrs["long_name"] = "Daily mean 2m temperature [K]"

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
    if init_time is not None:
        base = np.datetime64(init_time)
        times = base + np.arange(1, ndays + 1).astype("timedelta64[D]")
    else:
        times = np.arange(1, ndays + 1).astype("int32")

    daily = daily.assign_coords(time=("lead_day", times))
    daily = daily.swap_dims({"lead_day": "time"})
    daily = daily.drop_vars("lead_day")

    # 6) Build dataset with dims (time, lat, lon)
    ds_out = daily.to_dataset(name="t2m")

    # Global attributes
    if init_time is not None:
        ds_out.attrs["forecast_reference_time"] = str(init_time)
    ds_out.attrs.setdefault(
        "title", "ECMWF IFS HRES (0.25°) daily mean 2m temperature"
    )
    ds_out.attrs.setdefault("source", "ECMWF Open Data (IFS, param=2t)")
    ds_out.attrs.setdefault(
        "history",
        "Daily means computed from instantaneous 2m temperature steps, "
        "optionally converted from K to degC using download_ecmwf_hres_2t.py",
    )

    # 7) Safe compression
    encoding = None
    if compress:
        encoding = {
            "t2m": {
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
        description="Download ECMWF HRES (IFS 0.25°) 2m temperature (2t), "
                    "compute daily means and clip to ROI."
    )
    p.add_argument(
        "--outdir",
        type=str,
        default="ecmwf_hres_2t",
        help="Output directory for GRIB & NetCDF (default: %(default)s)",
    )
    p.add_argument(
        "--outfile",
        type=str,
        default="ecmwf_hres_2t_daily.nc",
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
    p.add_argument(
        "--keep-kelvin",
        action="store_true",
        help="Do NOT convert to Celsius; keep output in Kelvin.",
    )

    return p.parse_args()


def main():
    args = parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    grib_path = outdir / "ecmwf_hres_2t.grib2"
    out_nc = outdir / args.outfile

    print("[info] Downloading ECMWF HRES 2t from Open Data...")
    result = download_hres_2t_grib(
        target_path=grib_path,
        ndays=args.ndays,
        date=args.date,
        time=args.time,
    )
    print(f"[info] Forecast init time (UTC): {result.datetime}")

    print("[info] Processing GRIB -> daily means -> clip -> NetCDF...")
    process_to_netcdf(
        grib_path=grib_path,
        out_nc=out_nc,
        ndays=args.ndays,
        lat_min=args.lat_min,
        lat_max=args.lat_max,
        lon_min=args.lon_min,
        lon_max=args.lon_max,
        init_time=result.datetime,
        to_celsius=not args.keep_kelvin,
    )


if __name__ == "__main__":
    main()