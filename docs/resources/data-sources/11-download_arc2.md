# 🌧️ ARC2 Rainfall Data Download Tutorial

Learn how to download ARC2 (Africa Rainfall Climatology version 2) daily rainfall data for climate and malaria modeling in Africa.

---

## 📋 Overview

This tutorial provides a complete Python script to download, convert, clip, and merge ARC2 daily rainfall data for any African region and time period.

!!! info "ARC2 Dataset"
    **ARC2 (Africa Rainfall Climatology v2.0)** is NOAA's operational African rainfall dataset combining GPI satellite estimates with gauge observations.
    
    - **Temporal Coverage**: 1983–present (near-real-time updates)
    - **Temporal Resolution**: Daily
    - **Spatial Resolution**: 0.1° (~10 km)
    - **Geographic Coverage**: Africa only (40°S–40°N, 20°W–55°E)
    - **Format**: Binary (.gz) → converted to NetCDF
    - **Update Lag**: ~2 days
    - **Best For**: Continental-scale African rainfall analysis

---

## 🎯 What This Script Does

The download script performs five main operations:

1. **📥 Downloads** ARC2 daily binary (.gz) files from NOAA CPC
2. **🔄 Converts** binary data to NetCDF format with proper georeferencing
3. **✂️ Clips** data to your region of interest (optional)
4. **🔗 Merges** multiple days into a single time-series NetCDF
5. **💾 Saves** compressed output for efficient storage

```mermaid
graph LR
    A[Start Date] --> B[Download Binary .gz]
    B --> C[Convert to NetCDF]
    C --> D{Clip Region?}
    D -->|Yes| E[Clip to Bounding Box]
    D -->|No| F[Keep Full Africa]
    E --> G[Merge Daily Files]
    F --> G
    G --> H[Save Time Series]
```

---

## 🚀 Quick Start

### 1. Installation

Install the required Python packages:

```bash
pip install requests xarray netCDF4 numpy
```

### 2. Save the Script

Create a new file called `download_arc2.py` and copy the script below into it.

### 3. Run Examples

**Download 1 year, full Africa:**

```bash
python download_arc2.py --start 2020-01-01 --end 2020-12-31 \
  --outdir data/arc2_2020 \
  --merge-name arc2_africa_2020.nc
```

**Download and clip to Ethiopia:**

```bash
python download_arc2.py --start 2013-01-01 --end 2019-12-31 \
  --clip 18 3 32 50 \
  --outdir data/arc2_ethiopia \
  --merge-name arc2_ethiopia_2013-2019.nc
```

**Convert existing files without re-downloading:**

```bash
python download_arc2.py --start 2015-01-01 --end 2015-12-31 \
  --outdir data/arc2_2015 \
  --clip 15 -5 30 50 \
  --merge-name arc2_ea_2015.nc \
  --skip-download
```

---

## 📜 The Complete Python Script

Click the tabs below to view different sections of the script, or scroll down for the complete code.

