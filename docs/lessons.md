# Lessons

Detailed breakdown of all 13 hands-on labs throughout the workshop.

---

## Lab Overview

| Lab | Day | Topic | Duration | Difficulty |
|-----|-----|-------|----------|------------|
| **1** | 1 | Environment & Repo Setup | 1.5h | ⭐ Easy |
| **2** | 1 | Climate Data Download | 1.5h | ⭐⭐ Medium |
| **3** | 1 | Preprocessing & EDA | 1.5h | ⭐⭐ Medium |
| **4** | 2 | VECTRI Compilation | 1.5h | ⭐⭐⭐ Hard |
| **5** | 2 | Single-Location Run | 1.5h | ⭐⭐ Medium |
| **6** | 2 | Gridded Simulations | 1.5h | ⭐⭐⭐ Hard |
| **7** | 3 | Health Data Preparation | 1.5h | ⭐⭐ Medium |
| **8** | 3 | Model Calibration | 1.5h | ⭐⭐⭐ Hard |
| **9** | 3 | Validation & Sensitivity | 1.5h | ⭐⭐⭐ Hard |
| **10** | 4 | Seasonal Forecasting | 1.5h | ⭐⭐⭐ Hard |
| **11** | 4 | Climate Scenarios | 1.5h | ⭐⭐ Medium |
| **12** | 4 | Ensemble & Uncertainty | 1.5h | ⭐⭐⭐ Hard |
| **13** | 5 | Interactive Dashboard | 2.5h | ⭐⭐⭐ Hard |

---

## Day 1 Labs

### Lab 1: Environment & Repository Setup
**Duration:** 10:45–12:30 (1h 45min)  
**Objective:** Configure Python environment and VECTRI build dependencies

#### Tasks

1. **Install Miniconda** (if not done pre-workshop)
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

2. **Create workshop environment**
```bash
conda env create -f environment.yml
conda activate vectri-workshop
```

3. **Install Lmod and compile dependencies** (see [Setup](setup.md))
```bash
# Follow steps 1-7 from Setup guide
sudo apt install build-essential gfortran
# Install Lua, Lmod, NetCDF, HDF5...
```

4. **Clone workshop repository**
```bash
git clone https://github.com/your-org/vectri-workshop-2025.git
cd vectri-workshop-2025
```

5. **Test installations**
```bash
python -c "import xarray, pandas, geopandas; print('Python OK')"
which nc-config
module list
```

#### Deliverable
- [ ] Screenshot of successful environment test
- [ ] Output of `conda list` saved to `lab1_packages.txt`

---

### Lab 2: Climate Data Download
**Duration:** 14:00–15:30 (1h 30min)  
**Objective:** Download CHIRPS and ERA5-Land data for study region

#### Tasks

1. **Define study area** (e.g., Kenya, Uganda, or Ethiopia)
```python
region = {
    'lon_min': 33.0, 'lon_max': 42.0,
    'lat_min': -5.0, 'lat_max': 15.0
}
```

2. **Download CHIRPS precipitation** (2010-2023)
```python
import requests
for year in range(2010, 2024):
    url = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/{year}/"
    # Download daily .tif files
```

3. **Download ERA5-Land via CDS API**
```python
import cdsapi
c = cdsapi.Client()

c.retrieve('reanalysis-era5-land',
    {'variable': ['2m_temperature', 'total_precipitation'],
     'year': list(range(2010, 2024)),
     'month': list(range(1, 13)),
     'area': [region['lat_max'], region['lon_min'], 
              region['lat_min'], region['lon_max']],
     'format': 'netcdf'},
    'era5_land_region.nc')
```

4. **Download administrative boundaries** (GADM)
```python
import geopandas as gpd
url = "https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_KEN_shp.zip"
gdf = gpd.read_file(url)
gdf.to_file("admin_boundaries.shp")
```

#### Deliverable
- [ ] `chirps_2010_2023.nc` (or .tif files)
- [ ] `era5_land_region.nc`
- [ ] `admin_boundaries.shp` (or .geojson)
- [ ] Download log notebook

---

### Lab 3: Preprocessing & EDA
**Duration:** 15:45–17:00 (1h 15min)  
**Objective:** Resample data to VECTRI grid, create masks, perform EDA

