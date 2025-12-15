# 🌍 Climate Data Access and Extraction

Welcome to the comprehensive guide for accessing climate datasets! This page provides you with direct access to various climate data sources essential for VECTRI modeling and climate research.

---

## 🎯 Overview

Climate data forms the backbone of malaria modeling and forecasting. This guide covers:

- **Historical data** for model validation and retrospective analysis
- **Near-real-time data** for operational monitoring
- **Forecast data** (sub-seasonal to seasonal) for early warning systems
- **Climate projections** for impact assessment and planning

!!! info "Data Categories"
    We organize climate data into two main categories:
    
    - **🌧️ Precipitation (Rainfall)** - Critical for vector breeding habitat formation
    - **🌡️ Temperature** - Controls vector and parasite development rates

---

## 🌧️ Precipitation Data Sources

Precipitation data is essential for modeling mosquito breeding site dynamics and population emergence.

### 📊 Historical Rainfall Data

Historical datasets provide validated, quality-controlled rainfall records for model calibration and validation.

<div class="grid cards" markdown>

-   :material-water:{ .lg .middle } __CHIRPS__

    ---

    **Climate Hazards Group InfraRed Precipitation with Station data**
    
    - **Resolution**: 0.05° (~5 km)
    - **Temporal**: Daily, 1981–present
    - **Coverage**: 50°S–50°N globally
    - **Best for**: High-resolution rainfall analysis
    - **Update**: 2-week lag
    
    [:octicons-download-24: Download Tutorial](../resources/data-sources/10-download_chirps.md){ .md-button .md-button--primary }

-   :material-chart-line:{ .lg .middle } __ARC2__

    ---

    **Africa Rainfall Climatology version 2**
    
    - **Resolution**: 0.1° (~10 km)
    - **Temporal**: Daily, 1983–present
    - **Coverage**: Africa only
    - **Best for**: Continental-scale African studies
    - **Update**: 2-day lag
    
    [:octicons-download-24: Download Tutorial](../resources/data-sources/11-download_arc2.md){ .md-button }

-   :material-satellite-variant:{ .lg .middle } __TAMSAT__

    ---

    **Tropical Applications of Meteorology using SATellite**
    
    - **Resolution**: 0.0375° (~4 km)
    - **Temporal**: Daily/Pentadal/Dekadal, 1983–present
    - **Coverage**: Africa (40°S–40°N, 20°W–55°E)
    - **Best for**: African tropical regions
    - **Update**: 2-day lag
    
    [:octicons-download-24: Download Tutorial](../resources/data-sources/11-download_arc2.md){ .md-button }

</div>

---

### ⚡ Near-Real-Time Rainfall Data

Near-real-time products enable operational monitoring and short-term forecasting.

=== "CHIRPS-GEFS"

    **CHIRPS Global Ensemble Forecast System**
    
    !!! success "Recommended for Operations"
        Best choice for near-real-time monitoring with CHIRPS compatibility
    
    **Specifications:**
    
    - **Resolution**: 0.05° (~5 km)
    - **Temporal**: Daily, 16-day forecast
    - **Coverage**: 50°S–50°N globally
    - **Ensemble**: 11 members
    - **Update**: Daily
    - **Latency**: 1-day
    
    **Use Cases:**
    
    - Bridge gap between historical CHIRPS and forecasts
    - Consistent with CHIRPS for seamless integration
    - Operational early warning systems
    
    **Download Script:**
    
    ```python
    # Coming soon - CHIRPS-GEFS download script
    ```

=== "NCEP-GFS"

    **NOAA Global Forecast System**
    
    **Specifications:**
    
    - **Resolution**: 0.25° (~25 km)
    - **Temporal**: 3-hourly to daily, 16-day forecast
    - **Coverage**: Global
    - **Update**: 4 times daily (00, 06, 12, 18 UTC)
    - **Latency**: ~4 hours
    
    **Use Cases:**
    
    - Real-time weather monitoring
    - Short-term precipitation forecasts
    - High temporal resolution needs
    
    **Download Script:**
    
    ```python
    # Coming soon - GFS download script
    ```

