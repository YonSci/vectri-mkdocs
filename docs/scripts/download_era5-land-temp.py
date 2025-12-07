#!/usr/bin/env python3
"""
Download ERA5-Land 2m temperature (hourly) from CDS, convert to daily means,
optionally convert Kelvin -> Celsius, and merge outputs.

Default strategy retrieves data month-by-month to reduce request size and
avoid "cost limits exceeded / request too large" errors.

Examples
--------
# 1) One year, small box, daily means, keep Kelvin
python download_era5_land_t2m_daily.py \
  --start-year 2020 --end-year 2020 \
  --lat-min 3 --lat-max 6 --lon-min 33 --lon-max 35 \
  --outdir data/era5_land_t2m_ea \
  --merge-outfile era5_land_t2m_daily_2020.nc

# 2) Two years, Ethiopia-ish box, convert to Celsius, delete hourly
python download_era5_land_t2m_daily.py \
  --start-year 2020 --end-year 2021 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48 \
  --outdir data/era5_land_t2m_ea \
  --merge-outfile era5_land_t2m_daily_2020_2021_ea.nc \
  --to-Celsius --delete-hourly

# 3) Keep hourly + keep monthly daily intermediates
python download_era5_land_t2m_daily.py \
  --start-year 2020 --end-year 2020 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48 \
  --outdir data/era5_land_t2m_ea \
  --keep-hourly --keep-monthly-daily
"""

import argparse
import calendar
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import xarray as xr

try:
    import cdsapi
except ImportError as e:
    raise SystemExit(
        "Missing dependency 'cdsapi'. Install with:\n"
        "  pip install cdsapi\n"
    ) from e


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def build_area(lat_min: float, lat_max: float, lon_min: float, lon_max: float):
    """
    CDS area format: [N, W, S, E]
    """
    if lat_min >= lat_max:
        raise ValueError("lat-min must be < lat-max")
    if lon_min >= lon_max:
        raise ValueError("lon-min must be < lon-max")
    return [float(lat_max), float(lon_min), float(lat_min), float(lon_max)]


def days_in_month(year: int, month: int) -> List[str]:
    n_days = calendar.monthrange(year, month)[1]
    return [f"{d:02d}" for d in range(1, n_days + 1)]


def hours_list() -> List[str]:
    return [f"{h:02d}:00" for h in range(24)]


def safe_remove(path: Path):
    try:
        if path.exists():
            path.unlink()
    except PermissionError:
        # Windows occasionally keeps handles briefly; user can manually delete later.
        print(f"[warn] Could not delete file (in use): {path}")


def detect_t2m_var(ds: xr.Dataset) -> str:
    """
    ERA5-Land usually uses 't2m'. Fall back to the first data variable.
    """
    if "t2m" in ds.data_vars:
        return "t2m"
    # fallback
    vars_list = list(ds.data_vars)
    if not vars_list:
        raise ValueError("No data variables found in dataset.")
    return vars_list[0]


def retrieve_hourly_t2m_month(
    client: "cdsapi.Client",
    year: int,
    month: int,
    out_path: Path,
    area,
):
    """
    Retrieve one month of hourly ERA5-Land 2m temperature.
    """
    request = {
        "variable": "2m_temperature",
        "year": f"{year}",
        "month": f"{month:02d}",
        "day": days_in_month(year, month),
        "time": hours_list(),
        "area": area,
        "format": "netcdf",
    }

    print(f"[info] Requesting ERA5-Land hourly T2M for {year}-{month:02d}...")
    print(f"[info] Target: {out_path}")

    # Use the standard collection id
    client.retrieve("reanalysis-era5-land", request).download(str(out_path))


