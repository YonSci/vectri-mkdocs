# 🌡️ Downloading NCEP GFS Temperature Forecasts

## Overview

**NCEP GFS (Global Forecast System)** provides global weather forecasts including 2-meter air temperature. This tutorial guides you through downloading, processing, and converting GFS 0.25° temperature data into daily mean values using a Python script.

<div class="grid cards" markdown>

-   :material-thermometer: **Dataset**
    
    ---
    
    NCEP GFS 0.25° 2m Temperature Forecast
    
    **Variable:** TMP at 2m above ground  
    **Resolution:** 0.25° (~28 km)  
    **Output:** Daily mean temperature  
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
    C --> D[Extract T2m Variable]
    D --> E[Average to Daily Means]
    E --> F[Convert K → °C]
    F --> G[Save NetCDF]
    
    style A fill:#fff3e0
    style G fill:#c8e6c9
```

The script performs the following operations:

1. **Downloads** 3-hourly instantaneous 2m temperature GRIB2 files
2. **Extracts** temperature data using cfgrib
3. **Computes** 24-hour daily means by averaging 3-hourly values
4. **Converts** from Kelvin to Celsius (optional)
5. **Clips** data to your specified bounding box
6. **Saves** the result as a compressed NetCDF file

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

=== "10-Day Forecast (°C)"
    ```bash
    python download_gfs_temp.py \
        --outdir data/gfs_temp \
        --outfile gfs_temp_ethiopia_10day.nc \
        --ndays 10 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --date 2025-01-15 \
        --cycle 0
    ```

=== "Today's Forecast"
    ```bash
    python download_gfs_temp.py \
        --outdir data/gfs_temp_today \
        --outfile gfs_temp_ethiopia_today.nc \
        --ndays 7 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --cycle 0
    ```

=== "Keep Kelvin Units"
    ```bash
    python download_gfs_temp.py \
        --outdir data/gfs_temp \
        --outfile gfs_temp_ethiopia_K.nc \
        --ndays 10 \
        --lat-min 3 --lat-max 15 \
        --lon-min 33 --lon-max 48 \
        --keep-kelvin
    ```

---

## 📋 The Complete Script

### Python Download Script

Save this as `download_gfs_temp.py`:

```python
#!/usr/bin/env python
"""
Download NCEP GFS 0.25° 2-meter temperature (TMP at 2 m AGL),
compute 1–N-day daily mean temperature from 3-hourly instantaneous fields,
clip to a bounding box, and save as a single NetCDF file
with dims (time, lat, lon).

Notes
-----
For GFS 0.25° on NOMADS:
- 2m temperature is an *instantaneous* forecast field.
- To derive daily means, we AVERAGE the 3-hourly values within each 24-h window.

Daily window convention used here:
- Day 1 (time = init + 24h): average hours [0, 3, 6, ..., 24] if 0 is available,
  otherwise average (3, 6, ..., 24).
- Day 2 (time = init + 48h): average hours (24, 48] i.e., 27, 30, ..., 48
- ...
This avoids double-counting the boundary hour across days.

Example
-------
python download_gfs_t2m_daily.py \
    --outdir data/gfs_t2m \
    --outfile gfs_t2m_ea_10day.nc \
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


def build_gfs_url_t2m(
    init_date: dt.date,
    cycle: int,
    fhour: int,
    lon_min: float,
    lon_max: float,
    lat_min: float,
    lat_max: float,
) -> str:
    """
    Build NOMADS GRIB-filter URL for GFS 0.25° 2m temperature at a given forecast hour.
    """
    date_str = init_date.strftime("%Y%m%d")
    file_name = f"gfs.t{cycle:02d}z.pgrb2.0p25.f{fhour:03d}"
    dir_path = f"/gfs.{date_str}/{cycle:02d}/atmos"

    params = {
        "file": file_name,
        # 2m temperature level + variable
        "lev_2_m_above_ground": "on",
        "var_TMP": "on",
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


def open_t2m_from_grib(grib_path: Path) -> xr.DataArray:
    """
    Open a GFS 2m temperature GRIB2 file and return a DataArray (lat, lon).

    Tries to filter to 2m heightAboveGround first; falls back to generic open.
    """
    backend_kwargs = {"indexpath": ""}

    try:
        ds = xr.open_dataset(
            grib_path,
            engine="cfgrib",
            backend_kwargs={
                **backend_kwargs,
                "filter_by_keys": {"typeOfLevel": "heightAboveGround", "level": 2},
            },
        )
    except Exception:
        ds = xr.open_dataset(grib_path, engine="cfgrib", backend_kwargs=backend_kwargs)

    if not ds.data_vars:
        raise RuntimeError(f"No data variables found in {grib_path}")

    # Try to pick the most likely 2m temperature variable
    var_name = None
    for name in ds.data_vars:
        lower = name.lower()
        attrs = ds[name].attrs
        long = (attrs.get("long_name", "") + " " + attrs.get("name", "")).lower()
        if any(k in lower for k in ("t2m", "tmp", "2t", "temperature")) and (
            "2 m" in long or "2m" in long or "above ground" in long or "height" in long or True
        ):
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

    # Drop any singleton time/step/valid_time dimension
    for dim in list(da.dims):
        if dim not in ("lat", "lon") and da.sizes.get(dim, 0) == 1:
            da = da.isel({dim: 0}, drop=True)

    # Ensure lat ascending (south→north)
    if da.lat.size > 1 and float(da.lat[0]) > float(da.lat[-1]):
        da = da.sortby("lat")

    # Drop stray surface or height coords if present
    for c in ("surface", "heightAboveGround"):
        if c in da.coords:
            da = da.reset_coords(c, drop=True)

    da.name = "t2m"
    return da


def compute_daily_means_from_inst(
    inst_by_hour: Dict[int, xr.DataArray],
    init_datetime: dt.datetime,
    ndays: int,
    to_celsius: bool = True,
) -> xr.DataArray:
    """
    Convert 3-hourly instantaneous 2m temperature into daily means.

    Convention:
    - Day 1 uses [0, 3, ..., 24] if hour 0 exists
    - Days 2..N use hours in (start, end] to avoid double counting boundaries.
    """
    hours = sorted(inst_by_hour.keys())

    if not hours:
        raise RuntimeError("No forecast hours provided for temperature.")

    if hours[-1] < 24 * ndays:
        raise RuntimeError(
            f"Need temperature up to at least hour {24*ndays}, got max hour {hours[-1]}"
        )

    daily_list: List[xr.DataArray] = []
    time_coords: List[dt.datetime] = []

    for day in range(1, ndays + 1):
        start = 24 * (day - 1)
        end = 24 * day

        if day == 1:
            # Prefer including 0 if available
            hs = [h for h in hours if (0 <= h <= end)]
        else:
            hs = [h for h in hours if (start < h <= end)]

        # Keep only 3-hourly steps (defensive)
        hs = sorted([h for h in hs if h % 3 == 0])

        if not hs:
            raise RuntimeError(f"No temperature hours found for day {day}")

        stack = xr.concat([inst_by_hour[h] for h in hs], dim="step")
        daily = stack.mean(dim="step")

        # Unit handling
        daily = daily.copy()
        src_units = (daily.attrs.get("units") or "").lower()

        # GFS TMP is typically Kelvin
        if to_celsius:
            # If units look like K or empty, assume Kelvin
            if "k" in src_units or src_units == "":
                daily = daily - 273.15
            daily.attrs["units"] = "degC"
            daily.attrs["long_name"] = "GFS daily mean 2m air temperature"
        else:
            daily.attrs["units"] = "K"
            daily.attrs["long_name"] = "GFS daily mean 2m air temperature"

        daily.attrs["description"] = (
            "24-hour mean 2m temperature computed by averaging 3-hourly "
            f"instantaneous GFS TMP within the day window."
        )

        valid_time = init_datetime + dt.timedelta(hours=end)
        daily = daily.expand_dims(time=[np.datetime64(valid_time)])
        daily_list.append(daily)
        time_coords.append(valid_time)

    t2m = xr.concat(daily_list, dim="time")
    t2m.name = "t2m"
    t2m.coords["time"] = np.array(time_coords, dtype="datetime64[ns]")

    return t2m


def process_to_netcdf(
    out_nc: Path,
    init_date: dt.date,
    cycle: int,
    ndays: int,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    to_celsius: bool = True,
) -> None:
    """
    Main workflow: download GFS 2m temperature 3-hourly fields needed for ndays,
    compute daily means, and save to NetCDF.
    """
    if ndays < 1 or ndays > 16:
        raise ValueError("ndays must be between 1 and 16 for GFS.")

    max_fhour = 24 * ndays
    if max_fhour > 384:
        raise ValueError("Maximum forecast hour must be <= 384 for GFS.")

    init_dt = dt.datetime.combine(init_date, dt.time(cycle))
    log(f"GFS init time (UTC): {init_dt.isoformat()}")

    # 0, 3, 6, ..., 24*ndays
    fhours = list(range(0, max_fhour + 1, 3))
    inst: Dict[int, xr.DataArray] = {}

    for fh in fhours:
        url = build_gfs_url_t2m(
            init_date=init_date,
            cycle=cycle,
            fhour=fh,
            lon_min=lon_min,
            lon_max=lon_max,
            lat_min=lat_min,
            lat_max=lat_max,
        )
        grib_name = f"gfs_t2m_f{fh:03d}.grib2"
        grib_path = out_nc.parent / grib_name

        log(f"Downloading T2m fhour={fh:03d} → {grib_name}")
        download_grib(url, grib_path)

        log(f"Opening {grib_name} with xarray/cfgrib...")
        da = open_t2m_from_grib(grib_path)
        inst[fh] = da

    log("Computing daily mean temperature from 3-hourly T2m...")
    t2m = compute_daily_means_from_inst(inst, init_dt, ndays, to_celsius=to_celsius)

    # Build final Dataset
    ds_out = xr.Dataset({"t2m": t2m})
    ds_out.attrs["title"] = "NCEP GFS 0.25° daily mean 2m air temperature"
    ds_out.attrs["source"] = "NCEP GFS 0.25-degree (TMP at 2 m AGL from NOMADS filter_gfs_0p25)"
    ds_out.attrs["history"] = (
        f"Created on {dt.datetime.utcnow().isoformat()}Z by download_gfs_t2m_daily.py; "
        "daily means computed by averaging 3-hourly instantaneous 2m temperature."
    )
    ds_out.attrs["forecast_reference_time"] = init_dt.isoformat()

    # Conservative chunking
    ntime = ds_out.dims["time"]
    nlat = ds_out.dims["lat"]
    nlon = ds_out.dims["lon"]

    encoding = {
        "t2m": {
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
            "Download NCEP GFS 0.25° 2m temperature (TMP), "
            "compute daily means (degC by default), "
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

    parser.add_argument(
        "--keep-kelvin",
        action="store_true",
        help="If set, do NOT convert to Celsius; keep output in Kelvin.",
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
| `--outdir` | String | Output directory path | `data/gfs_temp` |
| `--outfile` | String | Output NetCDF filename | `gfs_temp_ethiopia_10day.nc` |
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
| `--keep-kelvin` | Flag | Keep temperature in Kelvin | False (outputs °C) |

---

## 🌡️ Understanding Temperature Data

### Instantaneous vs. Accumulated Fields

Unlike precipitation (which is accumulated), **temperature is an instantaneous field**:

| Field Type | Variable | How It Works |
|------------|----------|--------------|
| **Instantaneous** | TMP (Temperature) | Value at exact forecast time |
| **Accumulated** | APCP (Precipitation) | Sum over previous interval |

### Daily Mean Calculation

The script averages 3-hourly instantaneous values to compute daily means:

```
Day 1 Mean = mean(T2m at f000, f003, f006, ..., f024)
Day 2 Mean = mean(T2m at f027, f030, f033, ..., f048)
...
```

!!! info "Boundary Handling"
    - **Day 1** includes hour 0 (initialization time) if available
    - **Days 2+** use hours (start, end] to avoid double-counting boundary hours

### Unit Conversion

| Input (GFS) | Output (Default) | Conversion |
|-------------|------------------|------------|
| Kelvin (K) | Celsius (°C) | T(°C) = T(K) - 273.15 |

Use `--keep-kelvin` to output in Kelvin instead.

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

---

## 💡 Usage Examples

### Example 1: 10-Day Temperature Forecast for Ethiopia

```bash
python download_gfs_temp.py \
    --outdir data/gfs_temp_eth \
    --outfile gfs_temp_ethiopia_10day.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --date 2025-01-15 \
    --cycle 0
```

**What it does:**

- Downloads 81 GRIB2 files (3-hourly from f000 to f240)
- Extracts 2m temperature for Ethiopia
- Computes 10 daily mean temperatures in °C
- Saves as single NetCDF (~5-10 MB)

---

### Example 2: Today's 7-Day Forecast (Automatic Date)

```bash
python download_gfs_temp.py \
    --outdir data/gfs_temp_today \
    --outfile gfs_temp_eth_7day.nc \
    --ndays 7 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --cycle 0
```

**What it does:**

- Uses today's date automatically
- Downloads 7 days of temperature forecast
- Ideal for daily operational forecasting

---

### Example 3: Extended 16-Day Forecast

```bash
python download_gfs_temp.py \
    --outdir data/gfs_temp_extended \
    --outfile gfs_temp_eth_16day.nc \
    --ndays 16 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --date 2025-01-15 \
    --cycle 0
```

**What it does:**

- Downloads maximum forecast range (16 days)
- 129 GRIB2 files processed (f000 to f384)
- Useful for medium-range planning

!!! warning "Extended Forecasts"
    Temperature forecast skill decreases significantly after day 7-10. Use extended forecasts with appropriate caution.

---

### Example 4: Keep Temperature in Kelvin

```bash
python download_gfs_temp.py \
    --outdir data/gfs_temp_K \
    --outfile gfs_temp_eth_kelvin.nc \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --keep-kelvin
```

**What it does:**

- Outputs temperature in Kelvin (K)
- Useful for direct model input
- No unit conversion applied

---

### Example 5: Combined Precipitation and Temperature Download

Create a script to download both variables:

```bash
#!/bin/bash
# download_gfs_both.sh

TODAY=$(date -u +%Y-%m-%d)
OUTDIR="data/gfs_operational"

# Download precipitation forecast
python download_gfs_precip.py \
    --outdir "$OUTDIR" \
    --outfile "gfs_precip_eth_${TODAY}.nc" \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --cycle 0

# Download temperature forecast
python download_gfs_temp.py \
    --outdir "$OUTDIR" \
    --outfile "gfs_temp_eth_${TODAY}.nc" \
    --ndays 10 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --cycle 0

echo "Downloaded GFS forecasts for $TODAY"
```

---

### Example 6: Operational Daily Script with Cron

For automated daily downloads, create a cron job:

```bash
# Edit crontab
crontab -e

# Add this line to run at 06:00 UTC daily (after 00Z data is available)
0 6 * * * /path/to/download_gfs_both.sh >> /var/log/gfs_download.log 2>&1
```

---

## 📂 Output Directory Structure

After running the script, your output directory will contain:

```
data/gfs_temp/
├── gfs_t2m_f000.grib2           # 3-hourly GRIB2 files (temporary)
├── gfs_t2m_f003.grib2
├── gfs_t2m_f006.grib2
├── ...
├── gfs_t2m_f240.grib2           # Last file for 10-day forecast
└── gfs_temp_ethiopia_10day.nc   # Final merged NetCDF
```

!!! tip "Cleaning Up GRIB Files"
    The intermediate GRIB2 files can be deleted after the NetCDF is created:
    ```bash
    rm data/gfs_temp/*.grib2
    ```

---

## 🔍 Verifying Your Download

After downloading, verify your data using Python:

```python
import xarray as xr
import matplotlib.pyplot as plt

# Open the forecast file
ds = xr.open_dataset('data/gfs_temp/gfs_temp_ethiopia_10day.nc')

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
ax.set_title(f"GFS Day 1 Temperature Forecast\n{ds.time.values[0]}")
plt.savefig('gfs_temp_day1.png', dpi=150, bbox_inches='tight')
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
plt.savefig('gfs_temp_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()

# Plot all days as a heatmap
fig, axes = plt.subplots(2, 5, figsize=(20, 8))
for i, ax in enumerate(axes.flat):
    if i < len(ds.time):
        ds.t2m.isel(time=i).plot(ax=ax, cmap='RdYlBu_r', vmin=10, vmax=35, add_colorbar=False)
        ax.set_title(f"Day {i+1}")
    ax.set_xlabel('')
    ax.set_ylabel('')
plt.tight_layout()
plt.savefig('gfs_temp_all_days.png', dpi=150, bbox_inches='tight')
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
| `time` | Valid time (end of 24h period) |
| `lat` | Latitude (degrees north) |
| `lon` | Longitude (degrees east) |

### Attributes

```python
# Dataset attributes (example)
{
    'title': 'NCEP GFS 0.25° daily mean 2m air temperature',
    'source': 'NCEP GFS 0.25-degree (TMP at 2 m AGL from NOMADS)',
    'forecast_reference_time': '2025-01-15T00:00:00',
    'history': 'Created by download_gfs_t2m_daily.py'
}

# Variable attributes
{
    'units': 'degC',
    'long_name': 'GFS daily mean 2m air temperature',
    'description': '24-hour mean computed by averaging 3-hourly values'
}
```

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

=== "Unrealistic Temperature Values"

    **Problem:** Temperature values seem wrong (e.g., 280°C)
    
    **Cause:** Data still in Kelvin but script expected Celsius
    
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
    &lev_2_m_above_ground=on               # 2m level
    &var_TMP=on                            # Temperature variable only
    &subregion=                            # Enable subsetting
    &leftlon=33&rightlon=48                # Longitude bounds
    &toplat=15&bottomlat=3                 # Latitude bounds
    &dir=/gfs.20250115/00/atmos            # Directory path
```

### Benefits of GRIB Filter

- ✅ **Faster downloads** - Only transfers needed data
- ✅ **Lower bandwidth** - Subset before download
- ✅ **Variable selection** - Only TMP, not all variables
- ✅ **Level selection** - Only 2m above ground
- ✅ **Spatial subsetting** - Only your region

---

## 🎓 Data Quality Notes

!!! success "Strengths"
    - **High temporal frequency** (4 cycles daily)
    - **Global coverage** at 0.25° resolution
    - **Extended forecast range** (up to 16 days)
    - **Operational model** - constantly improved
    - **Free and open access** via NOMADS
    - **Temperature forecasts** generally more skillful than precipitation

!!! warning "Limitations"
    - **Forecast skill degrades** after day 7-10
    - **Limited data retention** (~10 days on NOMADS)
    - **Model biases** vary by region, season, and terrain
    - **2m temperature** may not represent complex terrain well
    - **Rate limiting** during high traffic periods

!!! tip "Best Practices"
    - **Validate against observations** when possible
    - **Consider elevation effects** in mountainous regions
    - **Use bias correction** for your specific region
    - **Archive forecasts** for verification studies
    - **Compare multiple cycles** for consistency
    - **Combine with precipitation** for complete weather picture

---

## 🔗 Combining Temperature and Precipitation

For malaria modeling with VECTRI, you'll need both temperature and precipitation. Here's how to combine them:

```python
import xarray as xr

# Load both datasets
ds_temp = xr.open_dataset('data/gfs_temp_ethiopia_10day.nc')
ds_precip = xr.open_dataset('data/gfs_precip_ethiopia_10day.nc')

# Merge into single dataset
ds_combined = xr.merge([ds_temp, ds_precip])

# Verify
print(ds_combined)
# Dimensions: (time: 10, lat: 49, lon: 61)
# Variables: t2m, tp

# Save combined file
ds_combined.to_netcdf('data/gfs_combined_ethiopia_10day.nc')
```

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

### Related Tutorials

- [GFS Precipitation Forecast](13-download_gfs_precip_forecast.md) - Download precipitation data
- [CHIRPS Rainfall](10-download_chirps.md) - Historical rainfall observations
- [ERA5 Reanalysis](#) - Historical temperature and precipitation

---

## 🚀 Next Steps

<div class="grid cards" markdown>

-   :material-chart-line: **Analyze Temperature Trends**
    
    ---
    
    Calculate anomalies and trends  
    Compare with climatology  
    
    → [Xarray Tutorial](06-Xarray_for_Climate_and_Meteorology_Workshop.md)

-   :material-map: **Create Temperature Maps**
    
    ---
    
    Visualize spatial patterns  
    Plot time series  
    
    → [Matplotlib Tutorial](05-Matplotlib_for_Climate_and_Meteorology_Workshop.md)

-   :material-weather-cloudy: **Download Precipitation**
    
    ---
    
    Get matching precipitation forecasts  
    Combine for complete weather  
    
    → [GFS Precipitation](13-download_gfs_precip_forecast.md)

-   :material-bug: **VECTRI Integration**
    
    ---
    
    Prepare inputs for malaria modeling  
    Temperature-dependent transmission  
    
    → [VECTRI Model](../day1/06-vectri_model_components_larvae_to_hydrology.md)

</div>

---

!!! example "Need Help?"
    If you encounter issues or have questions:
    
    - Check the [Troubleshooting](#troubleshooting) section
    - Review [NOMADS documentation](https://nomads.ncep.noaa.gov/)
    - Check [NCEP status page](https://www.nco.ncep.noaa.gov/status/messages/)
    - Contact workshop instructors

---

<div style="background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
  <h3 style="margin: 0 0 1rem 0;">🌡️ Ready for Temperature Forecasting!</h3>
  <p style="margin: 0; opacity: 0.95;">You now have everything you need to download and process NCEP GFS temperature forecasts for your climate and malaria modeling applications.</p>
</div>