=== "Main Script"

    This is the complete, production-ready script you can use immediately.

    ```python title="download_arc2.py" linenums="1"
    #!/usr/bin/env python
    """
    Download daily ARC2 binary rainfall data and convert to (optionally clipped) NetCDF.
    
    Example usage:
    
      # Download + convert + clip to Ethiopia box and merge:
      python download_arc2.py \
          --start 2010-01-01 \
          --end   2010-12-31 \
          --outdir data/arc2_ea \
          --clip 18 3 32 50 \
          --merge-name arc2_ea_2010.nc
    
      # Only convert existing .gz files (no download):
      python download_arc2.py \
          --start 2010-01-01 \
          --end   2010-12-31 \
          --outdir data/arc2_ea \
          --clip 18 3 32 50 \
          --merge-name arc2_ea_2010.nc \
          --skip-download
    """
    
    import argparse
    from datetime import datetime, timedelta
    from pathlib import Path
    import gzip
    
    import numpy as np
    import xarray as xr
    import requests
    
    # ---------------------------------------------------------------------
    # ARC2 constants (from CPC/NOAA documentation)
    # ---------------------------------------------------------------------
    ARC2_BASE_URL = "https://ftp.cpc.ncep.noaa.gov/fews/fewsdata/africa/arc2/bin"
    
    # Grid: -40S to 40N, 20W to 55E, 0.1° resolution
    NLAT = 801  # south–north
    NLON = 751  # west–east
    LAT_S, LAT_N = -40.0, 40.0
    LON_W, LON_E = -20.0, 55.0
    
    
    # ---------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------
    def parse_date(s):
        """Parse date from 'YYYYMMDD' or 'YYYY-MM-DD'."""
        s = s.strip()
        for fmt in ("%Y%m%d", "%Y-%m-%d"):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                pass
        raise ValueError(f"Could not parse date '{s}' (expected YYYYMMDD or YYYY-MM-DD)")
    
    
    def date_range(start, end):
        """Inclusive daily date range."""
        if end < start:
            raise ValueError("End date is earlier than start date")
        cur = start
        one = timedelta(days=1)
        while cur <= end:
            yield cur
            cur += one
    
    
    def build_arc2_url(d):
        """Construct ARC2 URL for a given date."""
        return f"{ARC2_BASE_URL}/daily_clim.bin.{d:%Y%m%d}.gz"
    
    
    def download_file(url, dest, overwrite=False):
        """
        Download a file with basic logging and 404 handling.
        Returns True if file is present locally after this call.
        """
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
    
        if dest.exists() and not overwrite:
            print(f"[info] already exists, skipping download: {dest.name}")
            return True
    
        tmp = dest.with_suffix(dest.suffix + ".part")
        if tmp.exists():
            tmp.unlink()
    
        try:
            print(f"[info] downloading {url}")
            with requests.get(url, stream=True, timeout=300) as r:
                try:
                    r.raise_for_status()
                except requests.HTTPError as e:
                    code = r.status_code
                    if code == 404:
                        print(f"[warn] 404 not found, skipping: {url}")
                        return False
                    print(f"[err] HTTP {code} for {url}: {e}")
                    return False
    
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
    
            tmp.replace(dest)
            print(f"[✓] Downloaded: {dest.name}")
            return True
    
        except Exception as e:
            print(f"[err] download failed for {url}: {e}")
            if tmp.exists():
                tmp.unlink()
            return False
    
    
    def read_arc2_gz_to_array(bin_gz):
        """
        Read a gzipped ARC2 binary file into a 2D numpy array (lat, lon).
        
        NOTE on dtype/endianness:
        - CPC docs say "single precision floating point".
        - Here we assume big-endian (">f4").
        - If values look strange, change to "<f4".
        """
        bin_gz = Path(bin_gz)
        if not bin_gz.exists():
            raise FileNotFoundError(bin_gz)
    
        with gzip.open(bin_gz, "rb") as f:
            buf = f.read()
    
        data = np.frombuffer(buf, dtype=">f4")  # big-endian float32
        expected = NLAT * NLON
        if data.size != expected:
            raise ValueError(
                f"{bin_gz} has {data.size} values, expected {expected} "
                f"({NLAT}x{NLON}); check format/endianness."
            )
    
        # reshape to (lat, lon)
        arr = data.reshape((NLAT, NLON))
    
        # Orientation note:
        # Grid is 801 pixels south–north and 751 west–east.
        # First row = LAT_S (-40), last row = LAT_N (40).
        # If maps are flipped N/S, use: arr = arr[::-1, :]
    
        return arr
    
    
    def make_lat_lon():
        """Create 1D lat/lon coordinate arrays."""
        lats = np.linspace(LAT_S, LAT_N, NLAT, dtype="float32")
        lons = np.linspace(LON_W, LON_E, NLON, dtype="float32")
        return lats, lons
    
    
    def convert_bin_to_nc(bin_gz, nc_path, clip_box=None, overwrite=False):
        """
        Convert one gzipped ARC2 binary file to a 1-day NetCDF.
        
        clip_box: (N, S, W, E) if not None.
        Returns True if NetCDF exists/was created; False on failure.
        """
        bin_gz = Path(bin_gz)
        nc_path = Path(nc_path)
    
        if not bin_gz.exists():
            print(f"[warn] missing file (skipping): {bin_gz.name}")
            return False
    
        if nc_path.exists() and not overwrite:
            print(f"[info] daily NetCDF exists, skipping convert: {nc_path.name}")
            return True
    
        try:
            arr = read_arc2_gz_to_array(bin_gz)
            lats, lons = make_lat_lon()
    
            data3d = arr[np.newaxis, :, :]  # (time, lat, lon)
    
            # Extract date from filename: daily_clim.bin.YYYYMMDD.gz
            stem = bin_gz.name
            date_str = stem.split(".")[-2]
            t = np.datetime64(datetime.strptime(date_str, "%Y%m%d"))
    
            ds = xr.Dataset(
                {
                    "precip": (("time", "lat", "lon"), data3d.astype("float32")),
                },
                coords={
                    "time": [t],
                    "lat": lats,
                    "lon": lons,
                },
            )
    
            ds["precip"].attrs["long_name"] = "ARC2 daily rainfall"
            ds["precip"].attrs["units"] = "mm/day"
            ds.attrs["source"] = "NOAA CPC Africa Rainfall Climatology v2.0 (ARC2)"
            ds.attrs["history"] = f"created from {bin_gz.name}"
    
            if clip_box is not None:
                N, S, W, E = clip_box
                if S > N or W > E:
                    raise ValueError(f"Invalid clip box (N={N}, S={S}, W={W}, E={E})")
                ds = ds.sel(lat=slice(S, N), lon=slice(W, E))
    
            nc_path.parent.mkdir(parents=True, exist_ok=True)
    
            encoding = {
                "precip": {
                    "zlib": True,
                    "complevel": 4,
                    "dtype": "float32",
                    "_FillValue": np.float32(-9999.0),
                }
            }
            ds.to_netcdf(nc_path, format="NETCDF4", encoding=encoding)
            print(f"[✓] Converted: {nc_path.name}")
            return True
    
        except Exception as e:
            print(f"[err] failed to convert {bin_gz.name}: {e}")
            return False
    
    
    def merge_daily_nc(nc_paths, out_path, overwrite=False):
        """Merge a list of daily NetCDF files into a single time-series file."""
        out_path = Path(out_path)
    
        if out_path.exists() and not overwrite:
            print(f"[info] merged file already exists, skipping: {out_path.name}")
            return
    
        if not nc_paths:
            print("[warn] no daily NetCDF files to merge; skipping merge.")
            return
    
        print(f"[merge] {len(nc_paths)} daily files → {out_path.name}")
    
        ds = xr.open_mfdataset(
            [str(p) for p in nc_paths],
            combine="by_coords",
            parallel=False,
            chunks={"time": 30},
        )
    
        encoding = {vn: {"zlib": True, "complevel": 4} for vn in ds.data_vars}
        ds.to_netcdf(out_path, format="NETCDF4", encoding=encoding)
        print(f"[✓] Merged file saved: {out_path}")
    
    
    # ---------------------------------------------------------------------
    # CLI
    # ---------------------------------------------------------------------
    def main(argv=None):
        p = argparse.ArgumentParser(
            description="Download daily ARC2 binary rainfall and convert to (optionally clipped) NetCDF."
        )
        p.add_argument("--start", required=True,
                       help="Start date (YYYYMMDD or YYYY-MM-DD)")
        p.add_argument("--end", required=True,
                       help="End date (YYYYMMDD or YYYY-MM-DD, inclusive)")
        p.add_argument("--outdir", default="data/arc2",
                       help="Root output directory (bin/ and nc_daily/ subdirs created)")
        p.add_argument(
            "--clip",
            nargs=4,
            type=float,
            metavar=("N", "S", "W", "E"),
            help="Optional clip box [North South West East] in degrees"
        )
        p.add_argument(
            "--merge-name",
            default=None,
            help=(
                "Filename for merged time-series NetCDF (e.g. 'arc2_ea_2010.nc'). "
                "If omitted, no merge is done."
            ),
        )
        p.add_argument(
            "--skip-download",
            action="store_true",
            help="Do not download, only convert existing local .gz files"
        )
        p.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing .gz and .nc files"
        )
    
        args = p.parse_args(argv)
    
        start = parse_date(args.start)
        end = parse_date(args.end)
    
        out_root = Path(args.outdir)
        bin_dir = out_root / "bin"
        nc_dir = out_root / "nc_daily"
    
        clip_box = tuple(args.clip) if args.clip is not None else None
    
        all_nc_paths = []
    
        for d in date_range(start, end):
            ymd = d.strftime("%Y%m%d")
            gz_name = f"daily_clim.bin.{ymd}.gz"
            bin_path = bin_dir / gz_name
            nc_path = nc_dir / f"arc2_{ymd}.nc"
    
            # 1) Download step (unless user asked to skip)
            if not args.skip_download:
                url = build_arc2_url(d)
                ok = download_file(url, bin_path, overwrite=args.overwrite)
                if not ok:
                    continue
    
            # 2) Convert step (only if file exists locally)
            if bin_path.exists():
                ok_nc = convert_bin_to_nc(
                    bin_path,
                    nc_path,
                    clip_box=clip_box,
                    overwrite=args.overwrite,
                )
                if ok_nc:
                    all_nc_paths.append(nc_path)
            else:
                print(f"[warn] binary file missing, skipping: {bin_path.name}")
    
        # 3) Merge step
        if args.merge_name:
            merge_path = out_root / args.merge_name
            merge_daily_nc(all_nc_paths, merge_path, overwrite=args.overwrite)
        else:
            print("[info] merge step skipped (no --merge-name given).")
    
    
    if __name__ == "__main__":
        main()
    ```