#### Tasks

1. **Merge CHIRPS daily to monthly**
```python
import xarray as xr
chirps = xr.open_mfdataset('chirps/*.tif')
chirps_monthly = chirps.resample(time='1M').sum()
```

2. **Resample to VECTRI grid** (e.g., 0.25° or 0.5°)
```python
target_grid = xr.Dataset({
    'lon': (['lon'], np.arange(33, 42, 0.25)),
    'lat': (['lat'], np.arange(-5, 15, 0.25))
})

chirps_regrid = chirps_monthly.interp_like(target_grid)
era5_regrid = era5.interp_like(target_grid)
```

3. **Create land/water mask**
```python
from rasterio import features
mask = features.rasterize(admin_gdf.geometry, ...)
```

4. **Exploratory Data Analysis**
```python
# Time series plots
chirps_regrid.precip.mean(dim=['lat','lon']).plot()

# Spatial climatology
chirps_regrid.precip.mean(dim='time').plot()

# Seasonal cycle
chirps_regrid.groupby('time.month').mean().plot(col='month', col_wrap=4)
```

#### Deliverable
- [ ] `climate_data_vectri_grid.nc` (preprocessed NetCDF)
- [ ] `region_mask.nc`
- [ ] Jupyter notebook with EDA plots

---

## Day 2 Labs

### Lab 4: VECTRI Compilation
**Duration:** 10:45–12:30  
**Objective:** Compile VECTRI from source

#### Tasks

1. **Clone VECTRI repository**
```bash
cd ~
git clone https://github.com/ICTP/vectri.git
cd vectri
```

2. **Load required modules**
```bash
module load netcdf-fortran/4.6.0
```

3. **Compile VECTRI**
```bash
make clean
make NETCDF_HOME=/opt/apps/libs/netcdf/4.9.0 \
     HDF5_HOME=/opt/apps/libs/hdf5/1.12.2
```

4. **Test compilation**
```bash
./vectri -h
./vectri -c data/example_sys5.nc -d data/example_data.nc
```

#### Deliverable
- [ ] `vectri` executable (screenshot of version)
- [ ] Test run output (`vectri_test.log`)

---

### Lab 5: Single-Location Run
**Duration:** 14:00–15:30  
**Objective:** Run VECTRI for one location, interpret outputs

#### Tasks

1. **Create config file** for single point (e.g., Kisumu, Kenya)
2. **Run VECTRI** for 2010-2020
3. **Extract outputs:** EIR, vector density, larvae density
4. **Plot time series** and compare with observations (if available)

#### Deliverable
- [ ] Config file (`kisumu_config.nc`)
- [ ] Output file (`kisumu_output.nc`)
- [ ] Notebook with plots

---

### Lab 6: Gridded Simulations
**Duration:** 15:45–17:00  
**Objective:** Run VECTRI over full domain, QC outputs

#### Tasks

1. **Create gridded config**
2. **Run batch simulations** (parallelize if possible)
3. **Quality control:** Check for NaNs, outliers, physical constraints
4. **Visualize:** Create maps of annual mean EIR

#### Deliverable
- [ ] Gridded output NetCDF
- [ ] QC report
- [ ] Maps notebook

---

## Day 3 Labs

### Lab 7: Health Data Preparation
**Duration:** 10:45–12:30  
**Objective:** Download and preprocess HMIS/DHIS2 malaria cases

#### Tasks

1. **Access DHIS2 API** (or use provided CSV)
2. **Aggregate to district/month**
3. **Calculate incidence rates** (cases per 1000 population)
4. **Align with climate data** (spatial/temporal matching)

#### Deliverable
- [ ] `malaria_cases_monthly.csv`
- [ ] Preprocessing script

---

### Lab 8: Model Calibration
**Duration:** 14:00–15:30  
**Objective:** Calibrate VECTRI parameters to match observations

#### Tasks

1. **Define parameter ranges** (e.g., mosquito lifespan, biting rate)
2. **Run parameter sweep** (Latin hypercube or grid search)
3. **Evaluate fit:** RMSE, correlation, Nash-Sutcliffe
4. **Select optimal parameters**

