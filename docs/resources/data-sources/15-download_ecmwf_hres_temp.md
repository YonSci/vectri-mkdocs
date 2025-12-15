# 🌡️ Downloading ECMWF HRES Temperature Forecasts

## Overview

**ECMWF HRES (High Resolution Forecast)** is the world's leading deterministic weather forecast model. This tutorial guides you through downloading, processing, and converting ECMWF IFS 0.25° 2-meter temperature data into daily mean values using the ECMWF Open Data API.

<div class="grid cards" markdown>

-   :material-thermometer: **Dataset**
    
    ---
    
    ECMWF IFS HRES 0.25° Temperature
    
    **Variable:** 2m Temperature (2t)  
    **Resolution:** 0.25° (~28 km)  
    **Output:** Daily mean (°C)  
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
    C --> D[Extract 2t Variable]
    D --> E[Compute Daily Means]
    E --> F[Convert K → °C]
    F --> G[Clip to Region]
    G --> H[Save NetCDF]
    
    style A fill:#fff3e0
    style H fill:#c8e6c9
```

The script performs the following operations:

1. **Downloads** instantaneous 2m temperature from ECMWF Open Data
2. **Extracts** temperature (2t) at 3-hourly intervals
3. **Computes** daily means by averaging 3-hourly values
4. **Converts** from Kelvin to Celsius (optional)
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

=== "10-Day Forecast (°C)"
    ```bash
    python download_ecmwf_hres_temp.py \
        --outdir data/ecmwf_hres_temp \
        --outfile ecmwf_hres_temp_ethiopia_10day.nc \
        --ndays 10 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --time 0
    ```

=== "Latest Available"
    ```bash
    python download_ecmwf_hres_temp.py \
        --outdir data/ecmwf_hres_temp \
        --outfile ecmwf_hres_temp_ethiopia.nc \
        --ndays 10 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48
    ```

=== "Keep Kelvin Units"
    ```bash
    python download_ecmwf_hres_temp.py \
        --outdir data/ecmwf_hres_temp \
        --outfile ecmwf_hres_temp_ethiopia_K.nc \
        --ndays 10 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --keep-kelvin
    ```

---

## 📋 The Complete Script

### Python Download Script

Save this as `download_ecmwf_hres_temp.py`:

```python
#!/usr/bin/env python
"""
Download ECMWF HRES (IFS 0.25°) 2-meter temperature (2t) from ECMWF Open Data,
compute daily mean temperature, clip to a region of interest,
and save as a single merged NetCDF file.

- Uses ECMWF Free & Open Data (IFS HRES, 0.25° resolution, GRIB2).
- Downloads instantaneous 2m temperature (2t) at selected lead times.
- Computes daily mean 2m temperature for lead days 1..N (N <= 10).
- Clips to lat/lon bounding box.
- Writes a single NetCDF with dims (time, lat, lon) and units degC.

Example
-------
python download_ecmwf_hres_2t.py \
    --outdir data/ecmwf_hres_2t \
    --outfile ecmwf_hres_2t_ea_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --time 0

Notes
-----
- 2m temperature (2t) is an instantaneous field (units K in GRIB).
- Daily mean is computed by averaging all available steps within each 24h window:
    Day 1: mean of steps in [0, 24]
    Day 2: mean of steps in (24, 48]
    ...
  This avoids double-counting boundary hours across days.
- HRES open-data step schedule for 00/12 UTC:
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
    return sorted(set(steps))


def temp_steps(max_lead_days: int):
    """
    Return the list of step hours needed to compute daily means
    up to max_lead_days (1–10 for HRES).

    For temperature daily means, we keep all available steps
    up to 24*max_lead_days.
    """
    max_lead_days = int(max_lead_days)
    if max_lead_days < 1 or max_lead_days > 10:
        raise ValueError("max_lead_days must be between 1 and 10 for HRES.")

    max_step_hours = max_lead_days * 24
    steps_all = hres_all_steps()
    needed = [s for s in steps_all if 0 <= s <= max_step_hours]

    # Ensure we have step=0
    if 0 not in needed:
        needed = [0] + needed

    return sorted(set(needed))


# ---------------------------------------------------------------------------
# Download ECMWF HRES 2t from Open Data
# ---------------------------------------------------------------------------

def download_hres_2t_grib(
    target_path: Path,
    ndays: int = 10,
    date: "str | int | None" = None,
    time: "int | None" = None,
):
    """
    Download ECMWF HRES (IFS 0.25°) 2m temperature (2t) GRIB2 file
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
    steps = temp_steps(ndays)

    client = Client(
        source="ecmwf",
        model="ifs",
        resol="0p25",
    )

    request_kwargs = {
        "type": "fc",
        "param": "2t",
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
# Processing GRIB -> daily means -> clip -> NetCDF
# ---------------------------------------------------------------------------

def open_2t_from_grib(grib_path: Path) -> xr.DataArray:
    """
    Open GRIB2 file and return 2t DataArray with step_hours coordinate.

    Returns
    -------
    t2m : xr.DataArray
        Dimensions: (step_hours, latitude, longitude)
    """
    ds = xr.open_dataset(
        grib_path,
        engine="cfgrib",
        backend_kwargs={
            "indexpath": "",
            "filter_by_keys": {"shortName": "2t"},
        },
    )

    t2m = ds["t2m"] if "t2m" in ds.data_vars else ds["2t"]

    # Drop singleton time dimension (forecast run time)
    if "time" in t2m.dims and t2m.sizes["time"] == 1:
        t2m = t2m.isel(time=0, drop=True)

    # Convert 'step' (timedelta64) to integer hours
    step = t2m["step"]
    step_hours = (step / np.timedelta64(1, "h")).astype("int32").values

    t2m = t2m.assign_coords(step_hours=("step", step_hours))
    t2m = t2m.swap_dims({"step": "step_hours"}).drop_vars("step")

    t2m.name = "t2m"
    return t2m


def compute_daily_means(t2m: xr.DataArray, ndays: int) -> xr.DataArray:
    """
    Compute daily mean 2m temperature from instantaneous steps.

    Day 1: mean of steps in [0, 24]
    Day 2: mean of steps in (24, 48]
    ...
    """
    max_step_hours = ndays * 24
    step_hours = t2m["step_hours"].values

    if step_hours.max() < max_step_hours:
        raise RuntimeError(
            f"Need steps up to at least {max_step_hours}h, "
            f"got max {int(step_hours.max())}h"
        )

    daily_list = []
    lead_days = []

    for day in range(1, ndays + 1):
        h1 = day * 24
        h0 = (day - 1) * 24

        if day == 1:
            mask = (t2m.step_hours >= 0) & (t2m.step_hours <= h1)
        else:
            mask = (t2m.step_hours > h0) & (t2m.step_hours <= h1)

        sub = t2m.where(mask, drop=True)
        if sub.step_hours.size == 0:
            raise RuntimeError(f"No temperature steps found for day {day}")

        daily_mean = sub.mean(dim="step_hours", skipna=True)
        daily_list.append(daily_mean)
        lead_days.append(day)

    daily = xr.concat(daily_list, dim="lead_day")
    daily = daily.assign_coords(lead_day=("lead_day", lead_days))

    daily.name = "t2m"
    daily.attrs["units"] = t2m.attrs.get("units", "K")
    daily.attrs["long_name"] = "Daily mean 2m temperature"

    return daily


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
    to_celsius: bool = True,
):
    """
    End-to-end processing:
    - Open GRIB
    - Compute daily means 1..ndays
    - Convert from K to degC (optional)
    - Rename dims to time, lat, lon
    - Clip to ROI (optional)
    - Save to NetCDF
    """
    # 1) Open and compute daily means (still in Kelvin)
    t2m = open_2t_from_grib(grib_path)
    daily = compute_daily_means(t2m, ndays)

    # 2) Clip to bounding box (still latitude/longitude dims)
    if None not in (lat_min, lat_max, lon_min, lon_max):
        daily = clip_to_bbox(daily, lat_min, lat_max, lon_min, lon_max)

    # 3) Convert units
    if to_celsius:
        daily = daily - 273.15
        daily.attrs["units"] = "degC"
        daily.attrs["long_name"] = "Daily mean 2m temperature [degC]"
    else:
        daily.attrs["units"] = "K"
        daily.attrs["long_name"] = "Daily mean 2m temperature [K]"

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
    if init_time is not None:
        base = np.datetime64(init_time)
        times = base + np.arange(1, ndays + 1).astype("timedelta64[D]")
    else:
        times = np.arange(1, ndays + 1).astype("int32")

    daily = daily.assign_coords(time=("lead_day", times))
    daily = daily.swap_dims({"lead_day": "time"})
    daily = daily.drop_vars("lead_day")

    # 6) Build dataset with dims (time, lat, lon)
    ds_out = daily.to_dataset(name="t2m")

    # Global attributes
    if init_time is not None:
        ds_out.attrs["forecast_reference_time"] = str(init_time)
    ds_out.attrs.setdefault(
        "title", "ECMWF IFS HRES (0.25°) daily mean 2m temperature"
    )
    ds_out.attrs.setdefault("source", "ECMWF Open Data (IFS, param=2t)")
    ds_out.attrs.setdefault(
        "history",
        "Daily means computed from instantaneous 2m temperature steps, "
        "optionally converted from K to degC using download_ecmwf_hres_2t.py",
    )

    # 7) Safe compression
    encoding = None
    if compress:
        encoding = {
            "t2m": {
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
        description="Download ECMWF HRES (IFS 0.25°) 2m temperature (2t), "
                    "compute daily means and clip to ROI."
    )
    p.add_argument(
        "--outdir",
        type=str,
        default="ecmwf_hres_2t",
        help="Output directory for GRIB & NetCDF (default: %(default)s)",
    )
    p.add_argument(
        "--outfile",
        type=str,
        default="ecmwf_hres_2t_daily.nc",
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
    p.add_argument(
        "--keep-kelvin",
        action="store_true",
        help="Do NOT convert to Celsius; keep output in Kelvin.",
    )

    return p.parse_args()


def main():
    args = parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    grib_path = outdir / "ecmwf_hres_2t.grib2"
    out_nc = outdir / args.outfile

    print("[info] Downloading ECMWF HRES 2t from Open Data...")
    result = download_hres_2t_grib(
        target_path=grib_path,
        ndays=args.ndays,
        date=args.date,
        time=args.time,
    )
    print(f"[info] Forecast init time (UTC): {result.datetime}")

    print("[info] Processing GRIB -> daily means -> clip -> NetCDF...")
    process_to_netcdf(
        grib_path=grib_path,
        out_nc=out_nc,
        ndays=args.ndays,
        lat_min=args.lat_min,
        lat_max=args.lat_max,
        lon_min=args.lon_min,
        lon_max=args.lon_max,
        init_time=result.datetime,
        to_celsius=not args.keep_kelvin,
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
| `--outdir` | String | Output directory path | `ecmwf_hres_2t` |
| `--outfile` | String | Output NetCDF filename | `ecmwf_hres_2t_daily.nc` |
| `--ndays` | Integer | Forecast days (1–10) | `10` |
| `--date` | Date (YYYY-MM-DD) | Forecast initialization date | Latest available |
| `--time` | Integer | Model cycle (0 or 12) | Latest available |
| `--keep-kelvin` | Flag | Keep temperature in Kelvin | False (outputs °C) |

---

## 🌡️ Understanding Temperature Data

### Instantaneous vs. Accumulated Fields

Unlike precipitation (which is accumulated), **temperature is an instantaneous field**:

| Field Type | Variable | How It Works |
|------------|----------|--------------|
| **Instantaneous** | 2t (Temperature) | Value at exact forecast time |
| **Accumulated** | tp (Precipitation) | Sum over previous interval |

### Daily Mean Calculation

The script averages 3-hourly instantaneous values to compute daily means:

```
Day 1 Mean = mean(T2m at steps 0, 3, 6, ..., 24)
Day 2 Mean = mean(T2m at steps 27, 30, 33, ..., 48)
...
```

!!! info "Boundary Handling"
    - **Day 1** includes step 0 (initialization time) through step 24
    - **Days 2+** use steps (start, end] to avoid double-counting boundary hours

### Unit Conversion

| ECMWF Native | Script Output (Default) | Conversion |
|--------------|------------------------|------------|
| Kelvin (K) | Celsius (°C) | T(°C) = T(K) - 273.15 |

Use `--keep-kelvin` to output in Kelvin instead.

---

## ⏰ Understanding ECMWF Cycles

ECMWF HRES runs **2 times daily** (Open Data availability):

| Cycle | Init Time (UTC) | Typical Availability | Forecast Range |
|-------|-----------------|---------------------|----------------|
| **00Z** | 00:00 UTC | ~06:00-08:00 UTC | 10 days |
| **12Z** | 12:00 UTC | ~18:00-20:00 UTC | 10 days |

!!! info "Open Data Time Steps"
    ECMWF HRES provides data at these intervals:
    
    - **0–144 hours:** Every 3 hours (49 steps)
    - **144–240 hours:** Every 6 hours (17 steps)
    
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

### Example 1: 10-Day Temperature Forecast for Ethiopia

```bash
python download_ecmwf_hres_temp.py \
    --outdir data/ecmwf_hres_temp_eth \
    --outfile ecmwf_hres_temp_ethiopia_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --time 0
```

**What it does:**

- Downloads all 3-hourly temperature steps (0, 3, 6, ..., 240)
- Computes 10 daily mean temperatures
- Converts from Kelvin to Celsius
- Clips to Ethiopia boundaries
- Saves as compressed NetCDF

---

### Example 2: Latest Available Forecast

```bash
python download_ecmwf_hres_temp.py \
    --outdir data/ecmwf_hres_temp_latest \
    --outfile ecmwf_hres_temp_ethiopia_latest.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48
```

**What it does:**

- Automatically selects the most recent available forecast
- No need to specify `--date` or `--time`
- Ideal for operational forecasting

---

### Example 3: Keep Temperature in Kelvin

```bash
python download_ecmwf_hres_temp.py \
    --outdir data/ecmwf_hres_temp_K \
    --outfile ecmwf_hres_temp_ethiopia_kelvin.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --keep-kelvin
```

**What it does:**

- Outputs temperature in Kelvin (K)
- Useful for direct model input (e.g., VECTRI)
- No unit conversion applied

---

### Example 4: Short-Range Forecast (5 Days)

```bash
python download_ecmwf_hres_temp.py \
    --outdir data/ecmwf_hres_temp_short \
    --outfile ecmwf_hres_temp_ethiopia_5day.nc \
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

### Example 5: Combined Precipitation and Temperature Download

Create a script to download both variables:

```bash
#!/bin/bash
# download_ecmwf_both.sh

TODAY=$(date -u +%Y-%m-%d)
OUTDIR="data/ecmwf_operational"

# Download precipitation forecast
python download_ecmwf_hres_precip.py \
    --outdir "$OUTDIR" \
    --outfile "ecmwf_hres_precip_eth_${TODAY}.nc" \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48

# Download temperature forecast
python download_ecmwf_hres_temp.py \
    --outdir "$OUTDIR" \
    --outfile "ecmwf_hres_temp_eth_${TODAY}.nc" \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48

echo "Downloaded ECMWF HRES forecasts for $TODAY"
```

---

## 📂 Output Directory Structure

After running the script, your output directory will contain:

```
data/ecmwf_hres_temp/
├── ecmwf_hres_2t.grib2                    # Raw GRIB2 file (can be deleted)
└── ecmwf_hres_temp_ethiopia_10day.nc      # Final NetCDF output
```

!!! tip "Cleaning Up GRIB Files"
    The intermediate GRIB2 file can be deleted after the NetCDF is created:
    ```bash
    rm data/ecmwf_hres_temp/*.grib2
    ```

---

## 🔍 Verifying Your Download

After downloading, verify your data using Python:

```python
import xarray as xr
import matplotlib.pyplot as plt

# Open the forecast file
ds = xr.open_dataset('data/ecmwf_hres_temp/ecmwf_hres_temp_ethiopia_10day.nc')

# Display dataset information
print(ds)

# Check dimensions and units
print(f"Forecast days: {len(ds.time)}")
print(f"Temperature units: {ds.t2m.attrs.get('units', 'N/A')}")
print(f"Latitude range: {float(ds.lat.min()):.2f} to {float(ds.lat.max()):.2f}")
print(f"Longitude range: {float(ds.lon.min()):.2f} to {float(ds.lon.max()):.2f}")

# Check temperature range (sanity check)
print(f"Temperature range: {float(ds.t2m.min()):.1f} to {float(ds.t2m.max()):.1f} °C")

# Check forecast reference time
print(f"Forecast init: {ds.attrs.get('forecast_reference_time', 'N/A')}")

# Plot Day 1 temperature forecast
fig, ax = plt.subplots(figsize=(10, 8))
ds.t2m.isel(time=0).plot(ax=ax, cmap='RdYlBu_r', vmin=10, vmax=35)
ax.set_title(f"ECMWF HRES Day 1 Temperature Forecast\n{ds.time.values[0]}")
plt.savefig('ecmwf_temp_day1.png', dpi=150, bbox_inches='tight')
plt.show()

# Plot time series for a point (e.g., Addis Ababa)
lat_point, lon_point = 9.0, 38.7
point_data = ds.t2m.sel(lat=lat_point, lon=lon_point, method='nearest')
point_data.plot(marker='o', figsize=(10, 4), color='orangered')
plt.title(f'10-Day Temperature Forecast for Addis Ababa ({lat_point}°N, {lon_point}°E)')
plt.ylabel('Temperature (°C)')
plt.xlabel('Date')
plt.grid(True, alpha=0.3)
plt.axhline(y=point_data.mean(), color='gray', linestyle='--', label='Mean')
plt.legend()
plt.savefig('ecmwf_temp_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()

# Plot all days as panels
fig, axes = plt.subplots(2, 5, figsize=(20, 8))
for i, ax in enumerate(axes.flat):
    if i < len(ds.time):
        ds.t2m.isel(time=i).plot(ax=ax, cmap='RdYlBu_r', vmin=10, vmax=35, add_colorbar=False)
        ax.set_title(f"Day {i+1}")
    ax.set_xlabel('')
    ax.set_ylabel('')
plt.tight_layout()
plt.savefig('ecmwf_temp_all_days.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## 📊 Output Variable Details

### Main Variable

| Variable | Description | Units (Default) | Units (--keep-kelvin) |
|----------|-------------|-----------------|----------------------|
| `t2m` | Daily mean 2m air temperature | °C (degC) | K (Kelvin) |

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
    'title': 'ECMWF IFS HRES (0.25°) daily mean 2m temperature',
    'source': 'ECMWF Open Data (IFS, param=2t)',
    'forecast_reference_time': '2025-01-15T00:00:00',
    'history': 'Daily means computed from instantaneous 2m temperature steps'
}

# Variable attributes
{
    'units': 'degC',
    'long_name': 'Daily mean 2m temperature [degC]'
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

=== "Unrealistic Temperature Values"

    **Problem:** Temperature values seem wrong (e.g., 280°C)
    
    **Cause:** Data still in Kelvin but expected Celsius
    
    **Solutions:**
    
    1. **Check units in output:**
        ```python
        print(ds.t2m.attrs.get('units'))
        ```
    2. **Re-run without `--keep-kelvin`**
    3. **Manual conversion:**
        ```python
        ds['t2m'] = ds['t2m'] - 273.15
        ```

=== "Missing Steps"

    **Problem:** Expected time steps not found
    
    ```
    RuntimeError: Need steps up to at least 240h, got max 144h
    ```
    
    **Solutions:**
    
    1. **Check ndays:** Must be 1–10 for HRES
    2. **Verify GRIB file:** Check if download completed
    3. **Re-download:** Delete GRIB and try again

---

## 🔗 Combining Temperature and Precipitation

For complete weather forecasts, combine both variables:

```python
import xarray as xr

# Load both datasets
ds_temp = xr.open_dataset('data/ecmwf_hres_temp_ethiopia_10day.nc')
ds_precip = xr.open_dataset('data/ecmwf_hres_precip_ethiopia_10day.nc')

# Merge into single dataset
ds_combined = xr.merge([ds_temp, ds_precip])

# Verify
print(ds_combined)
# Dimensions: (time: 10, lat: 49, lon: 61)
# Variables: t2m, tp

# Save combined file
ds_combined.to_netcdf('data/ecmwf_hres_combined_ethiopia_10day.nc')
```

---

## 🎓 Data Quality Notes

!!! success "Strengths"
    - **Highest forecast skill** globally - consistently #1 in verification
    - **Excellent tropical performance** - important for Africa
    - **Temperature forecasts** generally more skillful than precipitation
    - **Smooth spatial patterns** - advanced physics and data assimilation
    - **Free Open Data access** - no registration required

!!! warning "Limitations"
    - **10-day maximum** for Open Data (vs. 15 days for licensed)
    - **Limited data retention** (~2-3 days on Open Data)
    - **2m temperature** may not represent complex terrain well
    - **Forecast skill degrades** after day 5-7
    - **Diurnal cycle** - daily means may miss extremes

!!! tip "Best Practices"
    - **Use for short-range** (1-5 days) for highest skill
    - **Compare with GFS** for consistency checks
    - **Validate locally** with station data
    - **Consider elevation effects** in mountainous regions
    - **Archive forecasts** for verification studies
    - **Combine with precipitation** for complete weather picture

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

### Related Tutorials

- [ECMWF HRES Precipitation](15-download_ecmwf_hres_precip.md) - Download precipitation data
- [GFS Temperature Forecast](14-download_gfs_temp_forecast.md) - Alternative forecast source
- [ERA5 Reanalysis](#) - Historical temperature data

---

## 🚀 Next Steps

<div class="grid cards" markdown>

-   :material-chart-line: **Analyze Temperature Trends**
    
    ---
    
    Calculate anomalies and trends  
    Compare with climatology  
    
    → [Xarray Tutorial](../../day3/06-Xarray_for_Climate_and_Meteorology_Workshop.md)

-   :material-map: **Create Temperature Maps**
    
    ---
    
    Visualize spatial patterns  
    Plot time series  
    
    → [Matplotlib Tutorial](../../day3/05-Matplotlib_for_Climate_and_Meteorology_Workshop.md)

-   :material-weather-pouring: **Download Precipitation**
    
    ---
    
    Get matching precipitation forecasts  
    Combine for complete weather  
    
    → [ECMWF HRES Precipitation](15-download_ecmwf_hres_precip.md)

-   :material-bug: **VECTRI Integration**
    
    ---
    
    Prepare inputs for malaria modeling  
    Temperature-dependent transmission  
    
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

<div style="background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
  <h3 style="margin: 0 0 1rem 0;">🌡️ Ready for ECMWF Temperature Forecasting!</h3>
  <p style="margin: 0; opacity: 0.95;">You now have everything you need to download and process ECMWF HRES temperature forecasts — the world's leading weather model — for your climate and malaria modeling applications.</p>
</div>
