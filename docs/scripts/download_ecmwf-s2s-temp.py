#!/usr/bin/env python
"""
Download ECMWF S2S realtime **daily-averaged 2m temperature (T2M)**.

Example:
python download_ecmwf_s2s_t2m_daily.py \
  --outdir data/s2s_ecmwf \
  --outfile s2s_ecmwf_daily_t2m_2025-11-01_ea.nc \
  --date 2025-11-01 \
  --lead-days 5 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48
"""

import argparse
import os
from datetime import datetime
from ecmwfapi import ECMWFDataServer


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def build_daily_step_string(lead_days: int) -> str:
    """
    Build ECMWF S2S *daily* step string with intervals:
    "0-24/24-48/48-72/..."

    According to the S2S docs, this is the way to request
    daily-mean/daily-accumulated products.
    """
    periods = []
    for i in range(lead_days):
        start = i * 24
        end = (i + 1) * 24
        periods.append(f"{start}-{end}")
    return "/".join(periods)


def retrieve_s2s_t2m_daily(
    date_str: str,
    lead_days: int,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    out_path: str,
    grid: str | None = None,
    fmt: str = "netcdf",
) -> None:
    """
    Submit an ECMWF S2S request for daily-averaged
    2m temperature (T2M, param=2t), control forecast.
    """
    server = ECMWFDataServer()

    # S2S ECMWF daily-averaged typically goes up to 46 days
    if lead_days < 1 or lead_days > 46:
        raise ValueError("lead_days must be between 1 and 46 for ECMWF S2S.")

    steps = build_daily_step_string(lead_days)

    # ECMWF area string is N/W/S/E
    area = f"{lat_max}/{lon_min}/{lat_min}/{lon_max}"

    request = {
        "class": "s2",
        "dataset": "s2s",
        "expver": "prod",
        "origin": "ecmf",
        "model": "glob",
        "levtype": "sfc",
        "stream": "enfo",
        "type": "cf",       # control forecast
        "number": "0",      # control member
        "param": "2t",      # ONLY 2m temperature
        "date": date_str,   # YYYY-MM-DD
        "time": "00:00:00",
        "step": steps,      # "0-24/24-48/..."
        "area": area,
        "format": fmt,
        "target": out_path,
        # Allow partial retrieval instead of failing with "Expected N, got M"
        "expect": "any",
    }

    # Optional regular grid
    if grid is not None:
        request["grid"] = grid  # e.g. "1.5/1.5" or "0.5/0.5"

    print("[info] Submitting ECMWF S2S T2M daily request…")
    print("[info] Request:", request)
    server.retrieve(request)
    print(f"[info] Download finished → {out_path}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Download ECMWF S2S realtime daily-averaged 2m temperature (T2M)."
    )
    p.add_argument("--outdir", required=True, help="Output directory")
    p.add_argument("--outfile", required=True, help="Output filename (NetCDF)")
    p.add_argument(
        "--date",
        required=True,
        help="Forecast initial date (YYYY-MM-DD) for S2S start",
    )
    p.add_argument(
        "--lead-days",
        type=int,
        required=True,
        help="Number of lead days (1–46) of daily averages to retrieve",
    )
    p.add_argument("--lat-min", type=float, required=True)
    p.add_argument("--lat-max", type=float, required=True)
    p.add_argument("--lon-min", type=float, required=True)
    p.add_argument("--lon-max", type=float, required=True)
    p.add_argument(
        "--grid",
        default=None,
        help="Optional output grid resolution 'lat/lon', "
             "e.g. '1.5/1.5' or '0.5/0.5'",
    )
    p.add_argument(
        "--fmt",
        default="netcdf",
        choices=["netcdf", "grib"],
        help="Output format (default: netcdf)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # Ensure output dir exists
    os.makedirs(args.outdir, exist_ok=True)
    out_path = os.path.join(args.outdir, args.outfile)

    # Basic date sanity check
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit(f"Invalid --date '{args.date}', expected YYYY-MM-DD") from exc

    retrieve_s2s_t2m_daily(
        date_str=args.date,
        lead_days=args.lead_days,
        lat_min=args.lat_min,
        lat_max=args.lat_max,
        lon_min=args.lon_min,
        lon_max=args.lon_max,
        out_path=out_path,
        grid=args.grid,
        fmt=args.fmt,
    )


if __name__ == "__main__":
    main()