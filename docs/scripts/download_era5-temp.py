#!/usr/bin/env python3
"""
Download ERA5 hourly 2m temperature (t2m) from CDS and compute daily means.

Key features
------------
- Monthly hourly download to avoid CDS "cost limits exceeded"
- Computes daily mean per month
- Optional unit conversion to Celsius
- Region bounding box support (N/W/S/E)
- Optional cleanup of hourly files
- Optional merge of all daily files into one NetCDF

Examples
--------
1) Download 2020 only (Ethiopia-ish box), compute daily mean, convert to Celsius,
   delete hourly files, merge into one file:
python download_era5_t2m_daily.py \
  --start-year 2020 --end-year 2020 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48 \
  --outdir data/era5_t2m_ea \
  --merge-outfile era5_t2m_daily_2020_2020_ea.nc \
  --to-celsius --delete-hourly

2) Keep hourly monthly files:
python download_era5_t2m_daily.py \
  --start-year 2020 --end-year 2021 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48 \
  --outdir data/era5_t2m_ea \
  --keep-hourly

Notes
-----
Dataset used:
  reanalysis-era5-single-levels

Variable:
  2m_temperature (saved as t2m in NetCDF by CDS)
"""

import argparse
import os
import glob
from datetime import datetime

import numpy as np
import xarray as xr
import cdsapi


# --------------------------------------------------------------------------- #
# Helpers: time handling (robust to CDS variations)
# --------------------------------------------------------------------------- #

def find_time_dim(ds: xr.Dataset) -> str:
    """
    Find the most likely time dimension/coordinate in a CDS ERA5 file.
    Handles cases where time is named 'valid_time' or missing as a coord.
    """
    # 1) Common names first
    for cand in ("time", "valid_time"):
        if cand in ds.coords or cand in ds.dims:
            return cand

    # 2) Any coord that looks like time
    for name, coord in ds.coords.items():
        if "time" in name.lower():
            return name
        try:
            if np.issubdtype(coord.dtype, np.datetime64):
                return name
        except Exception:
            pass

    # 3) Any dim with CF-style time units
    for dim in ds.dims:
        if dim in ds.variables:
            units = str(ds[dim].attrs.get("units", ""))
            if "since" in units:
                return dim

    raise KeyError(
        "Could not find a time dimension/coordinate. "
        f"coords={list(ds.coords)}, dims={list(ds.dims)}"
    )


def standardise_time_for_resample(ds: xr.Dataset) -> xr.Dataset:
    """
    Ensure the dataset has a usable coordinate named 'time'
    so that ds['t2m'].resample(time='1D') works reliably.
    """
    time_dim = find_time_dim(ds)

    # If it's a dim but not a coord, attach it as a coord
    if time_dim in ds.dims and time_dim not in ds.coords:
        if time_dim in ds.variables:
            ds = ds.assign_coords({time_dim: ds[time_dim]})

    # Normalize to 'time'
    if time_dim != "time":
        ds = ds.rename({time_dim: "time"})

    # Ensure time is decoded if needed
    if "time" in ds.coords:
        if not np.issubdtype(ds["time"].dtype, np.datetime64):
            try:
                ds = xr.decode_cf(ds)
            except Exception:
                # If decode_cf fails, we still try resampling
                pass

    return ds


# --------------------------------------------------------------------------- #
# ERA5 retrieval and processing
# --------------------------------------------------------------------------- #

def build_monthly_request(year: int, month: int, area: list[float]) -> dict:
    """
    Build a CDS request for ERA5 hourly 2m temperature for a given year+month.
    """
    year_str = f"{year:04d}"
    month_str = f"{month:02d}"

    days = [f"{d:02d}" for d in range(1, 32)]
    times = [f"{h:02d}:00" for h in range(0, 24)]

    return {
        "product_type": "reanalysis",
        "variable": "2m_temperature",
        "year": year_str,
        "month": month_str,
        "day": days,
        "time": times,
        "area": area,  # [N, W, S, E]
        "format": "netcdf",
    }


def retrieve_hourly_t2m_month(year: int, month: int, out_path: str, area: list[float]) -> None:
    """
    Download ERA5 hourly 2m temperature for a specific month.
    """
    client = cdsapi.Client()

    request = build_monthly_request(year, month, area)

    print(f"[info] Requesting ERA5 hourly T2M for {year:04d}-{month:02d}...")
    print(f"[info] Target: {out_path}")

    # CDS API style that works across versions:
    result = client.retrieve("reanalysis-era5-single-levels", request)
    result.download(out_path)


def compute_daily_mean_t2m(hourly_path: str, daily_path: str, to_celsius: bool) -> None:
    """
    Open an hourly ERA5 file and write a daily-mean file.
    Robust to CDS files where time is named 'valid_time'
    or not attached as a coordinate.
    """
    ds = xr.open_dataset(hourly_path)

    if "t2m" not in ds:
        available = list(ds.data_vars)
        ds.close()
        raise KeyError(f"'t2m' not found in {hourly_path}. Found: {available}")

    ds = standardise_time_for_resample(ds)

    # Compute daily mean
    t2m_daily = ds["t2m"].resample(time="1D").mean()

    ds_daily = t2m_daily.to_dataset(name="t2m")

    # Units
    if to_celsius:
        ds_daily["t2m"] = ds_daily["t2m"] - 273.15
        ds_daily["t2m"].attrs["units"] = "C"
        ds_daily["t2m"].attrs["long_name"] = "2m temperature (daily mean)"
    else:
        ds_daily["t2m"].attrs.setdefault("units", "K")
        ds_daily["t2m"].attrs.setdefault("long_name", "2m temperature (daily mean)")

    ds_daily.attrs["source"] = "ERA5 reanalysis (CDS)"
    ds_daily.attrs["processing"] = "Monthly hourly download; daily mean computed with xarray"

    encoding = {"t2m": {"zlib": True, "complevel": 4}}
    ds_daily.to_netcdf(daily_path, encoding=encoding)

    ds.close()
    ds_daily.close()


