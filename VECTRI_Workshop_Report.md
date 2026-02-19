# Climate-Driven Malaria Modeling with VECTRI  
## Comprehensive Workshop Report (Standard Format)

**Workshop Title:** Climate-Driven Malaria Modeling with VECTRI (One-Week Training Workshop)  
**Workshop Dates (per official schedule):** 8–12 December 2025  
**Location:** Elilly Hotel, Addis Ababa, Ethiopia  
**Prepared for:** Ethiopian Meteorological Institute (EMI) and partners  
**Prepared by:** _[Your Name / Team]_  
**Affiliation:** _[Your Organization]_  
**Report Date:** _[Insert date]_  

> **Note on dates:** The repository contains two different date ranges in different pages (e.g., `docs/index.md` and `docs/schedule.md` show **Dec 8–12, 2025**, while `README.md` mentions **Dec 15–19, 2025**). This report follows the **detailed official agenda in `docs/schedule.md` (Dec 8–12, 2025)**.

---

## Executive Summary

This report documents the one-week “Climate-Driven Malaria Modeling with VECTRI” training workshop delivered in Addis Ababa, Ethiopia. The workshop combined lectures and practical labs to build participant capacity in climate data processing, running the VECTRI malaria transmission model, and analyzing spatio-temporal malaria risk indicators (e.g., **EIR**, **HBR**, vector density, and simulated cases). The training emphasized operational relevance for malaria early warning in Ethiopia—particularly through an Amhara region use case, seasonal lag interpretation, and reproducible workflows for data harmonization, model configuration, and output visualization.

Key outcomes included: improved participant competence in acquiring and preparing climate/environmental inputs (ERA5/CHIRPS; population and soil), executing and troubleshooting VECTRI runs, interpreting VECTRI output groups (input/hydrology/vector/disease), and producing analysis-ready maps and time series for decision support. The workshop also introduced a mini sensitivity suite to demonstrate how parameter uncertainty influences transmission metrics and to reinforce best practices for documenting model configuration.

---

## 1. Background and Rationale

Malaria transmission in Ethiopia is climate-sensitive and varies across space and time. Temperature and rainfall influence mosquito breeding habitat, development rates, survival, biting intensity, and parasite development. Climate variability and anomalies can therefore alter transmission timing and intensity, including in highland fringes where risk may expand under warming conditions.

Process-based models such as **VECTRI** support climate-informed risk analysis by coupling climate forcing, hydrology (breeding habitat), vector dynamics, and disease transmission metrics. This training was designed to strengthen capacity to apply VECTRI for malaria early warning and evidence-based public health decision-making.

---

## 2. Workshop Overview

### 2.1 Purpose

To provide a structured, hands-on training that enables participants to:
- Prepare climate and environmental inputs for VECTRI in consistent NetCDF format
- Compile, configure, and run VECTRI simulations for Ethiopia-focused domains
- Inspect and interpret model outputs and key transmission indicators
- Conduct spatial/temporal analyses and produce clear visualizations for communication
- Understand sensitivity of modeled transmission to selected parameters and assumptions

### 2.2 Organizers and Partners

The workshop was prepared in collaboration between:
- **Swedish Meteorological and Hydrological Institute (SMHI)**
- **Addis Ababa University (AAU)**

With support for and participation from:
- **Ethiopian Meteorological Institute (EMI)**
- **Ethiopian Public Health Institute (EPHI)** (surveillance data context/validation use)

Funding context referenced in the materials:
- Financed by **Sida** under **WACCA-E (phase 2)**.

### 2.3 Target Audience

As described in the materials, the target participants included:
- EMI health, hydrology, and meteorology team members
- MSc/PhD students from AAU
- Experts from EPHI

### 2.4 Learning Outcomes (as stated in the workshop materials)

By the end of the training, participants were expected to be able to:
1. Source, quality check, and preprocess ERA5/CHIRPS climate data into daily, VECTRI-ready NetCDF format (rainfall, 2-m temperature).
2. Compile and run VECTRI; interpret outputs (EIR, HBR, cases) and evaluate lags (EIR → cases).
3. Understand the biological basis of malaria transmission and how climate variables drive vector and parasite dynamics.
4. Create environmental input files (population, soil type/fractions) for VECTRI modeling.
5. Conduct spatial and temporal analysis of model outputs to identify hotspots and seasonal patterns.

---

## 3. Workshop Design and Methodology

### 3.1 Training Approach

The workshop used a blended approach:
- **Lectures** to establish conceptual foundations (malaria–climate links, VECTRI structure, model components).
- **Hands-on sessions** to practice environment setup, climate data processing, model execution, and analysis workflows.
- **Discussion and review** to reinforce interpretation, troubleshooting, and operational framing for early warning.

