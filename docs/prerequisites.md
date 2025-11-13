# Prerequisites

!!! tip "Before the Workshop"
    Please ensure you have the following prerequisites completed **before Day 1**. This will help us maximize hands-on learning time!

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

### 2. Software Dependencies

You'll need these installed before the workshop:

#### Core Development Tools
```bash
sudo apt update
sudo apt install -y build-essential gfortran gcc g++ git wget curl
```

#### Python Environment
- **Python:** 3.9 or higher
- **Conda/Miniconda:** [Download here](https://docs.conda.io/en/latest/miniconda.html)

#### Required Libraries (covered in Setup)
- NetCDF C/Fortran
- HDF5
- ZLIB, SZIP, JasPer
- Lmod (module system)

---

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

### 2. Collaboration Tools

- **Slack/Teams:** Join the workshop channel (link provided via email)
- **GitHub:** Account for code sharing (optional but recommended)

---

## Pre-Workshop Checklist

Use this checklist to ensure you're ready:

- [ ] Ubuntu 22.04 LTS environment set up
- [ ] Git, GCC, gfortran installed
- [ ] Miniconda/Anaconda installed
- [ ] CDS account created + API key configured
- [ ] CHIRPS data access confirmed
- [ ] Basic Python packages installed (`pandas`, `numpy`, `matplotlib`, `xarray`)
- [ ] Stable internet connection confirmed
- [ ] Workshop Slack/Teams channel joined
- [ ] GitHub account created (optional)

---

## Test Your Setup

Run this quick test to verify your environment:

```bash
# Check compilers
gcc --version
gfortran --version
python3 --version

# Check Python environment
python3 -c "import pandas, numpy, matplotlib, xarray; print('Python packages OK')"

# Check CDS API
python3 -c "import cdsapi; print('CDS API configured')"
```

!!! success "Ready to Go!"
    If all checks pass, you're ready for Day 1! See you on **15 December 2025**.

---

## Need Help?

If you encounter setup issues:

1. **Check the Setup Guide:** [Setup](setup.md) page has detailed instructions
2. **Email:** [workshop-support@example.org](mailto:workshop-support@example.org)
3. **Slack:** Post in `#technical-help` channel
4. **Office Hours:** Available Dec 12-14, 14:00-16:00 UTC+3

!!! tip "Early Setup Recommended"
    Complete setup at least 3 days before the workshop to allow time for troubleshooting!

