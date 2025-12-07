#!/usr/bin/env python
"""
Download ECMWF S2S realtime daily-averaged 2m temperature (T2M)
for multiple ensemble members and compute the ensemble mean.

Example:
python download_ecmwf_s2s_t2m_ensemble_dailymean.py \
  --outdir data/s2s_ecmwf \
  --outfile s2s_ecmwf_t2m_ensmean_2025-12-01_ea.nc \
  --date 2025-12-01 \
  --lead-days 30 \
  --members 10 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48
"""

import argparse
import os
from datetime import datetime
from ecmwfapi import ECMWFDataServer
import xarray as xr
import numpy as np


def build_daily_step_string(lead_days: int) -> str:
    """Build ECMWF S2S daily step string: '0-24/24-48/48-72/...'"""
    periods = [f"{i*24}-{(i+1)*24}" for i in range(lead_days)]
    return "/".join(periods)


def retrieve_member_t2m_daily(
    date_str: str,
    lead_days: int,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    member: int,
    out_path: str,
    grid: str | None = None,
    fmt: str = "netcdf",
) -> bool:
    """
    Retrieve ECMWF S2S daily-averaged 2m temperature for one ensemble member.

    Returns True if successful, False otherwise.
    """
    server = ECMWFDataServer()
    if lead_days < 1 or lead_days > 46:
        raise ValueError("lead_days must be between 1 and 46 for ECMWF S2S.")

    steps = build_daily_step_string(lead_days)
    area = f"{lat_max}/{lon_min}/{lat_min}/{lon_max}"

    req = {
        "class": "s2",
        "dataset": "s2s",
        "expver": "prod",
        "origin": "ecmf",
        "model": "glob",
        "levtype": "sfc",
        "stream": "enfo",
        "type": "pf",           # perturbed forecast
        "number": str(member),  # ensemble member id (1..N)
        "param": "2t",
        "date": date_str,
        "time": "00:00:00",
        "step": steps,
        "area": area,
        "format": fmt,
        "target": out_path,
        "expect": "any",
    }
    if grid is not None:
        req["grid"] = grid

    print(f"[info] Requesting member={member}...")

    try:
        server.retrieve(req)
    except Exception as exc:
        print(f"[warn] ECMWF request failed for member={member}: {exc}")
        return False

    # Check file validity
    if (not os.path.exists(out_path)) or (os.path.getsize(out_path) < 500):
        print(f"[warn] Output for member={member} looks empty or too small")
        return False

    print(f"[done] Member {member} → {out_path}")
    return True


def compute_ensemble_mean(member_files, out_path, to_celsius=True):
    """
    Compute ensemble mean across member files (preserving lead days).

    Parameters
    ----------
    member_files : list
        List of paths to member NetCDF files
    out_path : str
        Output path for ensemble mean
    to_celsius : bool
        Convert from Kelvin to Celsius (default True)
    """
    print(f"[info] Merging {len(member_files)} members...")

    datasets = []
    valid_members = []

    for i, f in enumerate(member_files, 1):
        if not os.path.exists(f):
            print(f"[warn] Member file missing: {f}")
            continue
        try:
            ds = xr.open_dataset(f)
            # Handle different variable names
            if 't2m' in ds:
                da = ds['t2m']
            elif '2t' in ds:
                da = ds['2t']
            else:
                print(f"[warn] No temperature variable in {f}")
                continue
            datasets.append(da)
            valid_members.append(i)
        except Exception as exc:
            print(f"[warn] Failed to open {f}: {exc}")
            continue

    if not datasets:
        raise RuntimeError("No valid member files found")

    # Stack along member dimension
    da_stack = xr.concat(
        datasets,
        dim=xr.DataArray(valid_members, dims="member"),
    )

    # Compute ensemble mean
    ens_mean = da_stack.mean("member")

    # Convert to Celsius if needed
    if to_celsius and float(ens_mean.max()) > 200:  # Likely Kelvin
        ens_mean = ens_mean - 273.15
        ens_mean.attrs["units"] = "degC"
        print("[info] Converted temperature from Kelvin to Celsius")

    ens_mean.attrs["long_name"] = "Ensemble mean daily 2m temperature"
    ens_mean.name = "t2m"

    # Save to NetCDF
    ds_out = ens_mean.to_dataset(name="t2m")
    ds_out.attrs["title"] = "ECMWF S2S Ensemble Mean 2m Temperature"
    ds_out.attrs["source"] = "ECMWF S2S (param=2t, perturbed forecasts)"
    ds_out.attrs["n_members"] = len(valid_members)

    ds_out.to_netcdf(out_path)
    print(f"[done] Ensemble mean saved → {out_path}")


