#!/usr/bin/env python3
"""
Download CHIRTS-daily yearly NetCDFs (Tmax, Tmin) for a year range,
optionally clip to a region, compute daily mean temperature (Tavg),
and merge all processed yearly files into a single NetCDF.

CHIRTS-daily (v1.0) Africa NetCDF collections:
- 0.25°: https://data.chc.ucsb.edu/products/CHIRTSdaily/v1.0/africa_netcdf_p25/
- 0.05°: https://data.chc.ucsb.edu/products/CHIRTSdaily/v1.0/africa_netcdf_p05/

File naming:
- Tmax.<year>.nc
- Tmin.<year>.nc

Outputs
-------
Yearly processed files (in outdir):
  chirts_daily_<res>_<year>[_clip].nc with variables:
    - tmax (degC)
    - tmin (degC)
    - tavg (degC) = (tmax + tmin)/2

Merged file (in outdir):
  chirts_<res>_<start>-<end>[_clip].nc
  (unless --merge-name provided)

Examples
--------
# 1) Download 2000–2002 at 0.25°, clip to Ethiopia box, merge
python download_merge_chirts_daily.py --start 2000 --end 2002 \
  --res p25 --clip 15 3 33 48 --outdir data/chirts_daily_eth

# 2) Same but explicit merged name
python download_merge_chirts_daily.py --start 2000 --end 2002 \
  --res p25 --clip 15 3 33 48 --outdir data/chirts_daily_eth \
  --merge-name chirts_p25_2000-2002_clip.nc

Notes
-----
- CHIRTS-daily v1.0 coverage is 1983–2016.
- p05 files are large; test with p25 first if you're unsure.
"""

import argparse
from pathlib import Path
import sys
import requests


# -----------------------------------------------------------------------------#
# Logging
# -----------------------------------------------------------------------------#

def log(msg: str) -> None:
    print(f"[info] {msg}")

def warn(msg: str) -> None:
    print(f"[warn] {msg}")


# -----------------------------------------------------------------------------#
# Download helpers
# -----------------------------------------------------------------------------#