=== "ECMWF HRES"

    **ECMWF High-Resolution Forecast**
    
    **Specifications:**
    
    - **Resolution**: 0.1° (~10 km)
    - **Temporal**: Hourly to daily, 10-day forecast
    - **Coverage**: Global
    - **Update**: 2 times daily (00, 12 UTC)
    - **Latency**: ~6 hours
    
    **Use Cases:**
    
    - High-accuracy short-term forecasts
    - Extreme event prediction
    - Research applications
    
    !!! warning "Access Requirements"
        Requires ECMWF account and API key
    
    **Download Script:**
    
    ```python
    # Coming soon - ECMWF HRES download script
    ```

---

### 🔮 Sub-Seasonal Rainfall Forecasts

Sub-seasonal forecasts (weeks 2-6) fill the gap between weather and seasonal predictions.

!!! info "Sub-Seasonal to Seasonal (S2S) Prediction"
    The S2S timescale (2 weeks to 2 months) is critical for malaria early warning, bridging short-term weather and long-term climate forecasts.

**ECMWF S2S**

- **Resolution**: 0.4° (~40 km)
- **Temporal**: Daily, 46-day forecast
- **Coverage**: Global
- **Ensemble**: 51 members
- **Update**: 2 times per week (Monday, Thursday)
- **Best for**: Week 2-6 rainfall probability forecasts

**Key Variables:**

- Total precipitation
- Probability of exceeding thresholds
- Ensemble spread (uncertainty)

**Download Script:**

```python
# Coming soon - ECMWF S2S download script
```

---

### 📅 Seasonal Rainfall Forecasts

Seasonal forecasts (1-6 months ahead) enable strategic planning for malaria control campaigns.

<div class="grid cards" markdown>

-   __ECMWF SEAS5__

    ---
    
    - **Resolution**: 0.4° (~40 km)
    - **Temporal**: Monthly, 7-month forecast
    - **Ensemble**: 51 members
    - **Update**: Monthly
    - **Best for**: Operational seasonal forecasting

-   __NCEP CFSv2__

    ---
    
    - **Resolution**: 0.5° (~50 km)
    - **Temporal**: Daily to monthly, 9-month forecast
    - **Ensemble**: 4 members per day (×4 runs = 16 total)
    - **Update**: Daily
    - **Best for**: North American focus, frequent updates

-   __NMME__

    ---
    
    **North American Multi-Model Ensemble**
    
    - **Resolution**: Variable (0.5°–2°)
    - **Temporal**: Monthly, 12-month forecast
    - **Ensemble**: 100+ members (multi-model)
    - **Update**: Monthly
    - **Best for**: Multi-model consensus forecasts

</div>

**Download Scripts:**

```python
# Coming soon - Seasonal forecast download scripts
```

---

### 🌍 Long-Term Climate Projections

Climate projections assess future malaria risk under different emissions scenarios.

=== "CMIP6"

    **Coupled Model Intercomparison Project Phase 6**
    
    !!! abstract "What is CMIP6?"
        The latest generation of global climate models providing projections through 2100 under various greenhouse gas scenarios (SSPs).
    
    **Specifications:**
    
    - **Resolution**: Variable (0.5°–2°, model-dependent)
    - **Temporal**: Daily to monthly, 1850–2100
    - **Coverage**: Global
    - **Scenarios**: SSP1-2.6, SSP2-4.5, SSP3-7.0, SSP5-8.5
    - **Models**: 50+ international climate models
    
    **Key Variables:**
    
    - Precipitation (pr)
    - Temperature (tas, tasmax, tasmin)
    - Relative humidity
    - Wind speed
    
    **Use Cases:**
    
    - Long-term malaria risk projections
    - Climate change impact assessment
    - Adaptation planning
    
    **Download Script:**
    
    ```python
    # Coming soon - CMIP6 download script
    ```

