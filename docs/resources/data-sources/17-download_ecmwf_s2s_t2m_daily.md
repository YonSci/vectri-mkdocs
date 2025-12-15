# 🌡️ Downloading ECMWF S2S Temperature Forecasts

## Overview

**ECMWF S2S (Sub-seasonal to Seasonal)** provides extended-range weather forecasts up to 46 days ahead. This tutorial guides you through downloading daily-averaged 2-meter temperature from the ECMWF S2S database using the ECMWF API.

<div class="grid cards" markdown>

-   :material-thermometer: **Dataset**
    
    ---
    
    ECMWF S2S Daily Temperature
    
    **Variable:** 2m Temperature (2t)  
    **Resolution:** ~1.5° (native) or custom  
    **Output:** Daily means (24h average)  
    **Forecast Range:** 1–46 days

-   :material-earth: **Spatial Coverage**
    
    ---
    
    **Region:** Global  
    **Latitude:** 90°S to 90°N  
    **Longitude:** -180° to 180°  
    **Subsetting:** Supported

-   :material-update: **Update Frequency**
    
    ---
    
    **Cycles:** Monday & Thursday  
    **Latency:** ~1-2 days after init  
    **Ensemble:** 51 members (control + 50)

-   :material-file-download: **Access**
    
    ---
    
    **Source:** ECMWF MARS  
    **Method:** ecmwfapi Python  
    **Authentication:** Required (free)  
    **Format:** NetCDF or GRIB

</div>

---

## 🎯 What This Script Does

```mermaid
graph LR
    A[Select Forecast Date] --> B[Build MARS Request]
    B --> C[Submit to ECMWF]
    C --> D[Download NetCDF]
    D --> E[Daily Mean T2M Ready]
    
    style A fill:#fff3e0
    style E fill:#c8e6c9
```

The script performs the following operations:

1. **Builds** a MARS request for S2S daily-averaged temperature
2. **Submits** the request to ECMWF servers
3. **Downloads** data clipped to your region of interest
4. **Saves** as NetCDF with daily 24-hour mean temperatures

---

## 🚀 Quick Start Guide

### Prerequisites

