# 🌧️ CHIRPS Rainfall Data Download Tutorial

Learn how to download CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data) rainfall datasets for climate and malaria modeling.

---

## 📋 Overview

This tutorial provides a complete Python script to download, clip, and merge CHIRPS daily rainfall data for any region and time period.

!!! info "CHIRPS Dataset"
    **CHIRPS v2.0** is a quasi-global (50°S–50°N) rainfall dataset combining satellite imagery with in-situ station data.
    
    - **Temporal Coverage**: 1981–present (updated every 2 weeks)
    - **Temporal Resolution**: Daily
    - **Spatial Resolution**: 0.05° (~5 km) or 0.25° (~25 km)
    - **Format**: NetCDF
    - **Best For**: High-resolution rainfall analysis in Africa

---

## 🎯 What This Script Does

The download script performs four main operations:

1. **📥 Downloads** CHIRPS yearly NetCDF files from the official repository
2. **✂️ Clips** data to your region of interest (optional)
3. **🔗 Merges** multiple years into a single NetCDF file
4. **💾 Saves** compressed output for efficient storage

```mermaid
graph LR
    A[Start Year] --> B[Download Yearly Files]
    B --> C{Clip Region?}
    C -->|Yes| D[Clip to Bounding Box]
    C -->|No| E[Use Full Files]
    D --> F[Merge All Years]
    E --> F
    F --> G[Save Single NetCDF]
```

---

## 🚀 Quick Start

### 1. Installation

First, install the required Python packages:

```bash
pip install requests xarray netCDF4 numpy
```

### 2. Save the Script

Create a new file called `download_chirps.py` and copy the script below into it.

### 3. Run Examples

**Download 3 years without clipping:**

```bash
python download_chirps.py --start 2018 --end 2020 --outdir data/chirps_p25
```

**Download and clip to East Africa (Ethiopia region):**

```bash
python download_chirps.py --start 2013 --end 2019 \
  --clip 15 3 33 48 \
  --outdir data/chirps_ethiopia \
  --res p05
```

**Download with custom merged filename:**

```bash
python download_chirps.py --start 2015 --end 2017 \
  --clip 15 -5 30 50 \
  --outdir data/chirps_ea \
  --merge-name chirps_east_africa.nc
```

---

## 📜 The Complete Python Script

Click the tabs below to view different sections of the script, or scroll down for the complete code.