=== "ISIMIP3b"

    **Inter-Sectoral Impact Model Intercomparison Project**
    
    **Specifications:**
    
    - **Resolution**: 0.5° (~50 km)
    - **Temporal**: Daily, 1850–2100
    - **Coverage**: Global
    - **Scenarios**: SSP1-2.6, SSP3-7.0, SSP5-8.5
    - **Models**: Bias-corrected CMIP6 subset
    
    **Advantages:**
    
    - Bias-corrected for impact modeling
    - Standardized format across models
    - Impact-relevant variables
    
    **Download Script:**
    
    ```python
    # Coming soon - ISIMIP3b download script
    ```

=== "CHC-CMIP6"

    **Climate Hazards Center CMIP6 Rainfall**
    
    **Specifications:**
    
    - **Resolution**: 0.05° (~5 km)
    - **Temporal**: Daily, 1980–2100
    - **Coverage**: 50°S–50°N
    - **Scenarios**: SSP2-4.5, SSP5-8.5
    - **Models**: Downscaled CMIP6
    
    **Advantages:**
    
    - High resolution (consistent with CHIRPS)
    - Bias-corrected to CHIRPS baseline
    - Seamless integration with historical CHIRPS
    
    **Download Script:**
    
    ```python
    # Coming soon - CHC-CMIP6 download script
    ```

=== "CORDEX"

    **Coordinated Regional Climate Downscaling Experiment**
    
    **Specifications:**
    
    - **Resolution**: 0.22° or 0.44° (~25 or 50 km)
    - **Temporal**: Daily, 1950–2100
    - **Coverage**: Regional (Africa, Asia, Europe, etc.)
    - **Scenarios**: RCP2.6, RCP4.5, RCP8.5 (some SSPs)
    - **Models**: Multiple regional climate models (RCMs)
    
    **Regional Domains:**
    
    - **CORDEX-Africa**: AFR-44 (50 km) and AFR-22 (25 km)
    - Other regions available
    
    **Advantages:**
    
    - Higher resolution than global models
    - Better representation of regional processes
    - Topography-sensitive (e.g., Ethiopian highlands)
    
    **Download Script:**
    
    ```python
    # Coming soon - CORDEX download script
    ```

---

## 🌡️ Temperature Data Sources

Temperature data drives vector and parasite development rates in VECTRI.

### 📊 Historical Temperature Data

=== "ERA5"

    **ECMWF Reanalysis v5**
    
    !!! success "Recommended for VECTRI"
        ERA5 is the gold standard for historical temperature data in climate modeling
    
    **Specifications:**
    
    - **Resolution**: 0.25° (~25 km)
    - **Temporal**: Hourly, 1940–present
    - **Coverage**: Global
    - **Variables**: 
        - 2-m temperature (t2m)
        - 2-m dewpoint temperature
        - Surface pressure
        - 10-m winds
        - And 100+ more
    - **Update**: 5-day lag (behind real-time)
    
    **Advantages:**
    
    - High quality, physically consistent
    - Assimilates millions of observations
    - Hourly to monthly aggregations available
    - Excellent for model forcing
    
    **Use Cases:**
    
    - VECTRI model forcing (2013–2019 Amhara case study)
    - Model validation and calibration
    - Climate analysis and trends
    
    **Download Tutorial:**
    
    [:octicons-download-24: View Tutorial](../resources/data-sources/24-download_era5_temp_daily.md){ .md-button .md-button--primary }

=== "ERA5-Land"

    **ECMWF Reanalysis v5 - Land**
    
    **Specifications:**
    
    - **Resolution**: 0.1° (~10 km)
    - **Temporal**: Hourly, 1950–present
    - **Coverage**: Global land areas
    - **Variables**: Land surface variables (temperature, soil moisture, etc.)
    
    **Advantages:**
    
    - Higher resolution than ERA5
    - Better topography representation
    - Improved for land applications
    
    **Download Tutorial:**
    
    [:octicons-download-24: View Tutorial](../resources/data-sources/23-download_era5_land_temp_daily.md){ .md-button .md-button--primary }

---

### ⚡ Near-Real-Time Temperature Data

