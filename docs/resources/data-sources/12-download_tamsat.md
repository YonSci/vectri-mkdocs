# 📥 Downloading TAMSAT Rainfall Data

## Overview

**TAMSAT (Tropical Applications of Meteorology using SATellite data)** provides high-resolution daily rainfall estimates for Africa. This tutorial guides you through downloading, clipping, and merging TAMSAT v3.1 daily rainfall data using a Python script.

<div class="grid cards" markdown>

-   :material-database-outline: **Dataset**
    
    ---
    
    TAMSAT v3.1 Daily Rainfall
    
    **Coverage:** Africa (1983–present)  
    **Resolution:** ~4 km (0.0375°)  
    **Temporal:** Daily  
    **Format:** NetCDF

-   :material-earth: **Spatial Coverage**
    
    ---
    
    **Region:** African continent  
    **Latitude:** ~40°S to 40°N  
    **Longitude:** ~20°W to 55°E

-   :material-calendar-range: **Temporal Range**
    
    ---
    
    **Start:** January 1, 1983  
    **End:** Near real-time (updated daily)  
    **Latency:** ~2-3 days

-   :material-file-download: **Access**
    
    ---
    
    **Source:** JASMIN GWS  
    **Method:** Direct HTTP download  
    **Authentication:** Not required

</div>

---

## 🎯 What This Script Does

```mermaid
graph LR
    A[Start & End Dates] --> B[Build Daily URLs]
    B --> C[Download NetCDF Files]
    C --> D[Organize by Year/Month]
    D --> E[Merge All Files]
    E --> F[Clip to Region]
    F --> G[Save Final NetCDF]
    
    style A fill:#e3f2fd
    style G fill:#c8e6c9
```

The script performs the following operations:

1. **Downloads** daily NetCDF files for your specified date range
2. **Organizes** files in a structured directory (by year and month)
3. **Merges** all daily files into a single multi-temporal NetCDF
4. **Clips** data to your region of interest (optional)
5. **Compresses** the final output for efficient storage

---

## 🚀 Quick Start Guide

### Prerequisites

!!! info "Required Python Packages"
    ```bash
    pip install requests xarray netCDF4
    ```

### Basic Usage

=== "Full Workflow"
    ```bash
    python download_tamsat.py \
        --start 2020-01-01 \
        --end 2020-12-31 \
        --outdir data/tamsat_2020 \
        --clip 12 2 32 42 \
        --merge-name tamsat_ethiopia_2020.nc
    ```

=== "Download Only"
    ```bash
    python download_tamsat.py \
        --start 2020-01-01 \
        --end 2020-12-31 \
        --outdir data/tamsat_2020
    ```

=== "Merge Existing Files"
    ```bash
    python download_tamsat.py \
        --start 2020-01-01 \
        --end 2020-12-31 \
        --outdir data/tamsat_2020 \
        --skip-download
    ```

---

## 📋 The Complete Script

### Python Download Script

Save this as `download_tamsat.py`:

```python
#!/usr/bin/env python
"""
Download, clip, and merge TAMSAT v3.1 daily rainfall (Africa) into one NetCDF,
using explicit start/end dates (YYYY-MM-DD) and daily NetCDF URLs.

Data source (daily NetCDFs):
    https://gws-access.jasmin.ac.uk/public/tamsat/rfe/data/v3.1/daily/YYYY/MM/rfeYYYY_MM_DD.v3.1.nc

Example file:
    https://gws-access.jasmin.ac.uk/public/tamsat/rfe/data/v3.1/daily/1983/01/rfe1983_01_01.v3.1.nc

This script:
    1) Iterates from --start YYYY-MM-DD to --end YYYY-MM-DD inclusive.
    2) For each date, builds the daily URL and downloads the NetCDF (unless --skip-download).
    3) Saves files under outdir/nc/YYYY/MM/.
    4) Merges all available daily files into a single multi-day NetCDF.
    5) Optionally clips to a lat/lon bounding box.
    6) Writes a compressed NetCDF file.

Example:
    python download_tamsat.py \
        --start 2010-01-01 --end 2011-03-31 \
        --outdir data/tamsat_ea \
        --clip 12 2 32 42 \
        --merge-name tamsat_v3.1_daily_20100101-20110331_ea.nc

Requirements:
    - Python 3.x
    - requests
    - xarray
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, date, timedelta

import requests
import xarray as xr

BASE_DAILY_URL = (
    "https://gws-access.jasmin.ac.uk/public/tamsat/rfe/data/v3.1/daily"
)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def parse_iso_date(s: str) -> date:
    """
    Parse a YYYY-MM-DD string into a datetime.date, with argparse-friendly errors.
    """
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{s}'. Expected format YYYY-MM-DD, e.g. 2010-01-01."
        )


def date_range(start: date, end: date):
    """
    Yield all dates from start to end inclusive.
    """
    current = start
    one_day = timedelta(days=1)
    while current <= end:
        yield current
        current += one_day


def download_file(url: str, dest: Path, overwrite: bool = False) -> bool:
    """
    Download URL to dest (streamed). Returns True if file is present after call.
    """
    if dest.exists() and not overwrite:
        print(f"[download] {dest} exists, skipping download.")
        return True

    print(f"[download] {url} -> {dest}")
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            if r.status_code >= 400:
                print(f"[warning] HTTP {r.status_code} for {url}, skipping.")
                return dest.exists()
            ensure_dir(dest.parent)
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception as exc:
        print(f"[error] failed to download {url}: {exc}")
        return dest.exists()


def detect_lat_lon_names(ds: xr.Dataset):
    """
    Detect latitude and longitude coordinate names in a dataset.
    Returns (lat_name, lon_name).
    """
    lat_candidates = ["lat", "latitude", "y"]
    lon_candidates = ["lon", "longitude", "x"]

    lat_name = None
    lon_name = None

    for name in lat_candidates:
        if name in ds.dims or name in ds.coords:
            lat_name = name
            break
    for name in lon_candidates:
        if name in ds.dims or name in ds.coords:
            lon_name = name
            break

    if lat_name is None or lon_name is None:
        raise ValueError(
            f"Could not detect lat/lon names in dataset. "
            f"Dims: {list(ds.dims.keys())}, Coords: {list(ds.coords.keys())}"
        )

    return lat_name, lon_name


def standardize_for_merge(ds: xr.Dataset) -> xr.Dataset:
    """
    Standardize coordinate names and ordering for safe merge.

    - Rename latitude/longitude to 'lat'/'lon' if needed.
    - Ensure lat and lon are sorted ascending.
    """
    lat_name, lon_name = detect_lat_lon_names(ds)

    rename_map = {}
    if lat_name != "lat":
        rename_map[lat_name] = "lat"
    if lon_name != "lon":
        rename_map[lon_name] = "lon"
    if rename_map:
        ds = ds.rename(rename_map)

    # Sort coordinates ascending
    if ds["lat"].values[0] > ds["lat"].values[-1]:
        ds = ds.sortby("lat")
    if ds["lon"].values[0] > ds["lon"].values[-1]:
        ds = ds.sortby("lon")

    return ds


def clip_box(ds: xr.Dataset, north: float, south: float, west: float, east: float) -> xr.Dataset:
    """
    Clip dataset to a lat/lon box: N, S, W, E.
    Assumes 'lat' and 'lon' coordinates are already standardized.
    """

    ds = standardize_for_merge(ds)

    lat = ds["lat"]
    if lat.values[0] < lat.values[-1]:
        lat_slice = slice(south, north)
    else:
        lat_slice = slice(north, south)

    lon = ds["lon"]
    lon_min = float(lon.min())
    lon_max = float(lon.max())

    if not (lon_min <= west <= lon_max and lon_min <= east <= lon_max):
        print(
            "[warning] Requested lon bounds not fully within data range; "
            "still attempting a simple slice."
        )
    lon_slice = slice(west, east)

    ds_clipped = ds.sel(lat=lat_slice, lon=lon_slice)
    return ds_clipped


def default_encoding(ds: xr.Dataset):
    """
    Build a simple compression encoding dict for NetCDF output.
    """
    encoding = {}
    for var in ds.data_vars:
        encoding[var] = {
            "zlib": True,
            "complevel": 4,
            "shuffle": True,
            "dtype": ds[var].dtype,
        }
    return encoding


# ---------------------------------------------------------------------------
# Core workflow
# ---------------------------------------------------------------------------

def build_tamsat_url(d: date) -> str:
    """
    Build the TAMSAT daily NetCDF URL for a given date.
    Example:
        BASE/1983/01/rfe1983_01_01.v3.1.nc
    """
    return (
        f"{BASE_DAILY_URL}/{d.year:04d}/{d.month:02d}/"
        f"rfe{d.year:04d}_{d.month:02d}_{d.day:02d}.v3.1.nc"
    )


def build_local_path(nc_root: Path, d: date) -> Path:
    """
    Build local path where the daily NetCDF will be stored.
    e.g. nc_root/2010/01/rfe2010_01_01.v3.1.nc
    """
    return (
        nc_root
        / f"{d.year:04d}"
        / f"{d.month:02d}"
        / f"rfe{d.year:04d}_{d.month:02d}_{d.day:02d}.v3.1.nc"
    )


def merge_tamsat_files(
    nc_files,
    out_path: Path,
    clip_bounds=None,
):
    """
    Merge a list of daily TAMSAT NetCDF files into one file.
    clip_bounds: (N, S, W, E) or None.
    """
    if not nc_files:
        raise RuntimeError("No NetCDF files provided for merging.")

    print(f"[merge] Opening {len(nc_files)} files with xarray.open_mfdataset...")
    nc_files_str = [str(p) for p in nc_files]

    def preprocess(ds):
        ds = standardize_for_merge(ds)
        return ds

    ds = xr.open_mfdataset(
        nc_files_str,
        combine="by_coords",
        parallel=False,   # set True if you have dask
        preprocess=preprocess,
    )

    print("[merge] Dataset opened. Coordinates:", list(ds.coords))

    if clip_bounds is not None:
        N, S, W, E = clip_bounds
        print(f"[clip] Applying bounding box N={N}, S={S}, W={W}, E={E}")
        ds = clip_box(ds, N, S, W, E)

    enc = default_encoding(ds)
    ensure_dir(out_path.parent)
    print(f"[write] Writing merged NetCDF -> {out_path}")
    ds.to_netcdf(out_path, encoding=enc)
    ds.close()
    print("[done] Merge complete.")


def run(args):
    start_date: date = args.start
    end_date: date = args.end

    outdir = Path(args.outdir).expanduser().resolve()
    nc_root = outdir / "nc"

    ensure_dir(outdir)
    ensure_dir(nc_root)

    all_local_files = []

    print(
        f"[info] Date range: {start_date.isoformat()} "
        f"-> {end_date.isoformat()}"
    )

    for d in date_range(start_date, end_date):
        url = build_tamsat_url(d)
        local_path = build_local_path(nc_root, d)

        if args.skip_download:
            if local_path.exists():
                all_local_files.append(local_path)
            else:
                print(
                    f"[warning] --skip-download set and local file missing for "
                    f"{d.isoformat()}: {local_path}"
                )
            continue

        ok = download_file(url, local_path, overwrite=args.overwrite)
        if ok and local_path.exists():
            all_local_files.append(local_path)
        else:
            print(f"[warning] Missing or failed file for {d.isoformat()}")

    if not all_local_files:
        print("[error] No NetCDF files found/downloaded in the requested range. Exiting.")
        sys.exit(1)

    # Deduplicate & sort
    all_local_files = sorted(set(all_local_files))

    # Determine output path
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    if args.merge_name:
        merge_path = Path(args.merge_name)
        if not merge_path.is_absolute():
            merge_path = outdir / merge_path
    else:
        bbox_suffix = ""
        if args.clip:
            N, S, W, E = args.clip
            bbox_suffix = f"_N{N}_S{S}_W{W}_E{E}"
        merge_path = outdir / f"tamsat_v3.1_daily_{start_str}-{end_str}{bbox_suffix}.nc"

    clip_bounds = tuple(args.clip) if args.clip else None

    merge_tamsat_files(
        nc_files=all_local_files,
        out_path=merge_path,
        clip_bounds=clip_bounds,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Download, clip and merge TAMSAT v3.1 daily rainfall NetCDFs "
                    "for a given date range."
    )
    parser.add_argument(
        "--start",
        type=parse_iso_date,
        required=True,
        help="Start date (YYYY-MM-DD), e.g. 2010-01-01",
    )
    parser.add_argument(
        "--end",
        type=parse_iso_date,
        required=True,
        help="End date (YYYY-MM-DD, inclusive), e.g. 2011-03-31",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="tamsat_data",
        help="Output directory (default: ./tamsat_data)",
    )
    parser.add_argument(
        "--clip",
        type=float,
        nargs=4,
        metavar=("N", "S", "W", "E"),
        help="Optional lat/lon bounding box: N S W E (e.g. 12 2 32 42)",
    )
    parser.add_argument(
        "--merge-name",
        type=str,
        default=None,
        help="Filename for merged NetCDF (relative to outdir if not absolute). "
             "If omitted, a default name is constructed from the date range.",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Do not download; only merge existing local NetCDFs "
             "for the specified date range.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing daily NetCDFs if they already exist.",
    )
    args = parser.parse_args()

    if args.end < args.start:
        parser.error("--end must be >= --start (in time).")

    return args


def main():
    args = parse_args()
    run(args)


if __name__ == "__main__":
    main()
```