!!! warning "ECMWF Account Required"
    You need a free ECMWF account to access S2S data:
    
    1. **Register:** [https://apps.ecmwf.int/registration/](https://apps.ecmwf.int/registration/)
    2. **Get API key:** [https://api.ecmwf.int/v1/key/](https://api.ecmwf.int/v1/key/)
    3. **Configure:** Create `~/.ecmwfapirc` with your credentials

!!! info "Required Python Packages"
    ```bash
    pip install ecmwf-api-client
    ```

### API Configuration

Create a file `~/.ecmwfapirc` (Linux/Mac) or `%USERPROFILE%\.ecmwfapirc` (Windows):

```json
{
    "url"   : "https://api.ecmwf.int/v1",
    "key"   : "YOUR-API-KEY-HERE",
    "email" : "your.email@example.com"
}
```

### Basic Usage

=== "30-Day Forecast"
    ```bash
    python download_ecmwf_s2s_t2m.py \
        --outdir data/s2s_ecmwf \
        --outfile s2s_ecmwf_t2m_ethiopia_30day.nc \
        --date 2025-01-13 \
        --lead-days 30 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48
    ```

=== "Full 46-Day Forecast"
    ```bash
    python download_ecmwf_s2s_t2m.py \
        --outdir data/s2s_ecmwf \
        --outfile s2s_ecmwf_t2m_ethiopia_46day.nc \
        --date 2025-01-13 \
        --lead-days 46 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48
    ```

=== "Custom Grid Resolution"
    ```bash
    python download_ecmwf_s2s_t2m.py \
        --outdir data/s2s_ecmwf \
        --outfile s2s_ecmwf_t2m_ethiopia_0p5.nc \
        --date 2025-01-13 \
        --lead-days 30 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --grid 0.5/0.5
    ```

---

## 📋 The Complete Script

### Python Download Script

Save this as `download_ecmwf_s2s_t2m.py`:

```python
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
```

---

## 🔧 Command-Line Arguments

### Required Arguments

| Argument | Type | Description | Example |
|----------|------|-------------|---------|
| `--outdir` | String | Output directory path | `data/s2s_ecmwf` |
| `--outfile` | String | Output filename | `s2s_t2m_ethiopia.nc` |
| `--date` | Date (YYYY-MM-DD) | Forecast initialization date | `2025-01-13` |
| `--lead-days` | Integer | Number of forecast days (1–46) | `30` |
| `--lat-min` | Float | Minimum latitude (south) | `3` |
| `--lat-max` | Float | Maximum latitude (north) | `15` |
| `--lon-min` | Float | Minimum longitude (west) | `33` |
| `--lon-max` | Float | Maximum longitude (east) | `48` |

### Optional Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `--grid` | String | Output grid resolution | Native (~1.5°) |
| `--fmt` | String | Output format (netcdf/grib) | `netcdf` |

---

## 🌡️ Understanding S2S Temperature Data

### Daily Mean vs Instantaneous

S2S provides **daily-averaged** temperature, not instantaneous values:

| Data Type | Request Format | Description |
|-----------|---------------|-------------|
| **Daily Mean** | `"0-24/24-48/..."` | 24-hour average temperature |
| **Instantaneous** | `"0/24/48/..."` | Value at specific time |

The script uses daily means, which are more appropriate for:
- Climate analysis
- Malaria modeling (VECTRI)
- Seasonal outlook products

### Units

| Native Units | Typical Range | Notes |
|--------------|---------------|-------|
| Kelvin (K) | 250-320 K | Convert to °C: T(°C) = T(K) - 273.15 |

### Step Format

For daily-averaged products, S2S uses interval notation:

```
"0-24"    → Day 1 mean (hours 0 to 24)
"24-48"   → Day 2 mean (hours 24 to 48)
"48-72"   → Day 3 mean (hours 48 to 72)
...
```

---

## 📅 Understanding S2S Forecast Dates

### ECMWF S2S Schedule

ECMWF S2S forecasts are issued **twice weekly**:

| Day | Initialization | Typical Availability |
|-----|---------------|---------------------|
| **Monday** | 00Z | Tuesday ~12:00 UTC |
| **Thursday** | 00Z | Friday ~12:00 UTC |

!!! warning "Valid Dates"
    Only Monday and Thursday dates are valid for S2S requests. Using other dates will result in an error.

### Finding Valid Dates

```python
from datetime import datetime, timedelta

def get_recent_s2s_dates(n=4):
    """Get the most recent n valid S2S dates (Mondays and Thursdays)."""
    today = datetime.now()
    dates = []
    
    # Go back up to 30 days to find valid dates
    for i in range(30):
        check_date = today - timedelta(days=i)
        if check_date.weekday() in [0, 3]:  # Monday=0, Thursday=3
            dates.append(check_date.strftime("%Y-%m-%d"))
            if len(dates) >= n:
                break
    
    return dates

print("Recent S2S dates:", get_recent_s2s_dates())
```

---

## ⏰ S2S vs HRES Temperature Comparison

| Feature | ECMWF S2S | ECMWF HRES |
|---------|-----------|------------|
| **Forecast Range** | 46 days | 10 days |
| **Resolution** | ~1.5° (~150 km) | 0.25° (~28 km) |
| **Update Frequency** | Mon & Thu | Daily (00Z, 12Z) |
| **Ensemble Members** | 51 | 1 (deterministic) |
| **Temperature Type** | Daily mean | Instantaneous → daily mean |
| **Best For** | Weeks 2-6 | Days 1-10 |
| **Access** | MARS API (account) | Open Data (free) |

!!! tip "When to Use S2S Temperature"
    - **Seasonal disease risk** - temperature-dependent transmission
    - **Agricultural planning** - growing degree days
    - **Energy demand forecasting** - heating/cooling needs
    - **Climate anomaly monitoring** - warm/cold spells

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

### Example 1: 30-Day Temperature Forecast for Ethiopia

```bash
python download_ecmwf_s2s_t2m.py \
    --outdir data/s2s_ecmwf \
    --outfile s2s_ecmwf_t2m_ethiopia_30day.nc \
    --date 2025-01-13 \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48
```

**What it does:**

- Downloads 30 days of daily mean temperature
- Clips to Ethiopia boundaries
- Uses native ~1.5° resolution
- Saves as NetCDF

---

### Example 2: Full 46-Day Extended Forecast

```bash
python download_ecmwf_s2s_t2m.py \
    --outdir data/s2s_ecmwf \
    --outfile s2s_ecmwf_t2m_ethiopia_46day.nc \
    --date 2025-01-13 \
    --lead-days 46 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48
```

**What it does:**

- Downloads maximum forecast range (46 days)
- Useful for seasonal outlook
- ~6.5 weeks of daily temperature

---

### Example 3: Higher Resolution Output

```bash
python download_ecmwf_s2s_t2m.py \
    --outdir data/s2s_ecmwf \
    --outfile s2s_ecmwf_t2m_ethiopia_0p5.nc \
    --date 2025-01-13 \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --grid 0.5/0.5
```

**What it does:**

- Interpolates to 0.5° grid
- Higher spatial detail (but no new information)
- Useful for matching other datasets

---

### Example 4: Combined Temperature and Precipitation

Download both variables for complete weather forecasts:

```bash
#!/bin/bash
# download_s2s_both.sh

S2S_DATE="2025-01-13"
OUTDIR="data/s2s_operational"

# Download precipitation
python download_ecmwf_s2s_tp.py \
    --outdir "$OUTDIR" \
    --outfile "s2s_ecmwf_tp_eth_${S2S_DATE}.nc" \
    --date "$S2S_DATE" \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48

# Download temperature
python download_ecmwf_s2s_t2m.py \
    --outdir "$OUTDIR" \
    --outfile "s2s_ecmwf_t2m_eth_${S2S_DATE}.nc" \
    --date "$S2S_DATE" \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48

echo "Downloaded S2S temperature and precipitation for $S2S_DATE"
```

---

### Example 5: Operational Weekly Script

Create a script for weekly automated downloads:

```bash
#!/bin/bash
# weekly_s2s_t2m_download.sh
# Run on Tuesday and Friday after S2S data is available

# Find the most recent Monday or Thursday
TODAY=$(date -u +%Y-%m-%d)
DOW=$(date -u +%u)  # 1=Monday, 4=Thursday

if [ $DOW -ge 1 ] && [ $DOW -le 3 ]; then
    DAYS_BACK=$((DOW - 1))
elif [ $DOW -ge 4 ] && [ $DOW -le 6 ]; then
    DAYS_BACK=$((DOW - 4))
else
    DAYS_BACK=3
fi

S2S_DATE=$(date -u -d "$TODAY - $DAYS_BACK days" +%Y-%m-%d)

OUTDIR="data/s2s_operational"
OUTFILE="s2s_ecmwf_t2m_eth_${S2S_DATE}.nc"

python download_ecmwf_s2s_t2m.py \
    --outdir "$OUTDIR" \
    --outfile "$OUTFILE" \
    --date "$S2S_DATE" \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48

echo "Downloaded S2S temperature forecast initialized on $S2S_DATE"
```

---

## 📂 Output Directory Structure

After running the script, your output directory will contain:

```
data/s2s_ecmwf/
└── s2s_ecmwf_t2m_ethiopia_30day.nc    # NetCDF output
```

---

## 🔍 Verifying Your Download

After downloading, verify your data using Python:

```python
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# Open the forecast file
ds = xr.open_dataset('data/s2s_ecmwf/s2s_ecmwf_t2m_ethiopia_30day.nc')

# Display dataset information
print(ds)

# Check dimensions
print(f"Lead times: {len(ds.time) if 'time' in ds.dims else len(ds.step)}")
print(f"Latitude range: {float(ds.latitude.min()):.2f} to {float(ds.latitude.max()):.2f}")
print(f"Longitude range: {float(ds.longitude.min()):.2f} to {float(ds.longitude.max()):.2f}")

# Get temperature variable (may be 't2m' or '2t')
temp_var = 't2m' if 't2m' in ds.data_vars else '2t' if '2t' in ds.data_vars else list(ds.data_vars)[0]
temp = ds[temp_var]

# Convert from Kelvin to Celsius if needed
if temp.max() > 200:  # Likely in Kelvin
    temp_c = temp - 273.15
    units = '°C'
else:
    temp_c = temp
    units = temp.attrs.get('units', '°C')

print(f"Temperature range: {float(temp_c.min()):.1f} to {float(temp_c.max()):.1f} {units}")

# Plot Week 1 mean temperature
fig, ax = plt.subplots(figsize=(10, 8))
week1_mean = temp_c.isel(time=slice(0, 7)).mean(dim='time')
week1_mean.plot(ax=ax, cmap='RdYlBu_r', vmin=15, vmax=35)
ax.set_title('S2S Week 1 Mean Daily Temperature')
plt.savefig('s2s_week1_temp.png', dpi=150, bbox_inches='tight')
plt.show()

# Plot weekly evolution
weeks = [0, 7, 14, 21, 28]
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for i, (start, end) in enumerate(zip(weeks[:-1], weeks[1:])):
    if end <= len(temp_c.time):
        weekly_mean = temp_c.isel(time=slice(start, end)).mean(dim='time')
        weekly_mean.plot(ax=axes[i], cmap='RdYlBu_r', vmin=15, vmax=35, add_colorbar=False)
        axes[i].set_title(f'Week {i+1}')
        axes[i].set_xlabel('')
        axes[i].set_ylabel('')
plt.tight_layout()
plt.savefig('s2s_temp_weekly_evolution.png', dpi=150, bbox_inches='tight')
plt.show()

# Time series for a point
lat_point, lon_point = 9.0, 38.7  # Addis Ababa
point_data = temp_c.sel(latitude=lat_point, longitude=lon_point, method='nearest')
point_data.plot(marker='o', figsize=(12, 4), color='orangered')
plt.title(f'S2S 30-Day Temperature Forecast for Addis Ababa')
plt.ylabel('Temperature (°C)')
plt.xlabel('Lead Time')
plt.grid(True, alpha=0.3)
plt.axhline(y=point_data.mean(), color='gray', linestyle='--', label='Mean')
plt.legend()
plt.savefig('s2s_temp_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()

# Calculate temperature anomaly (if climatology available)
# climatology = ...  # Load your climatology
# anomaly = temp_c - climatology
```

---

## 📊 Output Variable Details

### Main Variable

| Variable | Description | Native Units | Typical Conversion |
|----------|-------------|--------------|-------------------|
| `t2m` or `2t` | Daily mean 2m temperature | Kelvin (K) | °C = K - 273.15 |

### Coordinates

| Coordinate | Description |
|------------|-------------|
| `time` or `step` | Forecast lead time |
| `latitude` | Latitude (degrees north) |
| `longitude` | Longitude (degrees east) |

### Attributes

```python
# Dataset attributes (example)
{
    'Conventions': 'CF-1.6',
    'history': 'Retrieved from ECMWF S2S',
    'institution': 'ECMWF'
}

# Variable attributes
{
    'units': 'K',
    'long_name': '2 metre temperature',
    'standard_name': 'air_temperature'
}
```

---

## ⚠️ Troubleshooting

### Common Issues and Solutions

=== "Authentication Error"

    **Problem:** API key not configured
    
    ```
    APIKeyFetchError: Could not get API key
    ```
    
    **Solutions:**
    
    1. **Create API key file:**
        ```bash
        # Linux/Mac
        nano ~/.ecmwfapirc
        
        # Windows
        notepad %USERPROFILE%\.ecmwfapirc
        ```
    
    2. **Add credentials:**
        ```json
        {
            "url"   : "https://api.ecmwf.int/v1",
            "key"   : "YOUR-API-KEY",
            "email" : "your.email@example.com"
        }
        ```
    
    3. **Get your key:** [https://api.ecmwf.int/v1/key/](https://api.ecmwf.int/v1/key/)

=== "Invalid Date"

    **Problem:** Date is not a valid S2S initialization date
    
    ```
    Error: No data available for date 2025-01-14
    ```
    
    **Solutions:**
    
    1. **Use Monday or Thursday dates only**
    2. **Check recent valid dates** using the Python code above

=== "Data Not Yet Available"

    **Problem:** Forecast not yet produced
    
    **Solutions:**
    
    1. **Wait for processing:** S2S data is typically available ~24-36 hours after initialization
    2. **Use an earlier date:** Try the previous Monday or Thursday

=== "Temperature Values Seem Wrong"

    **Problem:** Values around 280-300 instead of expected °C
    
    **Cause:** Data is in Kelvin, not Celsius
    
    **Solution:**
    ```python
    # Convert from Kelvin to Celsius
    temp_celsius = temp_kelvin - 273.15
    ```

=== "Missing Steps"

    **Problem:** Some forecast steps not available
    
    **Solutions:**
    
    1. **Script handles this:** `"expect": "any"` allows partial downloads
    2. **Check available data:** Some dates may have fewer steps

---

## 🔗 Combining Temperature and Precipitation

For malaria modeling with VECTRI, combine both variables:

```python
import xarray as xr

# Load both datasets
ds_temp = xr.open_dataset('data/s2s_ecmwf/s2s_ecmwf_t2m_ethiopia_30day.nc')
ds_precip = xr.open_dataset('data/s2s_ecmwf/s2s_ecmwf_tp_ethiopia_30day.nc')

# Rename variables for consistency
ds_temp = ds_temp.rename({'2t': 't2m'} if '2t' in ds_temp else {})
ds_precip = ds_precip.rename({'tp': 'precip'} if 'tp' in ds_precip else {})

# Convert temperature to Celsius
if ds_temp.t2m.max() > 200:
    ds_temp['t2m'] = ds_temp['t2m'] - 273.15
    ds_temp['t2m'].attrs['units'] = 'degC'

# Convert precipitation to mm/day if in meters
if ds_precip.precip.max() < 1:
    ds_precip['precip'] = ds_precip['precip'] * 1000
    ds_precip['precip'].attrs['units'] = 'mm/day'

# Merge datasets
ds_combined = xr.merge([ds_temp, ds_precip])

# Verify
print(ds_combined)

# Save combined file
ds_combined.to_netcdf('data/s2s_ecmwf/s2s_combined_ethiopia_30day.nc')
print("Saved combined temperature and precipitation dataset")
```

---

## 🎓 Data Quality Notes

!!! success "Strengths"
    - **Extended range** - up to 46 days ahead
    - **Ensemble forecasts** - probabilistic information
    - **Global coverage** - worldwide forecasts
    - **Regular updates** - twice weekly
    - **Free access** - with ECMWF account
    - **Temperature skill** - generally better than precipitation

!!! warning "Limitations"
    - **Lower resolution** (~1.5°) compared to HRES
    - **Reduced skill** after week 2
    - **Limited availability** - Mon/Thu only
    - **Processing delay** - ~24-36 hours latency
    - **Account required** - not fully open data
    - **Kelvin units** - requires conversion

!!! tip "Best Practices"
    - **Use for weeks 2-6** - beyond HRES range
    - **Convert to Celsius** - for easier interpretation
    - **Consider ensemble spread** - uncertainty increases with lead time
    - **Combine with HRES** - HRES for week 1, S2S for weeks 2+
    - **Validate locally** - skill varies by region and season
    - **Calculate anomalies** - compare to climatology

---

## 📖 Additional Resources

### Official Documentation

- **S2S Database:** [https://apps.ecmwf.int/datasets/data/s2s/](https://apps.ecmwf.int/datasets/data/s2s/)
- **S2S Project:** [https://s2sprediction.net/](https://s2sprediction.net/)
- **MARS Documentation:** [https://confluence.ecmwf.int/display/UDOC/MARS](https://confluence.ecmwf.int/display/UDOC/MARS)

### Python Libraries

- **ecmwf-api-client:** [https://pypi.org/project/ecmwf-api-client/](https://pypi.org/project/ecmwf-api-client/)
- **xarray:** [https://xarray.pydata.org/](https://xarray.pydata.org/)

### Related Tutorials

- [S2S Precipitation](16-download_ecmwf_s2s_tp_daily.md) - Download precipitation data
- [ECMWF HRES Temperature](15-download_ecmwf_hres_temp.md) - Short-range forecasts
- [GFS Temperature](14-download_gfs_temp_forecast.md) - Alternative forecast source

---

## 🚀 Next Steps

<div class="grid cards" markdown>

-   :material-chart-line: **Analyze Temperature Trends**
    
    ---
    
    Calculate weekly/monthly anomalies  
    Compare with climatology  
    
    → [Xarray Tutorial](../../day3/06-Xarray_for_Climate_and_Meteorology_Workshop.md)

-   :material-map: **Visualize Extended Forecasts**
    
    ---
    
    Create weekly forecast maps  
    Plot temperature evolution  
    
    → [Matplotlib Tutorial](../../day3/05-Matplotlib_for_Climate_and_Meteorology_Workshop.md)

-   :material-weather-pouring: **Download Precipitation**
    
    ---
    
    Get matching precipitation forecasts  
    Complete weather picture  
    
    → [S2S Precipitation](16-download_ecmwf_s2s_tp_daily.md)

-   :material-bug: **VECTRI Early Warning**
    
    ---
    
    Temperature-dependent transmission  
    2-6 week malaria risk  
    
    → [VECTRI Model](../../day1/vectri_model_components_larvae_to_hydrology.md)

</div>

---

!!! example "Need Help?"
    If you encounter issues or have questions:
    
    - Check the [Troubleshooting](#troubleshooting) section
    - Review [ECMWF S2S documentation](https://apps.ecmwf.int/datasets/data/s2s/)
    - Visit [ECMWF Support Portal](https://confluence.ecmwf.int/)
    - Contact workshop instructors

---

<div style="background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
  <h3 style="margin: 0 0 1rem 0;">🌡️ Ready for Extended-Range Temperature Forecasting!</h3>
  <p style="margin: 0; opacity: 0.95;">You now have everything you need to download ECMWF S2S temperature forecasts for sub-seasonal to seasonal prediction and climate-sensitive disease early warning.</p>
</div>
