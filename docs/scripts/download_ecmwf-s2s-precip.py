#!/usr/bin/env python
"""
Download ECMWF S2S realtime **daily total precipitation** (24-hour accumulations).

Example:
python download_ecmwf_s2s_tp_daily.py \
  --outdir data/s2s_ecmwf \
  --outfile s2s_ecmwf_daily_tp_2025-11-01_ea.nc \
  --date 2025-11-01 \
  --lead-days 30 \
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
    Build a MARS step string for 24-hour lead times.

    For lead_days = 5 → "24/48/72/96/120"
    (i.e. end of each 24-hour accumulation period).
    """
    if lead_days < 1:
        raise ValueError("lead_days must be >= 1")

    steps = [str(24 * (i + 1)) for i in range(lead_days)]
    return "/".join(steps)


def retrieve_s2s_tp_daily(
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
    Submit an ECMWF S2S request for **daily total precipitation** (control forecast).

    The request uses:
      class  = s2
      stream = enfo
      type   = cf  (control forecast)
      origin = ecmf
      param  = tp  (internally mapped to paramId 228228 = 24h total precip)
    """
    # Safety: ECMWF S2S daily product goes up to 46 days
    if lead_days < 1 or lead_days > 46:
        raise ValueError("lead_days must be between 1 and 46 for ECMWF S2S.")

    server = ECMWFDataServer()

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
        "type": "cf",          # control forecast
        "number": "0",         # control member
        "param": "tp",         # daily total precip (internally paramId 228228)
        "date": date_str,      # YYYY-MM-DD, forecast start date
        "time": "00:00:00",
        "step": steps,         # e.g. "24/48/72/..."
        "area": area,
        "format": fmt,
        "target": out_path,
        # Avoid failing with "Expected N, got M" if some steps are missing
        "expect": "any",
    }

    # Optional horizontal interpolation grid, e.g. "1.5/1.5" or "0.5/0.5"
    if grid is not None:
        request["grid"] = grid

    print("[info] Submitting S2S daily TP request to ECMWF...")
    print("[info] Request:", request)
    server.retrieve(request)
    print(f"[info] Download finished: {out_path}")
    print("[info] NetCDF will contain a variable like 'tp' with dims (time, lat, lon).")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Download ECMWF S2S realtime daily total precipitation (24h accum)."
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
        help="Number of lead days (1–46) of daily totals to retrieve",
    )
    p.add_argument("--lat-min", type=float, required=True)
    p.add_argument("--lat-max", type=float, required=True)
    p.add_argument("--lon-min", type=float, required=True)
    p.add_argument("--lon-max", type=float, required=True)
    p.add_argument(
        "--grid",
        default=None,
        help="Optional output grid resolution 'lat/lon', e.g. '1.5/1.5' or '0.5/0.5'",
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

    # Ensure output directory exists
    os.makedirs(args.outdir, exist_ok=True)
    out_path = os.path.join(args.outdir, args.outfile)

    # Basic date sanity check
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit(f"Invalid --date '{args.date}', expected YYYY-MM-DD") from exc

    retrieve_s2s_tp_daily(
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