---

## 🔧 Command-Line Arguments

### Required Arguments

| Argument | Type | Description | Example |
|----------|------|-------------|---------|
| `--start` | Date (YYYY-MM-DD) | Start date for download | `2020-01-01` |
| `--end` | Date (YYYY-MM-DD) | End date (inclusive) | `2020-12-31` |

### Optional Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `--outdir` | String | Output directory path | `tamsat_data` |
| `--clip` | 4 Floats | Bounding box: N S W E | None (full extent) |
| `--merge-name` | String | Custom output filename | Auto-generated |
| `--skip-download` | Flag | Skip download, merge only | False |
| `--overwrite` | Flag | Overwrite existing files | False |

---

## 📍 Regional Bounding Boxes

Use these coordinates with the `--clip` argument to extract specific regions:

=== "Ethiopia"
    ```bash
    --clip 15 3 33 48
    ```
    **Coverage:** Entire Ethiopia  
    **Bounds:** N=15°, S=3°, W=33°, E=48°

=== "East Africa"
    ```bash
    --clip 12 -5 28 42
    ```
    **Coverage:** Kenya, Uganda, Tanzania, Rwanda, Burundi  
    **Bounds:** N=12°, S=-5°, W=28°, E=42°

=== "West Africa"
    ```bash
    --clip 18 4 -18 16
    ```
    **Coverage:** Sahel region  
    **Bounds:** N=18°, S=4°, W=-18°, E=16°

