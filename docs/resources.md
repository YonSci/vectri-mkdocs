# Resources

This page provides links to datasets, tools, documentation, and templates used throughout the workshop.

---

## 📊 Climate & Environmental Data

### Rainfall Data

=== "Historical"

    | Dataset | Resolution | Coverage | Access | Download Script |
    |---------|-----------|----------|--------|-----------------|
    | **CHIRPS** | 0.05° (~5km) | 1981-present | [CHC UCSB](https://data.chc.ucsb.edu/products/CHIRPS-2.0/) | [download_chirps.py](scripts/download_chirps.py) |
    | **ARC2** | 0.1° (~10km) | 1983-present | [CPC NOAA](https://ftp.cpc.ncep.noaa.gov/fews/fewsdata/africa/arc2/) | [download_arc2.py](scripts/download_arc2.py) |
    | **TAMSAT** | 0.0375° (~4km) | 1983-present | [TAMSAT](https://www.tamsat.org.uk/data) | [download_tamsat.py](scripts/download_tamsat.py) |
    | **GPM IMERG** | 0.1° (~11km) | 2000-present | [NASA GES DISC](https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDF_06/summary) | — |

=== "Near-Real-Time"

    | Dataset | Resolution | Lead Time | Access | Download Script |
    |---------|-----------|-----------|--------|-----------------|
    | **NCEP GFS** | 0.25° | 0-16 days | [NOMADS](https://nomads.ncep.noaa.gov/) | [download_gfs_precip_forecast.py](scripts/download_gfs_precip_forecast.py) |
    | **ECMWF HRES** | 0.25° | 0-10 days | [ECMWF Open Data](https://www.ecmwf.int/en/forecasts/datasets/open-data) | [download_ecmwf-hres_precip.py](scripts/download_ecmwf-hres_precip.py) |

=== "Sub-Seasonal"

    | Dataset | Resolution | Lead Time | Access | Download Script |
    |---------|-----------|-----------|--------|-----------------|
    | **ECMWF S2S** | 1.5° | 0-46 days | [ECMWF](https://www.ecmwf.int/en/forecasts/datasets/extended-range) | [download_ecmwf-s2s-precip.py](scripts/download_ecmwf-s2s-precip.py) |
    | **ECMWF S2S Ensemble** | 1.5° | 0-46 days | [ECMWF](https://www.ecmwf.int/en/forecasts/datasets/extended-range) | [download_ecmwf_s2s_precip_daily_ensemble.py](scripts/download_ecmwf_s2s_precip_daily_ensemble.py) |

=== "Seasonal"

    | Dataset | Resolution | Lead Time | Access | Download Script |
    |---------|-----------|-----------|--------|-----------------|
    | **ECMWF SEAS5 (C3S)** | 1° | 0-7 months | [CDS](https://cds.climate.copernicus.eu/) | [download_c3s_seasonal_precip_ensmean_daily.py](scripts/download_c3s_seasonal_precip_ensmean_daily.py) |
    | **NCEP CFSv2** | 1° | 0-9 months | [NCEP](https://www.ncep.noaa.gov/) | — |
    | **NMME** | 1° | 0-12 months | [NOAA](https://www.cpc.ncep.noaa.gov/products/NMME/) | — |

=== "Climate Projections"

    | Dataset | Resolution | Period | Access | Download Script |
    |---------|-----------|--------|--------|-----------------|
    | **CHC-CMIP6** | 0.05° (~5km) | 2015-2100 | [CHC UCSB](https://www.chc.ucsb.edu/) | [download_chc_cmip6_precip_daily.py](scripts/download_chc_cmip6_precip_daily.py) |
    | **CMIP6** | Variable | 1850-2100 | [ESGF](https://esgf-node.llnl.gov/projects/cmip6/) | — |
    | **ISIMIP3b** | 0.5° | 1850-2100 | [ISIMIP](https://www.isimip.org/) | — |
    | **CORDEX-Africa** | 0.44° (~50km) | 1950-2100 | [ESGF](https://esgf-node.llnl.gov/projects/cordex/) | — |

---

### Temperature Data

=== "Historical"

    | Dataset | Resolution | Coverage | Access | Download Script |
    |---------|-----------|----------|--------|-----------------|
    | **CHIRTS-daily** | 0.05° (~5km) | 1983-2016 | [CHC UCSB](https://www.chc.ucsb.edu/data/chirtsdaily) | [download_chirts.py](scripts/download_chirts.py) |
    | **ERA5-Land** | 0.1° (~9km) | 1950-present | [CDS](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land) | [download_era5-land-temp.py](scripts/download_era5-land-temp.py) |
    | **ERA5** | 0.25° (~25km) | 1940-present | [CDS](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels) | [download_era5-temp.py](scripts/download_era5-temp.py) |
    | **TerraClimate** | ~4km | 1958-present | [TerraClimate](https://www.climatologylab.org/terraclimate.html) | — |

=== "Near-Real-Time"

    | Dataset | Resolution | Lead Time | Access | Download Script |
    |---------|-----------|-----------|--------|-----------------|
    | **NCEP GFS** | 0.25° | 0-16 days | [NOMADS](https://nomads.ncep.noaa.gov/) | [download_gfs_temp_forecast.py](scripts/download_gfs_temp_forecast.py) |
    | **ECMWF HRES** | 0.25° | 0-10 days | [ECMWF Open Data](https://www.ecmwf.int/en/forecasts/datasets/open-data) | [download_ecmwf-hres_temp.py](scripts/download_ecmwf-hres_temp.py) |

=== "Sub-Seasonal"

    | Dataset | Resolution | Lead Time | Access | Download Script |
    |---------|-----------|-----------|--------|-----------------|
    | **ECMWF S2S** | 1.5° | 0-46 days | [ECMWF](https://www.ecmwf.int/en/forecasts/datasets/extended-range) | [download_ecmwf-s2s-temp.py](scripts/download_ecmwf-s2s-temp.py) |
    | **ECMWF S2S Ensemble** | 1.5° | 0-46 days | [ECMWF](https://www.ecmwf.int/en/forecasts/datasets/extended-range) | [download_ecmwf_s2s_temp_daily_ensemble.py](scripts/download_ecmwf_s2s_temp_daily_ensemble.py) |

=== "Seasonal"

    | Dataset | Resolution | Lead Time | Access | Download Script |
    |---------|-----------|-----------|--------|-----------------|
    | **ECMWF SEAS5 (C3S)** | 1° | 0-7 months | [CDS](https://cds.climate.copernicus.eu/) | [download_c3s_seasonal_temp_ensmean_daily.py](scripts/download_c3s_seasonal_temp_ensmean_daily.py) |
    | **NCEP CFSv2** | 1° | 0-9 months | [NCEP](https://www.ncep.noaa.gov/) | — |
    | **NMME** | 1° | 0-12 months | [NOAA](https://www.cpc.ncep.noaa.gov/products/NMME/) | — |

=== "Climate Projections"

    | Dataset | Resolution | Period | Access | Download Script |
    |---------|-----------|--------|--------|-----------------|
    | **CHC-CMIP6** | 0.05° (~5km) | 2015-2100 | [CHC UCSB](https://www.chc.ucsb.edu/) | [download_chc_cmip6_temp_daily.py](scripts/download_chc_cmip6_temp_daily.py) |
    | **CMIP6** | Variable | 1850-2100 | [ESGF](https://esgf-node.llnl.gov/projects/cmip6/) | — |
    | **ISIMIP3b** | 0.5° | 1850-2100 | [ISIMIP](https://www.isimip.org/) | — |
    | **CORDEX-Africa** | 0.44° (~50km) | 1950-2100 | [ESGF](https://esgf-node.llnl.gov/projects/cordex/) | — |

---

## 🗺️ Population & Environmental Data

### Population Data

| Dataset | Resolution | Coverage | Access | Download Script |
|---------|-----------|----------|--------|-----------------|
| **AfriPop (WorldPop)** | 100m-1km | Africa | [WorldPop](https://www.worldpop.org/) | [download_afripop_worldpop.py](scripts/download_afripop_worldpop.py) |
| **WorldPop Projections** | 1km | Global, 2015-2030 | [WorldPop](https://www.worldpop.org/) | [download_worldpop_projections.py](scripts/download_worldpop_projections.py) |
| **HRSL (Meta)** | 30m | Global | [HDX](https://data.humdata.org/organization/facebook) | — |
| **LandScan** | 1km | Global | [ORNL](https://landscan.ornl.gov/) | Registration required |

### Soil Data

| Dataset | Resolution | Coverage | Access | Download Script |
|---------|-----------|----------|--------|-----------------|
| **HWSD** | ~1km | Global | [ISIMIP](https://www.isimip.org/) | [download_harmonized_world_soil_database.py](scripts/download_harmonized_world_soil_database.py) |
| **SoilGrids** | 250m | Global | [ISRIC](https://soilgrids.org/) | — |

### Administrative Boundaries

| Dataset | Description | Access |
|---------|-------------|--------|
| **GADM** | Global administrative areas (levels 0-5), shapefiles | [gadm.org](https://gadm.org/) |
| **GAUL (FAO)** | Global administrative unit layers | [FAO GeoNetwork](https://www.fao.org/geonetwork/) |
| **geoBoundaries** | Open political boundaries | [geoboundaries.org](https://www.geoboundaries.org/) |

### Malaria Data

| Dataset | Description | Access |
|---------|-------------|--------|
| **EPHI Case Data** | Ethiopia confirmed malaria cases | Ethiopian Public Health Institute |
| **MAP** | Malaria Atlas Project - prevalence maps | [malariaatlas.org](https://malariaatlas.org/) |
| **WHO GHO** | Global malaria statistics | [WHO](https://www.who.int/data/gho/data/themes/malaria) |

---

## 📓 Lecture Notes, Scripts & Data

### Workshop Materials

<div class="grid cards" markdown>

-   :material-presentation: **Lecture Notes**
    
    ---
    
    - [Day 1: Malaria-Climate Link](lecture/Climate-Malaria-Link.pdf)
    
-   :material-language-python: **Python Tutorials**
    
    ---
    
    - [Python Basics](day2/02-Python_Basics_for_Climate_and_Meteorology_Workshop.md)
    - [NumPy](day2/03-Numpy_for_Climate_and_Meteorology_Workshop.md)
    - [Pandas](day2/04-Pandas_for_Climate_and_Meteorology_Workshop.md)
    - [Matplotlib](day2/05-Matplotlib_for_Climate_and_Meteorology_Workshop.md)
    - [Xarray](day2/06-Xarray_for_Climate_and_Meteorology_Workshop.md)
    - [GeoPandas](day2/07-Geopandas_for_Climate_and_Meteorology_Workshop.md)
    - [Cartopy](day2/08-Cartopy_for_Climate_and_Meteorology_Workshop.md)

-   :material-download: **Download Scripts**
    
    ---
    
    All scripts are available in the `scripts/` folder:
    
    - Rainfall: CHIRPS, ARC2, TAMSAT, GFS, ECMWF
    - Temperature: CHIRTS, ERA5, ERA5-Land, GFS, ECMWF
    - Population: WorldPop, AfriPop
    - Soil: HWSD

-   :material-database: **Sample Data**
    
    ---
    
    Pre-processed sample datasets for Ethiopia:
    
    - Climate forcing (NetCDF)
    - Population grids (GeoTIFF)
    - Administrative boundaries (Shapefile)
    - Example VECTRI outputs

</div>

### Quick Access to Download Tutorials

| Category | Tutorial | Script |
|----------|----------|--------|
| **Rainfall** | [CHIRPS](day2/10-download_chirps.md) | `download_chirps.py` |
| | [ARC2](day2/11-download_arc2.md) | `download_arc2.py` |
| | [TAMSAT](day2/12-download_tamsat.md) | `download_tamsat.py` |
| | [GFS Precipitation](day2/13-download_gfs_precip_forecast.md) | `download_gfs_precip_forecast.py` |
| | [ECMWF HRES Precip](day2/15-download_ecmwf_hres_precip.md) | `download_ecmwf-hres_precip.py` |
| | [ECMWF S2S Precip](day2/16-download_ecmwf_s2s_tp_daily.md) | `download_ecmwf-s2s-precip.py` |
| | [CHC-CMIP6 Precip](day2/20-download_chc_cmip6_precip_daily.md) | `download_chc_cmip6_precip_daily.py` |
| **Temperature** | [CHIRTS](day2/22-download_chirts_daily.md) | `download_chirts.py` |
| | [ERA5-Land](day2/23-download_era5_land_temp_daily.md) | `download_era5-land-temp.py` |
| | [ERA5](day2/24-download_era5_temp_daily.md) | `download_era5-temp.py` |
| | [GFS Temperature](day2/14-download_gfs_temp_forecast.md) | `download_gfs_temp_forecast.py` |
| | [ECMWF HRES Temp](day2/15-download_ecmwf_hres_temp.md) | `download_ecmwf-hres_temp.py` |
| | [ECMWF S2S Temp](day2/17-download_ecmwf_s2s_t2m_daily.md) | `download_ecmwf-s2s-temp.py` |
| | [CHC-CMIP6 Temp](day2/21-download_chc_cmip6_temp_daily.md) | `download_chc_cmip6_temp_daily.py` |
| **Population** | [WorldPop](day2/25-download_worldpop_population.md) | `download_afripop_worldpop.py` |
| | [WorldPop Projections](day2/26-download_worldpop_projections.md) | `download_worldpop_projections.py` |
| **Soil** | [HWSD](day2/27-download_hwsd_soil_texture.md) | `download_harmonized_world_soil_database.py` |

---

## 🦟 VECTRI Model Resources

### Official Documentation

- **VECTRI GitLab:** [gitlab.com/tompkins/vectri](https://gitlab.com/tompkins/vectri)
- **ICTP Documentation:** [www.ictp.it](https://www.ictp.it/) (search "VECTRI")
- **User Manual:** Available in the VECTRI repository

---

## 🛠️ Software & Tools

### Required Software

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Python 3.9+** | Data processing | [python.org](https://www.python.org/) |
| **Miniconda** | Environment manager | [docs.conda.io](https://docs.conda.io/en/latest/miniconda.html) |
| **Git** | Version control | [git-scm.com](https://git-scm.com/) |
| **GCC/gfortran** | VECTRI compilation | `sudo apt install build-essential gfortran` |
| **WSL 2** | Linux on Windows | [Setup Guide](setup.md) |

### Recommended Tools

| Tool | Purpose | Link |
|------|---------|------|
| **VS Code** | Code editor | [code.visualstudio.com](https://code.visualstudio.com/) |
| **Jupyter** | Interactive notebooks | [jupyter.org](https://jupyter.org/) |
| **Docker** | Containerization | [docker.com](https://www.docker.com/) |
| **QGIS** | GIS visualization | [qgis.org](https://qgis.org/) |

---

## 📚 Reference Materials

### Scientific Papers

1. **Tompkins & Ermert (2013):** "A regional-scale, high resolution dynamical malaria model..."  
   [DOI:10.1186/1475-2875-12-390](https://doi.org/10.1186/1475-2875-12-390)

2. **Yamana et al. (2016):** "Climate change unlikely to increase malaria burden..."  
   [DOI:10.1038/nclimate3065](https://doi.org/10.1038/nclimate3065)

3. **Tompkins & McCreesh (2016):** "Migration and malaria transmission potential..."  
   [DOI:10.1088/1748-9326/11/2/024006](https://doi.org/10.1088/1748-9326/11/2/024006)

---


## 💻 Code Repositories

### Workshop Materials

| Repository | Description | Link |
|------------|-------------|------|
| **Workshop Docs** | This documentation site | [GitHub](https://github.com/YonSci/vectri-mkdocs) |
| **VECTRI Model** | Official VECTRI source code | [GitLab](https://gitlab.com/tompkins/vectri) |
| **Binder** | Interactive notebooks | [Launch Binder](https://mybinder.org/v2/gh/YonSci/vectri-mkdocs/main) |

---