=== "Key Functions Explained"

    ### 📥 Download Function
    
    ```python
    def download_file(url, dest, overwrite=False):
        """Downloads file with 404 handling and atomic write."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        if dest.exists() and not overwrite:
            return True
        
        tmp = dest.with_suffix(dest.suffix + ".part")
        
        with requests.get(url, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
        
        tmp.replace(dest)  # Atomic rename
        return True
    ```
    
    **Features:**
    
    - Handles 404 errors gracefully (some dates may be missing)
    - 5-minute timeout for slow connections
    - Atomic write with `.part` temporary files
    - Streams large files efficiently
    
    ---
    
    ### 🔄 Binary to NetCDF Conversion
    
    ```python
    def read_arc2_gz_to_array(bin_gz):
        """Reads gzipped binary and converts to 2D array."""
        with gzip.open(bin_gz, "rb") as f:
            buf = f.read()
        
        data = np.frombuffer(buf, dtype=">f4")  # big-endian float32
        arr = data.reshape((NLAT, NLON))  # 801 x 751
        return arr
    ```
    
    **Grid Specifications:**
    
    - **Dimensions**: 801 (lat) × 751 (lon)
    - **Coverage**: 40°S to 40°N, 20°W to 55°E
    - **Resolution**: 0.1° (~10 km)
    - **Format**: Big-endian 32-bit floats
    
    ---
    
    ### ✂️ Clipping Function
    
    ```python
    def convert_bin_to_nc(bin_gz, nc_path, clip_box=None, overwrite=False):
        """Converts binary to NetCDF with optional clipping."""
        # Read binary data
        arr = read_arc2_gz_to_array(bin_gz)
        lats, lons = make_lat_lon()
        
        # Create xarray Dataset
        ds = xr.Dataset(
            {"precip": (("time", "lat", "lon"), data3d)},
            coords={"time": [t], "lat": lats, "lon": lons}
        )
        
        # Clip if requested
        if clip_box:
            N, S, W, E = clip_box
            ds = ds.sel(lat=slice(S, N), lon=slice(W, E))
        
        # Save with compression
        ds.to_netcdf(nc_path, encoding=encoding)
    ```
    
    ---
    
    ### 🔗 Merge Function
    
    ```python
    def merge_daily_nc(nc_paths, out_path, overwrite=False):
        """Merges daily files into time series."""
        ds = xr.open_mfdataset(
            nc_paths,
            combine="by_coords",
            parallel=False,
            chunks={"time": 30}  # Chunk for efficiency
        )
        
        encoding = {vn: {"zlib": True, "complevel": 4} for vn in ds.data_vars}
        ds.to_netcdf(out_path, encoding=encoding)
    ```