=== "Southern Africa"
    ```bash
    --clip -8 -35 10 36
    ```
    **Coverage:** South Africa, Zimbabwe, Mozambique, Zambia  
    **Bounds:** N=-8°, S=-35°, W=10°, E=36°

=== "Horn of Africa"
    ```bash
    --clip 18 -5 32 52
    ```
    **Coverage:** Ethiopia, Somalia, Eritrea, Djibouti, Kenya  
    **Bounds:** N=18°, S=-5°, W=32°, E=52°

---

## 💡 Usage Examples

### Example 1: Download Full Year for Ethiopia

```bash
python download_tamsat.py \
    --start 2020-01-01 \
    --end 2020-12-31 \
    --outdir data/tamsat_eth_2020 \
    --clip 15 3 33 48 \
    --merge-name tamsat_ethiopia_2020.nc
```

**What it does:**
- Downloads all daily files for 2020
- Clips to Ethiopia boundaries
- Saves as `tamsat_ethiopia_2020.nc`

---

### Example 2: Download Rainy Season (JJAS)

```bash
python download_tamsat.py \
    --start 2019-06-01 \
    --end 2019-09-30 \
    --outdir data/tamsat_jjas_2019 \
    --clip 15 3 33 48 \
    --merge-name tamsat_eth_jjas_2019.nc
```

**What it does:**
- Downloads June-September 2019
- Covers main rainy season
- Ideal for seasonal analysis

---

### Example 3: Multi-Year Climate Analysis

```bash
python download_tamsat.py \
    --start 2010-01-01 \
    --end 2020-12-31 \
    --outdir data/tamsat_decadal \
    --clip 15 3 33 48 \
    --merge-name tamsat_ethiopia_2010-2020.nc
```

**What it does:**
- Downloads 11 years of data
- Useful for climatology and trends
- ~4,000 daily files merged

!!! warning "Large Downloads"
    Multi-year downloads can take several hours and require significant disk space (~10-50 GB depending on region size).

---

### Example 4: Update Existing Dataset

```bash
# First, download historical data
python download_tamsat.py \
    --start 2020-01-01 \
    --end 2020-12-31 \
    --outdir data/tamsat_2020 \
    --clip 15 3 33 48

# Later, add recent data
python download_tamsat.py \
    --start 2021-01-01 \
    --end 2021-12-31 \
    --outdir data/tamsat_2021 \
    --clip 15 3 33 48
```