=== "Main Script"

    This is the complete, production-ready script you can use immediately.

    ```python title="download_chirps.py" linenums="1"
    #!/usr/bin/env python3
    """
    Download CHIRPS daily NetCDF (v2.0) by year range, optionally clip to a region,
    and merge all files into a single NetCDF.
    
    Examples
    --------
    # Download 2018–2020, no clip
    python download_chirps.py --start 2018 --end 2020 --outdir data/chirps
    
    # Clip to East Africa box
    python download_chirps.py --start 2015 --end 2017 \
      --clip 15 -10 30 50 --outdir data/chirps_ea
    """
    
    import argparse
    from pathlib import Path
    import sys
    import requests
    
    
    def download_file(url: str, dest: Path, chunk=2**20):
        """
        Download a file from URL and save to dest in chunks.
        
        Parameters
        ----------
        url : str
            HTTP(S) URL to download from
        dest : Path
            Local filesystem target path
        chunk : int
            Chunk size in bytes (default 1 MB)
        """
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".part")
        
        with requests.get(url, stream=True, timeout=180) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for blk in r.iter_content(chunk_size=chunk):
                    if blk:
                        f.write(blk)
        
        tmp.replace(dest)
    
    
    def build_url(year: int, res: str) -> str:
        """
        Build the CHIRPS daily NetCDF URL for a given year and resolution.
        
        Parameters
        ----------
        year : int
            Year to download (e.g., 2018)
        res : str
            Resolution: 'p25' for 0.25°, 'p05' for 0.05°
        
        Returns
        -------
        str
            Full URL to CHIRPS NetCDF file
        """
        base = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/{res}"
        return f"{base}/chirps-v2.0.{year}.days_{res}.nc"
    
    
    def standardize_for_merge(ds):
        """
        Standardize dimension names and latitude orientation.
        
        - Renames 'latitude' → 'lat' and 'longitude' → 'lon'
        - Flips latitude to run south to north
        """
        ren = {}
        if "latitude" in ds.dims:
            ren["latitude"] = "lat"
        if "longitude" in ds.dims:
            ren["longitude"] = "lon"
        if ren:
            ds = ds.rename(ren)
        
        try:
            lat = ds["lat"]
            if lat[0] > lat[-1]:
                ds = ds.reindex(lat=list(reversed(lat.values)))
        except Exception:
            pass
        
        return ds
    
    
    def clip_box(ds, N, S, W, E):
        """
        Clip dataset to a latitude/longitude bounding box.
        
        Parameters
        ----------
        ds : xarray.Dataset
            Input dataset
        N, S, W, E : float
            North, South, West, East boundaries in degrees
        
        Returns
        -------
        xarray.Dataset
            Clipped and standardized dataset
        """
        import numpy as np
        
        if S >= N:
            raise ValueError(f"Invalid bounds: South ({S}) must be < North ({N})")
        
        # Detect coordinate names
        lat_name = "latitude" if "latitude" in ds.dims else "lat"
        lon_name = "longitude" if "longitude" in ds.dims else "lon"
        
        lat = ds[lat_name].values
        lon = ds[lon_name].values
        
        # Latitude slice (south to north)
        lat_slice = slice(S, N)
        
        lon_min, lon_max = float(lon.min()), float(lon.max())
        W2, E2 = W, E
        
        # Handle longitude wrapping if needed
        if lon_min >= 0 and W < 0:
            W2 = (W + 360) % 360
            E2 = (E + 360) % 360
        
        sel_dict = {lat_name: lat_slice}
        
        if W2 <= E2:
            sel_dict[lon_name] = slice(W2, E2)
            ds_sub = ds.sel(sel_dict)
        else:
            # Handle wrapping across dateline
            left_dict = {lat_name: lat_slice, lon_name: slice(W2, lon_max)}
            right_dict = {lat_name: lat_slice, lon_name: slice(lon_min, E2)}
            left = ds.sel(left_dict)
            right = ds.sel(right_dict)
            ds_sub = type(ds).concat([left, right], dim=lon_name)
        
        ds_sub = standardize_for_merge(ds_sub)
        return ds_sub
    
    
    def merge_to_netcdf(nc_paths, out_path: Path):
        """
        Merge multiple NetCDF files into one.
        
        Parameters
        ----------
        nc_paths : list of Path
            Input NetCDF files
        out_path : Path
            Output merged file
        """
        import xarray as xr
        
        if not nc_paths:
            raise ValueError("No input files to merge")
        
        print(f"[merge] {len(nc_paths)} files → {out_path.name}")
        
        ds = xr.open_mfdataset(
            [str(p) for p in nc_paths],
            combine="by_coords",
            preprocess=standardize_for_merge,
            parallel=False,
        )
        
        data_vars = list(ds.data_vars)
        if not data_vars:
            raise ValueError("No data variables in datasets")
        
        # Compress output
        enc = {v: {"zlib": True, "complevel": 3} for v in data_vars}
        
        out_path.parent.mkdir(parents=True, exist_ok=True)
        ds.to_netcdf(out_path, encoding=enc)
        
        print(f"[✓] Merged saved: {out_path}")
    
    
    def main():
        """Main function: parse args, download, clip, merge."""
        ap = argparse.ArgumentParser(
            description="Download CHIRPS daily v2.0 by year range; optional clip & merge"
        )
        
        ap.add_argument("--start", type=int, required=True,
                        help="Start year (e.g., 2018)")
        ap.add_argument("--end", type=int, required=True,
                        help="End year inclusive (e.g., 2020)")
        ap.add_argument("--outdir", default="chirps_downloads",
                        help="Directory to save files")
        ap.add_argument("--res", choices=["p25", "p05"], default="p25",
                        help="Resolution: p25=0.25°, p05=0.05°")
        ap.add_argument("--clip", nargs=4, type=float, metavar=("N", "S", "W", "E"),
                        help="Clip box (degrees): North South West East")
        ap.add_argument("--merge-name", type=str, default=None,
                        help="Custom merged filename (optional)")
        ap.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing files")
        
        args = ap.parse_args()
        
        years = list(range(args.start, args.end + 1))
        outdir = Path(args.outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        
        downloaded = []
        clipped = []
        
        # Download and optionally clip each year
        for y in years:
            url = build_url(y, args.res)
            raw_nc = outdir / f"chirps-v2.0.{y}.days_{args.res}.nc"
            
            if not raw_nc.exists() or args.overwrite:
                print(f"[GET]  {url}")
                try:
                    download_file(url, raw_nc)
                    print(f"[✓]    Saved {raw_nc.name}")
                except Exception as e:
                    print(f"[✗]    Download failed for {y}: {e}")
                    continue
            else:
                print(f"[skip] {raw_nc.name} exists")
            
            downloaded.append(raw_nc)
            
            # Clip if requested
            if args.clip:
                N, S, W, E = args.clip
                out_clip = raw_nc.with_name(raw_nc.stem + "_clip.nc")
                
                if not out_clip.exists() or args.overwrite:
                    try:
                        import xarray as xr
                        ds = xr.open_dataset(raw_nc)
                        ds_sub = clip_box(ds, N, S, W, E)
                        enc = {v: {"zlib": True, "complevel": 3} for v in ds_sub.data_vars}
                        ds_sub.to_netcdf(out_clip, encoding=enc)
                        print(f"[✓]    Clipped → {out_clip.name}")
                    except Exception as e:
                        print(f"[warn] Clip failed for {y}: {e}")
                else:
                    print(f"[skip] {out_clip.name} exists")
                
                if out_clip.exists():
                    clipped.append(out_clip)
        
        # Generate merged filename
        if args.merge_name:
            merge_name = Path(args.merge_name).name
        else:
            suffix = "_clip" if args.clip else ""
            merge_name = f"chirps_{args.res}_{years[0]}-{years[-1]}{suffix}.nc"
        
        target = outdir / merge_name
        
        # Merge files
        to_merge = clipped if args.clip else downloaded
        to_merge = [p for p in to_merge if p.exists()]
        
        if to_merge:
            try:
                merge_to_netcdf(to_merge, target)
            except Exception as e:
                print(f"[✗] Merge failed: {e}")
                sys.exit(2)
        else:
            print("[warn] Nothing to merge")
    
    
    if __name__ == "__main__":
        main()
    ```

