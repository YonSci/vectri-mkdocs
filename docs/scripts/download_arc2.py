#!/usr/bin/env python
"""
Download daily ARC2 binary rainfall data and convert to (optionally clipped) NetCDF.

Example usage:

  # Download + convert + clip to Ethiopia box and merge:
  python download_arc2.py \
      --start 2010-01-01 \
      --end   2010-12-31 \
      --outdir data/arc2_ea \
      --clip 18 3 32 50 \
      --merge-name arc2_ea_2010.nc

  # Only convert existing .gz files (no download):
  python download_arc2.py \
      --start 2010-01-01 \
      --end   2010-12-31 \
      --outdir data/arc2_ea \
      --clip 18 3 32 50 \
      --merge-name arc2_ea_2010.nc \
      --skip-download
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import gzip

import numpy as np
import xarray as xr
import requests

# ---------------------------------------------------------------------
# ARC2 constants (from CPC/NOAA documentation)
# ---------------------------------------------------------------------
ARC2_BASE_URL = "https://ftp.cpc.ncep.noaa.gov/fews/fewsdata/africa/arc2/bin"

# Grid: -40S to 40N, 20W to 55E, 0.1° resolution
NLAT = 801  # south–north
NLON = 751  # west–east
LAT_S, LAT_N = -40.0, 40.0
LON_W, LON_E = -20.0, 55.0


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def parse_date(s):
    """Parse date from 'YYYYMMDD' or 'YYYY-MM-DD'."""
    s = s.strip()
    for fmt in ("%Y%m%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(f"Could not parse date '{s}' (expected YYYYMMDD or YYYY-MM-DD)")


def date_range(start, end):
    """Inclusive daily date range."""
    if end < start:
        raise ValueError("End date is earlier than start date")
    cur = start
    one = timedelta(days=1)
    while cur <= end:
        yield cur
        cur += one


def build_arc2_url(d):
    """Construct ARC2 URL for a given date."""
    return f"{ARC2_BASE_URL}/daily_clim.bin.{d:%Y%m%d}.gz"


def download_file(url, dest, overwrite=False):
    """
    Download a file with basic logging and 404 handling.
    Returns True if file is present locally after this call.
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and not overwrite:
        print(f"[info] already exists, skipping download: {dest.name}")
        return True

    tmp = dest.with_suffix(dest.suffix + ".part")
    if tmp.exists():
        tmp.unlink()

    try:
        print(f"[info] downloading {url}")
        with requests.get(url, stream=True, timeout=300) as r:
            try:
                r.raise_for_status()
            except requests.HTTPError as e:
                code = r.status_code
                if code == 404:
                    print(f"[warn] 404 not found, skipping: {url}")
                    return False
                print(f"[err] HTTP {code} for {url}: {e}")
                return False

            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

        tmp.replace(dest)
        print(f"[✓] Downloaded: {dest.name}")
        return True

    except Exception as e:
        print(f"[err] download failed for {url}: {e}")
        if tmp.exists():
            tmp.unlink()
        return False


def read_arc2_gz_to_array(bin_gz):
    """
    Read a gzipped ARC2 binary file into a 2D numpy array (lat, lon).

    NOTE on dtype/endianness:
    - CPC docs say "single precision floating point".
    - Here we assume big-endian (">f4").
    - If values look strange, change to "<f4".
    """
    bin_gz = Path(bin_gz)
    if not bin_gz.exists():
        raise FileNotFoundError(bin_gz)

    with gzip.open(bin_gz, "rb") as f:
        buf = f.read()

    data = np.frombuffer(buf, dtype=">f4")  # big-endian float32
    expected = NLAT * NLON
    if data.size != expected:
        raise ValueError(
            f"{bin_gz} has {data.size} values, expected {expected} "
            f"({NLAT}x{NLON}); check format/endianness."
        )

    # reshape to (lat, lon)
    arr = data.reshape((NLAT, NLON))

    # Orientation note:
    # Grid is 801 pixels south–north and 751 west–east.
    # First row = LAT_S (-40), last row = LAT_N (40).
    # If maps are flipped N/S, use: arr = arr[::-1, :]

    return arr


def make_lat_lon():
    """Create 1D lat/lon coordinate arrays."""
    lats = np.linspace(LAT_S, LAT_N, NLAT, dtype="float32")
    lons = np.linspace(LON_W, LON_E, NLON, dtype="float32")
    return lats, lons


