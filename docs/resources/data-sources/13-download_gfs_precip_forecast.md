# 📥 Downloading NCEP GFS Forecast Data

## Overview

**NCEP GFS (Global Forecast System)** provides global weather forecasts up to 16 days ahead. This tutorial guides you through downloading, processing, and converting GFS 0.25° accumulated precipitation (APCP) data into daily totals using a Python script.

<div class="grid cards" markdown>

-   :material-weather-cloudy: **Dataset**
    
    ---
    
    NCEP GFS 0.25° Precipitation Forecast
    
    **Coverage:** Global  
    **Resolution:** 0.25° (~28 km)  
    **Temporal:** 3-hourly → Daily  
    **Forecast Range:** 1–16 days

-   :material-earth: **Spatial Coverage**
    
    ---
    
    **Region:** Global  
    **Latitude:** 90°S to 90°N  
    **Longitude:** 0° to 360° (or -180° to 180°)

-   :material-update: **Update Frequency**
    
    ---
    
    **Cycles:** 00Z, 06Z, 12Z, 18Z (4× daily)  
    **Latency:** ~4-6 hours after init time  
    **Retention:** ~10 days on NOMADS

-   :material-file-download: **Access**
    
    ---
    
    **Source:** NOAA NOMADS  
    **Method:** GRIB Filter API  
    **Authentication:** Not required

</div>

---

## 🎯 What This Script Does

```mermaid
graph LR
    A[Select Init Date & Cycle] --> B[Build NOMADS URLs]
    B --> C[Download 3-hourly GRIB2]
    C --> D[Extract APCP Variable]
    D --> E[Sum to Daily Totals]
    E --> F[Clip to Region]
    F --> G[Save NetCDF]
    
    style A fill:#e3f2fd
    style G fill:#c8e6c9
```

The script performs the following operations:

1. **Downloads** 3-hourly APCP (accumulated precipitation) GRIB2 files
2. **Extracts** precipitation data using cfgrib
3. **Computes** 24-hour daily totals by summing 3-hourly values
4. **Clips** data to your specified bounding box
5. **Saves** the result as a compressed NetCDF file

---

## 🚀 Quick Start Guide

### Prerequisites

!!! info "Required Python Packages"
    ```bash
    pip install requests xarray cfgrib netCDF4 numpy
    ```
    
    !!! warning "cfgrib Requirement"
        The `cfgrib` package requires the **ecCodes** library. Install it via:
        
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
            conda install -c conda-forge cfgrib eccodes
            ```

### Basic Usage

=== "10-Day Forecast"
    ```bash
    python download_gfs.py \
        --outdir data/gfs_forecast \
        --outfile gfs_ethiopia_10day.nc \
        --ndays 10 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --date 2025-01-15 \
        --cycle 0
    ```

=== "Today's Forecast"
    ```bash
    python download_gfs.py \
        --outdir data/gfs_today \
        --outfile gfs_ethiopia_today.nc \
        --ndays 7 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --cycle 0
    ```

=== "Full 16-Day Forecast"
    ```bash
    python download_gfs.py \
        --outdir data/gfs_extended \
        --outfile gfs_ethiopia_16day.nc \
        --ndays 16 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --cycle 0
    ```

---

## 📋 The Complete Script

### Python Download Script

Save this as `download_gfs.py`:

```python
#!/usr/bin/env python
"""
Download NCEP GFS 0.25° accumulated precipitation (APCP),
compute 1–N-day daily totals, clip to a bounding box,
and save as a single NetCDF file with dims (time, lat, lon).

For GFS 0.25° on NOMADS:
- APCP is precipitation accumulated over the *previous interval* (3h),
  not from t0. So we SUM all 3-hourly APCP fields within each 24-h window
  instead of differencing them.

Example
-------
python download_gfs_apcp_daily.py \
    --outdir data/gfs_apcp \
    --outfile gfs_apcp_ea_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --date 2025-11-30 \
    --cycle 0
"""

import argparse
import datetime as dt
from pathlib import Path
from typing import Dict, List

import numpy as np
import requests
import xarray as xr
from urllib.parse import urlencode

NOMADS_BASE = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"