def hourly_to_daily_mean(
    hourly_nc: Path,
    daily_nc: Path,
    to_celsius: bool = False,
):
    """
    Convert hourly T2M to daily mean T2M.
    """
    print(f"[info] Converting hourly → daily mean: {hourly_nc.name}")

    ds = xr.open_dataset(hourly_nc)

    var = detect_t2m_var(ds)
    da = ds[var]

    # Ensure time decoded
    if "time" not in da.dims:
        ds.close()
        raise ValueError("Expected 'time' dimension not found in hourly file.")

    # Daily mean
    da_daily = da.resample(time="1D").mean(keep_attrs=True)
    da_daily = da_daily.rename("t2m")

    # Optional unit conversion K -> C
    if to_celsius:
        da_daily = da_daily - 273.15
        da_daily.attrs["units"] = "C"
    else:
        da_daily.attrs.setdefault("units", "K")

    da_daily.attrs.setdefault("long_name", "2 metre temperature")

    ds_out = da_daily.to_dataset()

    # Preserve basic coords
    for coord in ["latitude", "longitude"]:
        if coord in ds.coords and coord not in ds_out.coords:
            ds_out = ds_out.assign_coords({coord: ds[coord]})

    # Some files use 'lat/lon' naming
    if "lat" in ds.coords and "lat" not in ds_out.coords:
        ds_out = ds_out.assign_coords({"lat": ds["lat"]})
    if "lon" in ds.coords and "lon" not in ds_out.coords:
        ds_out = ds_out.assign_coords({"lon": ds["lon"]})

    # Write
    ds_out.to_netcdf(daily_nc)

    ds.close()
    ds_out.close()

    print(f"[info] Daily file saved → {daily_nc.name}")


def merge_netcdfs(nc_files: List[Path], out_path: Path):
    """
    Merge multiple NetCDF files by coords.
    """
    if not nc_files:
        raise ValueError("No NetCDF files provided for merging.")

    print(f"[info] Merging {len(nc_files)} files → {out_path.name}")

    # Use open_mfdataset carefully on Windows
    ds = xr.open_mfdataset(
        [str(p) for p in nc_files],
        combine="by_coords",
        parallel=False,
    )

    ds.to_netcdf(out_path)
    ds.close()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Download ERA5-Land hourly T2M, convert to daily means."
    )

    p.add_argument("--start-year", type=int, required=True)
    p.add_argument("--end-year", type=int, required=True)

    p.add_argument("--lat-min", type=float, required=True)
    p.add_argument("--lat-max", type=float, required=True)
    p.add_argument("--lon-min", type=float, required=True)
    p.add_argument("--lon-max", type=float, required=True)

    p.add_argument("--outdir", required=True)

    p.add_argument(
        "--merge-outfile",
        default=None,
        help="Optional merged daily NetCDF filename (stored in outdir)."
    )

    p.add_argument(
        "--keep-hourly",
        action="store_true",
        help="Keep monthly hourly NetCDF files."
    )

    p.add_argument(
        "--keep-monthly-daily",
        action="store_true",
        help="Keep monthly daily NetCDF intermediates."
    )

    # New flags requested
    p.add_argument(
        "--to-celsius", "--to-Celsius",
        dest="to_celsius",
        action="store_true",
        help="Convert daily t2m from Kelvin to Celsius."
    )

    p.add_argument(
        "--delete-hourly",
        action="store_true",
        help="Alias to ensure hourly files are deleted (default unless --keep-hourly)."
    )

    p.add_argument(
        "--request-mode",
        choices=["monthly", "yearly"],
        default="monthly",
        help="Retrieve data month-by-month (default) or attempt full-year request."
    )

    return p.parse_args()


def retrieve_hourly_t2m_year(
    client: "cdsapi.Client",
    year: int,
    out_path: Path,
    area,
):
    """
    Attempt a single yearly retrieval (may fail for size/limits).
    """
    request = {
        "variable": "2m_temperature",
        "year": f"{year}",
        "month": [f"{m:02d}" for m in range(1, 13)],
        "day": [f"{d:02d}" for d in range(1, 32)],
        "time": hours_list(),
        "area": area,
        "format": "netcdf",
    }

    print(f"[info] Requesting ERA5-Land hourly T2M for {year} (yearly request)...")
    print(f"[info] Target: {out_path}")

    client.retrieve("reanalysis-era5-land", request).download(str(out_path))


