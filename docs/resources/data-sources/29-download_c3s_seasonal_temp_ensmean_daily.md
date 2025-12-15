# 🌡️ Downloading C3S Seasonal ECMWF Temperature Forecasts

---

## Overview

**C3S Seasonal (Copernicus Climate Change Service)** provides seasonal forecasts from multiple centers including ECMWF. This tutorial guides you through downloading daily 2-meter temperature from the C3S Seasonal database using the CDS API, computing ensemble means, and preparing data for VECTRI.

<div class="grid cards" markdown>

-   :material-thermometer: **Dataset**
    
    ---
    
    C3S Seasonal ECMWF Temperature
    
    **Variable:** 2m Temperature (t2m)  
    **Resolution:** ~1° (native) or custom  
    **Output:** Daily ensemble mean (K or °C)  
    **Forecast Range:** Up to 7 months

-   :material-earth: **Spatial Coverage**
    
    ---
    
    **Region:** Global  
    **Latitude:** 90°S to 90°N  
    **Longitude:** -180° to 180°  
    **Subsetting:** Supported

-   :material-update: **Update Frequency**
    
    ---
    
    **Cycles:** Monthly (1st of month)  
    **Latency:** ~3-5 days after init  
    **Ensemble:** 51 members (ECMWF System 5)

-   :material-file-download: **Access**
    
    ---
    
    **Source:** CDS (Copernicus)  
    **Method:** cdsapi Python  
    **Authentication:** Required (free)  
    **Format:** NetCDF

</div>

---

## 🎯 What This Script Does

```mermaid
graph LR
    A[Select Forecast Date] --> B[Build CDS Request]
    B --> C[Submit to CDS]
    C --> D[Download All Members]
    D --> E[Compute Ensemble Mean]
    E --> F[Standardize Time]
    F --> G[Save as NetCDF]
    
    style A fill:#fff3e0
    style G fill:#c8e6c9
```

The script performs the following operations:

1. **Builds** a CDS request for C3S seasonal temperature
2. **Submits** the request to Copernicus servers
3. **Downloads** all ensemble members
4. **Computes** ensemble mean over members
5. **Standardizes** time coordinates
6. **Saves** as NetCDF with `t2m(time, latitude, longitude)`

---

## 🚀 Quick Start Guide

### Prerequisites