=== "NCEP-GFS"

    **Global Forecast System**
    
    - **Resolution**: 0.25° (~25 km)
    - **Temporal**: 3-hourly, 16-day forecast
    - **Variables**: T2m, Tmax, Tmin, dewpoint
    - **Update**: 4 times daily
    - **Latency**: ~4 hours
    
    **Download Script:**
    
    ```python
    # Coming soon - GFS temperature download script
    ```

=== "ECMWF HRES"

    **High-Resolution Forecast**
    
    - **Resolution**: 0.1° (~10 km)
    - **Temporal**: Hourly, 10-day forecast
    - **Variables**: T2m, Tmax, Tmin, dewpoint
    - **Update**: 2 times daily
    - **Latency**: ~6 hours
    
    **Download Script:**
    
    ```python
    # Coming soon - ECMWF temperature download script
    ```

---

### 🔮 Sub-Seasonal & Seasonal Temperature Forecasts

**ECMWF S2S**

- **Resolution**: 0.4° (~40 km)
- **Temporal**: Daily, 46-day forecast
- **Ensemble**: 51 members
- **Variables**: T2m, Tmax, Tmin

**ECMWF SEAS5**

- **Resolution**: 0.4° (~40 km)
- **Temporal**: Monthly, 7-month forecast
- **Ensemble**: 51 members
- **Variables**: T2m, Tmax, Tmin

**NCEP CFSv2 & NMME**

- Similar to rainfall products
- Temperature ensemble forecasts available

**Download Scripts:**

```python
# Coming soon - Forecast temperature download scripts
```

---

### 🌍 Long-Term Temperature Projections

**ISIMIP3b (Recommended)**

!!! success "Best for Impact Modeling"
    ISIMIP3b provides bias-corrected, impact-ready climate data
    
**Specifications:**

- **Resolution**: 0.5° (~50 km)
- **Temporal**: Daily, 1850–2100
- **Variables**: tas, tasmax, tasmin, hurs, pr
- **Scenarios**: SSP1-2.6, SSP3-7.0, SSP5-8.5
- **Models**: 5 bias-corrected CMIP6 models

**Available Models:**

- GFDL-ESM4
- IPSL-CM6A-LR
- MPI-ESM1-2-HR
- MRI-ESM2-0
- UKESM1-0-LL

**Advantages:**

- Daily temperature extremes (Tmax, Tmin)
- Bias-corrected to W5E5 reanalysis
- Consistent across sectors
- Impact-model ready

**Download Script:**

```python
# Coming soon - ISIMIP3b download script
```

---

## 📥 General Download Workflow

All datasets follow a similar download workflow:

```mermaid
graph LR
    A[Identify Data Source] --> B[Set Parameters]
    B --> C[Authenticate]
    C --> D[Download]
    D --> E[Process]
    E --> F[Quality Check]
    F --> G[Save]
```

### Common Steps

1. **Identify Requirements**
   - Spatial domain (bounding box or region)
   - Temporal range (start/end dates)
   - Variables needed
   - Resolution requirements

2. **Authentication**
   - Create accounts (CDS, NOAA, etc.)
   - Obtain API keys
   - Configure credentials

3. **Download**
   - Use provided Python scripts
   - Handle large files efficiently
   - Monitor progress

4. **Quality Control**
   - Check for missing data
   - Verify spatial/temporal coverage
   - Validate against known values

5. **Format Conversion**
   - Convert to NetCDF (if needed)
   - Standardize variable names
   - Add metadata

---

## 🛠️ Tools and Libraries

All download scripts use these Python libraries:

```python
# Data access
import cdsapi          # Copernicus Climate Data Store
import requests        # HTTP requests
import ftplib          # FTP downloads

# Data processing
import xarray as xr    # NetCDF handling
import pandas as pd    # Time series
import numpy as np     # Numerical operations

# Geospatial
import rioxarray       # Raster operations
import geopandas as gpd # Vector data
```

**Installation:**

```bash
pip install cdsapi requests xarray pandas numpy rioxarray geopandas netCDF4
```

---

## 📚 Data Access Tutorials

Detailed step-by-step tutorials are available for downloading each dataset. All tutorials can be found in the [Data Sources Reference](../resources/data-sources/) section.

### 🌧️ Precipitation Data Tutorials

