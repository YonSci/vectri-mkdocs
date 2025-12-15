# Lessons

Detailed breakdown of all hands-on labs and resources throughout the workshop.

---

## 📓 Jupyter Notebooks

Interactive notebooks for hands-on learning. Launch them in Binder or run locally.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/YonSci/vectri-mkdocs/main)

### Python Fundamentals

| Notebook | Description | Launch |
|----------|-------------|--------|
| [Python Setup](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Python_Setup_for_Climate_and_Meteorology_Workshop.ipynb) | Environment setup and configuration | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Python_Setup_for_Climate_and_Meteorology_Workshop.ipynb) |
| [Python Basics](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Python_Basics_for_Climate_and_Meteorology_Workshop1.ipynb) | Variables, data types, control flow | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Python_Basics_for_Climate_and_Meteorology_Workshop1.ipynb) |
| [NumPy](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Numpy_for_Climate_and_Meteorology_Workshop.ipynb) | Array operations and numerical computing | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Numpy_for_Climate_and_Meteorology_Workshop.ipynb) |
| [Pandas](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Pandas_for_Climate_and_Meteorology_Workshop.ipynb) | DataFrames and tabular data | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Pandas_for_Climate_and_Meteorology_Workshop.ipynb) |
| [Matplotlib](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Matplotlib_for_Climate_and_Meteorology_Workshop.ipynb) | Data visualization and plotting | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Matplotlib_for_Climate_and_Meteorology_Workshop.ipynb) |

### Geospatial & Climate Data

| Notebook | Description | Launch |
|----------|-------------|--------|
| [Xarray](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Xarray_for_Climate_and_Meteorology_Workshop.ipynb) | NetCDF and multidimensional arrays | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Xarray_for_Climate_and_Meteorology_Workshop.ipynb) |
| [GeoPandas](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Geopandas_for_Climate_and_Meteorology_Workshop.ipynb) | Vector data and spatial operations | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Geopandas_for_Climate_and_Meteorology_Workshop.ipynb) |
| [Cartopy](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Cartopy_for_Climate_and_Meteorology_Workshop.ipynb) | Map projections and geospatial plotting | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/Cartopy_for_Climate_and_Meteorology_Workshop.ipynb) |
| [CHIRPS Download & Preprocessing](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/01-download-preprocessing-chrips-data.ipynb) | Climate data acquisition workflow | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/01-download-preprocessing-chrips-data.ipynb) |

### VECTRI Modeling