### 3.2 Tools and Software

The training materials and labs utilized:
- **Python (3.8+)** with Jupyter notebooks
- Core scientific and geospatial Python stack: **NumPy, Pandas, Matplotlib, Xarray, GeoPandas, Cartopy** (and related dependencies)
- NetCDF utilities: **ncdump** and **ncview** for fast inspection and animation
- **VECTRI** (compiled from source; Linux/WSL2 recommended for Windows users)

### 3.3 Data Sources (as referenced in materials)

Primary categories included:
- **Climate (rainfall and temperature)**: CHIRPS, ERA5/ERA5-Land, and others for historical, near-real-time, sub-seasonal, seasonal contexts
- **Population**: AfriPop/WorldPop and projections
- **Soil fractions / soil type**: Harmonized World Soil Database (HWSD)
- **Malaria surveillance**: EPHI confirmed case data (for contextual comparison/validation)
- **Geographic boundaries**: administrative boundaries (e.g., shapefiles such as GADM/GAUL-type products)

---

## 4. Implementation (What Was Done During Training)

### 4.1 Day 1 — Foundations

Core topics included:
- Malaria–climate link, transmission biology, and modeling approaches
- Use case framing (Amhara region; seasonality and anomalies)
- VECTRI overview, model structure, and key components (larval habitat hydrology, gonotrophic/sporogonic cycles, survival)
- VECTRI core equations and parameter interpretation

### 4.2 Day 2–3 — Setup and Climate Data Skills (Python + Data Libraries)

Participants practiced:
- Environment setup and Linux basics (including Windows users via WSL2 guidance)
- Python fundamentals and scientific computing (NumPy)
- Data analysis and visualization (Pandas, Matplotlib)
- Working with NetCDF and multidimensional gridded data (Xarray)
- Geospatial workflows (GeoPandas, Cartopy)
- Overview of climate data access/download workflows

### 4.3 Day 4 — VECTRI Data Preparation, Configuration, Running, and Output Inspection

Hands-on workflows included:
- **Data harmonization** into VECTRI-ready NetCDF format, including:
  - Dimension name standardization
  - Regridding/interpolation to a target grid
  - Unit conversion (e.g., Kelvin → °C; precipitation to mm/day where required)
  - Output files to a `data/processed/` structure
- **Verification and quality control** using a dedicated notebook (`verify_processed_data.ipynb`) and visual inspection.
- **VECTRI configuration and execution** concepts (simulation period selection, spin-up, outputs, common errors).
- **Output inspection** using `ncdump` (metadata, variables, groups) and `ncview` (visual scanning/animation).

### 4.4 Day 5 — Advanced Analysis and Sensitivity

Participants applied a structured analysis workflow to VECTRI outputs:
- Identify and interpret variables across groups:
  - **Input** (forcing, population)
  - **Hydrology** (wpond, wperm, wurbn)
  - **Vector** (larvae, emergence, adult vector density, HBR)
  - **Disease** (CSPR, EIR, PRd, cases, immunity)
- Produce:
  - **Time-mean spatial maps**
  - **Spatially averaged time series**
  - **Monthly climatologies and seasonal composites**
  - **Anomaly analysis and coupling interpretation**
  - **Correlation matrices and spatial correlation maps**
  - **Lag analysis** between climate drivers and transmission indicators (supporting early warning lead-time discussion)
- Run a small **parameter sensitivity mini-pack**:
  - Baseline simulation + one-parameter-at-a-time experiments
  - Verification that parameter settings were captured in output metadata
  - Automated summaries of baseline vs experiment differences (regional and Ethiopia-focused options)

---

## 5. Results and Outputs (Training Deliverables)

### 5.1 Reproducible Processing and Analysis Workflows

The materials provide reproducible workflows for:
- Processing climate/environment inputs into consistent NetCDF
- Running and documenting VECTRI simulations
- Generating standardized visualization outputs (maps + time series)
- Producing sensitivity summary reports (Markdown + CSV)

### 5.2 Conceptual and Practical Competencies Strengthened

Participants strengthened capacity in:
- Interpreting how rainfall and temperature drive hydrology, vectors, and disease metrics
- Understanding and explaining lag effects (e.g., rainfall peaks preceding EIR/case peaks)
- Producing interpretable spatio-temporal products for stakeholders (hotspot maps, seasonal risk profiles)

---

## 6. Use Case Summary: Amhara Region (2013–2019) — Key Messages