def convert_bin_to_nc(bin_gz, nc_path, clip_box=None, overwrite=False):
    """
    Convert one gzipped ARC2 binary file to a 1-day NetCDF.

    clip_box: (N, S, W, E) if not None.
    Returns True if NetCDF exists/was created; False on failure.
    """
    bin_gz = Path(bin_gz)
    nc_path = Path(nc_path)

    if not bin_gz.exists():
        print(f"[warn] missing file (skipping): {bin_gz.name}")
        return False

    if nc_path.exists() and not overwrite:
        print(f"[info] daily NetCDF exists, skipping convert: {nc_path.name}")
        return True

    try:
        arr = read_arc2_gz_to_array(bin_gz)
        lats, lons = make_lat_lon()

        data3d = arr[np.newaxis, :, :]  # (time, lat, lon)

        # Extract date from filename: daily_clim.bin.YYYYMMDD.gz
        stem = bin_gz.name
        date_str = stem.split(".")[-2]
        t = np.datetime64(datetime.strptime(date_str, "%Y%m%d"))

        ds = xr.Dataset(
            {
                "precip": (("time", "lat", "lon"), data3d.astype("float32")),
            },
            coords={
                "time": [t],
                "lat": lats,
                "lon": lons,
            },
        )

        ds["precip"].attrs["long_name"] = "ARC2 daily rainfall"
        ds["precip"].attrs["units"] = "mm/day"
        ds.attrs["source"] = "NOAA CPC Africa Rainfall Climatology v2.0 (ARC2)"
        ds.attrs["history"] = f"created from {bin_gz.name}"

        if clip_box is not None:
            N, S, W, E = clip_box
            if S > N or W > E:
                raise ValueError(f"Invalid clip box (N={N}, S={S}, W={W}, E={E})")
            ds = ds.sel(lat=slice(S, N), lon=slice(W, E))

        nc_path.parent.mkdir(parents=True, exist_ok=True)

        encoding = {
            "precip": {
                "zlib": True,
                "complevel": 4,
                "dtype": "float32",
                "_FillValue": np.float32(-9999.0),
            }
        }
        ds.to_netcdf(nc_path, format="NETCDF4", encoding=encoding)
        print(f"[✓] Converted: {nc_path.name}")
        return True

    except Exception as e:
        print(f"[err] failed to convert {bin_gz.name}: {e}")
        return False


def merge_daily_nc(nc_paths, out_path, overwrite=False):
    """Merge a list of daily NetCDF files into a single time-series file."""
    out_path = Path(out_path)

    if out_path.exists() and not overwrite:
        print(f"[info] merged file already exists, skipping: {out_path.name}")
        return

    if not nc_paths:
        print("[warn] no daily NetCDF files to merge; skipping merge.")
        return

    print(f"[merge] {len(nc_paths)} daily files → {out_path.name}")

    ds = xr.open_mfdataset(
        [str(p) for p in nc_paths],
        combine="by_coords",
        parallel=False,
        chunks={"time": 30},
    )

    encoding = {vn: {"zlib": True, "complevel": 4} for vn in ds.data_vars}
    ds.to_netcdf(out_path, format="NETCDF4", encoding=encoding)
    print(f"[✓] Merged file saved: {out_path}")


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------
def main(argv=None):
    p = argparse.ArgumentParser(
        description="Download daily ARC2 binary rainfall and convert to (optionally clipped) NetCDF."
    )
    p.add_argument("--start", required=True,
                   help="Start date (YYYYMMDD or YYYY-MM-DD)")
    p.add_argument("--end", required=True,
                   help="End date (YYYYMMDD or YYYY-MM-DD, inclusive)")
    p.add_argument("--outdir", default="data/arc2",
                   help="Root output directory (bin/ and nc_daily/ subdirs created)")
    p.add_argument(
        "--clip",
        nargs=4,
        type=float,
        metavar=("N", "S", "W", "E"),
        help="Optional clip box [North South West East] in degrees"
    )
    p.add_argument(
        "--merge-name",
        default=None,
        help=(
            "Filename for merged time-series NetCDF (e.g. 'arc2_ea_2010.nc'). "
            "If omitted, no merge is done."
        ),
    )
    p.add_argument(
        "--skip-download",
        action="store_true",
        help="Do not download, only convert existing local .gz files"
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing .gz and .nc files"
    )

    args = p.parse_args(argv)

    start = parse_date(args.start)
    end = parse_date(args.end)

    out_root = Path(args.outdir)
    bin_dir = out_root / "bin"
    nc_dir = out_root / "nc_daily"

    clip_box = tuple(args.clip) if args.clip is not None else None

    all_nc_paths = []

    for d in date_range(start, end):
        ymd = d.strftime("%Y%m%d")
        gz_name = f"daily_clim.bin.{ymd}.gz"
        bin_path = bin_dir / gz_name
        nc_path = nc_dir / f"arc2_{ymd}.nc"

        # 1) Download step (unless user asked to skip)
        if not args.skip_download:
            url = build_arc2_url(d)
            ok = download_file(url, bin_path, overwrite=args.overwrite)
            if not ok:
                continue

        # 2) Convert step (only if file exists locally)
        if bin_path.exists():
            ok_nc = convert_bin_to_nc(
                bin_path,
                nc_path,
                clip_box=clip_box,
                overwrite=args.overwrite,
            )
            if ok_nc:
                all_nc_paths.append(nc_path)
        else:
            print(f"[warn] binary file missing, skipping: {bin_path.name}")

    # 3) Merge step
    if args.merge_name:
        merge_path = out_root / args.merge_name
        merge_daily_nc(all_nc_paths, merge_path, overwrite=args.overwrite)
    else:
        print("[info] merge step skipped (no --merge-name given).")


if __name__ == "__main__":
    main()