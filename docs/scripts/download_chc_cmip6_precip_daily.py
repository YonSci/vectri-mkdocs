#!/usr/bin/env python
"""
Download CHC-CMIP6 daily precipitation GeoTIFFs (CHIRPS-based),
clip to Ethiopia, convert to NetCDF, and fix units/variable names.

Example:
python download_chc_cmip6_precip_daily_to_netcdf.py \
  --period-tags 2030_SSP245 2030_SSP585 \
  --start-year 1983 --end-year 1984 \
  --outdir data/CHC_CMIP6 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48
"""

import argparse
import calendar
import os
from typing import Iterable, Tuple

import numpy as np
import requests
import rioxarray
import xarray as xr

BASE_URL = "https://data.chc.ucsb.edu/products/CHC_CMIP6"


# -----------------------------------------------------------------------------#
# Utilities
# -----------------------------------------------------------------------------#

def iter_dates(year: int) -> Iterable[Tuple[int, int, int]]:
    """Yield (year, month, day) for every day in a given year."""
    for month in range(1, 13):
        ndays = calendar.monthrange(year, month)[1]
        for day in range(1, ndays + 1):
            yield year, month, day


def download_file(url: str, dest_path: str) -> bool:
    """Download file from URL to dest_path. Return True on success."""
    try:
        r = requests.get(url, stream=True, timeout=60)
        if r.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(1024 * 1024):
                    f.write(chunk)
            return True
        else:
            print(f"[warn] HTTP {r.status_code} for {url}")
            return False
    except Exception as exc:
        print(f"[err] Failed to download {url}: {exc}")
        return False


def subset_ethiopia(
    da: xr.DataArray,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
) -> xr.DataArray:
    """Subset DataArray to an Ethiopia-like bounding box."""
    # CHIRPS is in EPSG:4326
    da = da.rio.write_crs("EPSG:4326", inplace=True)
    # CHIRPS y is usually descending (north -> south), so use slice(lat_max, lat_min)
    return da.sel(y=slice(lat_max, lat_min), x=slice(lon_min, lon_max))


def fix_units_and_name(da: xr.DataArray) -> xr.DataArray:
    """Standardise variable to pr [mm/day]."""
    da.name = "pr"
    da.attrs["long_name"] = "Daily precipitation"
    da.attrs["units"] = "mm/day"
    return da


def combine_and_save(daily_arrays, out_path: str):
    """Combine daily DataArrays into a single NetCDF file."""
    ds = xr.concat(daily_arrays, dim="time")
    ds = ds.sortby("time")
    encoding = {"pr": {"zlib": True, "complevel": 4}}
    ds.to_netcdf(out_path, encoding=encoding)
    print(f"[ok] Saved NetCDF → {out_path}")


# -----------------------------------------------------------------------------#
# Core processing
# -----------------------------------------------------------------------------#

def process_period(
    period_tag: str,
    start_year: int,
    end_year: int,
    outdir: str,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
):
    dataset_dir = "chirps-v2"
    file_tag = "CHIRPS"

    # temp directory for GeoTIFFs (inside outdir so it’s easy to inspect/clean)
    tmp_root = os.path.join(outdir, "_tmp_chc_cmip6")
    os.makedirs(tmp_root, exist_ok=True)

    for year in range(start_year, end_year + 1):
        print(f"[info] Processing {period_tag} {year}")
        daily_list = []

        year_url = f"{BASE_URL}/{period_tag}/{dataset_dir}/{year}"

        for y, m, d in iter_dates(year):
            fname = f"{period_tag}.{file_tag}.{y}.{m:02d}.{d:02d}.tif"
            url = f"{year_url}/{fname}"

            tmp_path = os.path.join(tmp_root, fname)

            # Download
            if not download_file(url, tmp_path):
                continue

            try:
                # Open GeoTIFF
                da = rioxarray.open_rasterio(tmp_path).squeeze(drop=True)

                # Subset + standardise metadata
                da = subset_ethiopia(da, lat_min, lat_max, lon_min, lon_max)
                da = fix_units_and_name(da)

                # Load data into memory so we can safely close/delete the file
                da = da.load()

                # Add time dimension
                time_val = np.datetime64(f"{y:04d}-{m:02d}-{d:02d}")
                da = da.expand_dims(time=[time_val])

                daily_list.append(da)

                # Explicitly close raster handle
                try:
                    da.rio.close()
                except Exception:
                    # Not critical; some versions may not need this
                    pass

            except Exception as exc:
                print(f"[warn] Failed to process {fname}: {exc}")

            finally:
                # Now that data is loaded & handle closed, we can delete the temp file
                try:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                except Exception as exc_rm:
                    print(f"[warn] Could not remove temp file {tmp_path}: {exc_rm}")

        if not daily_list:
            print(f"[warn] No valid data for {period_tag} {year}")
            continue

        # Output one NetCDF per year & scenario
        out_path = os.path.join(
            outdir,
            period_tag,
            f"{period_tag}_CHIRPS_{year}_ethiopia.nc",
        )
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        combine_and_save(daily_list, out_path)


# -----------------------------------------------------------------------------#
# CLI
# -----------------------------------------------------------------------------#

def parse_args():
    p = argparse.ArgumentParser(
        description=(
            "Download CHC-CMIP6 CHIRPS-based daily precipitation, "
            "subset to Ethiopia, convert to NetCDF."
        )
    )
    p.add_argument(
        "--period-tags",
        nargs="+",
        required=True,
        help="Period tags like 2030_SSP245 2030_SSP585 2050_SSP245 2050_SSP585",
    )
    p.add_argument("--start-year", type=int, default=1983)
    p.add_argument("--end-year", type=int, default=1983)
    p.add_argument("--outdir", required=True)
    p.add_argument("--lat-min", type=float, default=3.0)
    p.add_argument("--lat-max", type=float, default=15.0)
    p.add_argument("--lon-min", type=float, default=33.0)
    p.add_argument("--lon-max", type=float, default=48.0)
    return p.parse_args()


def main():
    args = parse_args()
    for tag in args.period_tags:
        process_period(
            period_tag=tag,
            start_year=args.start_year,
            end_year=args.end_year,
            outdir=args.outdir,
            lat_min=args.lat_min,
            lat_max=args.lat_max,
            lon_min=args.lon_min,
            lon_max=args.lon_max,
        )


if __name__ == "__main__":
    main()
