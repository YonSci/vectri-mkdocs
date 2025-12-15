# 🌧️ Downloading ECMWF HRES Precipitation Forecasts

## Overview

**ECMWF HRES (High Resolution Forecast)** is the world's leading deterministic weather forecast model. This tutorial guides you through downloading, processing, and converting ECMWF IFS 0.25° total precipitation data into daily accumulations using the ECMWF Open Data API.

<div class="grid cards" markdown>

-   :material-weather-pouring: **Dataset**
    
    ---
    
    ECMWF IFS HRES 0.25° Precipitation
    
    **Variable:** Total Precipitation (tp)  
    **Resolution:** 0.25° (~28 km)  
    **Output:** Daily totals (mm/day)  
    **Forecast Range:** 1–10 days

-   :material-earth: **Spatial Coverage**
    
    ---
    
    **Region:** Global  
    **Latitude:** 90°S to 90°N  
    **Longitude:** -180° to 180°

-   :material-update: **Update Frequency**
    
    ---
    
    **Cycles:** 00Z and 12Z (2× daily)  
    **Latency:** ~6-8 hours after init time  
    **Open Data:** Free access via API

-   :material-file-download: **Access**
    
    ---
    
    **Source:** ECMWF Open Data  
    **Method:** Python API  
    **Authentication:** Not required  
    **Format:** GRIB2 → NetCDF

</div>

---

## 🎯 What This Script Does

```mermaid
graph LR
    A[Select Forecast Run] --> B[ECMWF Open Data API]
    B --> C[Download GRIB2 File]
    C --> D[Extract tp Variable]
    D --> E[Compute Daily Totals]
    E --> F[Convert m → mm]
    F --> G[Clip to Region]
    G --> H[Save NetCDF]
    
    style A fill:#e8f5e9
    style H fill:#c8e6c9
```

The script performs the following operations:

1. **Downloads** accumulated precipitation from ECMWF Open Data
2. **Extracts** total precipitation (tp) at 24-hour intervals
3. **Computes** daily totals by differencing accumulated values
4. **Converts** from meters to mm/day
5. **Clips** data to your specified bounding box
6. **Saves** the result as a compressed NetCDF file

---

## 🚀 Quick Start Guide

### Prerequisites

!!! info "Required Python Packages"
    ```bash
    pip install ecmwf-opendata xarray cfgrib netCDF4 numpy
    ```
    
    !!! warning "cfgrib Requirement"
        The `cfgrib` package requires the **ecCodes** library:
        
        === "Ubuntu/Debian"
            ```bash
            sudo apt-get install libeccodes-dev
            ```
        
        === "macOS"
            ```bash
            brew install eccodes
            ```
        
        === "Conda (Recommended)"
            ```bash
            conda install -c conda-forge ecmwf-opendata cfgrib eccodes
            ```

### Basic Usage

=== "10-Day Forecast"
    ```bash
    python download_ecmwf_hres_precip.py \
        --outdir data/ecmwf_hres \
        --outfile ecmwf_hres_ethiopia_10day.nc \
        --ndays 10 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --time 0
    ```

=== "Latest Available"
    ```bash
    python download_ecmwf_hres_precip.py \
        --outdir data/ecmwf_hres \
        --outfile ecmwf_hres_ethiopia.nc \
        --ndays 10 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48
    ```

=== "Specific Date"
    ```bash
    python download_ecmwf_hres_precip.py \
        --outdir data/ecmwf_hres \
        --outfile ecmwf_hres_ethiopia_20250115.nc \
        --ndays 10 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --date 2025-01-15 \
        --time 0
    ```

---

## 📋 The Complete Script

### Python Download Script

Save this as `download_ecmwf_hres_precip.py`:

```python
#!/usr/bin/env python
"""
Download ECMWF HRES (IFS 0.25°) total precipitation (tp) from ECMWF Open Data,
compute daily 24-hour accumulations, clip to a region of interest,
and save as a single merged NetCDF file.

- Uses ECMWF Free & Open Data (IFS HRES, 0.25° resolution, GRIB2).
- Downloads accumulated total precipitation (tp) at selected lead times.
- Converts accumulated tp -> daily totals for lead days 1..N (N <= 10 for HRES).
- Clips to lat/lon bounding box.
- Writes a single NetCDF with dims (time, lat, lon) and units mm/day.

Example
-------
python download_ecmwf_hres_tp.py \
    --outdir data/ecmwf_hres_tp \
    --outfile ecmwf_hres_tp_ea_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --time 0

Notes
-----
- Daily accumulation is computed from total accumulated precipitation:
    Day 1: tp(24h) - tp(0h)
    Day 2: tp(48h) - tp(24h)
    ...
- Default forecast run: latest available (date/time inferred by ECMWF).
- HRES open-data time steps (00/12 UTC):
    0–144 by 3h, 144–240 by 6h → max 240h = 10 days.
"""

import argparse
from pathlib import Path

import numpy as np
import xarray as xr
from ecmwf.opendata import Client


# ---------------------------------------------------------------------------
# Step selection utilities
# ---------------------------------------------------------------------------

def hres_all_steps():
    """
    Full ECMWF HRES step list for 00Z/12Z in hours:
    0..144 by 3h, 144..240 by 6h
    """
    steps = list(range(0, 145, 3)) + list(range(144, 241, 6))
    # Ensure uniqueness and sorted order
    return sorted(set(steps))


def daily_steps(max_lead_days: int):
    """
    Return the list of step hours needed to compute daily 24h totals
    up to max_lead_days (1–10 for HRES).

    We need step=0 plus 24,48,..., 24*max_lead_days where each step
    actually exists in the open-data step schedule.
    """
    max_lead_days = int(max_lead_days)
    if max_lead_days < 1 or max_lead_days > 10:
        raise ValueError("max_lead_days must be between 1 and 10 for HRES.")

    steps_all = hres_all_steps()
    max_step_hours = max_lead_days * 24

    needed = {0}
    for s in steps_all:
        if 0 < s <= max_step_hours and s % 24 == 0:
            needed.add(s)

    return sorted(needed)


# ---------------------------------------------------------------------------
# Download ECMWF HRES tp from Open Data
# ---------------------------------------------------------------------------

def download_hres_tp_grib(
    target_path: Path,
    ndays: int = 10,
    date: "str | int | None" = None,
    time: "int | None" = None,
):
    """
    Download ECMWF HRES (IFS 0.25°) total precipitation (tp) GRIB2 file
    from ECMWF Free & Open Data for the requested forecast run.

    Parameters
    ----------
    target_path : Path
        Where to store the GRIB2 file.
    ndays : int, optional
        Number of forecast lead days (1–10). Default 10.
    date : str | int | None, optional
        Forecast start date. Examples:
        - '2025-11-30'
        - 0 (today), -1 (yesterday) etc.
        If None, ECMWF will choose the latest available date.
    time : int | None, optional
        Forecast start time (0, 6, 12, 18). If None, ECMWF chooses latest.

    Returns
    -------
    result : ecmwf.opendata.Result
        Result object; result.datetime is the actual forecast init time.
    """
    steps = daily_steps(ndays)

    client = Client(
        source="ecmwf",   # ECMWF Open Data servers
        model="ifs",      # IFS (physics-based HRES)
        resol="0p25",     # 0.25° resolution
    )

    request_kwargs = {
        "type": "fc",
        "param": "tp",
        "step": steps,
    }
    if date is not None:
        request_kwargs["date"] = date
    if time is not None:
        request_kwargs["time"] = time

    result = client.retrieve(
        target=str(target_path),
        **request_kwargs,
    )

    return result


# ---------------------------------------------------------------------------
# Processing GRIB -> daily totals -> clip -> NetCDF
# ---------------------------------------------------------------------------

def open_tp_from_grib(grib_path: Path) -> xr.DataArray:
    """
    Open GRIB2 file and return tp DataArray with step_hours coordinate.

    Returns
    -------
    tp : xr.DataArray
        Dimensions: (step_hours, latitude, longitude)
    """
    ds = xr.open_dataset(
        grib_path,
        engine="cfgrib",
        backend_kwargs={
            "indexpath": "",
            "filter_by_keys": {"shortName": "tp"},
        },
    )

    tp = ds["tp"]  # accumulated from forecast start

    # Drop singleton time dimension (HRES forecast run time)
    if "time" in tp.dims and tp.sizes["time"] == 1:
        tp = tp.isel(time=0, drop=True)

    # Convert 'step' (timedelta64) to integer hours as a numpy array
    step = tp["step"]
    step_hours = (step / np.timedelta64(1, "h")).astype("int32").values

    # Attach as a new coordinate using raw values, not a DataArray
    tp = tp.assign_coords(step_hours=("step", step_hours))

    # Swap dimensions: use step_hours instead of step
    tp = tp.swap_dims({"step": "step_hours"}).drop_vars("step")

    return tp


def compute_daily_totals(tp: xr.DataArray, ndays: int) -> xr.DataArray:
    """
    Compute 24h daily totals from accumulated tp (still in meters).

    tp is accumulated from step=0. We compute:
        day1 = tp(24h) - tp(0h)
        day2 = tp(48h) - tp(24h)
        ...
    """
    max_step_hours = ndays * 24
    step_hours = tp["step_hours"].values

    needed = np.arange(0, max_step_hours + 24, 24)
    missing = [s for s in needed if s not in step_hours]
    if missing:
        raise RuntimeError(
            f"Expected steps {missing} not found in tp; "
            f"got steps={step_hours.tolist()}"
        )

    daily = []
    lead_days = []
    for day in range(1, ndays + 1):
        h1 = day * 24
        h0 = (day - 1) * 24
        daily_tp = tp.sel(step_hours=h1) - tp.sel(step_hours=h0)
        daily.append(daily_tp)
        lead_days.append(day)

    daily_tp = xr.concat(daily, dim="lead_day")
    daily_tp = daily_tp.assign_coords(lead_day=("lead_day", lead_days))

    # Still in meters here; conversion to mm/day is done later
    daily_tp.name = "tp"
    daily_tp.attrs["units"] = tp.attrs.get("units", "m")
    daily_tp.attrs["long_name"] = "Daily total precipitation (24h)"

    return daily_tp


def clip_to_bbox(
    da: xr.DataArray,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
) -> xr.DataArray:
    """
    Clip DataArray to lat/lon bounding box.

    Handles both ascending and descending latitude.
    """
    lat = da.coords.get("latitude")
    lon = da.coords.get("longitude")
    if lat is None or lon is None:
        raise ValueError("Dataset must have 'latitude' and 'longitude' coords.")

    # ECMWF latitude is usually descending (90 -> -90)
    if lat[0] > lat[-1]:
        lat_slice = slice(lat_max, lat_min)
    else:
        lat_slice = slice(lat_min, lat_max)

    lon_slice = slice(lon_min, lon_max)

    return da.sel(latitude=lat_slice, longitude=lon_slice)


def process_to_netcdf(
    grib_path: Path,
    out_nc: Path,
    ndays: int,
    lat_min: float | None = None,
    lat_max: float | None = None,
    lon_min: float | None = None,
    lon_max: float | None = None,
    compress: bool = True,
    init_time=None,
):
    """
    End-to-end processing:
    - Open GRIB
    - Compute daily 24h totals 1..ndays
    - Convert from m to mm/day
    - Rename dims to time, lat, lon
    - Clip to ROI (optional)
    - Save to NetCDF
    """
    # 1) Open and compute daily totals (still in meters)
    tp = open_tp_from_grib(grib_path)
    daily = compute_daily_totals(tp, ndays)

    # 2) Clip to bounding box (still latitude/longitude dims)
    if None not in (lat_min, lat_max, lon_min, lon_max):
        daily = clip_to_bbox(daily, lat_min, lat_max, lon_min, lon_max)

    # 3) Convert from meters to mm/day
    #    (ECMWF tp is m of water equivalent over the accumulation period)
    daily = daily * 1000.0
    daily.attrs["units"] = "mm/day"
    daily.attrs["long_name"] = "Daily total precipitation (24h) [mm/day]"

    # 4) Rename spatial dims/coords to lat, lon
    rename_dims = {}
    if "latitude" in daily.dims:
        rename_dims["latitude"] = "lat"
    if "longitude" in daily.dims:
        rename_dims["longitude"] = "lon"
    if rename_dims:
        daily = daily.rename(rename_dims)


    # 4b) Drop scalar surface coordinate if present
    if "surface" in daily.coords:
        daily = daily.reset_coords("surface", drop=True)

    # 5) Create a proper time dimension (instead of lead_day)
    #    time = forecast_reference_time + lead_day (1..ndays)
    if init_time is not None:
        base = np.datetime64(init_time)
        times = base + np.arange(1, ndays + 1).astype("timedelta64[D]")
    else:
        # Fallback: just use 1..ndays as a dummy time axis
        times = np.arange(1, ndays + 1).astype("int32")

    daily = daily.assign_coords(time=("lead_day", times))
    daily = daily.swap_dims({"lead_day": "time"})
    # Optional: keep lead_day as an auxiliary coordinate or drop it.
    # If you want to drop it completely, uncomment:
    daily = daily.drop_vars("lead_day")

    # 6) Build dataset with dims (time, lat, lon)
    ds_out = daily.to_dataset(name="tp")

    # Some useful global attributes
    if init_time is not None:
        ds_out.attrs["forecast_reference_time"] = str(init_time)
    ds_out.attrs.setdefault(
        "title", "ECMWF IFS HRES (0.25°) daily total precipitation (mm/day)"
    )
    ds_out.attrs.setdefault("source", "ECMWF Open Data (IFS, param=tp)")
    ds_out.attrs.setdefault(
        "history",
        "Daily 24h totals computed from accumulated tp, "
        "converted from m to mm/day using download_ecmwf_hres_tp.py",
    )

    # 7) Safe compression: no manual chunksizes (avoid size mismatch errors)
    encoding = None
    if compress:
        encoding = {
            "tp": {
                "zlib": True,
                "complevel": 4,
                "dtype": "float32",
            }
        }

    out_nc.parent.mkdir(parents=True, exist_ok=True)
    ds_out.to_netcdf(out_nc, encoding=encoding)
    print(f"[info] Written NetCDF: {out_nc}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Download ECMWF HRES (IFS 0.25°) total precipitation, "
                    "compute daily 24h totals (mm/day) and clip to ROI."
    )
    p.add_argument(
        "--outdir",
        type=str,
        default="ecmwf_hres_tp",
        help="Output directory for GRIB & NetCDF (default: %(default)s)",
    )
    p.add_argument(
        "--outfile",
        type=str,
        default="ecmwf_hres_tp_daily.nc",
        help="Output NetCDF file name (default: %(default)s)",
    )
    p.add_argument(
        "--ndays",
        type=int,
        default=10,
        help="Number of forecast lead days (1–10, default: %(default)s)",
    )
    p.add_argument(
        "--date",
        type=str,
        default=None,
        help=(
            "Forecast start date (e.g. '2025-11-30'). "
            "If omitted, latest available is used."
        ),
    )
    p.add_argument(
        "--time",
        type=int,
        default=None,
        help="Forecast start time (0, 6, 12, 18). If omitted, latest is used.",
    )
    p.add_argument(
        "--lat-min", type=float, required=True, help="Minimum latitude"
    )
    p.add_argument(
        "--lat-max", type=float, required=True, help="Maximum latitude"
    )
    p.add_argument(
        "--lon-min", type=float, required=True, help="Minimum longitude"
    )
    p.add_argument(
        "--lon-max", type=float, required=True, help="Maximum longitude"
    )

    return p.parse_args()


def main():
    args = parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    grib_path = outdir / "ecmwf_hres_tp.grib2"
    out_nc = outdir / args.outfile

    print("[info] Downloading ECMWF HRES tp from Open Data...")
    result = download_hres_tp_grib(
        target_path=grib_path,
        ndays=args.ndays,
        date=args.date,
        time=args.time,
    )
    print(f"[info] Forecast init time (UTC): {result.datetime}")

    print("[info] Processing GRIB -> daily totals -> clip -> NetCDF...")
    process_to_netcdf(
        grib_path=grib_path,
        out_nc=out_nc,
        ndays=args.ndays,
        lat_min=args.lat_min,
        lat_max=args.lat_max,
        lon_min=args.lon_min,
        lon_max=args.lon_max,
        init_time=result.datetime,
    )


if __name__ == "__main__":
    main()
```

