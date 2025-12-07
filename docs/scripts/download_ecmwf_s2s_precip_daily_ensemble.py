#!/usr/bin/env python
"""
Download ECMWF S2S realtime **daily total precipitation (24h accumulations)**
for multiple ensemble members and compute the ensemble mean.

Example:
python download_ecmwf_s2s_tp_ensemble_dailymean.py \
  --outdir data/s2s_ecmwf \
  --outfile s2s_ecmwf_ensmean_tp_2025-11-03_ea.nc \
  --date 2025-11-03 \
  --lead-days 14 \
  --members 10 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48
"""

import argparse
import os
from datetime import datetime
from typing import List

import xarray as xr
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


def retrieve_s2s_tp_daily_member(
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
    Submit an ECMWF S2S request for **daily total precipitation** for ONE
    ensemble member (perturbed forecast, type=pf, number=member).

    Returns True if request appears to succeed, False if ECMWF returns an error
    (e.g. "data not found" or empty GRIB/NetCDF).
    """
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
        "type": "pf",          # perturbed forecast (ensemble members)
        "number": str(member),
        "param": "tp",         # daily total precip (paramId 228228 internally)
        "date": date_str,      # YYYY-MM-DD, forecast start date
        "time": "00:00:00",
        "step": steps,         # e.g. "24/48/72/..."
        "area": area,
        "format": fmt,
        "target": out_path,
        # Avoid failing with "Expected N, got M" if some steps are missing
        "expect": "any",
    }

    if grid is not None:
        request["grid"] = grid  # e.g. "1.5/1.5" or "0.5/0.5"

    print(f"[info] Submitting S2S daily TP request to ECMWF for member={member}...")
    print("[info] Request:", request)

    try:
        server.retrieve(request)
    except Exception as exc:
        print(f"[warn] ECMWF request failed for member={member}: {exc}")
        return False

    # Quick file sanity check (sometimes an empty file is created)
    if (not os.path.exists(out_path)) or (os.path.getsize(out_path) < 500):
        print(f"[warn] Output for member={member} looks empty or too small: {out_path}")
        return False

    print(f"[info] Download finished for member={member}: {out_path}")
    return True


def compute_ensemble_mean_tp(
    member_files: List[str],
    out_path: str,
) -> None:
    """
    Read all member NetCDFs, stack along 'member', optionally convert TP to
    mm/day (if still in m or kg m**-2), and write ensemble mean to out_path.
    """
    datasets = []
    member_ids = []

    for m, fpath in enumerate(member_files, start=1):
        if not os.path.exists(fpath):
            print(f"[warn] Member file missing, skipping: {fpath}")
            continue

        try:
            ds = xr.open_dataset(fpath)
        except Exception as exc:
            print(f"[warn] Failed to open {fpath}: {exc}")
            continue

        if "tp" not in ds:
            print(f"[warn] No 'tp' variable in {fpath}, skipping.")
            continue

        da = ds["tp"]

        units = str(da.attrs.get("units", "")).lower()

        # Convert only if still in m or kg m**-2
        if (
            "kg m-2" in units
            or "kg m**-2" in units
            or units.strip() == "m"
            or "m of water" in units
        ):
            da.attrs["units"] = "mm/day"
            print(f"[info] Converted TP from '{units}' to 'mm/day' for member {m}")
        elif "mm" in units:
            # Already in mm or mm/day → leave as is
            print(f"[info] TP already in mm units ('{units}') for member {m}, no scaling.")
        else:
            print(
                f"[warn] Unrecognized TP units '{units}' in {fpath}, "
                "leaving values unchanged."
            )

        # Add member dimension
        da = da.expand_dims({"member": [m]})
        datasets.append(da)
        member_ids.append(m)

    if not datasets:
        raise RuntimeError("No valid member files found to build ensemble mean.")

    tp_all = xr.concat(datasets, dim="member")
    tp_all["member"] = member_ids

    ens_mean = tp_all.mean(dim="member", skipna=True)
    ens_ds = ens_mean.to_dataset(name="tp")

    # Make sure units label is sensible
    if "units" not in ens_ds["tp"].attrs:
        ens_ds["tp"].attrs["units"] = "mm/day"

    ens_ds.to_netcdf(out_path)
    print(f"[info] Ensemble mean written to: {out_path}")
    print("[info] Variable: 'tp' (dims: time, lat, lon)")



# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Download ECMWF S2S realtime daily total precipitation (24h accum) "
            "for multiple ensemble members and compute ensemble mean."
        )
    )
    p.add_argument("--outdir", required=True, help="Output directory")
    p.add_argument("--outfile", required=True, help="Final ensemble-mean filename (NetCDF)")
    p.add_argument(
        "--date",
        required=True,
        help="Forecast initial date (YYYY-MM-DD) for S2S start (use valid S2S start, e.g. Monday/Thursday).",
    )
    p.add_argument(
        "--lead-days",
        type=int,
        required=True,
        help="Number of lead days (1–46) of daily totals to retrieve",
    )
    p.add_argument(
        "--members",
        type=int,
        required=True,
        help="Number of ensemble members (perturbed forecasts) to request (e.g. 10, 20, 50).",
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
        help="Output format for member files (default: netcdf).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # Ensure output directory exists
    os.makedirs(args.outdir, exist_ok=True)
    ens_out_path = os.path.join(args.outdir, args.outfile)

    # Basic date sanity check
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit(f"Invalid --date '{args.date}', expected YYYY-MM-DD") from exc

    # Base path for member files (same prefix as final ensemble file)
    base_prefix = os.path.splitext(ens_out_path)[0]

    member_files: List[str] = []

    for m in range(1, args.members + 1):
        member_path = f"{base_prefix}_member{m:02d}.nc"
        ok = retrieve_s2s_tp_daily_member(
            date_str=args.date,
            lead_days=args.lead_days,
            lat_min=args.lat_min,
            lat_max=args.lat_max,
            lon_min=args.lon_min,
            lon_max=args.lon_max,
            member=m,
            out_path=member_path,
            grid=args.grid,
            fmt=args.fmt,
        )
        if ok:
            member_files.append(member_path)
        else:
            print(f"[warn] Skipping member={m} due to retrieval/conversion issues.")

    if not member_files:
        raise SystemExit("No member files were successfully downloaded. Aborting.")

    # Compute ensemble mean from the successfully downloaded members
    compute_ensemble_mean_tp(member_files, ens_out_path)


if __name__ == "__main__":
    main()