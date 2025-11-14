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

---