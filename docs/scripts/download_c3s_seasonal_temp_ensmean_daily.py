#!/usr/bin/env python
"""
Download C3S seasonal ECMWF original single-level *2m temperature* for all
ensemble members, compute the ensemble mean at daily lead times, and save as a
compact [time, latitude, longitude] NetCDF file.

Example
-------
python download_c3s_seasonal_t2m_ensmean_daily.py \
  --outdir data/c3s_seasonal \
  --outfile c3s_seasonal_ecmwf_t2m_ensmean_2025-11_ea.nc \
  --originating-centre ecmwf \
  --system 51 \
  --year 2025 --month 11 --day 1 \
  --lead-days 30 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 46

Notes
-----
* Dataset: "seasonal-original-single-levels"
* Variable: "2m_temperature" (returned as `t2m`, usually in Kelvin).
* Lead times: requested as 24, 48, …, 24*lead_days hours.
* This script:
    - retrieves all ensemble members (dimension `number`)
    - computes the ensemble mean over `number`
    - builds a proper `time` coordinate from
      `forecast_reference_time + forecast_period`
    - drops `forecast_reference_time`, `forecast_period`, `valid_time`
    - outputs: t2m(time, latitude, longitude)
"""

import argparse
import os
from datetime import datetime

import cdsapi
import xarray as xr


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def build_leadtime_hours(lead_days: int) -> list[str]:
    """
    Build a list of lead times in hours for daily steps.

    For lead_days = 5 → ["24", "48", "72", "96", "120"].
    """
    if lead_days < 1:
        raise ValueError("lead_days must be >= 1")
    return [str(24 * (i + 1)) for i in range(lead_days)]


def standardise_t2m_dataset(ds: xr.Dataset) -> xr.Dataset:
    """
    Convert a Dataset with dims:
        (forecast_period, forecast_reference_time, latitude, longitude)
    into:
        t2m(time, latitude, longitude)

    where:
        time = forecast_reference_time + forecast_period

    It drops the original forecast_* coords and valid_time.
    """
    if "forecast_reference_time" not in ds.coords:
        raise ValueError("Dataset missing 'forecast_reference_time' coordinate")
    if "forecast_period" not in ds.coords:
        raise ValueError("Dataset missing 'forecast_period' coordinate")

    # 1. Build a proper datetime 'time' coordinate
    ref_time = ds["forecast_reference_time"].isel(forecast_reference_time=0)
    period = ds["forecast_period"]

    # ref_time is scalar datetime64, period is 1D timedelta64 → result is 1D datetime64
    time_values = (ref_time + period).values  # IMPORTANT: use .values (numpy array)

    ds = ds.assign_coords(time=("forecast_period", time_values))

    # 2. Make 'time' the main dimension instead of 'forecast_period'
    ds = ds.swap_dims({"forecast_period": "time"})

    # 3. Drop singleton forecast_reference_time dimension
    ds = ds.squeeze("forecast_reference_time", drop=True)

    # 4. Drop coordinates/variables we no longer want to expose
    drop_names = []
    for name in ["forecast_reference_time", "forecast_period", "valid_time"]:
        if name in ds.coords or name in ds.variables:
            drop_names.append(name)
    if drop_names:
        ds = ds.drop_vars(drop_names)

    # 5. Ensure dimension order is [time, latitude, longitude]
    ds = ds.transpose("time", "latitude", "longitude")

    return ds


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Download C3S seasonal ECMWF 2m temperature for all ensemble "
            "members, compute daily ensemble mean, and save as "
            "t2m(time, latitude, longitude)."
        )
    )
    p.add_argument("--outdir", required=True, help="Output directory")
    p.add_argument("--outfile", required=True, help="Output NetCDF filename")
    p.add_argument(
        "--originating-centre",
        default="ecmwf",
        help="Originating centre (e.g. 'ecmwf', default: ecmwf)",
    )
    p.add_argument(
        "--system",
        default="51",
        help="Forecast system identifier as string (e.g. '51')",
    )
    p.add_argument("--year", type=int, required=True, help="Forecast year")
    p.add_argument("--month", type=int, required=True, help="Forecast month (1–12)")
    p.add_argument("--day", type=int, required=True, help="Forecast day (1–31)")
    p.add_argument(
        "--lead-days",
        type=int,
        required=True,
        help="Number of daily lead times to retrieve (e.g. 30)",
    )
    p.add_argument("--lat-min", type=float, required=True, help="Southern latitude")
    p.add_argument("--lat-max", type=float, required=True, help="Northern latitude")
    p.add_argument("--lon-min", type=float, required=True, help="Western longitude")
    p.add_argument("--lon-max", type=float, required=True, help="Eastern longitude")
    p.add_argument(
        "--max-members",
        type=int,
        default=None,
        help=(
            "Optional: use only the first N ensemble members when computing "
            "the mean. By default all members are used."
        ),
    )
    return p.parse_args()