---

## 🔧 Command-Line Arguments

### Required Arguments

| Argument | Type | Description | Example |
|----------|------|-------------|---------|
| `--lat-min` | Float | Minimum latitude (south) | `3` |
| `--lat-max` | Float | Maximum latitude (north) | `15` |
| `--lon-min` | Float | Minimum longitude (west) | `33` |
| `--lon-max` | Float | Maximum longitude (east) | `48` |

### Optional Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `--outdir` | String | Output directory path | `ecmwf_hres_tp` |
| `--outfile` | String | Output NetCDF filename | `ecmwf_hres_tp_daily.nc` |
| `--ndays` | Integer | Forecast days (1–10) | `10` |
| `--date` | Date (YYYY-MM-DD) | Forecast initialization date | Latest available |
| `--time` | Integer | Model cycle (0 or 12) | Latest available |

---

## 🌍 ECMWF HRES vs GFS Comparison

| Feature | ECMWF HRES | NCEP GFS |
|---------|------------|----------|
| **Resolution** | 0.25° (~28 km) | 0.25° (~28 km) |
| **Forecast Range** | 10 days (Open Data) | 16 days |
| **Update Cycles** | 00Z, 12Z | 00Z, 06Z, 12Z, 18Z |
| **Skill** | Generally higher | Good, slightly lower |
| **Access** | ecmwf-opendata API | NOMADS GRIB Filter |
| **Authentication** | Not required | Not required |
| **Data Format** | GRIB2 | GRIB2 |