| Dataset | Description | Tutorial Link |
|---------|-------------|---------------|
| **CHIRPS** | High-resolution rainfall (0.05°, daily, 1981-present) | [Download Tutorial](../resources/data-sources/10-download_chirps.md) |
| **ARC2** | Africa Rainfall Climatology (0.1°, daily, 1983-present) | [Download Tutorial](../resources/data-sources/11-download_arc2.md) |
| **TAMSAT** | Tropical Applications of Meteorology using SATellite (0.0375°, daily, 1983-present) | [Download Tutorial](../resources/data-sources/12-download_tamsat.md) |
| **GFS Precipitation** | NOAA Global Forecast System precipitation forecasts | [Download Tutorial](../resources/data-sources/13-download_gfs_precip_forecast.md) |
| **ECMWF HRES Precipitation** | ECMWF High-Resolution precipitation forecasts | [Download Tutorial](../resources/data-sources/15-download_ecmwf_hres_precip.md) |
| **ECMWF S2S Precipitation** | ECMWF Sub-Seasonal to Seasonal precipitation forecasts | [Download Tutorial](../resources/data-sources/16-download_ecmwf_s2s_tp_daily.md) |
| **ECMWF S2S Ensemble Precipitation** | ECMWF S2S ensemble precipitation forecasts | [Download Tutorial](../resources/data-sources/18-download_ecmwf_s2s_tp_daily_ensemble.md) |
| **CHC-CMIP6 Precipitation** | Climate Hazards Center CMIP6 downscaled rainfall projections | [Download Tutorial](../resources/data-sources/20-download_chc_cmip6_precip_daily.md) |
| **C3S Seasonal ECMWF Precipitation** | Copernicus Climate Change Service seasonal precipitation forecasts | [Download Tutorial](../resources/data-sources/28-download_c3s_seasonal_precip_ensmean_daily.md) |

### 🌡️ Temperature Data Tutorials

| Dataset | Description | Tutorial Link |
|---------|-------------|---------------|
| **ERA5 Temperature** | ECMWF Reanalysis v5 temperature (0.25°, hourly, 1940-present) | [Download Tutorial](../resources/data-sources/24-download_era5_temp_daily.md) |
| **ERA5-Land Temperature** | ECMWF Reanalysis v5 Land temperature (0.1°, hourly, 1950-present) | [Download Tutorial](../resources/data-sources/23-download_era5_land_temp_daily.md) |
| **GFS Temperature** | NOAA Global Forecast System temperature forecasts | [Download Tutorial](../resources/data-sources/14-download_gfs_temp_forecast.md) |
| **ECMWF HRES Temperature** | ECMWF High-Resolution temperature forecasts | [Download Tutorial](../resources/data-sources/15-download_ecmwf_hres_temp.md) |
| **ECMWF S2S Temperature** | ECMWF Sub-Seasonal to Seasonal temperature forecasts | [Download Tutorial](../resources/data-sources/17-download_ecmwf_s2s_t2m_daily.md) |
| **ECMWF S2S Ensemble Temperature** | ECMWF S2S ensemble temperature forecasts | [Download Tutorial](../resources/data-sources/19-download_ecmwf_s2s_t2m_daily_ensemble.md) |
| **CHC-CMIP6 Temperature** | Climate Hazards Center CMIP6 downscaled temperature projections | [Download Tutorial](../resources/data-sources/21-download_chc_cmip6_temp_daily.md) |
| **CHIRTS Daily Temperature** | Climate Hazards Center InfraRed Temperature with Stations | [Download Tutorial](../resources/data-sources/22-download_chirts_daily.md) |
| **C3S Seasonal ECMWF Temperature** | Copernicus Climate Change Service seasonal temperature forecasts | [Download Tutorial](../resources/data-sources/29-download_c3s_seasonal_temp_ensmean_daily.md) |

### 🌍 Environmental Data Tutorials