---

### Example 5: Merge Without Re-downloading

If you've already downloaded files and want to re-merge with different settings:

```bash
python download_tamsat.py \
    --start 2020-01-01 \
    --end 2020-12-31 \
    --outdir data/tamsat_2020 \
    --skip-download \
    --clip 15 3 33 48 \
    --merge-name tamsat_ethiopia_2020_clipped.nc
```

---

## 📂 Output Directory Structure

After running the script, your output directory will be organized as follows:

```
tamsat_data/
├── nc/                                    # Raw daily files
│   ├── 2020/
│   │   ├── 01/
│   │   │   ├── rfe2020_01_01.v3.1.nc
│   │   │   ├── rfe2020_01_02.v3.1.nc
│   │   │   └── ...
│   │   ├── 02/
│   │   │   └── ...
│   │   └── ...
│   └── 2021/
│       └── ...
└── tamsat_ethiopia_2020.nc                # Merged output
```

---

## 🔍 Verifying Your Download

After downloading, verify your data using Python:

```python
import xarray as xr

# Open the merged file
ds = xr.open_dataset('data/tamsat_eth_2020/tamsat_ethiopia_2020.nc')

# Display dataset information
print(ds)

# Check dimensions
print(f"Time steps: {len(ds.time)}")
print(f"Latitude range: {float(ds.lat.min()):.2f} to {float(ds.lat.max()):.2f}")
print(f"Longitude range: {float(ds.lon.min()):.2f} to {float(ds.lon.max()):.2f}")

# Check for missing data
print(f"Missing values: {ds.rfe_filled.isnull().sum().values}")

# Quick visualization
ds.rfe_filled.sel(time='2020-07-15').plot()
```

---

## ⚠️ Troubleshooting

### Common Issues and Solutions

=== "Download Failures"

    **Problem:** HTTP errors or timeouts
    
    ```
    [warning] HTTP 404 for https://gws-access.jasmin.ac.uk/...
    ```
    
    **Solutions:**
    
    1. **Check date range:** TAMSAT data starts from 1983-01-01
    2. **Verify internet connection:** Ensure stable connection
    3. **Retry specific dates:** Some recent dates may not be available yet
    4. **Use `--overwrite`:** Re-download failed files
    
    ```bash
    python download_tamsat.py \
        --start 2020-01-01 \
        --end 2020-01-31 \
        --outdir data/tamsat_test \
        --overwrite
    ```

=== "Merge Errors"

    **Problem:** Coordinate mismatch or dimension errors
    
    ```
    ValueError: Could not detect lat/lon names in dataset
    ```
    
    **Solutions:**
    
    1. **Check file integrity:** Corrupted downloads
    2. **Verify date range:** Ensure files exist
    3. **Inspect individual files:**
    
    ```python
    import xarray as xr
    ds = xr.open_dataset('data/tamsat_data/nc/2020/01/rfe2020_01_01.v3.1.nc')
    print(ds.coords)
    ```

=== "Memory Issues"

    **Problem:** Out of memory when merging large datasets
    
    ```
    MemoryError: Unable to allocate array
    ```
    
    **Solutions:**
    
    1. **Process in chunks:** Download and merge by year
    2. **Use smaller regions:** Apply `--clip` to reduce spatial extent
    3. **Enable Dask:** Modify script to use `parallel=True`
    4. **Increase system memory:** Use a machine with more RAM

=== "Clipping Issues"

    **Problem:** Empty dataset after clipping
    
    ```
    [warning] Requested lon bounds not fully within data range
    ```
    
    **Solutions:**
    
    1. **Verify coordinates:** Check that N > S and E > W
    2. **Check data extent:** TAMSAT covers Africa only
    3. **Test without clipping:** Ensure data downloads correctly first
    
    ```bash
    # First test without clipping
    python download_tamsat.py \
        --start 2020-01-01 \
        --end 2020-01-31 \
        --outdir data/tamsat_test
    
    # Then add clipping
    python download_tamsat.py \
        --start 2020-01-01 \
        --end 2020-01-31 \
        --outdir data/tamsat_test \
        --skip-download \
        --clip 15 3 33 48
    ```

---

## 📊 Data Variables and Metadata

### Main Variable