def download_file(url: str, dest: Path, chunk=2**20):
    """Download a file from URL to dest (atomic write)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")

    with requests.get(url, stream=True, timeout=180) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for blk in r.iter_content(chunk_size=chunk):
                if blk:
                    f.write(blk)

    tmp.replace(dest)

def build_urls(year: int, res: str) -> dict:
    """
    Build Africa CHIRTS-daily URLs for Tmax and Tmin.
    res: 'p25' or 'p05'
    """
    base = f"https://data.chc.ucsb.edu/products/CHIRTSdaily/v1.0/africa_netcdf_{res}"
    return {
        "tmax": f"{base}/Tmax.{year}.nc",
        "tmin": f"{base}/Tmin.{year}.nc",
    }


# -----------------------------------------------------------------------------#
# Xarray utilities
# -----------------------------------------------------------------------------#

def standardize_for_merge(ds):
    """
    Standardize dimension names and latitude orientation for merging:
    - rename latitude/longitude -> lat/lon if needed
    - ensure lat ascending
    """
    ren = {}
    if "latitude" in ds.dims:
        ren["latitude"] = "lat"
    if "longitude" in ds.dims:
        ren["longitude"] = "lon"
    if ren:
        ds = ds.rename(ren)

    try:
        lat = ds["lat"]
        if lat.size > 1 and lat[0] > lat[-1]:
            ds = ds.reindex(lat=list(reversed(lat.values)))
    except Exception:
        pass

    return ds

def clip_box(ds, N, S, W, E):
    """
    Clip dataset to bounding box (N, S, W, E).
    Works with either latitude/longitude or lat/lon.
    Handles simple longitude wrapping if needed.
    """
    import numpy as np
    import xarray as xr

    if S >= N:
        raise ValueError(f"Invalid latitude bounds: South ({S}) must be less than North ({N})")

    lat_name = "latitude" if "latitude" in ds.dims else "lat"
    lon_name = "longitude" if "longitude" in ds.dims else "lon"

    lat = ds[lat_name].values
    lon = ds[lon_name].values

    # Select latitude range (assume increasing selection)
    lat_slice = slice(S, N)

    lon_min, lon_max = float(np.nanmin(lon)), float(np.nanmax(lon))
    W2, E2 = W, E

    # If dataset uses 0..360 and user requests -180..180
    if lon_min >= 0 and W < 0:
        W2 = (W + 360) % 360
        E2 = (E + 360) % 360

    sel_dict = {lat_name: lat_slice}

    if W2 <= E2:
        sel_dict[lon_name] = slice(W2, E2)
        ds_sub = ds.sel(sel_dict)
    else:
        # Dateline wrap case
        left = ds.sel({lat_name: lat_slice, lon_name: slice(W2, lon_max)})
        right = ds.sel({lat_name: lat_slice, lon_name: slice(lon_min, E2)})
        ds_sub = xr.concat([left, right], dim=lon_name)

    return standardize_for_merge(ds_sub)

def pick_temp_var(ds, kind: str):
    """
    Robustly select a temperature variable from a CHIRTS dataset.
    kind: 'tmax' or 'tmin'
    """
    if not ds.data_vars:
        raise ValueError("No data variables found.")

    kind = kind.lower()

    # Common patterns to try
    preferred_names = []
    if kind == "tmax":
        preferred_names = ["tmax", "Tmax", "temperature_max", "temp_max"]
    else:
        preferred_names = ["tmin", "Tmin", "temperature_min", "temp_min"]

    for n in preferred_names:
        if n in ds.data_vars:
            return ds[n]

    # Fuzzy search by name/attrs
    for name in ds.data_vars:
        lname = name.lower()
        long_name = str(ds[name].attrs.get("long_name", "")).lower()
        units = str(ds[name].attrs.get("units", "")).lower()

        if kind in lname:
            return ds[name]

        if kind == "tmax" and ("max" in lname or "maximum" in long_name):
            return ds[name]

        if kind == "tmin" and ("min" in lname or "minimum" in long_name):
            return ds[name]

        # Sometimes variable is just "temperature"
        if "temperature" in lname and ("c" in units or "degc" in units):
            return ds[name]

    # Fallback to first variable
    return ds[list(ds.data_vars)[0]]

def ensure_celsius(da):
    """
    Convert to degC if units indicate Kelvin OR values look like Kelvin.
    """
    import numpy as np

    units = str(da.attrs.get("units", "")).strip().lower()

    # Unit-based conversion
    if units in ("k", "kelvin"):
        da = da - 273.15
        da.attrs["units"] = "degC"
        return da

    # Heuristic conversion if units missing/unclear
    try:
        vmax = float(np.nanmax(da.values))
        if vmax > 100:
            da = da - 273.15
            da.attrs["units"] = "degC"
    except Exception:
        pass

    # Standardize label if still missing
    if not units:
        da.attrs["units"] = "degC"

    return da

def build_year_dataset(ds_tmax, ds_tmin):
    """
    Create a standardized Dataset with:
      tmax, tmin, tavg
    """
    import xarray as xr

    ds_tmax = standardize_for_merge(ds_tmax)
    ds_tmin = standardize_for_merge(ds_tmin)

    tmax = pick_temp_var(ds_tmax, "tmax")
    tmin = pick_temp_var(ds_tmin, "tmin")

    tmax = ensure_celsius(tmax).rename("tmax")
    tmin = ensure_celsius(tmin).rename("tmin")

    # Align grids/time exactly
    tmax, tmin = xr.align(tmax, tmin, join="exact", copy=False)

    tavg = ((tmax + tmin) / 2.0).rename("tavg")

    # Add basic attrs
    tmax.attrs.update({"long_name": "Daily maximum 2m air temperature"})
    tmin.attrs.update({"long_name": "Daily minimum 2m air temperature"})
    tavg.attrs.update({
        "long_name": "Daily mean 2m air temperature",
        "units": tmax.attrs.get("units", "degC"),
        "description": "Computed as (tmax + tmin)/2."
    })

    return xr.Dataset({"tmax": tmax, "tmin": tmin, "tavg": tavg})

def merge_to_netcdf(nc_paths, out_path: Path):
    """Merge multiple NetCDF files into one output file."""
    import xarray as xr

    if not nc_paths:
        raise ValueError("No input files found to merge.")

    log(f"[merge] {len(nc_paths)} files -> {out_path.name}")

    ds = xr.open_mfdataset(
        [str(p) for p in nc_paths],
        combine="by_coords",
        preprocess=standardize_for_merge,
        parallel=False,
    )

    data_vars = list(ds.data_vars)
    if not data_vars:
        raise ValueError("No data variables in opened datasets.")

    enc = {v: {"zlib": True, "complevel": 3, "dtype": "float32"} for v in data_vars}

    out_path.parent.mkdir(parents=True, exist_ok=True)
    ds.to_netcdf(out_path, encoding=enc)
    log(f"[ok] merged saved: {out_path}")


# -----------------------------------------------------------------------------#
# Main
# -----------------------------------------------------------------------------#

def build_parser():
    ap = argparse.ArgumentParser(
        description=(
            "Download CHIRTS-daily Tmax/Tmin by year range; optional clip; "
            "compute Tavg; merge outputs (saved in --outdir)."
        )
    )

    ap.add_argument("--start", type=int, required=True, help="Start year (>=1983)")
    ap.add_argument("--end", type=int, required=True, help="End year (<=2016)")

    ap.add_argument(
        "--outdir",
        default="chirts_daily_downloads",
        help="Directory to save yearly and merged files",
    )

    ap.add_argument(
        "--res",
        choices=["p25", "p05"],
        default="p25",
        help="Africa CHIRTS resolution: p25=0.25°, p05=0.05°",
    )

    ap.add_argument(
        "--clip",
        nargs=4,
        type=float,
        metavar=("N", "S", "W", "E"),
        help="Optional clip box (degrees): North South West East",
    )

    ap.add_argument(
        "--merge-name",
        type=str,
        default=None,
        help="Merged filename (no path). If omitted, an automatic name is used.",
    )

    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing yearly files",
    )

    return ap

def main():
    # Windows-friendly hint when run with no arguments (e.g., double-click)
    if sys.platform.startswith("win") and len(sys.argv) == 1:
        print(
            "\n[hint] This script is best run from CMD/PowerShell like:\n"
            "  python download_merge_chirts_daily.py --start 2000 --end 2002 "
            "--res p25 --clip 15 3 33 48 --outdir data/chirts_daily_eth\n"
        )
        build_parser().print_help()
        return

    ap = build_parser()
    args = ap.parse_args()

    # CHIRTS-daily v1 coverage guard
    if args.start < 1983 or args.end > 2016 or args.start > args.end:
        raise ValueError("CHIRTS-daily v1.0 valid year range is 1983–2016.")

    if args.res == "p05":
        warn("You selected p05 (0.05°). Files can be very large. "
             "Consider testing with p25 first.")

    years = list(range(args.start, args.end + 1))
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    processed_year_files = []

    for y in years:
        urls = build_urls(y, args.res)

        raw_tmax = outdir / f"Tmax.{y}.{args.res}.nc"
        raw_tmin = outdir / f"Tmin.{y}.{args.res}.nc"

        # Download Tmax
        if not raw_tmax.exists() or args.overwrite:
            log(f"[GET] {urls['tmax']}")
            try:
                download_file(urls["tmax"], raw_tmax)
                log(f"[ok ] saved {raw_tmax.name}")
            except Exception as e:
                print(f"[ERR] download failed for Tmax {y}: {e}")
                continue
        else:
            log(f"[skip] {raw_tmax.name} exists")

        # Download Tmin
        if not raw_tmin.exists() or args.overwrite:
            log(f"[GET] {urls['tmin']}")
            try:
                download_file(urls["tmin"], raw_tmin)
                log(f"[ok ] saved {raw_tmin.name}")
            except Exception as e:
                print(f"[ERR] download failed for Tmin {y}: {e}")
                continue
        else:
            log(f"[skip] {raw_tmin.name} exists")

        # Process yearly pair -> combined dataset
        try:
            import xarray as xr

            ds_max = xr.open_dataset(raw_tmax)
            ds_min = xr.open_dataset(raw_tmin)

            # Optional clip
            if args.clip:
                N, S, W, E = args.clip
                ds_max = clip_box(ds_max, N, S, W, E)
                ds_min = clip_box(ds_min, N, S, W, E)
            else:
                ds_max = standardize_for_merge(ds_max)
                ds_min = standardize_for_merge(ds_min)

            ds_year = build_year_dataset(ds_max, ds_min)

            clip_tag = "_clip" if args.clip else ""
            out_year = outdir / f"chirts_daily_{args.res}_{y}{clip_tag}.nc"

            if not out_year.exists() or args.overwrite:
                enc = {
                    "tmax": {"zlib": True, "complevel": 3, "dtype": "float32"},
                    "tmin": {"zlib": True, "complevel": 3, "dtype": "float32"},
                    "tavg": {"zlib": True, "complevel": 3, "dtype": "float32"},
                }
                ds_year.to_netcdf(out_year, encoding=enc)
                log(f"[ok ] yearly processed → {out_year.name}")
            else:
                log(f"[skip] {out_year.name} exists")

            if out_year.exists():
                processed_year_files.append(out_year)

        except Exception as e:
            print(f"[warn] processing failed for {y}: {e}")
            continue

    # ------------------------------------------------------------------#
    # Merged filename: chirts_p25_2000-2002[_clip].nc
    # ------------------------------------------------------------------#
    if args.merge_name:
        merge_name = Path(args.merge_name).name
    else:
        clip_tag = "_clip" if args.clip else ""
        merge_name = f"chirts_{args.res}_{args.start}-{args.end}{clip_tag}.nc"

    target = outdir / merge_name

    to_merge = [p for p in processed_year_files if p.exists()]

    if to_merge:
        try:
            merge_to_netcdf(to_merge, target)
        except Exception as e:
            print(f"[ERR] merge failed: {e}")
            sys.exit(2)
    else:
        print("[warn] nothing to merge (no processed yearly files).")


if __name__ == "__main__":
    main()