def main() -> None:
    args = parse_args()

    if args.end_year < args.start_year:
        raise SystemExit("--end-year must be >= --start-year")

    # Alias behaviour
    if getattr(args, "delete_hourly", False):
        args.keep_hourly = False

    # Basic date sanity (years only)
    if args.start_year < 1950 or args.end_year > 2100:
        print("[warn] Year range looks unusual for ERA5-Land.")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    area = build_area(args.lat_min, args.lat_max, args.lon_min, args.lon_max)

    client = cdsapi.Client()

    yearly_daily_files: List[Path] = []

    for year in range(args.start_year, args.end_year + 1):
        year_str = str(year)

        hourly_dir = outdir / "hourly"
        daily_dir = outdir / "daily"
        hourly_dir.mkdir(exist_ok=True)
        daily_dir.mkdir(exist_ok=True)

        monthly_hourly_files: List[Path] = []
        monthly_daily_files: List[Path] = []

        if args.request_mode == "yearly":
            # Single yearly file
            hourly_year_path = hourly_dir / f"era5_land_t2m_hourly_{year}.nc"
            try:
                retrieve_hourly_t2m_year(client, year, hourly_year_path, area)
            except Exception as e:
                print("[warn] Yearly request failed; switching to monthly mode.")
                print(f"[warn] Reason: {e}")
                args.request_mode = "monthly"
            else:
                # Convert to daily directly from yearly hourly
                daily_year_path = daily_dir / f"era5_land_t2m_daily_{year}.nc"
                hourly_to_daily_mean(
                    hourly_year_path,
                    daily_year_path,
                    to_celsius=args.to_celsius,
                )
                yearly_daily_files.append(daily_year_path)

                if not args.keep_hourly:
                    safe_remove(hourly_year_path)

                continue  # next year

        # Monthly mode
        for month in range(1, 13):
            hourly_m_path = hourly_dir / f"era5_land_t2m_hourly_{year}{month:02d}.nc"
            daily_m_path = daily_dir / f"era5_land_t2m_daily_{year}{month:02d}.nc"

            # Skip download if daily already exists
            if daily_m_path.exists():
                print(f"[info] Found existing daily file, skipping month: {daily_m_path.name}")
                monthly_daily_files.append(daily_m_path)
                continue

            try:
                retrieve_hourly_t2m_month(client, year, month, hourly_m_path, area)
                monthly_hourly_files.append(hourly_m_path)

                hourly_to_daily_mean(
                    hourly_m_path,
                    daily_m_path,
                    to_celsius=args.to_celsius,
                )
                monthly_daily_files.append(daily_m_path)

            except Exception as e:
                print(f"[error] Failed for {year}-{month:02d}: {e}")
                # Continue to next month
                continue

            finally:
                # Close file handles are managed inside conversion
                pass

            # Cleanup hourly month if not requested
            if not args.keep_hourly and hourly_m_path.exists():
                safe_remove(hourly_m_path)

        # Merge monthly daily to yearly daily
        daily_year_path = daily_dir / f"era5_land_t2m_daily_{year}.nc"
        if monthly_daily_files:
            try:
                merge_netcdfs(monthly_daily_files, daily_year_path)
                yearly_daily_files.append(daily_year_path)
            except Exception as e:
                print(f"[error] Could not merge monthly daily for {year}: {e}")
                # If merge fails, still allow later global merge using monthly files.

        # Cleanup monthly daily intermediates
        if not args.keep_monthly_daily:
            for p in monthly_daily_files:
                # Don't delete if it's the same as the yearly output path
                if p.resolve() != daily_year_path.resolve():
                    safe_remove(p)

    # Final merge across years
    if args.merge_outfile:
        merged_path = outdir / args.merge_outfile

        # Prefer yearly daily files if available
        if yearly_daily_files:
            merge_inputs = yearly_daily_files
        else:
            # Fallback: search for any daily files
            merge_inputs = sorted((outdir / "daily").glob("era5_land_t2m_daily_*.nc"))

        if merge_inputs:
            try:
                merge_netcdfs(merge_inputs, merged_path)
                print(f"[info] Final merged file saved → {merged_path}")
            except Exception as e:
                print(f"[error] Final merge failed: {e}")
        else:
            print("[warn] No daily files found to merge.")

    print("[info] Done.")


if __name__ == "__main__":
    main()