| Notebook | Description | Launch |
|----------|-------------|--------|
| [VECTRI Single Location Demo](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/vectri_single_location_timeseries_demo.ipynb) | Time series demonstration | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/vectri_single_location_timeseries_demo.ipynb) |
| [VECTRI Explicit Equations](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/vectri_single_location_explicit_equations.ipynb) | Core equations implementation | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/vectri_single_location_explicit_equations.ipynb) |
| [VECTRI Physical Plots](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/vectri_single_location_explicit_equations_physical_plots.ipynb) | Equations with visualizations | [![Open](https://img.shields.io/badge/Open-Notebook-blue)](https://github.com/YonSci/vectri-mkdocs/blob/main/notebooks/vectri_single_location_explicit_equations_physical_plots.ipynb) |

---

## 📜 Download Scripts

Python scripts for automated data downloading. All scripts are in the `docs/scripts/` folder.

### Rainfall Data

| Script | Dataset | Description |
|--------|---------|-------------|
| `download_chirps.py` | CHIRPS | Daily rainfall (0.05°, 1981-present) |
| `download_arc2.py` | ARC2 | Africa rainfall (0.1°, 1983-present) |
| `download_tamsat.py` | TAMSAT | Africa rainfall (0.0375°, 1983-present) |
| `download_gfs_precip_forecast.py` | NCEP GFS | Precipitation forecast (0.25°, 0-16 days) |
| `download_ecmwf-hres_precip.py` | ECMWF HRES | Precipitation forecast (0.25°, 0-10 days) |
| `download_ecmwf-s2s-precip.py` | ECMWF S2S | Sub-seasonal precipitation (1.5°, 0-46 days) |
| `download_ecmwf_s2s_precip_daily_ensemble.py` | ECMWF S2S Ensemble | Ensemble precipitation forecasts |
| `download_c3s_seasonal_precip_ensmean_daily.py` | C3S SEAS5 | Seasonal precipitation (0-7 months) |
| `download_chc_cmip6_precip_daily.py` | CHC-CMIP6 | Climate projections (2015-2100) |

### Temperature Data

| Script | Dataset | Description |
|--------|---------|-------------|
| `download_chirts.py` | CHIRTS | Daily temperature (0.05°, 1983-2016) |
| `download_era5-land-temp.py` | ERA5-Land | Reanalysis temperature (0.1°, 1950-present) |
| `download_era5-temp.py` | ERA5 | Reanalysis temperature (0.25°, 1940-present) |
| `download_gfs_temp_forecast.py` | NCEP GFS | Temperature forecast (0.25°, 0-16 days) |
| `download_ecmwf-hres_temp.py` | ECMWF HRES | Temperature forecast (0.25°, 0-10 days) |
| `download_ecmwf-s2s-temp.py` | ECMWF S2S | Sub-seasonal temperature (1.5°, 0-46 days) |
| `download_ecmwf_s2s_temp_daily_ensemble.py` | ECMWF S2S Ensemble | Ensemble temperature forecasts |
| `download_c3s_seasonal_temp_ensmean_daily.py` | C3S SEAS5 | Seasonal temperature (0-7 months) |
| `download_chc_cmip6_temp_daily.py` | CHC-CMIP6 | Temperature projections (2015-2100) |

### Population & Soil Data

| Script | Dataset | Description |
|--------|---------|-------------|
| `download_afripop_worldpop.py` | AfriPop/WorldPop | Population density (100m-1km) |
| `download_worldpop_projections.py` | WorldPop Projections | Population projections (2015-2030) |
| `download_harmonized_world_soil_database.py` | HWSD | Soil texture fractions (~1km) |

---

## 📊 Sample Data

Pre-processed sample datasets for testing and learning (available in `/data/samples/`):

| File | Description | Size |
|------|-------------|------|
| `sample_chirps.nc` | CHIRPS rainfall for Ethiopia | ~10 MB |
| `sample_era5.nc` | ERA5 temperature for Ethiopia | ~15 MB |
| `ethiopia_admin.shp` | Administrative boundaries | ~2 MB |
| `example_sys5.nc` | VECTRI system configuration | ~1 MB |
| `example_data.nc` | VECTRI input data | ~5 MB |

---

## 🚀 Quick Start

### Run Notebooks Locally

```bash
# Clone the repository
git clone https://github.com/YonSci/vectri-mkdocs.git
cd vectri-mkdocs

# Create environment
conda create -n vectri python=3.11 -y
conda activate vectri

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter lab
```

### Run Download Scripts

```bash
# Example: Download CHIRPS data for Ethiopia
python docs/scripts/download_chirps.py \
    --start-date 2020-01-01 \
    --end-date 2020-12-31 \
    --lat-min 3 --lat-max 15 \
    --lon-min 33 --lon-max 48 \
    --output data/chirps_ethiopia_2020.nc
```

---

!!! tip "Need Help?"
    - Check the [Resources](resources.md) page for documentation
    - Review the [Setup](setup.md) guide for installation issues
    - Ask instructors during workshop sessions
    - Collaborate with teammates!

---

## 📚 Related Documentation

- [Climate Data Access](day3/09-climate_data_access_and_extraction.md) - Overview of all datasets
- [VECTRI Model Components](day1/vectri_model_components_larvae_to_hydrology.md) - Model documentation
- [Setup Guide](setup.md) - Installation instructions
