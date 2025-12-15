# 🌧️ Downloading ECMWF S2S Precipitation Forecasts

## Overview

**ECMWF S2S (Sub-seasonal to Seasonal)** provides extended-range weather forecasts up to 46 days ahead. This tutorial guides you through downloading daily total precipitation from the ECMWF S2S database using the ECMWF API.

<div class="grid cards" markdown>

-   :material-weather-pouring: **Dataset**
    
    ---
    
    ECMWF S2S Daily Precipitation
    
    **Variable:** Total Precipitation (tp)  
    **Resolution:** ~1.5° (native) or custom  
    **Output:** Daily totals (24h)  
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
    D --> E[Daily Totals Ready]
    
    style A fill:#e8eaf6
    style E fill:#c8e6c9
```

The script performs the following operations:

1. **Builds** a MARS request for S2S daily precipitation
2. **Submits** the request to ECMWF servers
3. **Downloads** data clipped to your region of interest
4. **Saves** as NetCDF with daily 24-hour accumulations

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
    python download_ecmwf_s2s_tp.py \
        --outdir data/s2s_ecmwf \
        --outfile s2s_ecmwf_tp_ethiopia_30day.nc \
        --date 2025-01-13 \
        --lead-days 30 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48
    ```

=== "Full 46-Day Forecast"
    ```bash
    python download_ecmwf_s2s_tp.py \
        --outdir data/s2s_ecmwf \
        --outfile s2s_ecmwf_tp_ethiopia_46day.nc \
        --date 2025-01-13 \
        --lead-days 46 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48
    ```

=== "Custom Grid Resolution"
    ```bash
    python download_ecmwf_s2s_tp.py \
        --outdir data/s2s_ecmwf \
        --outfile s2s_ecmwf_tp_ethiopia_0p5.nc \
        --date 2025-01-13 \
        --lead-days 30 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --grid 0.5/0.5
    ```

---

## 📋 The Complete Script

### Python Download Script

Save this as `download_ecmwf_s2s_tp.py`:

```python
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
```

---

## 🔧 Command-Line Arguments

### Required Arguments

| Argument | Type | Description | Example |
|----------|------|-------------|---------|
| `--outdir` | String | Output directory path | `data/s2s_ecmwf` |
| `--outfile` | String | Output filename | `s2s_tp_ethiopia.nc` |
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

def next_s2s_date(from_date=None):
    """Find the next valid S2S forecast date (Monday or Thursday)."""
    if from_date is None:
        from_date = datetime.now()
    
    weekday = from_date.weekday()  # 0=Monday, 3=Thursday
    
    # Days until next Monday or Thursday
    days_to_monday = (7 - weekday) % 7 if weekday != 0 else 0
    days_to_thursday = (3 - weekday) % 7 if weekday != 3 else 0
    
    if days_to_monday == 0:
        return from_date.strftime("%Y-%m-%d")
    elif days_to_thursday == 0:
        return from_date.strftime("%Y-%m-%d")
    elif days_to_monday < days_to_thursday:
        return (from_date + timedelta(days=days_to_monday)).strftime("%Y-%m-%d")
    else:
        return (from_date + timedelta(days=days_to_thursday)).strftime("%Y-%m-%d")

print(f"Next S2S date: {next_s2s_date()}")
```

---

## ⏰ S2S vs HRES Comparison

| Feature | ECMWF S2S | ECMWF HRES |
|---------|-----------|------------|
| **Forecast Range** | 46 days | 10 days |
| **Resolution** | ~1.5° (~150 km) | 0.25° (~28 km) |
| **Update Frequency** | Mon & Thu | Daily (00Z, 12Z) |
| **Ensemble Members** | 51 | 1 (deterministic) |
| **Best For** | Weeks 2-6 | Days 1-10 |
| **Skill** | Lower (extended range) | Higher (short range) |
| **Access** | MARS API (account) | Open Data (free) |

!!! tip "When to Use S2S"
    - **Early warning systems** - 2-6 week lead time
    - **Seasonal planning** - agricultural decisions
    - **Outbreak prediction** - malaria risk forecasting
    - **Climate variability** - MJO, ENSO impacts

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

### Example 1: 30-Day Forecast for Ethiopia

```bash
python download_ecmwf_s2s_tp.py \
    --outdir data/s2s_ecmwf \
    --outfile s2s_ecmwf_tp_ethiopia_30day.nc \
    --date 2025-01-13 \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48
