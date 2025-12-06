#!/usr/bin/env python
"""
Download, clip, and merge TAMSAT v3.1 daily rainfall (Africa) into one NetCDF,
using explicit start/end dates (YYYY-MM-DD) and daily NetCDF URLs.

Data source (daily NetCDFs):
    https://gws-access.jasmin.ac.uk/public/tamsat/rfe/data/v3.1/daily/YYYY/MM/rfeYYYY_MM_DD.v3.1.nc

Example file:
    https://gws-access.jasmin.ac.uk/public/tamsat/rfe/data/v3.1/daily/1983/01/rfe1983_01_01.v3.1.nc

This script:
    1) Iterates from --start YYYY-MM-DD to --end YYYY-MM-DD inclusive.
    2) For each date, builds the daily URL and downloads the NetCDF (unless --skip-download).
    3) Saves files under outdir/nc/YYYY/MM/.
    4) Merges all available daily files into a single multi-day NetCDF.
    5) Optionally clips to a lat/lon bounding box.
    6) Writes a compressed NetCDF file.

Example:
    python download_tamsat.py \
        --start 2010-01-01 --end 2011-03-31 \
        --outdir data/tamsat_ea \
        --clip 12 2 32 42 \
        --merge-name tamsat_v3.1_daily_20100101-20110331_ea.nc

Requirements:
    - Python 3.x
    - requests
    - xarray
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, date, timedelta

import requests
import xarray as xr

BASE_DAILY_URL = (
    "https://gws-access.jasmin.ac.uk/public/tamsat/rfe/data/v3.1/daily"
)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def parse_iso_date(s: str) -> date:
    """
    Parse a YYYY-MM-DD string into a datetime.date, with argparse-friendly errors.
    """
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{s}'. Expected format YYYY-MM-DD, e.g. 2010-01-01."
        )


def date_range(start: date, end: date):
    """
    Yield all dates from start to end inclusive.
    """
    current = start
    one_day = timedelta(days=1)
    while current <= end:
        yield current
        current += one_day


def download_file(url: str, dest: Path, overwrite: bool = False) -> bool:
    """
    Download URL to dest (streamed). Returns True if file is present after call.
    """
    if dest.exists() and not overwrite:
        print(f"[download] {dest} exists, skipping download.")
        return True

    print(f"[download] {url} -> {dest}")
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            if r.status_code >= 400:
                print(f"[warning] HTTP {r.status_code} for {url}, skipping.")
                return dest.exists()
            ensure_dir(dest.parent)
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception as exc:
        print(f"[error] failed to download {url}: {exc}")
        return dest.exists()


def detect_lat_lon_names(ds: xr.Dataset):
    """
    Detect latitude and longitude coordinate names in a dataset.
    Returns (lat_name, lon_name).
    """
    lat_candidates = ["lat", "latitude", "y"]
    lon_candidates = ["lon", "longitude", "x"]

    lat_name = None
    lon_name = None

    for name in lat_candidates:
        if name in ds.dims or name in ds.coords:
            lat_name = name
            break
    for name in lon_candidates:
        if name in ds.dims or name in ds.coords:
            lon_name = name
            break

    if lat_name is None or lon_name is None:
        raise ValueError(
            f"Could not detect lat/lon names in dataset. "
            f"Dims: {list(ds.dims.keys())}, Coords: {list(ds.coords.keys())}"
        )

    return lat_name, lon_name


def standardize_for_merge(ds: xr.Dataset) -> xr.Dataset:
    """
    Standardize coordinate names and ordering for safe merge.

    - Rename latitude/longitude to 'lat'/'lon' if needed.
    - Ensure lat and lon are sorted ascending.
    """
    lat_name, lon_name = detect_lat_lon_names(ds)

    rename_map = {}
    if lat_name != "lat":
        rename_map[lat_name] = "lat"
    if lon_name != "lon":
        rename_map[lon_name] = "lon"
    if rename_map:
        ds = ds.rename(rename_map)

    # Sort coordinates ascending
    if ds["lat"].values[0] > ds["lat"].values[-1]:
        ds = ds.sortby("lat")
    if ds["lon"].values[0] > ds["lon"].values[-1]:
        ds = ds.sortby("lon")

    return ds


def clip_box(ds: xr.Dataset, north: float, south: float, west: float, east: float) -> xr.Dataset:
    """
    Clip dataset to a lat/lon box: N, S, W, E.
    Assumes 'lat' and 'lon' coordinates are already standardized.
    """

    ds = standardize_for_merge(ds)

    lat = ds["lat"]
    if lat.values[0] < lat.values[-1]:
        lat_slice = slice(south, north)
    else:
        lat_slice = slice(north, south)

    lon = ds["lon"]
    lon_min = float(lon.min())
    lon_max = float(lon.max())

    if not (lon_min <= west <= lon_max and lon_min <= east <= lon_max):
        print(
            "[warning] Requested lon bounds not fully within data range; "
            "still attempting a simple slice."
        )
    lon_slice = slice(west, east)

    ds_clipped = ds.sel(lat=lat_slice, lon=lon_slice)
    return ds_clipped


def default_encoding(ds: xr.Dataset):
    """
    Build a simple compression encoding dict for NetCDF output.
    """
    encoding = {}
    for var in ds.data_vars:
        encoding[var] = {
            "zlib": True,
            "complevel": 4,
            "shuffle": True,
            "dtype": ds[var].dtype,
        }
    return encoding


# ---------------------------------------------------------------------------
# Core workflow
# ---------------------------------------------------------------------------

def build_tamsat_url(d: date) -> str:
    """
    Build the TAMSAT daily NetCDF URL for a given date.
    Example:
        BASE/1983/01/rfe1983_01_01.v3.1.nc
    """
    return (
        f"{BASE_DAILY_URL}/{d.year:04d}/{d.month:02d}/"
        f"rfe{d.year:04d}_{d.month:02d}_{d.day:02d}.v3.1.nc"
    )


def build_local_path(nc_root: Path, d: date) -> Path:
    """
    Build local path where the daily NetCDF will be stored.
    e.g. nc_root/2010/01/rfe2010_01_01.v3.1.nc
    """
    return (
        nc_root
        / f"{d.year:04d}"
        / f"{d.month:02d}"
        / f"rfe{d.year:04d}_{d.month:02d}_{d.day:02d}.v3.1.nc"
    )


def merge_tamsat_files(
    nc_files,
    out_path: Path,
    clip_bounds=None,
):
    """
    Merge a list of daily TAMSAT NetCDF files into one file.
    clip_bounds: (N, S, W, E) or None.
    """
    if not nc_files:
        raise RuntimeError("No NetCDF files provided for merging.")

    print(f"[merge] Opening {len(nc_files)} files with xarray.open_mfdataset...")
    nc_files_str = [str(p) for p in nc_files]

    def preprocess(ds):
        ds = standardize_for_merge(ds)
        return ds

    ds = xr.open_mfdataset(
        nc_files_str,
        combine="by_coords",
        parallel=False,   # set True if you have dask
        preprocess=preprocess,
    )

    print("[merge] Dataset opened. Coordinates:", list(ds.coords))

    if clip_bounds is not None:
        N, S, W, E = clip_bounds
        print(f"[clip] Applying bounding box N={N}, S={S}, W={W}, E={E}")
        ds = clip_box(ds, N, S, W, E)

    enc = default_encoding(ds)
    ensure_dir(out_path.parent)
    print(f"[write] Writing merged NetCDF -> {out_path}")
    ds.to_netcdf(out_path, encoding=enc)
    ds.close()
    print("[done] Merge complete.")


def run(args):
    start_date: date = args.start
    end_date: date = args.end

    outdir = Path(args.outdir).expanduser().resolve()
    nc_root = outdir / "nc"

    ensure_dir(outdir)
    ensure_dir(nc_root)

    all_local_files = []

    print(
        f"[info] Date range: {start_date.isoformat()} "
        f"-> {end_date.isoformat()}"
    )

    for d in date_range(start_date, end_date):
        url = build_tamsat_url(d)
        local_path = build_local_path(nc_root, d)

        if args.skip_download:
            if local_path.exists():
                all_local_files.append(local_path)
            else:
                print(
                    f"[warning] --skip-download set and local file missing for "
                    f"{d.isoformat()}: {local_path}"
                )
            continue

        ok = download_file(url, local_path, overwrite=args.overwrite)
        if ok and local_path.exists():
            all_local_files.append(local_path)
        else:
            print(f"[warning] Missing or failed file for {d.isoformat()}")

    if not all_local_files:
        print("[error] No NetCDF files found/downloaded in the requested range. Exiting.")
        sys.exit(1)

    # Deduplicate & sort
    all_local_files = sorted(set(all_local_files))

    # Determine output path
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    if args.merge_name:
        merge_path = Path(args.merge_name)
        if not merge_path.is_absolute():
            merge_path = outdir / merge_path
    else:
        bbox_suffix = ""
        if args.clip:
            N, S, W, E = args.clip
            bbox_suffix = f"_N{N}_S{S}_W{W}_E{E}"
        merge_path = outdir / f"tamsat_v3.1_daily_{start_str}-{end_str}{bbox_suffix}.nc"

    clip_bounds = tuple(args.clip) if args.clip else None

    merge_tamsat_files(
        nc_files=all_local_files,
        out_path=merge_path,
        clip_bounds=clip_bounds,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Download, clip and merge TAMSAT v3.1 daily rainfall NetCDFs "
                    "for a given date range."
    )
    parser.add_argument(
        "--start",
        type=parse_iso_date,
        required=True,
        help="Start date (YYYY-MM-DD), e.g. 2010-01-01",
    )
    parser.add_argument(
        "--end",
        type=parse_iso_date,
        required=True,
        help="End date (YYYY-MM-DD, inclusive), e.g. 2011-03-31",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="tamsat_data",
        help="Output directory (default: ./tamsat_data)",
    )
    parser.add_argument(
        "--clip",
        type=float,
        nargs=4,
        metavar=("N", "S", "W", "E"),
        help="Optional lat/lon bounding box: N S W E (e.g. 12 2 32 42)",
    )
    parser.add_argument(
        "--merge-name",
        type=str,
        default=None,
        help="Filename for merged NetCDF (relative to outdir if not absolute). "
             "If omitted, a default name is constructed from the date range.",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Do not download; only merge existing local NetCDFs "
             "for the specified date range.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing daily NetCDFs if they already exist.",
    )
    args = parser.parse_args()

    if args.end < args.start:
        parser.error("--end must be >= --start (in time).")

    return args


def main():
    args = parse_args()
    run(args)


if __name__ == "__main__":
    main()