def merge_daily_files(daily_files: list[str], out_path: str, to_celsius: bool) -> None:
    """
    Merge multiple daily NetCDF files into one.
    """
    if not daily_files:
        raise FileNotFoundError("No daily files found to merge.")

    ds = xr.open_mfdataset(daily_files, combine="by_coords")

    # Ensure sorted time
    if "time" in ds.coords:
        ds = ds.sortby("time")

    # Ensure units metadata is consistent
    if "t2m" in ds:
        if to_celsius:
            ds["t2m"].attrs["units"] = "C"
        else:
            ds["t2m"].attrs.setdefault("units", "K")

    encoding = {"t2m": {"zlib": True, "complevel": 4}}
    ds.to_netcdf(out_path, encoding=encoding)
    ds.close()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Download ERA5 hourly 2m temperature and compute daily means."
    )

    p.add_argument("--start-year", type=int, required=True)
    p.add_argument("--end-year", type=int, required=True)

    p.add_argument("--lat-min", type=float, required=True)
    p.add_argument("--lat-max", type=float, required=True)
    p.add_argument("--lon-min", type=float, required=True)
    p.add_argument("--lon-max", type=float, required=True)

    p.add_argument("--outdir", required=True, help="Output directory")

    p.add_argument(
        "--merge-outfile",
        default=None,
        help="If provided, merge all daily files into this NetCDF in --outdir",
    )

    p.add_argument(
        "--to-celsius",
        action="store_true",
        help="Convert daily mean t2m from K to C",
    )

    # Hourly retention policy
    p.add_argument(
        "--keep-hourly",
        action="store_true",
        help="Keep downloaded hourly monthly files",
    )
    p.add_argument(
        "--delete-hourly",
        action="store_true",
        help="Delete hourly monthly files after daily computation",
    )

    # Daily monthly retention policy (optional)
    p.add_argument(
        "--keep-monthly-daily",
        action="store_true",
        help="Keep per-month daily files even if merging",
    )

    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.start_year > args.end_year:
        raise SystemExit("--start-year must be <= --end-year")

    if args.keep_hourly and args.delete_hourly:
        raise SystemExit("Choose only one of --keep-hourly or --delete-hourly")

    os.makedirs(args.outdir, exist_ok=True)

    # CDS area is [N, W, S, E]
    area = [args.lat_max, args.lon_min, args.lat_min, args.lon_max]

    hourly_dir = os.path.join(args.outdir, "hourly_monthly")
    daily_dir = os.path.join(args.outdir, "daily_monthly")
    os.makedirs(hourly_dir, exist_ok=True)
    os.makedirs(daily_dir, exist_ok=True)

    daily_files = []

    for year in range(args.start_year, args.end_year + 1):
        for month in range(1, 13):
            hourly_path = os.path.join(hourly_dir, f"era5_t2m_hourly_{year:04d}_{month:02d}.nc")
            daily_path = os.path.join(daily_dir, f"era5_t2m_daily_{year:04d}_{month:02d}.nc")

            # Download hourly if needed
            if not os.path.exists(hourly_path):
                retrieve_hourly_t2m_month(year, month, hourly_path, area)
            else:
                print(f"[info] Hourly file exists, skipping download: {hourly_path}")

            # Compute daily mean
            if not os.path.exists(daily_path):
                print(f"[info] Computing daily mean for {year:04d}-{month:02d}...")
                compute_daily_mean_t2m(hourly_path, daily_path, args.to_celsius)
                print(f"[info] Saved daily file → {daily_path}")
            else:
                print(f"[info] Daily file exists, skipping compute: {daily_path}")

            daily_files.append(daily_path)

            # Hourly cleanup policy
            if args.delete_hourly or (not args.keep_hourly and not args.delete_hourly):
                # Default behavior: delete hourly to save space
                try:
                    os.remove(hourly_path)
                    print(f"[info] Deleted hourly file → {hourly_path}")
                except OSError:
                    pass

    # Merge all monthly daily files if requested
    if args.merge_outfile:
        merged_path = os.path.join(args.outdir, args.merge_outfile)
        print("[info] Merging all daily monthly files...")
        merge_daily_files(daily_files, merged_path, args.to_celsius)
        print(f"[info] Merged file saved → {merged_path}")

        # Optionally delete monthly daily files after merge
        if not args.keep_monthly_daily:
            for f in daily_files:
                try:
                    os.remove(f)
                except OSError:
                    pass
            print("[info] Deleted monthly daily files after merge (use --keep-monthly-daily to retain).")

    print("[info] Done.")


if __name__ == "__main__":
    main()