!!! tip "Why Choose ECMWF HRES?"
    - **Higher forecast skill** - consistently ranked #1 in verification
    - **Better tropical precipitation** - important for Africa
    - **Smoother spatial patterns** - advanced physics
    - **Free Open Data access** - no registration required

---

## ⏰ Understanding ECMWF Cycles

ECMWF HRES runs **2 times daily** (Open Data availability):

| Cycle | Init Time (UTC) | Typical Availability | Forecast Range |
|-------|-----------------|---------------------|----------------|
| **00Z** | 00:00 UTC | ~06:00-08:00 UTC | 10 days |
| **12Z** | 12:00 UTC | ~18:00-20:00 UTC | 10 days |

!!! info "Open Data Time Steps"
    ECMWF HRES provides data at these intervals:
    
    - **0–144 hours:** Every 3 hours
    - **144–240 hours:** Every 6 hours
    
    Maximum lead time: **240 hours (10 days)**

---

## 📍 Regional Bounding Boxes

Use these coordinates with the `--lat-min`, `--lat-max`, `--lon-min`, `--lon-max` arguments:

=== "Ethiopia"
    ```bash
    --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48
    ```
    **Coverage:** Entire Ethiopia

=== "East Africa"
    ```bash
    --lat-min -5 --lat-max 12 --lon-min 28 --lon-max 42
    ```
    **Coverage:** Kenya, Uganda, Tanzania, Rwanda, Burundi