| Dataset | Description | Tutorial Link |
|---------|-------------|---------------|
| **WorldPop Population** | High-resolution population density data | [Download Tutorial](../resources/data-sources/25-download_worldpop_population.md) |
| **WorldPop Projections** | Future population projections | [Download Tutorial](../resources/data-sources/26-download_worldpop_projections.md) |
| **HWSD Soil Texture** | Harmonized World Soil Database soil texture data | [Download Tutorial](../resources/data-sources/27-download_hwsd_soil_texture.md) |

!!! tip "Quick Access"
    All data download tutorials are organized in the [Data Sources Reference](../resources/data-sources/) section under Resources. Each tutorial includes:
    - Step-by-step download instructions
    - Python code examples
    - Parameter configuration
    - Quality control checks
    - Data processing tips

---

## 🔗 External Resources

### Data Portals

- [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/) - ERA5, SEAS5, and more
- [CHIRPS Data Portal](https://data.chc.ucsb.edu/products/CHIRPS-2.0/) - CHIRPS rainfall
- [IRI Data Library](https://iridl.ldeo.columbia.edu/) - Climate data repository
- [NOAA PSL](https://psl.noaa.gov/data/gridded/) - Reanalysis and forecasts
- [ISIMIP](https://www.isimip.org/) - Impact model data

### Documentation

- [ECMWF API Documentation](https://www.ecmwf.int/en/forecasts/datasets)
- [CHIRPS Documentation](https://www.chc.ucsb.edu/data/chirps)
- [CMIP6 at ESGF](https://esgf-node.llnl.gov/projects/cmip6/)
- [CORDEX at ESGF](https://cordex.org/data-access/)

### Python API Libraries

- [cdsapi](https://pypi.org/project/cdsapi/) - Copernicus Climate Data Store
- [ecmwf-api-client](https://pypi.org/project/ecmwf-api-client/) - ECMWF public datasets
- [siphon](https://unidata.github.io/siphon/) - THREDDS and weather data

---

## 💡 Tips and Best Practices

!!! tip "Data Selection Strategy"
    
    **For Historical Analysis:**
    
    - Rainfall: CHIRPS (highest resolution)
    - Temperature: ERA5 (best quality)
    
    **For Operational Monitoring:**
    
    - Rainfall: CHIRPS + CHIRPS-GEFS (seamless)
    - Temperature: ERA5 + GFS (consistent)
    
    **For Seasonal Forecasting:**
    
    - Multi-model ensemble (ECMWF SEAS5 + NCEP CFSv2)
    - Downscale/bias-correct to historical baseline
    
    **For Climate Change Studies:**
    
    - ISIMIP3b (bias-corrected, impact-ready)
    - Multiple scenarios (SSP1-2.6, SSP3-7.0, SSP5-8.5)

!!! warning "Common Pitfalls"
    
    - **Large file sizes**: Download by chunks (monthly/yearly)
    - **API limits**: Respect rate limits, use retries
    - **Data gaps**: Always check for missing values
    - **CRS mismatches**: Verify coordinate systems
    - **Time zones**: Be consistent (UTC recommended)

!!! success "Optimization"
    
    - Use spatial subsetting at download (not after)
    - Download overnight for large requests
    - Store in efficient formats (NetCDF4 compressed)
    - Document your data processing pipeline
    - Version control your download scripts

---

## 📞 Support and Help

Need assistance with data access?

- **Workshop Support**: [yonas.mersha14@gmail.com](mailto:yonas.mersha14@gmail.com)
- **CHIRPS Support**: [chc@ucsb.edu](mailto:chc@ucsb.edu)
- **ECMWF Support**: [Copernicus Support](https://support.ecmwf.int/)
- **Community**: [Climate Data Operators Forum](https://code.mpimet.mpg.de/projects/cdo)

---

## 🎯 Next Steps

Ready to start downloading climate data? 

1. **Choose your dataset** based on your needs (historical, forecast, or projection)
2. **Follow the tutorial** for your selected dataset
3. **Run the download script** with your parameters
4. **Quality check** the downloaded data
5. **Proceed to data processing** and VECTRI modeling

[Start with CHIRPS →](../resources/data-sources/10-download_chirps.md){ .md-button .md-button--primary }
[View All Tutorials →](#){ .md-button }