=== "Command-Line Arguments"

    The script accepts several command-line arguments:
    
    | Argument | Required | Description | Example |
    |----------|----------|-------------|---------|
    | `--start` | ✅ | Starting date | `--start 2020-01-01` |
    | `--end` | ✅ | Ending date (inclusive) | `--end 2020-12-31` |
    | `--outdir` | ❌ | Output directory | `--outdir data/arc2` |
    | `--clip` | ❌ | Bounding box [N S W E] | `--clip 18 3 32 50` |
    | `--merge-name` | ❌ | Merged filename | `--merge-name arc2_ea.nc` |
    | `--skip-download` | ❌ | Skip download, only convert | `--skip-download` |
    | `--overwrite` | ❌ | Overwrite existing files | `--overwrite` |
    
    **Default Values:**
    
    - `outdir`: `"data/arc2"`
    - `merge-name`: None (no merge unless specified)
    
    **Date Formats:**
    
    - `YYYYMMDD` (e.g., `20200101`)
    - `YYYY-MM-DD` (e.g., `2020-01-01`)

---

## 📍 Regional Bounding Boxes

Use these bounding boxes for common African regions:

=== "Ethiopia"

    ```bash
    --clip 18 3 32 50
    ```
    
    - North: 18°N
    - South: 3°N
    - West: 32°E
    - East: 50°E