=== "Horn of Africa"
    ```bash
    --lat-min -5 --lat-max 18 --lon-min 32 --lon-max 52
    ```
    **Coverage:** Ethiopia, Somalia, Eritrea, Djibouti, Kenya

=== "West Africa"
    ```bash
    --lat-min 4 --lat-max 18 --lon-min -18 --lon-max 16
    ```
    **Coverage:** Sahel region

=== "Southern Africa"
    ```bash
    --lat-min -35 --lat-max -8 --lon-min 10 --lon-max 36
    ```
    **Coverage:** South Africa, Zimbabwe, Mozambique, Zambia

---

## 💡 Usage Examples

### Example 1: 10-Day Forecast for Ethiopia

```bash
python download_ecmwf_hres_precip.py \
    --outdir data/ecmwf_hres_eth \
    --outfile ecmwf_hres_ethiopia_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --time 0
```

**What it does:**

- Downloads accumulated tp at steps 0, 24, 48, ..., 240 hours
- Computes 10 daily precipitation totals
- Converts from meters to mm/day
- Clips to Ethiopia boundaries
- Saves as compressed NetCDF

---

### Example 2: Latest Available Forecast

```bash
python download_ecmwf_hres_precip.py \
    --outdir data/ecmwf_hres_latest \
    --outfile ecmwf_hres_ethiopia_latest.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48
```

**What it does:**

- Automatically selects the most recent available forecast
- No need to specify `--date` or `--time`
- Ideal for operational forecasting

---

### Example 3: Specific Date Forecast

```bash
python download_ecmwf_hres_precip.py \
    --outdir data/ecmwf_hres_archive \
    --outfile ecmwf_hres_ethiopia_20250115.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --date 2025-01-15 \
    --time 0
```

**What it does:**

- Downloads the 00Z forecast from January 15, 2025
- Useful for case studies or verification