| Variable | Description | Units | Fill Value |
|----------|-------------|-------|------------|
| `rfe_filled` | Rainfall estimate (filled) | mm/day | -999.0 or NaN |

### Coordinates

| Coordinate | Description | Range (Africa) |
|------------|-------------|----------------|
| `time` | Daily timestamp | 1983-01-01 to present |
| `lat` | Latitude | ~-40° to +40° |
| `lon` | Longitude | ~-20° to +55° |

### Attributes

```python
# Dataset attributes (example)
{
    'title': 'TAMSAT v3.1 Daily Rainfall Estimates',
    'institution': 'University of Reading',
    'source': 'Satellite data (Meteosat)',
    'spatial_resolution': '0.0375 degrees (~4 km)',
    'temporal_resolution': 'daily',
    'coverage': 'Africa'
}
```

---

## 🎓 Data Quality Notes

!!! success "Strengths"
    - **High spatial resolution** (~4 km) compared to other products
    - **Long temporal record** (1983–present, 40+ years)
    - **Africa-focused** with local calibration
    - **Near real-time** updates (2-3 day latency)
    - **Well-validated** against rain gauges across Africa

!!! warning "Limitations"
    - **Africa only** - not available for other continents
    - **Satellite-based** - may underestimate heavy rainfall or complex terrain
    - **Cold cloud duration method** - less accurate in coastal/mountain areas
    - **Recent data gaps** - Latest 2-3 days may not be available yet
    - **Quality varies** by season and region

!!! tip "Best Practices"
    - **Validate locally** with rain gauge data when available
    - **Compare with other products** (CHIRPS, ARC2) for consistency
    - **Consider climatology** for context
    - **Check for outliers** and missing values
    - **Use appropriate temporal aggregation** (pentadal, dekadal, monthly)

---

## 📖 Additional Resources

### Official Documentation

- **TAMSAT Homepage:** [https://www.tamsat.org.uk/](https://www.tamsat.org.uk/)
- **Data Portal:** [https://www.tamsat.org.uk/data](https://www.tamsat.org.uk/data)
- **User Guide:** [TAMSAT v3.1 Methodology](https://www.tamsat.org.uk/about/tamsat_v3)
- **Publications:** Key papers on TAMSAT validation and methodology

### Python Libraries

- **xarray:** [https://xarray.pydata.org/](https://xarray.pydata.org/)
- **requests:** [https://docs.python-requests.org/](https://docs.python-requests.org/)
- **netCDF4:** [https://unidata.github.io/netcdf4-python/](https://unidata.github.io/netcdf4-python/)

### Alternative Data Sources

- **CHIRPS:** Higher temporal consistency, coarser resolution (5 km)
- **ARC2:** Pan-African, daily, 10 km resolution
- **IMERG:** Global, 30-min resolution, shorter record (2000+)
- **ERA5:** Reanalysis, global, hourly, model-based

---

## 🚀 Next Steps

<div class="grid cards" markdown>

-   :material-chart-line: **Analyze Your Data**
    
    ---
    
    Load and explore TAMSAT data with xarray  
    Calculate statistics and trends  
    
    → [Xarray Tutorial](#)

-   :material-map: **Visualize Rainfall**
    
    ---
    
    Create maps with Cartopy and GeoPandas  
    Time series and spatial plots  
    
    → [Matplotlib Tutorial](../../day3/05-Matplotlib_for_Climate_and_Meteorology_Workshop.md)

-   :material-vector-combine: **Compare Datasets**
    
    ---
    
    Merge TAMSAT with CHIRPS and ARC2  
    Validate against observations  
    
    → [Data Comparison Guide](#)

-   :material-database-export: **Export Results**
    
    ---
    
    Convert to CSV, GeoTIFF, or other formats  
    Prepare data for VECTRI model  
    
    → [Data Processing](#)

</div>

---

!!! example "Need Help?"
    If you encounter issues or have questions:
    
    - Check the [Troubleshooting](#troubleshooting) section
    - Review the [TAMSAT documentation](https://www.tamsat.org.uk/)
    - Contact workshop instructors
    - Visit the TAMSAT user forum

---

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
  <h3 style="margin: 0 0 1rem 0;">🎯 Ready to Download!</h3>
  <p style="margin: 0; opacity: 0.95;">You now have everything you need to successfully download and process TAMSAT rainfall data for your climate and malaria modeling research.</p>
</div>