=== "Amhara Region"

    ```bash
    --clip 13.5 9.0 36.0 40.5
    ```
    
    - North: 13.5°N
    - South: 9.0°N
    - West: 36.0°E
    - East: 40.5°E

=== "East Africa"

    ```bash
    --clip 15 -12 28 52
    ```
    
    - North: 15°N
    - South: 12°S
    - West: 28°E
    - East: 52°E

=== "West Africa"

    ```bash
    --clip 20 0 -18 20
    ```
    
    - North: 20°N
    - South: 0°
    - West: 18°W
    - East: 20°E

=== "Southern Africa"

    ```bash
    --clip -10 -35 10 42
    ```
    
    - North: 10°S
    - South: 35°S
    - West: 10°E
    - East: 42°E

---

## 💡 Usage Examples

### Example 1: Ethiopia - Full Time Period (2013-2019)

Download ARC2 data for the VECTRI Amhara case study:

```bash
python download_arc2.py \
  --start 2013-01-01 \
  --end 2019-12-31 \
  --clip 18 3 32 50 \
  --outdir data/arc2_ethiopia \
  --merge-name arc2_ethiopia_2013-2019.nc
```

**Output:**

```
data/arc2_ethiopia/
├── bin/
│   ├── daily_clim.bin.20130101.gz
│   ├── daily_clim.bin.20130102.gz
│   └── ...
├── nc_daily/
│   ├── arc2_20130101.nc
│   ├── arc2_20130102.nc
│   └── ...
└── arc2_ethiopia_2013-2019.nc  ← Use this file!
```

---

### Example 2: Single Year - Full Africa

Download one year of continental data:

```bash
python download_arc2.py \
  --start 2020-01-01 \
  --end 2020-12-31 \
  --outdir data/arc2_africa_2020 \
  --merge-name arc2_africa_2020.nc
```

**Note:** Full Africa files are moderate size (~20 MB per day uncompressed, ~5 MB compressed)

---

### Example 3: Convert Existing Files (No Download)

If you already have `.gz` files and just need to convert them:

```bash
python download_arc2.py \
  --start 2015-01-01 \
  --end 2015-12-31 \
  --outdir data/arc2_2015 \
  --clip 15 -5 30 50 \
  --merge-name arc2_ea_2015.nc \
  --skip-download
```

This is useful for:

- Re-clipping to a different region
- Re-processing with different settings
- Recovering from interrupted conversions

---

### Example 4: Monthly Download Loop

Download data month by month (better for slow connections):

```bash
for month in {01..12}; do
  python download_arc2.py \
    --start 2020-${month}-01 \
    --end 2020-${month}-31 \
    --clip 15 -5 30 50 \
    --outdir data/arc2_2020_monthly \
    --merge-name arc2_ea_2020_${month}.nc
done

# Then merge monthly files
python -c "
import xarray as xr
from pathlib import Path

files = sorted(Path('data/arc2_2020_monthly').glob('arc2_ea_2020_*.nc'))
ds = xr.open_mfdataset(files, combine='by_coords')
ds.to_netcdf('data/arc2_ea_2020_full.nc', 
             encoding={'precip': {'zlib': True, 'complevel': 4}})
"
```

---

## 🔍 Understanding the Output

### File Structure

```
data/arc2_ethiopia/
├── bin/                                    # Downloaded binary files
│   ├── daily_clim.bin.20130101.gz
│   ├── daily_clim.bin.20130102.gz
│   └── ...
├── nc_daily/                               # Individual daily NetCDFs
│   ├── arc2_20130101.nc
│   ├── arc2_20130102.nc
│   └── ...
└── arc2_ethiopia_2013-2019.nc             # Merged time series (use this!)
```

### NetCDF Structure

Inspect the merged file:

```python
import xarray as xr

ds = xr.open_dataset("data/arc2_ethiopia/arc2_ethiopia_2013-2019.nc")
print(ds)
```

**Expected Structure:**

```
<xarray.Dataset>
Dimensions:  (time: 2557, lat: 151, lon: 181)
Coordinates:
  * time     (time) datetime64[ns] 2013-01-01 ... 2019-12-31
  * lat      (lat) float32 3.0 3.1 3.2 ... 17.8 17.9 18.0
  * lon      (lon) float32 32.0 32.1 32.2 ... 49.8 49.9 50.0
Data variables:
    precip   (time, lat, lon) float32 ...
Attributes:
    source:   NOAA CPC Africa Rainfall Climatology v2.0 (ARC2)
    history:  created from daily_clim.bin.YYYYMMDD.gz
```

---

## 🎓 Advanced Usage

### Processing After Download

**1. Calculate Monthly Totals:**

```python
import xarray as xr

ds = xr.open_dataset("arc2_ethiopia_2013-2019.nc")
monthly = ds.resample(time="MS").sum()
monthly.to_netcdf("arc2_ethiopia_monthly.nc")
```

**2. Extract Time Series for Location:**

```python
# Addis Ababa (9.03°N, 38.74°E)
point = ds.sel(lat=9.03, lon=38.74, method="nearest")
precip_ts = point["precip"].to_pandas()
```

**3. Calculate Climatology:**

```python
# Mean daily rainfall for each day of year
climatology = ds.groupby("time.dayofyear").mean()
```

**4. Compare with CHIRPS:**

```python
import xarray as xr

arc2 = xr.open_dataset("arc2_ethiopia_2013-2019.nc")
chirps = xr.open_dataset("chirps_ethiopia_2013-2019.nc")

# Regrid ARC2 to CHIRPS resolution if needed
arc2_regrid = arc2.interp_like(chirps)

# Calculate difference
diff = arc2_regrid["precip"] - chirps["precip"]
```

---

## ⚠️ Troubleshooting

### Common Issues and Solutions

!!! warning "404 Not Found"
    **Problem:** Some dates return 404 errors
    
    **Solution:**
    
    - ARC2 has occasional missing days
    - Script automatically skips these
    - Check NOAA CPC website for data availability
    - Recent days may not be available yet (~2-day lag)