!!! warning "Data Retention"
    ECMWF Open Data keeps forecasts for approximately **2-3 days**. For older data, use the [ECMWF Climate Data Store (CDS)](https://cds.climate.copernicus.eu/).

---

### Example 4: Short-Range Forecast (5 Days)

```bash
python download_ecmwf_hres_precip.py \
    --outdir data/ecmwf_hres_short \
    --outfile ecmwf_hres_ethiopia_5day.nc \
    --ndays 5 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --time 0
```

**What it does:**

- Downloads only 5 days of forecast
- Faster download and smaller file
- Higher skill than extended forecasts

---

### Example 5: Operational Daily Script

Create a script for daily automated downloads:

```bash
#!/bin/bash
# daily_ecmwf_download.sh

TODAY=$(date -u +%Y-%m-%d)
OUTDIR="data/ecmwf_operational"
OUTFILE="ecmwf_hres_eth_${TODAY}.nc"

python download_ecmwf_hres_precip.py \
    --outdir "$OUTDIR" \
    --outfile "$OUTFILE" \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48

echo "Downloaded ECMWF HRES forecast for $TODAY"
```

---

## 📂 Output Directory Structure

After running the script, your output directory will contain:

```
data/ecmwf_hres/
├── ecmwf_hres_tp.grib2              # Raw GRIB2 file (can be deleted)
└── ecmwf_hres_ethiopia_10day.nc     # Final NetCDF output
```

!!! tip "Cleaning Up GRIB Files"
    The intermediate GRIB2 file can be deleted after the NetCDF is created:
    ```bash
    rm data/ecmwf_hres/*.grib2
    ```

---

## 🔍 Verifying Your Download

After downloading, verify your data using Python:

```python
import xarray as xr
import matplotlib.pyplot as plt

# Open the forecast file
ds = xr.open_dataset('data/ecmwf_hres/ecmwf_hres_ethiopia_10day.nc')

# Display dataset information
print(ds)

# Check dimensions
print(f"Forecast days: {len(ds.time)}")
print(f"Latitude range: {float(ds.lat.min()):.2f} to {float(ds.lat.max()):.2f}")
print(f"Longitude range: {float(ds.lon.min()):.2f} to {float(ds.lon.max()):.2f}")

# Check precipitation range (sanity check)
print(f"Precipitation range: {float(ds.tp.min()):.1f} to {float(ds.tp.max()):.1f} mm/day")

# Check forecast reference time
print(f"Forecast init: {ds.attrs.get('forecast_reference_time', 'N/A')}")

# Plot Day 1 precipitation forecast
fig, ax = plt.subplots(figsize=(10, 8))
ds.tp.isel(time=0).plot(ax=ax, cmap='Blues', vmin=0, vmax=50)
ax.set_title(f"ECMWF HRES Day 1 Precipitation Forecast\n{ds.time.values[0]}")
plt.savefig('ecmwf_precip_day1.png', dpi=150, bbox_inches='tight')
plt.show()

# Plot time series for a point (e.g., Addis Ababa)
lat_point, lon_point = 9.0, 38.7
point_data = ds.tp.sel(lat=lat_point, lon=lon_point, method='nearest')
point_data.plot(marker='o', figsize=(10, 4), color='steelblue')
plt.title(f'10-Day Precipitation Forecast for Addis Ababa ({lat_point}°N, {lon_point}°E)')
plt.ylabel('Precipitation (mm/day)')
plt.xlabel('Date')
plt.grid(True, alpha=0.3)
plt.savefig('ecmwf_precip_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()

# Plot all days as panels
fig, axes = plt.subplots(2, 5, figsize=(20, 8))
for i, ax in enumerate(axes.flat):
    if i < len(ds.time):
        ds.tp.isel(time=i).plot(ax=ax, cmap='Blues', vmin=0, vmax=50, add_colorbar=False)
        ax.set_title(f"Day {i+1}")
    ax.set_xlabel('')
    ax.set_ylabel('')
plt.tight_layout()
plt.savefig('ecmwf_precip_all_days.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## 📊 Understanding ECMWF Precipitation Data

### Accumulated vs. Daily Totals

ECMWF provides **accumulated** precipitation from forecast start:

```
Step 0h:   tp = 0 mm (start of forecast)
Step 24h:  tp = total precipitation from 0h to 24h
Step 48h:  tp = total precipitation from 0h to 48h
...
```

### Daily Total Calculation

The script computes daily totals by differencing:

```
Day 1 = tp(24h) - tp(0h)   = precipitation during hours 0-24
Day 2 = tp(48h) - tp(24h)  = precipitation during hours 24-48
Day 3 = tp(72h) - tp(48h)  = precipitation during hours 48-72
...
```

### Unit Conversion

| ECMWF Native | Script Output | Conversion |
|--------------|---------------|------------|
| meters (m) | mm/day | × 1000 |

!!! info "Water Equivalent"
    ECMWF precipitation is in meters of water equivalent. Multiplying by 1000 gives millimeters.

---

## 📊 Output Variable Details

### Main Variable

| Variable | Description | Units |
|----------|-------------|-------|
| `tp` | Daily total precipitation | mm/day |

### Coordinates

| Coordinate | Description |
|------------|-------------|
| `time` | Valid date (end of 24h period) |
| `lat` | Latitude (degrees north) |
| `lon` | Longitude (degrees east) |

### Attributes

```python
# Dataset attributes (example)
{
    'title': 'ECMWF IFS HRES (0.25°) daily total precipitation (mm/day)',
    'source': 'ECMWF Open Data (IFS, param=tp)',
    'forecast_reference_time': '2025-01-15T00:00:00',
    'history': 'Daily 24h totals computed from accumulated tp'
}
```

---

## ⚠️ Troubleshooting

### Common Issues and Solutions

=== "ecmwf-opendata Not Found"

    **Problem:** Package not installed
    
    ```
    ModuleNotFoundError: No module named 'ecmwf.opendata'
    ```
    
    **Solution:**
    ```bash
    pip install ecmwf-opendata
    # or
    conda install -c conda-forge ecmwf-opendata
    ```

=== "cfgrib Import Error"

    **Problem:** ecCodes library not installed
    
    ```
    ImportError: Cannot find the ecCodes library
    ```
    
    **Solutions:**
    
    ```bash
    # Ubuntu/Debian
    sudo apt-get install libeccodes-dev
    
    # macOS
    brew install eccodes
    
    # Conda (recommended)
    conda install -c conda-forge cfgrib eccodes
    ```

=== "Data Not Available"

    **Problem:** Requested date not available
    
    ```
    Exception: No data available for the requested date
    ```
    
    **Solutions:**
    
    1. **Check data retention:** Open Data keeps ~2-3 days
    2. **Use latest:** Omit `--date` and `--time` arguments
    3. **Wait for availability:** ~6-8 hours after cycle time
    4. **Check ECMWF status:** [ECMWF Open Data](https://www.ecmwf.int/en/forecasts/datasets/open-data)

=== "Connection Timeout"

    **Problem:** Network issues or server busy
    
    ```
    requests.exceptions.Timeout: Connection timed out
    ```
    
    **Solutions:**
    
    1. **Retry:** Run the script again
    2. **Check internet connection**
    3. **Try off-peak hours:** Early morning UTC
    4. **Use smaller region:** Reduce bounding box

=== "Missing Steps"

    **Problem:** Expected time steps not found
    
    ```
    RuntimeError: Expected steps [0, 24] not found in tp
    ```
    
    **Solutions:**
    
    1. **Check ndays:** Must be 1–10 for HRES
    2. **Verify GRIB file:** Check if download completed
    3. **Re-download:** Delete GRIB and try again

---

## 🌐 ECMWF Open Data API

### How It Works

The `ecmwf-opendata` package provides a simple Python interface:

```python
from ecmwf.opendata import Client

client = Client(
    source="ecmwf",   # ECMWF servers
    model="ifs",      # IFS model (HRES)
    resol="0p25",     # 0.25° resolution
)

result = client.retrieve(
    type="fc",        # Forecast
    param="tp",       # Total precipitation
    step=[0, 24, 48], # Lead times in hours
    target="output.grib2"
)
```

### Available Parameters

| Parameter | Description | Common Values |
|-----------|-------------|---------------|
| `type` | Data type | `fc` (forecast) |
| `param` | Variable | `tp`, `2t`, `10u`, `10v`, `msl` |
| `step` | Lead time (hours) | 0, 3, 6, ..., 240 |
| `date` | Init date | `2025-01-15`, `0` (today) |
| `time` | Init time | `0`, `12` |

---

## 🎓 Data Quality Notes

!!! success "Strengths"
    - **Highest forecast skill** globally - consistently #1 in verification
    - **Excellent tropical performance** - important for Africa
    - **Smooth spatial patterns** - advanced physics and data assimilation
    - **Free Open Data access** - no registration required
    - **Regular updates** - twice daily (00Z, 12Z)

!!! warning "Limitations"
    - **10-day maximum** for Open Data (vs. 15 days for licensed)
    - **Limited data retention** (~2-3 days on Open Data)
    - **No ensemble** in Open Data (deterministic only)
    - **Forecast skill degrades** after day 5-7
    - **May underestimate extremes** - common for NWP models

!!! tip "Best Practices"
    - **Use for short-range** (1-5 days) for highest skill
    - **Compare with GFS** for consistency checks
    - **Validate locally** with rain gauge data
    - **Consider bias correction** for your region
    - **Archive forecasts** for verification studies
    - **Combine with observations** (CHIRPS, TAMSAT) for hybrid products

---

## 🔗 Combining with Temperature Data

For complete weather forecasts, you may also want temperature. Here's a template for a combined download:

```python
# After downloading precipitation...

# Download temperature (if available in Open Data)
# Note: 2m temperature may require different parameters

# Combine datasets
import xarray as xr

ds_precip = xr.open_dataset('ecmwf_hres_precip.nc')
ds_temp = xr.open_dataset('ecmwf_hres_temp.nc')  # If available

ds_combined = xr.merge([ds_precip, ds_temp])
ds_combined.to_netcdf('ecmwf_hres_combined.nc')
```

!!! info "Temperature Data"
    For ECMWF temperature forecasts, you may need to modify the script to request `param="2t"` (2-meter temperature) instead of `tp`.

---

## 📖 Additional Resources

### Official Documentation

- **ECMWF Open Data:** [https://www.ecmwf.int/en/forecasts/datasets/open-data](https://www.ecmwf.int/en/forecasts/datasets/open-data)
- **ecmwf-opendata Package:** [https://github.com/ecmwf/ecmwf-opendata](https://github.com/ecmwf/ecmwf-opendata)
- **IFS Documentation:** [https://www.ecmwf.int/en/publications/ifs-documentation](https://www.ecmwf.int/en/publications/ifs-documentation)

### Python Libraries

- **ecmwf-opendata:** [https://pypi.org/project/ecmwf-opendata/](https://pypi.org/project/ecmwf-opendata/)
- **xarray:** [https://xarray.pydata.org/](https://xarray.pydata.org/)
- **cfgrib:** [https://github.com/ecmwf/cfgrib](https://github.com/ecmwf/cfgrib)

### Alternative Data Sources

| Source | Type | Resolution | Range | Access |
|--------|------|------------|-------|--------|
| **GFS** | Forecast | 0.25° | 16 days | NOMADS |
| **ECMWF ENS** | Ensemble | 0.5° | 15 days | CDS |
| **ICON** | Forecast | 13 km | 7 days | DWD OpenData |
| **ERA5** | Reanalysis | 0.25° | Historical | CDS |

---

## 🚀 Next Steps

<div class="grid cards" markdown>

-   :material-chart-line: **Analyze Forecasts**
    
    ---
    
    Compare with observations  
    Calculate skill scores  
    
    → [Xarray Tutorial](../../day3/06-Xarray_for_Climate_and_Meteorology_Workshop.md)

-   :material-map: **Visualize Forecasts**
    
    ---
    
    Create forecast maps  
    Plot time series  
    
    → [Matplotlib Tutorial](../../day3/05-Matplotlib_for_Climate_and_Meteorology_Workshop.md)

-   :material-weather-cloudy: **Compare with GFS**
    
    ---
    
    Multi-model comparison  
    Ensemble-like analysis  
    
    → [GFS Precipitation](13-download_gfs_precip_forecast.md)

-   :material-bug: **VECTRI Integration**
    
    ---
    
    Prepare inputs for malaria modeling  
    Forecast-based early warning  
    
    → [VECTRI Model](../../day1/vectri_model_components_larvae_to_hydrology.md)

</div>

---

!!! example "Need Help?"
    If you encounter issues or have questions:
    
    - Check the [Troubleshooting](#troubleshooting) section
    - Review [ECMWF Open Data documentation](https://www.ecmwf.int/en/forecasts/datasets/open-data)
    - Visit [ECMWF Support Portal](https://confluence.ecmwf.int/)
    - Contact workshop instructors

---

<div style="background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%); color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
  <h3 style="margin: 0 0 1rem 0;">🌧️ Ready for ECMWF Forecasting!</h3>
  <p style="margin: 0; opacity: 0.95;">You now have everything you need to download and process ECMWF HRES precipitation forecasts — the world's leading weather model — for your climate and malaria modeling applications.</p>
</div>
