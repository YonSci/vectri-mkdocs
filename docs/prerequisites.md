# Prerequisites

## Technical Requirements

### 1. Hardware & Operating System

**Minimum specifications:**  
- **OS:** Ubuntu 22.04 LTS (recommended) or Ubuntu 20.04 LTS  
- **RAM:** 8 GB minimum, 16 GB recommended  
- **Storage:** 50 GB free disk space  
- **Processor:** Multi-core CPU (4+ cores recommended)  
- **Internet:** Stable connection for data downloads (CHIRPS, ERA5-Land)  

!!! warning "Windows/macOS Users"
    VECTRI runs natively on Linux. If you use Windows or macOS, please set up:
    
    - **Windows:** WSL2 (Windows Subsystem for Linux) with Ubuntu 22.04  
    - **macOS:** Docker container or virtual machine with Ubuntu 22.04  


## Knowledge Prerequisites

### Required Background

!!! info "Essential Knowledge"
    - **Programming:** Basic Python (pandas, numpy, matplotlib)
    - **Command Line:** Comfortable with Linux terminal/bash
    - **Climate Science:** Understanding of precipitation, temperature, climate variables
    - **Public Health:** Basic malaria epidemiology concepts

### Helpful (Not Required)

- Experience with NetCDF/GRIB data formats
- GIS tools (QGIS, ArcGIS) or Python geospatial libraries (xarray, geopandas)
- Fortran compilation (for troubleshooting)
- Climate model output interpretation

---

## Accounts & Access

### 1. Data Access Accounts

Create these accounts **before the workshop**:

| Service | Purpose | Registration Link |
|---------|---------|-------------------|
| **Climate Data Store (CDS)** | ERA5-Land downloads | [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu) |
| **CHIRPS** | Rainfall data | [data.chc.ucsb.edu](https://data.chc.ucsb.edu/products/CHIRPS-2.0/) |
| **Google Earth Engine** | Optional: satellite data | [earthengine.google.com](https://earthengine.google.com/) |

!!! warning "CDS API Setup"
    After registering for CDS, retrieve your API key from your [profile page](https://cds.climate.copernicus.eu/api-how-to) and create `~/.cdsapirc`:
    
    ```
    url: https://cds.climate.copernicus.eu/api/v2
    key: YOUR_UID:YOUR_API_KEY
    ```