The training materials include an Amhara-focused assessment summary highlighting:
- Bimodal rainfall patterns with main Kiremt season (Jun–Sep)
- Typical lag where EIR peaks **1–2 months after peak rainfall**
- Peak transmission often in **Sep–Nov**
- Climate anomaly impacts (e.g., warm years increasing risk even with rainfall deficits)
- Spatial heterogeneity (e.g., western highlands showing higher risk than eastern lowlands)
- Importance of input dataset choice/resolution (CHIRPS vs ERA5 behavior differences)

These findings motivate operational early warning discussions on:
- Trigger windows for interventions timed post-rainfall
- Hotspot identification for targeted resource allocation
- Integrating climate monitoring/forecasting with disease risk indicators

---

## 7. Challenges, Risks, and Mitigations

### 7.1 Common Technical Challenges
- **Environment/installation issues:** especially for Windows users without WSL2
- **Geospatial stack complexity:** Cartopy/GEOS/PROJ dependencies can be brittle on some systems
- **NetCDF inconsistencies:** differing dimension names, coordinate conventions, units
- **Model runtime & configuration errors:** mis-specified domains, missing input variables, spin-up misunderstandings

### 7.2 Mitigations Embedded in the Training
- Step-by-step environment setup guidance and explicit package lists
- Standardized folder layouts for processed data and outputs
- Use of `ncdump`/`ncview` for quick diagnosis
- Verification notebook for processed data quality checks
- Emphasis on documenting configuration via output attributes and logs

---

## 8. Recommendations (Operational and Capacity-Building)

### 8.1 Operationalization Pathway
- **Standardize data pipelines** (scripts + versioned inputs) for routine updates
- **Adopt reproducible run templates** (baseline configs, domain bounds, spin-up conventions)
- **Define actionable thresholds** (e.g., EIR percentiles, exceedance probabilities) aligned with intervention planning calendars
- **Integrate forecast products** (sub-seasonal/seasonal) for lead-time decision support, with clear caveats and validation steps

### 8.2 Model Evaluation and Governance
- Maintain a clear **data provenance log** (sources, versions, retrieval date, processing steps)
- Validate outputs against surveillance and independent climate observations where available
- Use sensitivity experiments to identify parameters most influential for EIR/cases in local contexts
- Establish a cross-institution technical working group (EMI–EPHI–AAU) for maintenance and review

### 8.3 Future Training Enhancements
- Add structured assessments for NumPy/Pandas/NetCDF/VECTRI topics (beyond the existing quiz starter)
- Include a short “capstone” where groups produce a one-page early warning bulletin prototype
- Provide containerized environments (Docker) to reduce installation friction

---

## 9. Conclusion

The VECTRI workshop successfully provided a coherent pathway from climate data acquisition and preprocessing through VECTRI simulation, output inspection, and advanced analysis relevant to malaria early warning. By combining foundational theory with practical workflows and sensitivity exploration, the training strengthened participants’ ability to generate and interpret climate-driven malaria risk products and to communicate findings in an operationally meaningful way.

---

## References

- Workshop site materials in this repository (`docs/`, `notebooks/`, `docs/scripts/`)
- VECTRI documentation referenced in materials (see links in `docs/day4/02-vectri-output-analysis.md`)
- Dataset providers referenced in materials (e.g., CHIRPS, ERA5/ERA5-Land, WorldPop, HWSD)

---

## Appendices

### Appendix A — Workshop Agenda (Summary)

The training was structured across five days:
- **Day 1:** Foundations (malaria–climate link; VECTRI overview; model components; equations)
- **Day 2:** Setup + Python basics (Linux, Python fundamentals, NumPy)
- **Day 3:** Advanced Python + climate data (Pandas/Matplotlib/Xarray/GeoPandas/Cartopy; data access)
- **Day 4:** Data processing and VECTRI runs (harmonization, configuration, running, output inspection)
- **Day 5:** Advanced analysis + sensitivity (visualization workflows; parameter sensitivity; early warning concepts)

For full timing and session details, see `docs/schedule.md`.

### Appendix B — Outputs and Artifacts (Examples)

Depending on the exercises completed, outputs may include:
- Processed inputs in `data/processed/` (e.g., processed precip/temp/pop/soil NetCDF)
- VECTRI outputs in `outputs/` (e.g., `base.nc`, experiment `.nc` files)
- Figures in `figures/` or `output_figures/` (maps, time series, correlations)
- Sensitivity summary artifacts:
  - `outputs/sensitivity_report.md`
  - `outputs/sensitivity_report.csv`

### Appendix C — Privacy Note (Participants)

If you include participant names/emails in any final submitted report, ensure it complies with your organization’s privacy/data protection policy. A safer option is to report aggregated participation statistics (counts by institution) instead of individual contact details.