# --------------------------------------------------------------------------
# Utilities
# --------------------------------------------------------------------------
def log(msg: str) -> None:
    print(f"[info] {msg}")


def build_gfs_url(
    init_date: dt.date,
    cycle: int,
    fhour: int,
    lon_min: float,
    lon_max: float,
    lat_min: float,
    lat_max: float,
) -> str:
    """
    Build NOMADS GRIB-filter URL for GFS 0.25° APCP at a given forecast hour.
    """
    date_str = init_date.strftime("%Y%m%d")
    file_name = f"gfs.t{cycle:02d}z.pgrb2.0p25.f{fhour:03d}"
    dir_path = f"/gfs.{date_str}/{cycle:02d}/atmos"

    params = {
        "file": file_name,
        "lev_surface": "on",
        "var_APCP": "on",
        # spatial subset
        "subregion": "",
        "leftlon": str(lon_min),
        "rightlon": str(lon_max),
        "toplat": str(lat_max),
        "bottomlat": str(lat_min),
        "dir": dir_path,
    }

    return NOMADS_BASE + "?" + urlencode(params)


def download_grib(url: str, out_path: Path, max_retries: int = 10) -> None:
    """
    Download a single GRIB2 file with simple retry logic.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, max_retries + 1):
        try:
            with requests.get(url, stream=True, timeout=60) as r:
                if r.status_code == 429:
                    # Too many requests → small backoff
                    wait = min(60 * attempt, 300)
                    log(
                        f"HTTP 429 from NOMADS (attempt {attempt}/{max_retries}), "
                        f"sleeping {wait} s..."
                    )
                    import time

                    time.sleep(wait)
                    continue

                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            return
        except Exception as exc:  # noqa: BLE001
            if attempt == max_retries:
                raise RuntimeError(
                    f"Failed to download {url} after {max_retries} attempts"
                ) from exc
            wait = min(30 * attempt, 180)
            log(
                f"Error downloading {url} (attempt {attempt}/{max_retries}): "
                f"{exc}. Retrying in {wait} s..."
            )
            import time

            time.sleep(wait)


def open_apcp_from_grib(grib_path: Path) -> xr.DataArray:
    """
    Open a GFS APCP GRIB2 file and return a DataArray (lat, lon)
    in units of mm (kg m-2) for the 3-hour accumulation period.
    """
    backend_kwargs = {"indexpath": ""}

    # Try to restrict to accumulated fields; fall back to generic open
    try:
        ds = xr.open_dataset(
            grib_path,
            engine="cfgrib",
            backend_kwargs={
                **backend_kwargs,
                "filter_by_keys": {"stepType": "accum"},
            },
        )
    except Exception:
        ds = xr.open_dataset(grib_path, engine="cfgrib", backend_kwargs=backend_kwargs)

    if not ds.data_vars:
        raise RuntimeError(f"No data variables found in {grib_path}")

    # Pick the most likely precip variable
    var_name = None
    for name in ds.data_vars:
        lower = name.lower()
        attrs = ds[name].attrs
        long = (attrs.get("long_name", "") + attrs.get("name", "")).lower()
        if any(k in lower for k in ("apcp", "tp", "pr", "precip")) or "precip" in long:
            var_name = name
            break

    if var_name is None:
        var_name = list(ds.data_vars)[0]

    da = ds[var_name]

    # Unify coordinate names
    if "latitude" in da.dims:
        da = da.rename({"latitude": "lat"})
    if "longitude" in da.dims:
        da = da.rename({"longitude": "lon"})

    # Drop any singleton time/step dimension (one forecast hour per file)
    for dim in list(da.dims):
        if dim not in ("lat", "lon") and da.sizes[dim] == 1:
            da = da.isel({dim: 0}, drop=True)

    # Ensure lat ascending (south→north)
    if da.lat.size > 1 and float(da.lat[0]) > float(da.lat[-1]):
        da = da.sortby("lat")

    # Drop stray surface coord if present
    if "surface" in da.coords:
        da = da.reset_coords("surface", drop=True)

    da.name = "apcp"
    return da


def compute_daily_totals_from_accum(
    acc_by_hour: Dict[int, xr.DataArray],
    init_datetime: dt.datetime,
    ndays: int,
) -> xr.DataArray:
    """
    Convert 3-hourly APCP fields (mm over the last 3h) into
    24-hour totals (mm/day) by summing 3-hourly values.

    For a 00Z run:
      Day 1 (time = init+24h): sum hours 3, 6, ..., 24
      Day 2 (time = init+48h): sum hours 27, 30, ..., 48
      ...
    """
    hours = sorted(acc_by_hour.keys())

    # Basic consistency check
    if not hours or hours[0] != 3:
        raise RuntimeError(f"Expected first APCP hour to be 3, got {hours[0] if hours else 'none'}")
    if hours[-1] < 24 * ndays:
        raise RuntimeError(
            f"Need APCP up to at least hour {24*ndays}, got max hour {hours[-1]}"
        )

    daily_list: List[xr.DataArray] = []
    time_coords: List[dt.datetime] = []

    for day in range(1, ndays + 1):
        start = 24 * (day - 1)    # start of day window (in hours)
        end = 24 * day            # end of day window

        # 3-hourly forecast hours strictly inside (start, end]
        hs = [h for h in hours if (start < h <= end)]

        if not hs:
            raise RuntimeError(f"No APCP hours found for day {day}: start={start}, end={end}")

        # Sum 3-hourly APCP to get 24-h total (mm)
        stack = xr.concat([acc_by_hour[h] for h in hs], dim="step")
        daily = stack.sum(dim="step")

        # Attributes
        daily = daily.copy()
        daily.attrs["units"] = "mm/day"
        daily.attrs["long_name"] = "GFS daily total precipitation"
        daily.attrs["description"] = (
            "24-hour total precipitation computed by summing 3-hourly APCP "
            f"over ({start}h, {end}h]."
        )

        valid_time = init_datetime + dt.timedelta(hours=end)
        daily = daily.expand_dims(time=[np.datetime64(valid_time)])
        daily_list.append(daily)
        time_coords.append(valid_time)

    tp = xr.concat(daily_list, dim="time")
    tp.name = "tp"
    tp.coords["time"] = np.array(time_coords, dtype="datetime64[ns]")
    tp.attrs["units"] = "mm/day"
    tp.attrs["long_name"] = "GFS daily total precipitation"

    # Clip tiny negatives caused by numerical issues
    tp = tp.clip(min=0)

    return tp


def process_to_netcdf(
    out_nc: Path,
    init_date: dt.date,
    cycle: int,
    ndays: int,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
) -> None:
    """
    Main workflow: download GFS APCP 3-hourly fields needed for ndays,
    compute daily totals, and save to NetCDF.
    """
    if ndays < 1 or ndays > 16:
        raise ValueError("ndays must be between 1 and 16 for GFS.")

    max_fhour = 24 * ndays
    if max_fhour > 384:
        raise ValueError("Maximum forecast hour must be <= 384 for GFS.")

    init_dt = dt.datetime.combine(init_date, dt.time(cycle))
    log(f"GFS init time (UTC): {init_dt.isoformat()}")

    # 3, 6, 9, ..., 24*ndays
    fhours = list(range(3, max_fhour + 1, 3))
    acc: Dict[int, xr.DataArray] = {}

    for fh in fhours:
        url = build_gfs_url(
            init_date=init_date,
            cycle=cycle,
            fhour=fh,
            lon_min=lon_min,
            lon_max=lon_max,
            lat_min=lat_min,
            lat_max=lat_max,
        )
        grib_name = f"gfs_apcp_f{fh:03d}.grib2"
        grib_path = out_nc.parent / grib_name

        log(f"Downloading APCP fhour={fh:03d} → {grib_name}")
        download_grib(url, grib_path)

        log(f"Opening {grib_name} with xarray/cfgrib...")
        da = open_apcp_from_grib(grib_path)
        acc[fh] = da

    log("Computing daily totals from 3-hourly APCP...")
    tp = compute_daily_totals_from_accum(acc, init_dt, ndays)

    # Build final Dataset
    ds_out = xr.Dataset({"tp": tp})
    ds_out.attrs["title"] = "NCEP GFS 0.25° daily total precipitation (mm/day)"
    ds_out.attrs["source"] = "NCEP GFS 0.25-degree (APCP from NOMADS filter_gfs_0p25)"
    ds_out.attrs["history"] = (
        f"Created on {dt.datetime.utcnow().isoformat()}Z by download_gfs_apcp_daily.py; "
        "daily 24h totals computed by summing 3-hourly APCP."
    )
    ds_out.attrs["forecast_reference_time"] = init_dt.isoformat()

    # Conservative chunking; ensure chunk dims ≤ data dims
    ntime = ds_out.dims["time"]
    nlat = ds_out.dims["lat"]
    nlon = ds_out.dims["lon"]

    encoding = {
        "tp": {
            "zlib": True,
            "complevel": 4,
            "dtype": "float32",
            "chunksizes": (
                min(ntime, 1),
                min(nlat, 200),
                min(nlon, 200),
            ),
        }
    }

    log(f"Writing NetCDF → {out_nc}")
    out_nc.parent.mkdir(parents=True, exist_ok=True)
    ds_out.to_netcdf(out_nc, encoding=encoding)
    log("Done.")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download NCEP GFS 0.25° APCP, compute daily totals (mm/day), "
            "clip to a region, and save NetCDF."
        )
    )

    parser.add_argument(
        "--outdir",
        type=str,
        required=True,
        help="Output directory for NetCDF + temporary GRIB2 files.",
    )
    parser.add_argument(
        "--outfile",
        type=str,
        required=True,
        help="Name of the output NetCDF file (relative to outdir).",
    )
    parser.add_argument(
        "--ndays",
        type=int,
        default=10,
        help="Number of forecast days (1–16).",
    )

    parser.add_argument("--lat-min", type=float, required=True)
    parser.add_argument("--lat-max", type=float, required=True)
    parser.add_argument("--lon-min", type=float, required=True)
    parser.add_argument("--lon-max", type=float, required=True)

    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Initial date YYYY-MM-DD for the GFS run (UTC). "
        "If omitted, uses today's UTC date.",
    )
    parser.add_argument(
        "--cycle",
        type=int,
        default=0,
        choices=[0, 6, 12, 18],
        help="GFS cycle hour (0, 6, 12, or 18 UTC).",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.date:
        init_date = dt.datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        init_date = dt.datetime.utcnow().date()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    out_nc = outdir / args.outfile

    process_to_netcdf(
        out_nc=out_nc,
        init_date=init_date,
        cycle=args.cycle,
        ndays=args.ndays,
        lat_min=args.lat_min,
        lat_max=args.lat_max,
        lon_min=args.lon_min,
        lon_max=args.lon_max,
    )


if __name__ == "__main__":
    main()
```

---

## 🔧 Command-Line Arguments

### Required Arguments

| Argument | Type | Description | Example |
|----------|------|-------------|---------|
| `--outdir` | String | Output directory path | `data/gfs_forecast` |
| `--outfile` | String | Output NetCDF filename | `gfs_ethiopia_10day.nc` |
| `--lat-min` | Float | Minimum latitude (south) | `3` |
| `--lat-max` | Float | Maximum latitude (north) | `15` |
| `--lon-min` | Float | Minimum longitude (west) | `33` |
| `--lon-max` | Float | Maximum longitude (east) | `48` |

### Optional Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `--ndays` | Integer | Forecast days (1–16) | `10` |
| `--date` | Date (YYYY-MM-DD) | GFS initialization date | Today (UTC) |
| `--cycle` | Integer | Model cycle (0, 6, 12, 18) | `0` |

---

## ⏰ Understanding GFS Cycles

GFS runs **4 times daily** at specific UTC hours:

| Cycle | Init Time (UTC) | Typical Availability | Best For |
|-------|-----------------|---------------------|----------|
| **00Z** | 00:00 UTC | ~04:00 UTC | Overnight forecasts |
| **06Z** | 06:00 UTC | ~10:00 UTC | Morning updates |
| **12Z** | 12:00 UTC | ~16:00 UTC | Afternoon forecasts |
| **18Z** | 18:00 UTC | ~22:00 UTC | Evening updates |

!!! tip "Choosing the Right Cycle"
    - **00Z cycle** is typically the most stable and widely used
    - Allow **4-6 hours** after cycle time for data availability
    - For operational use, check NOMADS status before running

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

=== "Global"
    ```bash
    --lat-min -90 --lat-max 90 --lon-min -180 --lon-max 180
    ```
    **Coverage:** Entire globe (large download!)

---

## 💡 Usage Examples

### Example 1: 10-Day Forecast for Ethiopia

```bash
python download_gfs.py \
    --outdir data/gfs_eth \
    --outfile gfs_ethiopia_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --date 2025-01-15 \
    --cycle 0
```

**What it does:**

- Downloads 80 GRIB2 files (3-hourly for 10 days)
- Extracts APCP variable for Ethiopia
- Computes 10 daily precipitation totals
- Saves as single NetCDF (~5-10 MB)

---

### Example 2: Today's 7-Day Forecast (Automatic Date)

```bash
python download_gfs.py \
    --outdir data/gfs_today \
    --outfile gfs_eth_7day.nc \
    --ndays 7 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --cycle 0
```

**What it does:**

- Uses today's date automatically
- Downloads 7 days of forecast data
- Ideal for daily operational forecasting

---

### Example 3: Extended 16-Day Forecast

```bash
python download_gfs.py \
    --outdir data/gfs_extended \
    --outfile gfs_eth_16day.nc \
    --ndays 16 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --date 2025-01-15 \
    --cycle 0
```

**What it does:**

- Downloads maximum forecast range (16 days)
- 128 GRIB2 files processed
- Useful for medium-range planning

!!! warning "Extended Forecasts"
    Forecast skill decreases significantly after day 7-10. Use extended forecasts with appropriate caution.

---

### Example 4: Afternoon Cycle (12Z)

```bash
python download_gfs.py \
    --outdir data/gfs_12z \
    --outfile gfs_eth_12z_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --date 2025-01-15 \
    --cycle 12
```

**What it does:**

- Uses the 12Z model cycle
- May have more recent observations assimilated
- Good for afternoon updates

---

### Example 5: Operational Daily Script

Create a script for daily automated downloads:

```bash
#!/bin/bash
# daily_gfs_download.sh

TODAY=$(date -u +%Y-%m-%d)
OUTDIR="data/gfs_operational"
OUTFILE="gfs_eth_${TODAY}.nc"

python download_gfs.py \
    --outdir "$OUTDIR" \
    --outfile "$OUTFILE" \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --cycle 0

echo "Downloaded GFS forecast for $TODAY"
```

---

## 📂 Output Directory Structure

After running the script, your output directory will contain:

```
data/gfs_forecast/
├── gfs_apcp_f003.grib2          # 3-hourly GRIB2 files (temporary)
├── gfs_apcp_f006.grib2
├── gfs_apcp_f009.grib2
├── ...
├── gfs_apcp_f240.grib2          # Last file for 10-day forecast
└── gfs_ethiopia_10day.nc        # Final merged NetCDF
```

!!! tip "Cleaning Up GRIB Files"
    The intermediate GRIB2 files can be deleted after the NetCDF is created:
    ```bash
    rm data/gfs_forecast/*.grib2
    ```

---

## 🔍 Verifying Your Download

After downloading, verify your data using Python:

```python
import xarray as xr
import matplotlib.pyplot as plt

# Open the forecast file
ds = xr.open_dataset('data/gfs_forecast/gfs_ethiopia_10day.nc')

# Display dataset information
print(ds)

# Check dimensions
print(f"Forecast days: {len(ds.time)}")
print(f"Latitude range: {float(ds.lat.min()):.2f} to {float(ds.lat.max()):.2f}")
print(f"Longitude range: {float(ds.lon.min()):.2f} to {float(ds.lon.max()):.2f}")

# Check forecast reference time
print(f"Forecast init: {ds.attrs.get('forecast_reference_time', 'N/A')}")

# Plot Day 1 forecast
fig, ax = plt.subplots(figsize=(10, 8))
ds.tp.isel(time=0).plot(ax=ax, cmap='Blues', vmin=0, vmax=50)
ax.set_title(f"GFS Day 1 Precipitation Forecast\n{ds.time.values[0]}")
plt.savefig('gfs_day1_forecast.png', dpi=150, bbox_inches='tight')
plt.show()

# Plot time series for a point
lat_point, lon_point = 9.0, 38.7  # Addis Ababa
point_data = ds.tp.sel(lat=lat_point, lon=lon_point, method='nearest')
point_data.plot(marker='o', figsize=(10, 4))
plt.title(f'10-Day Precipitation Forecast for ({lat_point}°N, {lon_point}°E)')
plt.ylabel('Precipitation (mm/day)')
plt.grid(True, alpha=0.3)
plt.savefig('gfs_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## 📊 Understanding GFS APCP Data

### How APCP Works

GFS provides **APCP (Accumulated Precipitation)** as 3-hourly accumulations:

```
Hour 0   → Hour 3:   APCP at f003 = precipitation from 0-3h
Hour 3   → Hour 6:   APCP at f006 = precipitation from 3-6h
Hour 6   → Hour 9:   APCP at f009 = precipitation from 6-9h
...
```

### Daily Total Calculation

The script sums 3-hourly values to compute 24-hour totals:

```
Day 1 Total = APCP(f003) + APCP(f006) + ... + APCP(f024)
Day 2 Total = APCP(f027) + APCP(f030) + ... + APCP(f048)
...
```

### Output Variable

| Variable | Description | Units |
|----------|-------------|-------|
| `tp` | Total precipitation (24-hour) | mm/day |

### Coordinates

| Coordinate | Description |
|------------|-------------|
| `time` | Valid time (end of 24h period) |
| `lat` | Latitude (degrees north) |
| `lon` | Longitude (degrees east) |

---

## ⚠️ Troubleshooting

### Common Issues and Solutions

=== "HTTP 429 (Too Many Requests)"

    **Problem:** NOMADS rate limiting
    
    ```
    [info] HTTP 429 from NOMADS (attempt 1/10), sleeping 60 s...
    ```
    
    **Solutions:**
    
    1. **Wait and retry:** The script handles this automatically
    2. **Reduce request frequency:** Add delays between downloads
    3. **Try off-peak hours:** Early morning UTC is less busy
    4. **Use smaller regions:** Reduce spatial extent

=== "cfgrib Import Error"

    **Problem:** ecCodes library not installed
    
    ```
    ImportError: Cannot find the ecCodes library
    ```
    
    **Solutions:**
    
    1. **Install ecCodes:**
        ```bash
        # Ubuntu/Debian
        sudo apt-get install libeccodes-dev
        
        # macOS
        brew install eccodes
        
        # Conda (recommended)
        conda install -c conda-forge cfgrib eccodes
        ```

=== "Data Not Available"

    **Problem:** Requested date/cycle not on NOMADS
    
    ```
    HTTPError: 404 Client Error: Not Found
    ```
    
    **Solutions:**
    
    1. **Check data retention:** NOMADS keeps ~10 days of data
    2. **Wait for availability:** Allow 4-6 hours after cycle time
    3. **Verify date format:** Use YYYY-MM-DD
    4. **Check NOMADS status:** [NOMADS Status Page](https://nomads.ncep.noaa.gov/)

=== "Empty GRIB Files"

    **Problem:** No data variables found
    
    ```
    RuntimeError: No data variables found in gfs_apcp_f003.grib2
    ```
    
    **Solutions:**
    
    1. **Re-download the file:** May be corrupted
    2. **Check bounding box:** Ensure coordinates are valid
    3. **Verify file size:** Should be >10 KB typically
    4. **Inspect with grib_ls:**
        ```bash
        grib_ls gfs_apcp_f003.grib2
        ```

=== "Memory Issues"

    **Problem:** Out of memory for large regions/long forecasts
    
    **Solutions:**
    
    1. **Reduce spatial extent:** Use smaller bounding box
    2. **Reduce forecast days:** Start with fewer days
    3. **Process in chunks:** Download and merge separately
    4. **Use Dask:** Enable parallel processing

---

## 🌐 NOMADS Data Access

### Understanding the GRIB Filter

The script uses the NOMADS GRIB Filter to download only the needed data:

```
https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?
    file=gfs.t00z.pgrb2.0p25.f003          # Specific file
    &lev_surface=on                         # Surface level
    &var_APCP=on                            # APCP variable only
    &subregion=                             # Enable subsetting
    &leftlon=33&rightlon=48                 # Longitude bounds
    &toplat=15&bottomlat=3                  # Latitude bounds
    &dir=/gfs.20250115/00/atmos             # Directory path
```

### Benefits of GRIB Filter

- ✅ **Faster downloads** - Only transfers needed data
- ✅ **Lower bandwidth** - Subset before download
- ✅ **Variable selection** - Only APCP, not all variables
- ✅ **Spatial subsetting** - Only your region

---

## 🎓 Data Quality Notes

!!! success "Strengths"
    - **High temporal frequency** (4 cycles daily)
    - **Global coverage** at 0.25° resolution
    - **Extended forecast range** (up to 16 days)
    - **Operational model** - constantly improved
    - **Free and open access** via NOMADS

!!! warning "Limitations"
    - **Forecast skill degrades** after day 7-10
    - **Limited data retention** (~10 days on NOMADS)
    - **Model biases** vary by region and season
    - **Precipitation forecasts** have higher uncertainty
    - **Rate limiting** during high traffic periods

!!! tip "Best Practices"
    - **Validate against observations** when possible
    - **Use ensemble products** for uncertainty estimation
    - **Consider bias correction** for your region
    - **Archive forecasts** for verification studies
    - **Compare multiple cycles** for consistency

---

## 📖 Additional Resources

### Official Documentation

- **NCEP GFS:** [https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gfs.php](https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gfs.php)
- **NOMADS:** [https://nomads.ncep.noaa.gov/](https://nomads.ncep.noaa.gov/)
- **GFS Product Guide:** [GFS Documentation](https://www.nco.ncep.noaa.gov/pmb/products/gfs/)

### Python Libraries

- **xarray:** [https://xarray.pydata.org/](https://xarray.pydata.org/)
- **cfgrib:** [https://github.com/ecmwf/cfgrib](https://github.com/ecmwf/cfgrib)
- **ecCodes:** [https://confluence.ecmwf.int/display/ECC](https://confluence.ecmwf.int/display/ECC)

### Alternative Forecast Sources

| Source | Coverage | Resolution | Range | Access |
|--------|----------|------------|-------|--------|
| **ECMWF HRES** | Global | 0.1° | 10 days | CDS (registration) |
| **GFS Ensemble** | Global | 0.5° | 16 days | NOMADS |
| **NAM** | North America | 12 km | 3.5 days | NOMADS |
| **ICON** | Global | 13 km | 7 days | DWD OpenData |

---

## 🚀 Next Steps

<div class="grid cards" markdown>

-   :material-chart-line: **Analyze Forecasts**
    
    ---
    
    Compare forecasts with observations  
    Calculate skill scores and biases  
    
    → [Xarray Tutorial](../../day3/06-Xarray_for_Climate_and_Meteorology_Workshop.md)

-   :material-map: **Visualize Forecasts**
    
    ---
    
    Create forecast maps with Cartopy  
    Time series and ensemble plots  
    
    → [Matplotlib Tutorial](../../day3/05-Matplotlib_for_Climate_and_Meteorology_Workshop.md)

-   :material-vector-combine: **Combine with Observations**
    
    ---
    
    Merge GFS with CHIRPS/TAMSAT  
    Create blended products  
    
    → [CHIRPS Download](10-download_chirps.md)

-   :material-bug: **VECTRI Integration**
    
    ---
    
    Use forecasts for malaria modeling  
    Prepare inputs for VECTRI  
    
    → [VECTRI Model](../../day1/vectri_model_components_larvae_to_hydrology.md)

</div>

---

!!! example "Need Help?"
    If you encounter issues or have questions:
    
    - Check the [Troubleshooting](#troubleshooting) section
    - Review [NOMADS documentation](https://nomads.ncep.noaa.gov/)
    - Check [NCEP status page](https://www.nco.ncep.noaa.gov/status/messages/)
    - Contact workshop instructors

---

<div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
  <h3 style="margin: 0 0 1rem 0;">🌦️ Ready for Forecasting!</h3>
  <p style="margin: 0; opacity: 0.95;">You now have everything you need to download and process NCEP GFS precipitation forecasts for your climate and malaria modeling applications.</p>
</div>