```

**What it does:**

- Downloads 30 days of daily precipitation
- Clips to Ethiopia boundaries
- Uses native ~1.5° resolution
- Saves as NetCDF

---

### Example 2: Full 46-Day Extended Forecast

```bash
python download_ecmwf_s2s_tp.py \
    --outdir data/s2s_ecmwf \
    --outfile s2s_ecmwf_tp_ethiopia_46day.nc \
    --date 2025-01-13 \
    --lead-days 46 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48
```

**What it does:**

- Downloads maximum forecast range (46 days)
- Useful for seasonal outlook
- ~6.5 weeks of daily precipitation

---

### Example 3: Higher Resolution Output

```bash
python download_ecmwf_s2s_tp.py \
    --outdir data/s2s_ecmwf \
    --outfile s2s_ecmwf_tp_ethiopia_0p5.nc \
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

### Example 4: GRIB Output Format

```bash
python download_ecmwf_s2s_tp.py \
    --outdir data/s2s_ecmwf \
    --outfile s2s_ecmwf_tp_ethiopia.grib \
    --date 2025-01-13 \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --fmt grib
```

**What it does:**

- Downloads in GRIB format
- Smaller file size
- Requires cfgrib to read

---

### Example 5: Operational Weekly Script

Create a script for weekly automated downloads:

```bash
#!/bin/bash
# weekly_s2s_download.sh
# Run on Tuesday and Friday after S2S data is available

# Find the most recent Monday or Thursday
TODAY=$(date -u +%Y-%m-%d)
DOW=$(date -u +%u)  # 1=Monday, 4=Thursday

if [ $DOW -ge 1 ] && [ $DOW -le 3 ]; then
    # Monday, Tuesday, Wednesday -> use Monday
    DAYS_BACK=$((DOW - 1))
elif [ $DOW -ge 4 ] && [ $DOW -le 6 ]; then
    # Thursday, Friday, Saturday -> use Thursday
    DAYS_BACK=$((DOW - 4))
else
    # Sunday -> use Thursday
    DAYS_BACK=3
fi

S2S_DATE=$(date -u -d "$TODAY - $DAYS_BACK days" +%Y-%m-%d)

OUTDIR="data/s2s_operational"
OUTFILE="s2s_ecmwf_tp_eth_${S2S_DATE}.nc"

python download_ecmwf_s2s_tp.py \
    --outdir "$OUTDIR" \
    --outfile "$OUTFILE" \
    --date "$S2S_DATE" \
    --lead-days 30 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48

echo "Downloaded S2S forecast initialized on $S2S_DATE"
```

---

## 📂 Output Directory Structure

After running the script, your output directory will contain:

```
data/s2s_ecmwf/
└── s2s_ecmwf_tp_ethiopia_30day.nc    # NetCDF output
```

---

## 🔍 Verifying Your Download

After downloading, verify your data using Python:

```python
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# Open the forecast file
ds = xr.open_dataset('data/s2s_ecmwf/s2s_ecmwf_tp_ethiopia_30day.nc')

# Display dataset information
print(ds)

# Check dimensions
print(f"Lead times: {len(ds.time) if 'time' in ds.dims else len(ds.step)}")
print(f"Latitude range: {float(ds.latitude.min()):.2f} to {float(ds.latitude.max()):.2f}")
print(f"Longitude range: {float(ds.longitude.min()):.2f} to {float(ds.longitude.max()):.2f}")

# Get precipitation variable (may be 'tp' or 'tprate')
precip_var = 'tp' if 'tp' in ds.data_vars else list(ds.data_vars)[0]
precip = ds[precip_var]

# Check units - S2S tp is typically in meters, convert to mm
if precip.max() < 1:  # Likely in meters
    precip_mm = precip * 1000
    units = 'mm/day'
else:
    precip_mm = precip
    units = precip.attrs.get('units', 'unknown')

print(f"Precipitation range: {float(precip_mm.min()):.1f} to {float(precip_mm.max()):.1f} {units}")

# Plot Week 1 mean precipitation
fig, ax = plt.subplots(figsize=(10, 8))
week1_mean = precip_mm.isel(time=slice(0, 7)).mean(dim='time')
week1_mean.plot(ax=ax, cmap='Blues', vmin=0, vmax=20)
ax.set_title('S2S Week 1 Mean Daily Precipitation')
plt.savefig('s2s_week1_precip.png', dpi=150, bbox_inches='tight')
plt.show()

# Plot weekly evolution
weeks = [0, 7, 14, 21, 28]
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for i, (start, end) in enumerate(zip(weeks[:-1], weeks[1:])):
    if end <= len(precip_mm.time):
        weekly_mean = precip_mm.isel(time=slice(start, end)).mean(dim='time')
        weekly_mean.plot(ax=axes[i], cmap='Blues', vmin=0, vmax=20, add_colorbar=False)
        axes[i].set_title(f'Week {i+1}')
        axes[i].set_xlabel('')
        axes[i].set_ylabel('')
plt.tight_layout()
plt.savefig('s2s_weekly_evolution.png', dpi=150, bbox_inches='tight')
plt.show()

# Time series for a point
lat_point, lon_point = 9.0, 38.7  # Addis Ababa
point_data = precip_mm.sel(latitude=lat_point, longitude=lon_point, method='nearest')
point_data.plot(marker='o', figsize=(12, 4))
plt.title(f'S2S 30-Day Precipitation Forecast for Addis Ababa')
plt.ylabel('Precipitation (mm/day)')
plt.xlabel('Lead Time')
plt.grid(True, alpha=0.3)
plt.savefig('s2s_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## 📊 Understanding S2S Data

### Daily Accumulation

S2S provides **24-hour accumulated precipitation**:

```
Step 24:  Precipitation from hour 0 to 24 (Day 1)
Step 48:  Precipitation from hour 24 to 48 (Day 2)
Step 72:  Precipitation from hour 48 to 72 (Day 3)
...
```

### Units

| Native Units | Typical Range | Conversion |
|--------------|---------------|------------|
| meters (m) | 0 - 0.1 m/day | × 1000 → mm/day |

### Ensemble Members

The script downloads the **control forecast** (member 0). For probabilistic forecasts:

```python
# To request ensemble members, modify the request:
request = {
    ...
    "type": "pf",          # perturbed forecast (ensemble)
    "number": "1/2/3/.../50",  # all 50 members
    ...
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
    2. **Check recent valid dates:**
        ```python
        # Valid S2S dates are Mondays and Thursdays
        from datetime import datetime, timedelta
        today = datetime.now()
        # Find last Monday
        days_since_monday = today.weekday()
        last_monday = today - timedelta(days=days_since_monday)
        print(f"Last Monday: {last_monday.strftime('%Y-%m-%d')}")
        ```

=== "Data Not Yet Available"

    **Problem:** Forecast not yet produced
    
    ```
    Error: Data not available for the requested date
    ```
    
    **Solutions:**
    
    1. **Wait for processing:** S2S data is typically available ~24-36 hours after initialization
    2. **Use an earlier date:** Try the previous Monday or Thursday
    3. **Check S2S calendar:** [ECMWF S2S Database](https://apps.ecmwf.int/datasets/data/s2s/)

=== "Timeout or Slow Download"

    **Problem:** Large request takes too long
    
    **Solutions:**
    
    1. **Reduce lead_days:** Start with fewer days
    2. **Reduce region size:** Use smaller bounding box
    3. **Use coarser grid:** Don't specify `--grid` or use `--grid 1.5/1.5`
    4. **Try off-peak hours:** Early morning UTC

=== "Missing Steps"

    **Problem:** Some forecast steps not available
    
    ```
    Warning: Expected 30, got 28 steps
    ```
    
    **Solutions:**
    
    1. **Script handles this:** `"expect": "any"` allows partial downloads
    2. **Check available data:** Some dates may have fewer steps
    3. **Use GRIB format:** Sometimes more complete than NetCDF

---

## 🌐 ECMWF MARS Request Details

### Understanding the Request

The script builds a MARS request with these key parameters:

```python
request = {
    "class": "s2",           # S2S project
    "dataset": "s2s",        # S2S database
    "origin": "ecmf",        # ECMWF model
    "stream": "enfo",        # Ensemble forecast
    "type": "cf",            # Control forecast
    "param": "tp",           # Total precipitation
    "step": "24/48/72/...",  # Daily accumulation steps
    "area": "N/W/S/E",       # Bounding box
    "format": "netcdf",      # Output format
}
```

### Available Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| `type` | `cf`, `pf` | Control or perturbed (ensemble) |
| `number` | `0` to `50` | Ensemble member number |
| `param` | `tp`, `2t`, `msl`, ... | Meteorological variable |
| `step` | `24`, `48`, ... | Forecast lead time (hours) |
| `grid` | `1.5/1.5`, `0.5/0.5` | Output resolution |
| `format` | `netcdf`, `grib` | Output file format |

---

## 🎓 Data Quality Notes

!!! success "Strengths"
    - **Extended range** - up to 46 days ahead
    - **Ensemble forecasts** - probabilistic information
    - **Global coverage** - worldwide forecasts
    - **Regular updates** - twice weekly
    - **Free access** - with ECMWF account

!!! warning "Limitations"
    - **Lower resolution** (~1.5°) compared to HRES
    - **Reduced skill** after week 2
    - **Limited availability** - Mon/Thu only
    - **Processing delay** - ~24-36 hours latency
    - **Account required** - not fully open data

!!! tip "Best Practices"
    - **Use for weeks 2-6** - beyond HRES range
    - **Consider ensemble spread** - uncertainty increases with lead time
    - **Combine with HRES** - HRES for week 1, S2S for weeks 2+
    - **Validate locally** - skill varies by region and season
    - **Weekly updates** - download new forecasts regularly
    - **Probabilistic approach** - don't rely on single forecast

---

## 📖 Additional Resources

### Official Documentation

- **S2S Database:** [https://apps.ecmwf.int/datasets/data/s2s/](https://apps.ecmwf.int/datasets/data/s2s/)
- **S2S Project:** [https://s2sprediction.net/](https://s2sprediction.net/)
- **MARS Documentation:** [https://confluence.ecmwf.int/display/UDOC/MARS](https://confluence.ecmwf.int/display/UDOC/MARS)
- **API Documentation:** [https://www.ecmwf.int/en/computing/software/ecmwf-web-api](https://www.ecmwf.int/en/computing/software/ecmwf-web-api)

### Python Libraries

- **ecmwf-api-client:** [https://pypi.org/project/ecmwf-api-client/](https://pypi.org/project/ecmwf-api-client/)
- **xarray:** [https://xarray.pydata.org/](https://xarray.pydata.org/)

### Related Forecasts

| Source | Range | Resolution | Update | Access |
|--------|-------|------------|--------|--------|
| **ECMWF HRES** | 10 days | 0.25° | Daily | Open Data |
| **ECMWF S2S** | 46 days | 1.5° | Mon/Thu | MARS API |
| **ECMWF SEAS5** | 7 months | 1° | Monthly | CDS |
| **GFS** | 16 days | 0.25° | 4× daily | NOMADS |
| **CFSv2** | 9 months | 1° | Daily | NOMADS |

---

## 🚀 Next Steps

<div class="grid cards" markdown>

-   :material-chart-line: **Analyze S2S Forecasts**
    
    ---
    
    Calculate weekly/monthly anomalies  
    Compare with climatology  
    
    → [Xarray Tutorial](../../day3/06-Xarray_for_Climate_and_Meteorology_Workshop.md)

-   :material-map: **Visualize Extended Forecasts**
    
    ---
    
    Create weekly forecast maps  
    Plot probability distributions  
    
    → [Matplotlib Tutorial](../../day3/05-Matplotlib_for_Climate_and_Meteorology_Workshop.md)

-   :material-weather-cloudy: **Combine with HRES**
    
    ---
    
    HRES for week 1, S2S for weeks 2+  
    Seamless forecast products  
    
    → [ECMWF HRES Precipitation](15-download_ecmwf_hres_precip.md)

-   :material-bug: **VECTRI Early Warning**
    
    ---
    
    Extended-range malaria risk  
    2-6 week outbreak prediction  
    
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

<div style="background: linear-gradient(135deg, #5c6bc0 0%, #3949ab 100%); color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
  <h3 style="margin: 0 0 1rem 0;">🌧️ Ready for Extended-Range Forecasting!</h3>
  <p style="margin: 0; opacity: 0.95;">You now have everything you need to download ECMWF S2S precipitation forecasts for sub-seasonal to seasonal prediction and early warning applications.</p>
</div>