def compute_ensemble_statistics(member_files, out_path, to_celsius=True):
    """
    Compute full ensemble statistics (mean, std, percentiles).

    Use this for probabilistic products.
    """
    print(f"[info] Computing ensemble statistics from {len(member_files)} members...")

    datasets = []
    valid_members = []

    for i, f in enumerate(member_files, 1):
        if not os.path.exists(f):
            continue
        try:
            ds = xr.open_dataset(f)
            da = ds['t2m'] if 't2m' in ds else ds['2t']
            datasets.append(da)
            valid_members.append(i)
        except:
            continue

    if not datasets:
        raise RuntimeError("No valid member files found")

    # Stack along member dimension
    da_stack = xr.concat(datasets, dim=xr.DataArray(valid_members, dims="member"))

    # Convert to Celsius if needed
    if to_celsius and float(da_stack.max()) > 200:
        da_stack = da_stack - 273.15

    # Compute statistics
    ens_mean = da_stack.mean("member")
    ens_std = da_stack.std("member")
    ens_min = da_stack.min("member")
    ens_max = da_stack.max("member")
    ens_p10 = da_stack.quantile(0.1, dim="member")
    ens_p25 = da_stack.quantile(0.25, dim="member")
    ens_median = da_stack.quantile(0.5, dim="member")
    ens_p75 = da_stack.quantile(0.75, dim="member")
    ens_p90 = da_stack.quantile(0.9, dim="member")

    # Create output dataset
    ds_out = xr.Dataset({
        't2m_mean': ens_mean,
        't2m_std': ens_std,
        't2m_min': ens_min,
        't2m_max': ens_max,
        't2m_p10': ens_p10,
        't2m_p25': ens_p25,
        't2m_median': ens_median,
        't2m_p75': ens_p75,
        't2m_p90': ens_p90,
    })

    # Add attributes
    units = "degC" if to_celsius else "K"
    for var in ds_out.data_vars:
        ds_out[var].attrs["units"] = units

    ds_out.attrs["title"] = "ECMWF S2S Ensemble Temperature Statistics"
    ds_out.attrs["n_members"] = len(valid_members)

    ds_out.to_netcdf(out_path)
    print(f"[done] Ensemble statistics saved → {out_path}")


def main():
    p = argparse.ArgumentParser(
        description="Download ECMWF S2S ensemble daily-mean 2m temperature (T2M)."
    )
    p.add_argument("--outdir", required=True, help="Output directory")
    p.add_argument("--outfile", required=True, help="Final ensemble-mean filename")
    p.add_argument("--date", required=True, help="Forecast date (YYYY-MM-DD)")
    p.add_argument("--lead-days", type=int, required=True, help="Lead days (1-46)")
    p.add_argument("--members", type=int, default=10, help="Number of members (1-50)")
    p.add_argument("--lat-min", type=float, required=True)
    p.add_argument("--lat-max", type=float, required=True)
    p.add_argument("--lon-min", type=float, required=True)
    p.add_argument("--lon-max", type=float, required=True)
    p.add_argument("--grid", default=None, help="Output grid (e.g., '0.5/0.5')")
    p.add_argument("--fmt", default="netcdf", choices=["netcdf", "grib"])
    p.add_argument("--keep-kelvin", action="store_true", 
                   help="Keep temperature in Kelvin (default: convert to Celsius)")
    p.add_argument("--full-stats", action="store_true",
                   help="Compute full statistics (mean, std, percentiles)")
    args = p.parse_args()

    # Validate date
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        raise SystemExit(f"Invalid date format: {args.date}")

    os.makedirs(args.outdir, exist_ok=True)
    member_files = []

    # Download each member
    for m in range(1, args.members + 1):
        fpath = os.path.join(args.outdir, f"t2m_member{m:02d}.nc")
        ok = retrieve_member_t2m_daily(
            args.date,
            args.lead_days,
            args.lat_min, args.lat_max,
            args.lon_min, args.lon_max,
            member=m,
            out_path=fpath,
            grid=args.grid,
            fmt=args.fmt,
        )
        if ok:
            member_files.append(fpath)
        else:
            print(f"[warn] Skipping member={m}")

    if not member_files:
        raise SystemExit("No member files downloaded successfully")

    # Compute ensemble mean or full statistics
    out_nc = os.path.join(args.outdir, args.outfile)

    if args.full_stats:
        compute_ensemble_statistics(
            member_files, out_nc, 
            to_celsius=not args.keep_kelvin
        )
    else:
        compute_ensemble_mean(
            member_files, out_nc,
            to_celsius=not args.keep_kelvin
        )


if __name__ == "__main__":
    main()