=== "Key Functions Explained"

    ### 📥 Download Function
    
    ```python
    def download_file(url: str, dest: Path, chunk=2**20):
        """Downloads file in chunks with atomic write."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".part")
        
        with requests.get(url, stream=True, timeout=180) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for blk in r.iter_content(chunk_size=chunk):
                    if blk:
                        f.write(blk)
        
        tmp.replace(dest)  # Atomic rename
    ```
    
    **Features:**
    
    - Streams large files (doesn't load all into memory)
    - Uses temporary `.part` file during download
    - Atomic rename ensures complete files only
    - 180-second timeout for slow connections
    
    ---
    
    ### 🔗 URL Builder
    
    ```python
    def build_url(year: int, res: str) -> str:
        """Constructs CHIRPS URL for year and resolution."""
        base = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/{res}"
        return f"{base}/chirps-v2.0.{year}.days_{res}.nc"
    ```
    
    **Example URLs:**
    
    - 0.25°: `...netcdf/p25/chirps-v2.0.2018.days_p25.nc`
    - 0.05°: `...netcdf/p05/chirps-v2.0.2018.days_p05.nc`
    
    ---
    
    ### ✂️ Clipping Function
    
    ```python
    def clip_box(ds, N, S, W, E):
        """Clips dataset to bounding box [N, S, W, E]."""
        # Handles:
        # - Coordinate name variations (lat/latitude)
        # - Longitude wrapping (dateline crossing)
        # - Standardization for merging
    ```
    
    **Bounding Box Format:**
    
    - **N** = Northern latitude (e.g., 15°N)
    - **S** = Southern latitude (e.g., 3°N)
    - **W** = Western longitude (e.g., 33°E)
    - **E** = Eastern longitude (e.g., 48°E)
    
    ---
    
    ### 🔗 Merge Function
    
    ```python
    def merge_to_netcdf(nc_paths, out_path: Path):
        """Merges multiple years into single NetCDF."""
        ds = xr.open_mfdataset(
            nc_paths,
            combine="by_coords",      # Merge along time
            preprocess=standardize_for_merge,
            parallel=False,
        )
        
        # Compress output (zlib level 3)
        enc = {v: {"zlib": True, "complevel": 3} for v in ds.data_vars}
        ds.to_netcdf(out_path, encoding=enc)
    ```
    
    **Benefits:**
    
    - Concatenates along time dimension automatically
    - Compresses output (smaller file size)
    - Standardizes coordinates across years

=== "Command-Line Arguments"

    The script accepts several command-line arguments:
    
    | Argument | Required | Description | Example |
    |----------|----------|-------------|---------|
    | `--start` | ✅ | Starting year | `--start 2018` |
    | `--end` | ✅ | Ending year (inclusive) | `--end 2020` |
    | `--outdir` | ❌ | Output directory | `--outdir data/chirps` |
    | `--res` | ❌ | Resolution (p25 or p05) | `--res p05` |
    | `--clip` | ❌ | Bounding box [N S W E] | `--clip 15 3 33 48` |
    | `--merge-name` | ❌ | Custom merged filename | `--merge-name ethiopia.nc` |
    | `--overwrite` | ❌ | Overwrite existing files | `--overwrite` |
    
    **Default Values:**
    
    - `outdir`: `"chirps_downloads"`
    - `res`: `"p25"` (0.25° resolution)
    - `merge-name`: Auto-generated (e.g., `chirps_p25_2018-2020.nc`)

---

## 📍 Regional Bounding Boxes

Use these bounding boxes for common regions:

=== "Ethiopia"

    ```bash
    --clip 15 3 33 48
    ```
    
    - North: 15°N
    - South: 3°N
    - West: 33°E
    - East: 48°E

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

=== "Greater Horn of Africa"

    ```bash
    --clip 20 -15 20 55
    ```
    
    - North: 20°N
    - South: 15°S
    - West: 20°E
    - East: 55°E

---

## 💡 Usage Examples

### Example 1: Amhara Region (2013-2019) - High Resolution

Download high-resolution (0.05°) CHIRPS data for the Amhara case study:

```bash
python download_chirps.py \
  --start 2013 \
  --end 2019 \
  --res p05 \
  --clip 13.5 9.0 36.0 40.5 \
  --outdir data/chirps_amhara \
  --merge-name chirps_amhara_2013-2019.nc
```

**Output:**

- Individual years: `data/chirps_amhara/chirps-v2.0.2013.days_p05_clip.nc`, etc.
- Merged file: `data/chirps_amhara/chirps_amhara_2013-2019.nc`

---

### Example 2: Ethiopia - Multiple Resolutions

Download both resolutions for comparison:

```bash
# 0.25° resolution (faster download)
python download_chirps.py \
  --start 2015 \
  --end 2020 \
  --res p25 \
  --clip 15 3 33 48 \
  --outdir data/chirps_ethiopia_p25

# 0.05° resolution (higher detail)
python download_chirps.py \
  --start 2015 \
  --end 2020 \
  --res p05 \
  --clip 15 3 33 48 \
  --outdir data/chirps_ethiopia_p05
```

---

### Example 3: Global Data (No Clipping)

Download global CHIRPS without clipping:

```bash
python download_chirps.py \
  --start 2018 \
  --end 2020 \
  --res p25 \
  --outdir data/chirps_global
```

**Note:** Global files are large (~1.5 GB per year at 0.25°, ~8 GB at 0.05°)

---

## 🔍 Understanding the Output

### File Structure

After running the script, you'll have:

```
data/chirps_amhara/
├── chirps-v2.0.2013.days_p05.nc           # Raw yearly file
├── chirps-v2.0.2013.days_p05_clip.nc      # Clipped yearly file
├── chirps-v2.0.2014.days_p05.nc
├── chirps-v2.0.2014.days_p05_clip.nc
├── ...
└── chirps_amhara_2013-2019.nc             # Merged file (use this!)
```

### NetCDF Structure

Open the merged file to inspect:

```python
import xarray as xr

ds = xr.open_dataset("data/chirps_amhara/chirps_amhara_2013-2019.nc")
print(ds)
```

**Expected Structure:**

```
<xarray.Dataset>
Dimensions:  (time: 2557, lat: 47, lon: 46)
Coordinates:
  * time     (time) datetime64[ns] 2013-01-01 ... 2019-12-31
  * lat      (lat) float32 9.025 9.075 9.125 ... 13.375 13.425 13.475
  * lon      (lon) float32 36.025 36.075 ... 40.425 40.475
Data variables:
    precip   (time, lat, lon) float32 ...
Attributes:
    ...
```

---

## 🎓 Advanced Usage

### Processing After Download

Once you have the merged NetCDF, you can:

**1. Calculate Monthly Totals:**

```python
import xarray as xr

ds = xr.open_dataset("chirps_amhara_2013-2019.nc")
monthly = ds.resample(time="MS").sum()
monthly.to_netcdf("chirps_amhara_monthly.nc")
```

**2. Extract Specific Location:**

```python
# Extract time series for Addis Ababa (9.03°N, 38.74°E)
point = ds.sel(lat=9.03, lon=38.74, method="nearest")
precip_ts = point["precip"].values
```

**3. Calculate Seasonal Means:**

```python
# Kiremt season (June-September)
kiremt = ds.sel(time=ds.time.dt.month.isin([6, 7, 8, 9]))
kiremt_mean = kiremt.groupby("time.year").sum("time")
```

---

## ⚠️ Troubleshooting

### Common Issues and Solutions

!!! warning "Download Timeout"
    **Problem:** `requests.exceptions.Timeout`
    
    **Solution:**
    
    - Check your internet connection
    - Try again later (server may be busy)
    - Increase timeout: modify `timeout=180` to `timeout=300`

!!! warning "Out of Memory"
    **Problem:** Script crashes with memory error
    
    **Solution:**
    
    - Use lower resolution (`--res p25` instead of `p05`)
    - Clip to smaller region
    - Download fewer years at once
    - Close other applications

!!! warning "File Already Exists"
    **Problem:** Script skips downloading existing files
    
    **Solution:**
    
    - Use `--overwrite` flag to force re-download
    - Or manually delete old files

!!! warning "Invalid Bounding Box"
    **Problem:** `ValueError: Invalid latitude bounds`
    
    **Solution:**
    
    - Ensure South < North
    - Check coordinates are in valid range:
        - Latitude: -50 to 50 (CHIRPS coverage)
        - Longitude: -180 to 180

---

## 📊 Data Quality Notes

!!! info "CHIRPS Data Quality"
    
    **Strengths:**
    
    - High spatial resolution (0.05°)
    - Long temporal record (1981–present)
    - Blends satellite and station data
    - Regular updates (every 2 weeks)
    - Quasi-global coverage
    
    **Limitations:**
    
    - 2-week lag for final product
    - Station density varies by region
    - Better over land than ocean
    - May underestimate extreme events
    
    **Recommended For:**
    
    - Climate analysis and trends
    - Model forcing (e.g., VECTRI)
    - Drought monitoring
    - Agricultural applications

---

## 🔗 Additional Resources

- **CHIRPS Homepage**: [https://www.chc.ucsb.edu/data/chirps](https://www.chc.ucsb.edu/data/chirps)
- **CHIRPS Documentation**: [Technical Documentation](https://data.chc.ucsb.edu/products/CHIRPS-2.0/README-CHIRPS.txt)
- **Data Portal**: [https://data.chc.ucsb.edu/products/CHIRPS-2.0/](https://data.chc.ucsb.edu/products/CHIRPS-2.0/)
- **Publication**: Funk et al. (2015), Scientific Data
- **Xarray Documentation**: [https://docs.xarray.dev/](https://docs.xarray.dev/)

---

## 📞 Support

Need help with the download script?

- **Workshop Support**: [yonas.mersha14@gmail.com](mailto:yonas.mersha14@gmail.com)
- **CHIRPS Support**: [chc@ucsb.edu](mailto:chc@ucsb.edu)
- **Technical Issues**: Check the [GitHub Issues](https://github.com/YonSci/vectri-mkdocs/issues)

---

## 🎯 Next Steps

After downloading CHIRPS data:

1. **Quality Check**: Inspect the NetCDF file with `xarray`
2. **Visualization**: Plot spatial and temporal patterns
3. **Integration**: Combine with temperature data (ERA5)
4. **VECTRI Setup**: Prepare climate forcing files

[← Back to Data Access](09-climate_data_access_and_extraction.md){ .md-button }
[Continue to ERA5 Download →](#){ .md-button .md-button--primary }