!!! warning "CDS Account Required"
    You need a free CDS account to access C3S data:
    
    1. **Register:** [https://cds.climate.copernicus.eu/user/register](https://cds.climate.copernicus.eu/user/register)
    2. **Get API key:** [https://cds.climate.copernicus.eu/how-to-use-api](https://cds.climate.copernicus.eu/how-to-use-api)
    3. **Configure:** Create `~/.cdsapirc` with your credentials

!!! info "Required Python Packages"
    ```bash
    pip install cdsapi
    ```
    
    ```bash
    pip install xarray
    ```
    
    ```bash
    pip install numpy
    ```

### API Configuration

Create a file `~/.cdsapirc` (Linux/Mac) or `%USERPROFILE%\.cdsapirc` (Windows):

```text
url: https://cds.climate.copernicus.eu/api/v2
key: YOUR-UID:YOUR-API-KEY
```

Get your credentials from: [https://cds.climate.copernicus.eu/#!/home](https://cds.climate.copernicus.eu/#!/home)

### Basic Usage

=== "30-Day Forecast"
    ```bash
    python download_c3s_seasonal_temp_ensmean_daily.py \
        --outdir data/c3s_seasonal \
        --outfile c3s_seasonal_ecmwf_t2m_ensmean_2025-11_ea.nc \
        --originating-centre ecmwf \
        --system 51 \
        --year 2025 --month 11 --day 1 \
        --lead-days 30 \
        --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 46
    ```

=== "90-Day Forecast"
    ```bash
    python download_c3s_seasonal_temp_ensmean_daily.py \
        --outdir data/c3s_seasonal \
        --outfile c3s_seasonal_ecmwf_t2m_ensmean_2025-11_90d.nc \
        --originating-centre ecmwf \
        --system 51 \
        --year 2025 --month 11 --day 1 \
        --lead-days 90 \
        --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 46
    ```

=== "Limited Ensemble Members"
    ```bash
    python download_c3s_seasonal_temp_ensmean_daily.py \
        --outdir data/c3s_seasonal \
        --outfile c3s_seasonal_ecmwf_t2m_ensmean_2025-11_10m.nc \
        --originating-centre ecmwf \
        --system 51 \
        --year 2025 --month 11 --day 1 \
        --lead-days 30 \
        --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 46 \
        --max-members 10
    ```

---

## 📋 The Complete Script

### Python Download Script

Save this as `download_c3s_seasonal_temp_ensmean_daily.py`:

```python
#!/usr/bin/env python
"""
Download C3S seasonal ECMWF original single-level *2m temperature* for all
ensemble members, compute the ensemble mean at daily lead times, and save as a
compact [time, latitude, longitude] NetCDF file.

Example:
python download_c3s_seasonal_t2m_ensmean_daily.py \
  --outdir data/c3s_seasonal \
  --outfile c3s_seasonal_ecmwf_t2m_ensmean_2025-11_ea.nc \
  --originating-centre ecmwf \
  --system 51 \
  --year 2025 --month 11 --day 1 \
  --lead-days 30 \
  --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 46

Notes:
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
    time_values = (ref_time + period).values

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
    ds_mean['t2m'].attrs = {'units':'K', 'long_name':'2 metre temperature'}

    # Standardise to t2m(time, latitude, longitude)
    ds_final = standardise_t2m_dataset(ds_mean)

    ds_final.to_netcdf(final_path)
    print(f"[info] Ensemble-mean daily T2M saved → {final_path}")
    print("[info] Dimensions:", ds_final.dims)
    print("[info] Variables:", list(ds_final.data_vars))


if __name__ == "__main__":
    main()
```

---

## 🔧 Command-Line Arguments

### Required Arguments

| Argument | Type | Description | Example |
|----------|------|-------------|---------|
| `--outdir` | String | Output directory path | `data/c3s_seasonal` |
| `--outfile` | String | Output filename | `c3s_t2m_ensmean.nc` |
| `--year` | Integer | Forecast year | `2025` |
| `--month` | Integer | Forecast month (1–12) | `11` |
| `--day` | Integer | Forecast day (1–31) | `1` |
| `--lead-days` | Integer | Number of forecast days | `30` |
| `--lat-min` | Float | Minimum latitude (south) | `3` |
| `--lat-max` | Float | Maximum latitude (north) | `15` |
| `--lon-min` | Float | Minimum longitude (west) | `33` |
| `--lon-max` | Float | Maximum longitude (east) | `46` |

### Optional Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `--originating-centre` | String | Forecast center (e.g., 'ecmwf') | `ecmwf` |
| `--system` | String | Forecast system ID | `51` |
| `--max-members` | Integer | Limit ensemble members used | All members |

---

## 📅 Understanding C3S Seasonal Forecast Dates

### C3S Seasonal Schedule

C3S Seasonal forecasts are issued **monthly**:

| Day | Initialization | Typical Availability |
|-----|---------------|---------------------|
| **1st of month** | 00Z | ~3-5 days after init |

!!! warning "Valid Dates"
    Only the 1st of each month is typically available for C3S seasonal forecasts. Using other dates may result in an error.

### Finding Valid Dates

```python
from datetime import datetime, timedelta

def get_recent_c3s_dates(n=3):
    """Get the most recent n valid C3S dates (1st of month)."""
    today = datetime.now()
    dates = []
    
    # Go back up to 12 months to find valid dates
    for i in range(12):
        check_date = today - timedelta(days=30*i)
        # Set to 1st of month
        first_of_month = check_date.replace(day=1)
        dates.append(first_of_month.strftime("%Y-%m-%d"))
        if len(dates) >= n:
            break
    
    return dates

print("Recent C3S dates:", get_recent_c3s_dates())
```

---

## ⏰ C3S Seasonal vs S2S Temperature Comparison

| Feature | C3S Seasonal | ECMWF S2S |
|---------|--------------|-----------|
| **Forecast Range** | Up to 7 months | 46 days |
| **Resolution** | ~1° (~100 km) | ~1.5° (~150 km) |
| **Update Frequency** | Monthly (1st) | Mon & Thu |
| **Ensemble Members** | 51 (ECMWF) | 51 |
| **Temperature Type** | Daily mean | Daily mean |
| **Best For** | Months 1-3 | Weeks 2-6 |
| **Access** | CDS API (account) | MARS API (account) |
| **Processing** | Ensemble mean computed | Individual members |

!!! tip "When to Use C3S Seasonal Temperature"
    - **Long-range outlook** - 1-3 month forecasts
    - **Seasonal planning** - agricultural decisions
    - **Climate services** - monthly outlook products
    - **Research** - seasonal predictability studies
    - **Disease modeling** - temperature-dependent transmission

---

## 📍 Regional Bounding Boxes

Use these coordinates with the `--lat-min`, `--lat-max`, `--lon-min`, `--lon-max` arguments:

=== "Ethiopia"
    ```bash
    --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 46
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

=== "Greater Horn of Africa"
    ```bash
    --lat-min -12 --lat-max 23 --lon-min 21 --lon-max 52
    ```
    **Coverage:** Extended region including Sudan, South Sudan

=== "Africa"
    ```bash
    --lat-min -35 --lat-max 38 --lon-min -18 --lon-max 52
    ```
    **Coverage:** Entire African continent

---

## 💡 Usage Examples

### Example 1: 30-Day Forecast for Ethiopia

```bash
python download_c3s_seasonal_temp_ensmean_daily.py \
    --outdir data/c3s_seasonal \
    --outfile c3s_seasonal_ecmwf_t2m_ensmean_2025-11_ea.nc \
    --originating-centre ecmwf \
    --system 51 \
    --year 2025 --month 11 --day 1 \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 46
```

**What it does:**

- Downloads 30 days of daily temperature
- Computes ensemble mean over all 51 members
- Clips to Ethiopia boundaries
- Saves as NetCDF in Kelvin

---

### Example 2: 90-Day Extended Forecast

```bash
python download_c3s_seasonal_temp_ensmean_daily.py \
    --outdir data/c3s_seasonal \
    --outfile c3s_seasonal_ecmwf_t2m_ensmean_2025-11_90d.nc \
    --originating-centre ecmwf \
    --system 51 \
    --year 2025 --month 11 --day 1 \
    --lead-days 90 \
    --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 46
```

**What it does:**

- Downloads 90 days (3 months) of forecasts
- Useful for seasonal outlook
- ~3 months of daily temperature

---

### Example 3: Limited Ensemble Members

```bash
python download_c3s_seasonal_temp_ensmean_daily.py \
    --outdir data/c3s_seasonal \
    --outfile c3s_seasonal_ecmwf_t2m_ensmean_2025-11_10m.nc \
    --originating-centre ecmwf \
    --system 51 \
    --year 2025 --month 11 --day 1 \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 46 \
    --max-members 10
```

**What it does:**

- Uses only first 10 ensemble members
- Faster processing
- Smaller file size
- Useful for testing

---

## 📂 Output Directory Structure

After running the script, your output directory will contain:

```
data/c3s_seasonal/
├── c3s_seasonal_ecmwf_t2m_ensmean_2025-11_ea.nc      # Final output
└── c3s_seasonal_ecmwf_t2m_ensmean_2025-11_ea.nc.raw.nc  # Raw download (can be deleted)
```

---

## 🔍 Verifying Your Download

After downloading, verify your data using Python:

```python
import xarray as xr
import matplotlib.pyplot as plt

# Open the forecast file
ds = xr.open_dataset('data/c3s_seasonal/c3s_seasonal_ecmwf_t2m_ensmean_2025-11_ea.nc')

# Display dataset information
print(ds)

# Check dimensions
print(f"Time steps: {len(ds.time)}")
print(f"Latitude range: {float(ds.latitude.min()):.2f} to {float(ds.latitude.max()):.2f}")
print(f"Longitude range: {float(ds.longitude.min()):.2f} to {float(ds.longitude.max()):.2f}")

# Check temperature variable
temp = ds['t2m']
print(f"Temperature units: {temp.attrs.get('units', 'unknown')}")
print(f"Temperature range: {float(temp.min()):.1f} to {float(temp.max()):.1f} K")

# Convert to Celsius for easier interpretation
temp_c = temp - 273.15
print(f"Temperature range: {float(temp_c.min()):.1f} to {float(temp_c.max()):.1f} °C")

# Plot monthly mean
fig, ax = plt.subplots(figsize=(10, 8))
monthly_mean = temp_c.mean(dim='time')
monthly_mean.plot(ax=ax, cmap='RdYlBu_r', vmin=15, vmax=35)
ax.set_title('C3S Seasonal Monthly Mean Daily Temperature')
plt.savefig('c3s_monthly_temp.png', dpi=150, bbox_inches='tight')
plt.show()

# Time series for a point
lat_point, lon_point = 9.0, 38.7  # Addis Ababa
point_data = temp_c.sel(latitude=lat_point, longitude=lon_point, method='nearest')
point_data.plot(marker='o', figsize=(12, 4), color='orangered')
plt.title(f'C3S Seasonal 30-Day Temperature Forecast for Addis Ababa')
plt.ylabel('Temperature (°C)')
plt.xlabel('Date')
plt.grid(True, alpha=0.3)
plt.axhline(y=point_data.mean(), color='gray', linestyle='--', label='Mean')
plt.legend()
plt.savefig('c3s_temp_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## 📊 Understanding C3S Seasonal Temperature Data

### Daily Mean Temperature

C3S provides **daily mean 2-meter temperature**:

```
Lead time 24h:  Mean temperature for Day 1 (hours 0 to 24)
Lead time 48h:  Mean temperature for Day 2 (hours 24 to 48)
Lead time 72h:  Mean temperature for Day 3 (hours 48 to 72)
...
```

### Units

| Native Units | Conversion | Final Units |
|--------------|------------|-------------|
| Kelvin (K) | - 273.15 | Celsius (°C) |

The script outputs data in **Kelvin** by default. You can convert to Celsius in post-processing:

```python
temp_celsius = temp_kelvin - 273.15
```

Or modify the script to convert automatically (see commented code in script).

### Ensemble Mean

The script computes the **ensemble mean** over all members:

- Reduces uncertainty
- Provides smoother forecasts
- Suitable for deterministic applications

For probabilistic products, you would need to download individual members.

---

## ⚠️ Troubleshooting

### Common Issues and Solutions

=== "Authentication Error"

    **Problem:** CDS API key not configured
    
    ```
    Exception: Invalid key
    ```
    
    **Solutions:**
    
    1. **Create API key file:**
        ```bash
        # Linux/Mac
        nano ~/.cdsapirc
        
        # Windows
        notepad %USERPROFILE%\.cdsapirc
        ```
    
    2. **Add credentials:**
        ```text
        url: https://cds.climate.copernicus.eu/api/v2
        key: YOUR-UID:YOUR-API-KEY
        ```
    
    3. **Get your key:** [https://cds.climate.copernicus.eu/#!/home](https://cds.climate.copernicus.eu/#!/home)

=== "Invalid Date"

    **Problem:** Date is not valid for C3S seasonal
    
    ```
    Error: No data available for date
    ```
    
    **Solutions:**
    
    1. **Use 1st of month dates only**
    2. **Check recent valid dates** using the Python code above
    3. **Wait for processing:** Data available ~3-5 days after init

=== "Data Not Yet Available"

    **Problem:** Forecast not yet produced
    
    **Solutions:**
    
    1. **Wait for processing:** C3S data is typically available ~3-5 days after initialization
    2. **Use an earlier date:** Try the previous month's 1st
    3. **Check CDS calendar:** [C3S Seasonal Database](https://cds.climate.copernicus.eu/cdsapp#!/dataset/seasonal-original-single-levels)

=== "Timeout or Slow Download"

    **Problem:** Large request takes too long
    
    **Solutions:**
    
    1. **Reduce lead_days:** Start with fewer days
    2. **Reduce region size:** Use smaller bounding box
    3. **Use --max-members:** Limit ensemble members
    4. **Try off-peak hours:** Early morning UTC

=== "Temperature Values Seem Wrong"

    **Problem:** Values around 280-300 instead of expected °C
    
    **Cause:** Data is in Kelvin, not Celsius
    
    **Solution:**
    ```python
    # Convert from Kelvin to Celsius
    temp_celsius = temp_kelvin - 273.15
    ```

=== "Missing Variable 't2m'"

    **Problem:** Variable name mismatch
    
    **Solutions:**
    
    1. **Check raw file:** Inspect `*.raw.nc` file
    2. **Verify dataset:** Ensure correct dataset name
    3. **Check variable list:** Use `ncdump -h` to see available variables

---

## 🌐 CDS Request Details

### Understanding the Request

The script builds a CDS request with these key parameters:

```python
request = {
    "originating_centre": "ecmwf",      # Forecast center
    "system": "51",                      # ECMWF System 5
    "variable": ["2m_temperature"],      # Variable name
    "year": "2025",                      # Forecast year
    "month": "11",                       # Forecast month
    "day": "01",                         # Forecast day
    "leadtime_hour": ["24", "48", ...], # Lead times in hours
    "data_format": "netcdf",             # Output format
    "area": [N, W, S, E],                # Bounding box
}
```

### Available Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| `originating_centre` | `ecmwf`, `ukmo`, `meteo_france`, ... | Forecast center |
| `system` | `51`, `13`, ... | Forecast system version |
| `variable` | `2m_temperature`, `total_precipitation`, ... | Meteorological variable |
| `leadtime_hour` | `24`, `48`, `72`, ... | Forecast lead time (hours) |
| `area` | `[N, W, S, E]` | Bounding box (degrees) |

---

## 🔄 Converting Temperature Units

### Kelvin to Celsius

The script outputs temperature in **Kelvin** by default. To convert to Celsius:

```python
import xarray as xr

# Load the dataset
ds = xr.open_dataset('c3s_seasonal_ecmwf_t2m_ensmean_2025-11_ea.nc')

# Convert to Celsius
ds['t2m'] = ds['t2m'] - 273.15
ds['t2m'].attrs['units'] = 'degC'
ds['t2m'].attrs['long_name'] = '2 metre temperature'

# Save converted file
ds.to_netcdf('c3s_seasonal_ecmwf_t2m_ensmean_2025-11_ea_celsius.nc')
```

### Modify Script for Automatic Conversion

To automatically convert in the script, uncomment and modify these lines:

```python
# In the main() function, after computing ensemble mean:
t2m_ens_mean = t2m_ens_mean - 273.15
t2m_ens_mean.attrs["units"] = "degC"
```

---

## 🎓 Data Quality Notes

!!! success "Strengths"
    - **Long range** - up to 7 months ahead
    - **Ensemble forecasts** - probabilistic information
    - **Global coverage** - worldwide forecasts
    - **Regular updates** - monthly
    - **Free access** - with CDS account
    - **Multiple centers** - ECMWF, UKMO, Meteo-France, etc.
    - **Temperature skill** - generally better than precipitation

!!! warning "Limitations"
    - **Lower resolution** (~1°) compared to S2S/HRES
    - **Reduced skill** after month 1-2
    - **Limited availability** - 1st of month only
    - **Processing delay** - ~3-5 days latency
    - **Account required** - not fully open data
    - **Kelvin units** - requires conversion for most applications
    - **Large file sizes** - especially for long lead times

!!! tip "Best Practices"
    - **Use for months 1-3** - best skill window
    - **Convert to Celsius** - for easier interpretation
    - **Consider ensemble spread** - uncertainty increases with lead time
    - **Combine with S2S** - S2S for weeks 2-6, C3S for months 2-3
    - **Validate locally** - skill varies by region and season
    - **Monthly updates** - download new forecasts regularly
    - **Probabilistic approach** - don't rely on single forecast

---

## 📖 Additional Resources

### Official Documentation

- **C3S Seasonal Database:** [https://cds.climate.copernicus.eu/cdsapp#!/dataset/seasonal-original-single-levels](https://cds.climate.copernicus.eu/cdsapp#!/dataset/seasonal-original-single-levels)
- **CDS API Guide:** [https://cds.climate.copernicus.eu/how-to-use-api](https://cds.climate.copernicus.eu/how-to-use-api)
- **C3S Documentation:** [https://confluence.ecmwf.int/display/CKB](https://confluence.ecmwf.int/display/CKB)

### Python Libraries

- **cdsapi:** [https://pypi.org/project/cdsapi/](https://pypi.org/project/cdsapi/)
- **xarray:** [https://xarray.pydata.org/](https://xarray.pydata.org/)

### Related Forecasts

| Source | Range | Resolution | Update | Access |
|--------|-------|------------|--------|--------|
| **ECMWF HRES** | 10 days | 0.25° | Daily | Open Data |
| **ECMWF S2S** | 46 days | 1.5° | Mon/Thu | MARS API |
| **C3S Seasonal** | 7 months | 1° | Monthly | CDS API |
| **GFS** | 16 days | 0.25° | 4× daily | NOMADS |

---

## 🚀 Next Steps

<div class="grid cards" markdown>

-   :material-chart-line: **Analyze Seasonal Forecasts**
    
    ---
    
    Calculate monthly anomalies  
    Compare with climatology  
    
    → [Xarray Tutorial](06-Xarray_for_Climate_and_Meteorology_Workshop.md)

-   :material-map: **Visualize Seasonal Outlook**
    
    ---
    
    Create monthly forecast maps  
    Plot temperature evolution  
    
    → [Matplotlib Tutorial](05-Matplotlib_for_Climate_and_Meteorology_Workshop.md)

-   :material-weather-pouring: **Download Precipitation**
    
    ---
    
    Get matching precipitation forecasts  
    Complete weather picture  
    
    → [C3S Seasonal Precipitation](28-download_c3s_seasonal_precip_ensmean_daily.md)

-   :material-bug: **VECTRI Seasonal Outlook**
    
    ---
    
    Long-range malaria risk  
    1-3 month outbreak prediction  
    
    → [VECTRI Model](../day1/06-vectri-model-theory-and-code.md)

</div>

---

!!! example "Need Help?"
    If you encounter issues or have questions:
    
    - Check the [Troubleshooting](#troubleshooting) section
    - Review [C3S Seasonal documentation](https://cds.climate.copernicus.eu/cdsapp#!/dataset/seasonal-original-single-levels)
    - Visit [CDS Support Portal](https://cds.climate.copernicus.eu/contact)
    - Contact workshop instructors

---

<div style="background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
  <h3 style="margin: 0 0 1rem 0;">🌡️ Ready for Seasonal Temperature Forecasting!</h3>
  <p style="margin: 0; opacity: 0.95;">You now have everything you need to download C3S Seasonal temperature forecasts for long-range prediction and seasonal outlook applications.</p>
</div>

