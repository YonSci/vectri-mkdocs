# Resources

This page provides links to datasets, tools, documentation, and templates used throughout the workshop.

---

## 📊 Climate & Environmental Data

### Precipitation Data

| Dataset | Resolution | Coverage | Access |
|---------|-----------|----------|--------|
| **CHIRPS** | 0.05° (~5km) | 1981-present | [CHC UCSB](https://data.chc.ucsb.edu/products/CHIRPS-2.0/) |
| **TAMSAT** | 0.0375° (~4km) | 1983-present | [TAMSAT](https://www.tamsat.org.uk/data) |
| **GPM IMERG** | 0.1° (~11km) | 2000-present | [NASA GES DISC](https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDF_06/summary) |

### Temperature & Reanalysis

| Dataset | Resolution | Coverage | Access |
|---------|-----------|----------|--------|
| **ERA5-Land** | 0.1° (~9km) | 1950-present | [CDS](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land) |
| **CHIRTS-daily** | 0.05° (~5km) | 1983-2016 | [CHC UCSB](https://www.chc.ucsb.edu/data/chirtsdaily) |
| **TerraClimate** | ~4km | 1958-present | [TerraClimate](https://www.climatologylab.org/terraclimate.html) |

---

## 🗺️ Population & Administrative Boundaries

### Population Data

- **WorldPop:** [worldpop.org](https://www.worldpop.org/)  
  High-resolution population grids (100m-1km)

- **HRSL (Facebook/Meta):** [data.humdata.org](https://data.humdata.org/organization/facebook)  
  30m resolution population density

- **LandScan:** [landscan.ornl.gov](https://landscan.ornl.gov/)  
  1km global population (requires registration)

### Administrative Boundaries

- **GADM:** [gadm.org](https://gadm.org/)  
  Global administrative areas (levels 0-5), shapefiles

- **GAUL (FAO):** [FAO GeoNetwork](https://www.fao.org/geonetwork/)  
  Global administrative unit layers

- **geoBoundaries:** [geoboundaries.org](https://www.geoboundaries.org/)  
  Open political boundaries

---

## 🦟 VECTRI Model Resources

### Official Documentation

- **VECTRI GitHub:** [github.com/ICTP/vectri](https://github.com/ICTP/vectri)
- **ICTP Documentation:** [www.ictp.it](https://www.ictp.it/) (search "VECTRI")
- **User Manual:** [VECTRI_Manual.pdf](https://github.com/ICTP/vectri/blob/main/docs/VECTRI_Manual.pdf)

### Sample Configuration Files

Download workshop templates:

```bash
# Clone workshop repository
git clone https://github.com/your-org/vectri-workshop-2025.git
cd vectri-workshop-2025/configs/
```

**Available configs:**
- `example_sys5.nc` — System configuration (grid, parameters)
- `example_data.nc` — Input climate data template
- `vectri_params.yml` — Parameter sweep configurations
- `run_vectri.sh` — Batch submission script

---

## 🐍 Python Environment Setup

### Conda Environment File

Save as `environment.yml`:

```yaml
name: vectri-workshop
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy>=1.24
  - pandas>=2.0
  - xarray>=2023.1
  - netcdf4
  - matplotlib>=3.7
  - seaborn
  - cartopy
  - geopandas
  - rasterio
  - folium
  - streamlit>=1.28
  - jupyterlab
  - cdsapi
  - requests
  - pyyaml
  - scipy
  - scikit-learn
  - pip
  - pip:
    - streamlit-folium
```

**Install:**
```bash
conda env create -f environment.yml
conda activate vectri-workshop
```

---

## 📈 Health Surveillance Data

### DHIS2 / HMIS Data

!!! warning "Data Privacy"
    Health data is sensitive. Follow your organization's data governance policies.

- **DHIS2 API:** [docs.dhis2.org](https://docs.dhis2.org/en/develop/using-the-api/dhis-core-version-master/introduction.html)
- **Example query scripts:** Available in workshop repo `/scripts/dhis2_fetch.py`

### Survey Data (DHS/MIS)

- **DHS Program:** [dhsprogram.com](https://dhsprogram.com/)  
  Demographic and Health Surveys with malaria indicators

- **MIS (Malaria Indicator Surveys):** [malariasurveys.org](https://www.malariasurveys.org/)

---

## 🛠️ Software & Tools

### Required Software

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Python 3.9+** | Data processing | [python.org](https://www.python.org/) |
| **Miniconda** | Environment manager | [docs.conda.io](https://docs.conda.io/en/latest/miniconda.html) |
| **Git** | Version control | [git-scm.com](https://git-scm.com/) |
| **GCC/gfortran** | VECTRI compilation | `sudo apt install build-essential gfortran` |
| **Lmod** | Module system | [lmod.readthedocs.io](https://lmod.readthedocs.io/) |

### Recommended GIS Tools

- **QGIS:** [qgis.org](https://qgis.org/) — Open-source GIS desktop
- **VS Code:** [code.visualstudio.com](https://code.visualstudio.com/) — Code editor
- **Jupyter:** [jupyter.org](https://jupyter.org/) — Interactive notebooks

---

## 📚 Reference Materials

### Scientific Papers

1. **Tompkins & Ermert (2013):** "A regional-scale, high resolution dynamical malaria model..."  
   [DOI:10.1186/1475-2875-12-390](https://doi.org/10.1186/1475-2875-12-390)

2. **Yamana et al. (2016):** "Climate change unlikely to increase malaria burden..."  
   [DOI:10.1038/nclimate3065](https://doi.org/10.1038/nclimate3065)

3. **Tompkins & McCreesh (2016):** "Migration and malaria transmission potential..."  
   [DOI:10.1088/1748-9326/11/2/024006](https://doi.org/10.1088/1748-9326/11/2/024006)

### Books & Guides

- **Climate and Health:** WHO Climate and Health Country Profiles  
  [who.int/data/climate-change](https://www.who.int/data/climate-change)

- **NetCDF Operators (NCO):** [nco.sourceforge.net](http://nco.sourceforge.net/)

---

## 🎥 Video Tutorials

*Coming soon: Workshop lecture recordings will be posted here after the event.*

- Day 1: Data Pipeline & VECTRI Introduction
- Day 2: Model Configuration & Baseline Runs
- Day 3: Calibration & Validation
- Day 4: Forecasting & Scenarios
- Day 5: Decision Products & Dashboards

---

## 💻 Code Repositories

### Workshop Materials

- **Main Repository:** [github.com/your-org/vectri-workshop-2025](https://github.com/your-org/vectri-workshop-2025)
- **Lab Notebooks:** `/notebooks/` directory
- **Sample Data:** `/data/samples/` (small test datasets)
- **Scripts:** `/scripts/` (automation helpers)

### Community Resources

- **VECTRI Examples:** [github.com/ICTP/vectri/examples](https://github.com/ICTP/vectri/tree/main/examples)
- **Climate Data Processing:** [xarray.pydata.org/en/stable/tutorials](https://xarray.pydata.org/en/stable/tutorials-and-videos.html)

---

## 🎓 Additional Training

### Online Courses

- **ECMWF Summer of Weather Code:** [ecmwf.int](https://www.ecmwf.int/en/learning/workshops/summer-weather-code)
- **UCAR Climate Data Guide:** [climatedataguide.ucar.edu](https://climatedataguide.ucar.edu/)
- **Kaggle Climate Challenges:** [kaggle.com/competitions](https://www.kaggle.com/competitions)

### Upcoming Workshops

- **ICTP Earth System Physics:** [indico.ictp.it](https://indico.ictp.it/)
- **WMO Training Events:** [public.wmo.int/en/resources/training](https://public.wmo.int/en/resources/training)

---

## 💬 Support & Community

- **Workshop Slack:** `#vectri-workshop-2025` (invitation sent via email)
- **GitHub Issues:** Report bugs or ask questions in repo issues
- **Email Support:** [workshop-support@example.org](mailto:workshop-support@example.org)

---

## 📦 Downloads

### Quick Start Package

Download the complete workshop starter package (includes sample data, configs, and notebooks):

**[📥 Download Workshop Package (1.2 GB)](https://example.org/vectri-workshop-package.zip)**

Contents:
```
vectri-workshop-package/
├── data/
│   ├── chirps_sample.nc
│   ├── era5_sample.nc
│   └── admin_boundaries/
├── configs/
│   ├── example_sys5.nc
│   └── vectri_params.yml
├── notebooks/
│   ├── 01_data_download.ipynb
│   ├── 02_preprocessing.ipynb
│   └── ... (all 13 labs)
└── environment.yml
```

---

!!! tip "Bookmark This Page"
    Keep this resources page handy throughout the workshop!