# --------------------------------------------------------------------------- #
# Main logic
# --------------------------------------------------------------------------- #


def main() -> None:
    args = parse_args()

    # Basic input checks
    if args.lat_min >= args.lat_max:
        raise SystemExit("--lat-min must be < --lat-max")
    if args.lon_min >= args.lon_max:
        raise SystemExit("--lon-min must be < --lon-max")
    if args.lead_days < 1:
        raise SystemExit("--lead-days must be >= 1")

    # Ensure output dir exists
    os.makedirs(args.outdir, exist_ok=True)

    final_path = os.path.join(args.outdir, args.outfile)
    raw_path = final_path + ".raw.nc"

    # Date sanity check
    try:
        datetime(args.year, args.month, args.day)
    except ValueError as exc:
        raise SystemExit(f"Invalid date: {exc}") from exc

    # Build request pieces
    leadtime_hours = build_leadtime_hours(args.lead_days)
    area = [float(args.lat_max), float(args.lon_min),
            float(args.lat_min), float(args.lon_max)]

    dataset = "seasonal-original-single-levels"
    request = {
        "originating_centre": args.originating_centre,
        "system": str(args.system),
        "variable": ["2m_temperature"],
        "year": f"{args.year:04d}",
        "month": f"{args.month:02d}",
        "day": f"{args.day:02d}",
        "leadtime_hour": leadtime_hours,
        "data_format": "netcdf",
        "area": area,
    }

    print("[info] Submitting C3S seasonal T2M request …")
    print("[info] Dataset:", dataset)
    print("[info] Request payload:", request)

    client = cdsapi.Client()
    client.retrieve(dataset, request, raw_path)
    print(f"[info] Raw C3S file saved → {raw_path}")

    # Open with xarray
    ds_raw = xr.open_dataset(raw_path)

    if "t2m" not in ds_raw.data_vars:
        raise SystemExit("Variable 't2m' not found in retrieved dataset.")

    # Optionally restrict ensemble members before averaging
    if "number" in ds_raw.dims and args.max_members is not None:
        n_avail = ds_raw.sizes["number"]
        if args.max_members < 1:
            raise SystemExit("--max-members must be >= 1")
        if args.max_members > n_avail:
            print(
                f"[warn] Requested max_members={args.max_members}, "
                f"but only {n_avail} available. Using all members."
            )
        else:
            print(f"[info] Using only the first {args.max_members} members.")
            ds_raw = ds_raw.isel(number=slice(0, args.max_members))

    # Ensemble mean over 'number'
    t2m = ds_raw["t2m"]
    if "number" in t2m.dims:
        t2m_ens_mean = t2m.mean(dim="number", skipna=True)
    else:
        t2m_ens_mean = t2m

    # You can convert from K to °C if you want:
    # t2m_ens_mean = t2m_ens_mean - 273.15
    # t2m_ens_mean.attrs["units"] = "degC"

    ds_mean = t2m_ens_mean.to_dataset(name="t2m")


    ds_mean = t2m_ens_mean.to_dataset(name="t2m")
    ds_mean['t2m'].attrs = {'units':'K', 'long_name':'2 metre temperature'}
    ds_mean["t2m"].attrs.setdefault("long_name", "2 metre temperature")

    ds_mean.attrs["units"] = "K"
    ds_mean.attrs["long_name"] = "2 metre temperature"



    # Standardise to t2m(time, latitude, longitude)
    ds_final = standardise_t2m_dataset(ds_mean)

    ds_final.to_netcdf(final_path)
    print(f"[info] Ensemble-mean daily T2M saved → {final_path}")
    print("[info] Dimensions:", ds_final.dims)
    print("[info] Variables:", list(ds_final.data_vars))


if __name__ == "__main__":
    main()