!!! warning "Binary Format Error"
    **Problem:** `ValueError: wrong number of values`
    
    **Solution:**
    
    - Check endianness: Change `dtype=">f4"` to `dtype="<f4"`
    - Verify file is not corrupted (re-download)
    - Ensure complete download (check file size)

!!! warning "Out of Memory"
    **Problem:** Script crashes with memory error
    
    **Solution:**
    
    - Clip to smaller region
    - Download shorter time periods
    - Use chunking in merge step
    - Close other applications

!!! warning "Missing Binary Files"
    **Problem:** "binary file missing after download"
    
    **Solution:**
    
    - Check internet connection
    - Verify NOAA server is accessible
    - Try `--overwrite` to force re-download
    - Check disk space

!!! warning "Invalid Clip Bounds"
    **Problem:** Clip produces empty dataset
    
    **Solution:**
    
    - Ensure bounds within ARC2 coverage:
        - Latitude: -40° to 40°N
        - Longitude: -20° to 55°E
    - Check South < North and West < East
    - Verify coordinates are in correct hemisphere

---

## 🔄 ARC2 vs CHIRPS Comparison

Understanding when to use each dataset:

| Feature | ARC2 | CHIRPS |
|---------|------|--------|
| **Resolution** | 0.1° (~10 km) | 0.05° (~5 km) or 0.25° |
| **Coverage** | Africa only | Quasi-global (50°S–50°N) |
| **Temporal** | 1983–present | 1981–present |
| **Update Lag** | ~2 days | ~2 weeks (final) |
| **Data Format** | Binary → NetCDF | NetCDF (direct) |
| **Best For** | Continental Africa, NRT | High-resolution, validated |
| **Station Data** | Included | Heavily used |

**Recommendation:**

- **For Africa operational work**: ARC2 (faster updates)
- **For high-resolution studies**: CHIRPS (better resolution)
- **For validation**: Use both and compare!

---

## 📊 Data Quality Notes

!!! info "ARC2 Data Quality"
    
    **Strengths:**
    
    - Continental coverage of Africa
    - Near-real-time updates (~2 days)
    - Consistent methodology since 1983
    - Incorporates GTS station data
    - Operational reliability
    
    **Limitations:**
    
    - Coarser than CHIRPS (0.1° vs 0.05°)
    - Africa-only coverage
    - Less station data than CHIRPS
    - May miss localized extremes
    - Binary format requires conversion
    
    **Recommended For:**
    
    - Continental-scale African studies
    - Operational monitoring (NRT needs)
    - Drought early warning systems
    - Comparison with CHIRPS
    - FEWS NET applications

---

## 🔗 Additional Resources

- **ARC2 Homepage**: [](https://oasishub.co/dataset/africa-african-rainfall-climatology-1983-to-present-climate-prediction-center-noaa)https://oasishub.co/dataset/africa-african-rainfall-climatology-1983-to-present-climate-prediction-center-noaa
- **Data Portal**: [https://ftp.cpc.ncep.noaa.gov/fews/fewsdata/africa/arc2/](https://ftp.cpc.ncep.noaa.gov/fews/fewsdata/africa/arc2/)

- **Publication**: Novella & Thiaw (2013), Journal of Applied Meteorology

---

## 📞 Support

Need help with the download script?

- **Technical Issues**: [GitHub Issues](https://github.com/YonSci/vectri-mkdocs/issues)

---

## 🎯 Next Steps

After downloading ARC2 data:

1. **Quality Check**: Compare with CHIRPS or station data
2. **Visualization**: Plot spatial and temporal patterns
3. **Analysis**: Calculate statistics, trends, anomalies
4. **Integration**: Combine with temperature data for VECTRI
5. **Comparison**: Evaluate ARC2 vs CHIRPS for your region

[← Back to Data Access](../../day3/09-climate_data_access_and_extraction.md){ .md-button }
[Compare with CHIRPS →](10-download_chirps.md){ .md-button .md-button--primary }