#### Deliverable
- [ ] Calibration results table
- [ ] Scatter plots (obs vs. modeled)

---

### Lab 9: Validation & Sensitivity
**Duration:** 15:45–17:00  
**Objective:** Validate on holdout period, sensitivity analysis

#### Tasks

1. **Split data:** 2010-2018 (calibration), 2019-2020 (validation)
2. **Run validation** with optimal parameters
3. **Calculate metrics:** R², RMSE, bias
4. **Sensitivity analysis:** Vary key parameters, assess impact

#### Deliverable
- [ ] Validation report
- [ ] Sensitivity plots

---

## Day 4 Labs

### Lab 10: Seasonal Forecasting
**Duration:** 10:45–12:30  
**Objective:** Generate 3-month malaria forecast

#### Tasks

1. **Download forecast climate data** (ECMWF SEAS5 or CFSv2)
2. **Run VECTRI** with forecast forcing
3. **Generate probabilistic forecasts** (tercile categories)
4. **Create risk maps**

#### Deliverable
- [ ] Forecast output
- [ ] Probability maps (below/normal/above)

---

### Lab 11: Climate Scenarios
**Duration:** 14:00–15:30  
**Objective:** Run VECTRI under future climate (2030, 2050)

#### Tasks

1. **Download CMIP6 data** (SSP2-4.5, SSP5-8.5)
2. **Bias-correct** climate projections
3. **Run VECTRI** for future periods
4. **Compare** with baseline (2010-2020)

#### Deliverable
- [ ] Scenario outputs
- [ ] Change maps (future - baseline)

---

### Lab 12: Ensemble & Uncertainty
**Duration:** 15:45–17:00  
**Objective:** Quantify forecast uncertainty

#### Tasks

1. **Run ensemble** (multiple climate models or parameters)
2. **Calculate spread** (std dev, percentiles)
3. **Create probabilistic maps**

#### Deliverable
- [ ] Ensemble outputs
- [ ] Uncertainty plots

---

## Day 5 Lab

### Lab 13: Interactive Dashboard
**Duration:** 10:45–12:30  
**Objective:** Build Streamlit dashboard for decision-makers

#### Tasks

1. **Set up Streamlit app**
```python
import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Malaria Early Warning System")
```

2. **Add components:**
   - Region selector
   - Time slider
   - Risk map (Folium)
   - Time series plots
   - Downloadable CSV

3. **Deploy** (optional: Streamlit Cloud)

#### Deliverable
- [ ] `app.py` (Streamlit script)
- [ ] README with deployment instructions
- [ ] Screenshot or live URL

---

## Bonus Challenges

For advanced participants who finish early:

1. **Optimize VECTRI runs** (parallelize with Dask or multiprocessing)
2. **Add ML post-processing** (bias correction, downscaling)
3. **Create publication-quality figures** (matplotlib/seaborn styling)
4. **Integrate SMS alerts** (Twilio API for high-risk notifications)
5. **Deploy on cloud** (AWS, Azure, or Google Cloud)

---

## Lab Resources

### Jupyter Notebook Templates

All labs have starter notebooks:
- [Lab 1 Template](https://github.com/your-org/vectri-workshop-2025/blob/main/notebooks/lab01_setup_template.ipynb)
- [Lab 2 Template](https://github.com/your-org/vectri-workshop-2025/blob/main/notebooks/lab02_download_template.ipynb)
- ... (etc.)

### Helper Scripts

Common utilities in `/scripts/`:
- `download_chirps.py` — Automated CHIRPS download
- `regrid_data.py` — Rasterio/xarray regridding
- `plot_maps.py` — Cartopy map templates
- `dhis2_api.py` — DHIS2 data fetcher

### Sample Data

Small test datasets in `/data/samples/`:
- `sample_chirps.nc` (1 year, Kenya)
- `sample_era5.nc` (1 year, Kenya)
- `sample_cases.csv` (HMIS mock data)

---

!!! tip "Stuck on a Lab?"
    - Check the `#technical-help` Slack channel
    - Review the [Resources](resources.md) page
    - Ask instructors during office hours
    - Collaborate with teammates!
