#!/usr/bin/env python3
"""
vectri_plot_outputs.py

Auto-detect and plot VECTRI output variables:
- Vector, disease, hydrology groups (keyword-based)
- Time-mean maps
- Area-mean time series (global or Ethiopia bbox)
- Optional baseline vs compare file difference summaries

Usage:
  python vectri_plot_outputs.py --nc outputs/base.nc --outdir figures/global
  python vectri_plot_outputs.py --nc outputs/base.nc --outdir figures/ethiopia --ethiopia
  python vectri_plot_outputs.py --nc outputs/base.nc --compare outputs/exp_temp_plus1K.nc --outdir figures/ethiopia --ethiopia

Requirements:
  - xarray
  - numpy
  - matplotlib
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt


GROUP_KEYWORDS: Dict[str, List[str]] = {
    "vector": [
        "vector", "adult", "mosquito",
        "larv", "larvae",
        "emerge", "emergence",
        "hbr", "bite", "biting",
    ],
    "disease": [
        "prd", "cspr", "eir",
        "case", "cases",
        "immune", "immunity",
        "infect", "infection", "parasite", "pr",
    ],
    "hydro": [
        "wperm", "wurbn", "wpond",
        "pond", "water",
    ],
}


def detect_coord(ds: xr.Dataset, kind: str) -> Optional[str]:
    kind = kind.lower()
    # Search coords first
    for c in ds.coords:
        cl = c.lower()
        if kind == "time" and "time" in cl:
            return c
        if kind == "lat" and (cl in ["lat", "latitude", "y"] or "lat" in cl):
            return c
        if kind == "lon" and (cl in ["lon", "longitude", "x"] or "lon" in cl):
            return c
    # Then dims
    for d in ds.dims:
        dl = d.lower()
        if kind == "time" and "time" in dl:
            return d
        if kind == "lat" and (dl in ["lat", "latitude", "y"] or "lat" in dl):
            return d
        if kind == "lon" and (dl in ["lon", "longitude", "x"] or "lon" in dl):
            return d
    return None


def group_for_var(var_name: str) -> Optional[str]:
    vn = var_name.lower()
    for g, keys in GROUP_KEYWORDS.items():
        for k in keys:
            if k in vn:
                return g
    return None


def select_vars(ds: xr.Dataset, max_fallback: int = 6) -> Dict[str, List[str]]:
    grouped: Dict[str, List[str]] = {"vector": [], "disease": [], "hydro": []}
    other: List[str] = []

    for v in ds.data_vars:
        g = group_for_var(v)
        if g:
            grouped[g].append(v)
        else:
            other.append(v)

    # If nothing detected in all groups, fallback to first few vars
    if sum(len(vs) for vs in grouped.values()) == 0:
        fallback = list(ds.data_vars)[:max_fallback]
        grouped["vector"] = fallback  # place under vector just to ensure plotting
    return grouped


def subset_bbox(ds: xr.Dataset, lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> xr.Dataset:
    lat = detect_coord(ds, "lat")
    lon = detect_coord(ds, "lon")
    if not lat or not lon:
        return ds

    lat_vals = ds[lat].values
    lon_vals = ds[lon].values

    lat_slice = slice(lat_min, lat_max) if lat_vals[0] <= lat_vals[-1] else slice(lat_max, lat_min)
    lon_slice = slice(lon_min, lon_max) if lon_vals[0] <= lon_vals[-1] else slice(lon_max, lon_min)

    return ds.sel({lat: lat_slice, lon: lon_slice})


def time_mean_map(da: xr.DataArray) -> xr.DataArray:
    time_dim = next((d for d in da.dims if "time" in d.lower()), None)
    return da.mean(time_dim, skipna=True) if time_dim else da


def area_mean_ts(da: xr.DataArray) -> xr.DataArray:
    # identify spatial dims by name patterns
    lat_dim = next((d for d in da.dims if "lat" in d.lower()), None)
    lon_dim = next((d for d in da.dims if "lon" in d.lower()), None)
    spatial = [d for d in [lat_dim, lon_dim] if d and d in da.dims]
    return da.mean(spatial, skipna=True) if spatial else da


def save_map(fig_path: Path, field: xr.DataArray, title: str):
    plt.figure()
    try:
        field.plot()
    except Exception:
        # If plot fails due to non-2D structure, just skip gracefully
        plt.close()
        return
    plt.title(title)
    plt.tight_layout()
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(fig_path, dpi=180)
    plt.close()


def save_ts(fig_path: Path, ts: xr.DataArray, title: str):
    plt.figure()
    try:
        ts.plot()
    except Exception:
        plt.close()
        return
    plt.title(title)
    plt.tight_layout()
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(fig_path, dpi=180)
    plt.close()


def main():
    ap = argparse.ArgumentParser(description="Auto-plot VECTRI outputs by group.")
    ap.add_argument("--nc", required=True, help="Primary VECTRI NetCDF output.")
    ap.add_argument("--compare", default=None, help="Optional comparison NetCDF to compute simple deltas.")
    ap.add_argument("--outdir", required=True, help="Directory to save figures.")
    ap.add_argument("--ethiopia", action="store_true", help="Subset to Ethiopia bbox before plotting.")
    ap.add_argument("--lat-min", type=float, default=3)
    ap.add_argument("--lat-max", type=float, default=15)
    ap.add_argument("--lon-min", type=float, default=33)
    ap.add_argument("--lon-max", type=float, default=48)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    ds = xr.open_dataset(args.nc)

    ds_cmp: Optional[xr.Dataset] = None
    if args.compare:
        ds_cmp = xr.open_dataset(args.compare)

    if args.ethiopia:
        ds = subset_bbox(ds, args.lat_min, args.lat_max, args.lon_min, args.lon_max)
        if ds_cmp is not None:
            ds_cmp = subset_bbox(ds_cmp, args.lat_min, args.lat_max, args.lon_min, args.lon_max)

    grouped = select_vars(ds)

    # Plot per group
    for group, vars_list in grouped.items():
        for v in vars_list:
            if v not in ds.data_vars:
                continue

            da = ds[v]

            # 1) Map
            field = time_mean_map(da)
            map_path = outdir / f"{group}__{v}__map.png"
            save_map(map_path, field, title=f"{group.upper()} | {v} | time-mean")

            # 2) Time series
            ts = area_mean_ts(da)
            ts_path = outdir / f"{group}__{v}__ts.png"
            save_ts(ts_path, ts, title=f"{group.upper()} | {v} | area-mean")

            # 3) If compare provided, compute a simple delta summary
            if ds_cmp is not None and v in ds_cmp.data_vars:
                try:
                    da2 = ds_cmp[v]
                    # Align to avoid coordinate mismatch issues
                    da1a, da2a = xr.align(da, da2, join="inner")
                    delta = da2a - da1a

                    # Delta map
                    dfield = time_mean_map(delta)
                    dmap_path = outdir / f"{group}__{v}__delta_map.png"
                    save_map(dmap_path, dfield, title=f"{group.upper()} | {v} | compare - base (time-mean)")

                    # Delta time series
                    dts = area_mean_ts(delta)
                    dts_path = outdir / f"{group}__{v}__delta_ts.png"
                    save_ts(dts_path, dts, title=f"{group.UPPER()} | {v} | compare - base (area-mean)")
                except Exception:
                    # Don't fail the whole script for one variable
                    pass

    # Write a small text inventory for the instructor
    inv_path = outdir / "variable_inventory.txt"
    lines = [f"Source file: {args.nc}"]
    if args.compare:
        lines.append(f"Compare file: {args.compare}")
    if args.ethiopia:
        lines.append(f"Subset: Ethiopia bbox lat[{args.lat_min},{args.lat_max}] lon[{args.lon_min},{args.lon_max}]")
    lines.append("")
    lines.append("Detected grouping:")
    for g, vs in grouped.items():
        lines.append(f"- {g}:")
        for v in vs:
            lines.append(f"    * {v}")
    inv_path.write_text("\n".join(lines), encoding="utf-8")

    print("Done. Figures written to:", outdir)
    print("Inventory:", inv_path)


if __name__ == "__main__":
    main()