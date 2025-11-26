# Schedule

!!! info "Workshop Hours"
    **Time:** 09:00–17:00 daily (UTC+03:00, Addis Ababa, Ethiopia)  
    **Coffee Breaks:** 10:30–10:45 AM & 3:30–3:45 PM  
    **Lunch:** 12:30–2:00 PM

---

## Day 1 — Foundations and Setup
**Monday, December 8, 2025**

### Morning Session (9:00 AM - 12:30 PM)

| Time | Topic | Type |
|------|-------|------|
| 09:00–09:30 | **Welcome and Workshop Overview** | Plenary |
|  | • Welcoming remarks and Introduction<br>• Training objectives and expected outcomes<br>• Overview of the week's schedule and resources | |
| 09:30–10:30 | **Malaria-Climate Link** | Lecture |
|  | • Climate-sensitive transmission system<br>• Vector life cycle components<br>• Parasite development and EIP<br>• Host and environmental factors<br>• Modeling approaches | |
| 10:30–10:45 | ☕ **Coffee Break** | |
| 10:45–11:15 | **Use Case: Amhara Region Study** | Lecture |
|  | • Regional climate characteristics (Belg and Kiremt seasons)<br>• Case study overview (2013-2019)<br>• Climate anomalies and impacts (El Niño, La Niña)<br>• Spatial patterns and hotspots<br>• Policy implications for early warning | |
| 11:15–12:00 | **VECTRI Overview** | Lecture |
|  | • Model history and development<br>• What VECTRI is and is not<br>• Model structure and capabilities<br>• Inputs, outputs, and applications | |
| 12:00–12:30 | **VECTRI Model Components** | Lecture |
|  | • Larval cycle and breeding site hydrology<br>• Larval mortality (crowding, flushing)<br>• Gonotrophic cycle<br>• Sporogonic cycle<br>• Vector survival<br>• Indoor temperatures and host community | |

### Afternoon Session (2:00 PM - 5:00 PM)

| Time | Topic | Type |
|------|-------|------|
| 14:00–15:00 | **VECTRI Core Equations** | Hands-on |
|  | • Parameter definitions and physical meanings<br>• Larval development equations<br>• Survival probabilities and crowding effects<br>• Gonotrophic and sporogonic cycle rates<br>• Adult survival (Martens II model)<br>• Pond dynamics and hydrology<br>• Host-vector interactions<br>• Transmission metrics (EIR, HBR) | |
| 15:00–15:15 | ☕ **Coffee Break** | |
| 15:15–16:15 | **VECTRI Installation** | Hands-on |
|  | • Installing dependencies (Lua, Lmod, modules)<br>• Setting up compilers (GCC/gfortran)<br>• Installing NetCDF libraries<br>• Cloning VECTRI from GitLab<br>• Compiling VECTRI from source<br>• Testing installation<br>• Troubleshooting common issues | |
| 16:15–17:00 | **Basic Linux Commands** | Hands-on |
|  | • Navigation and file operations<br>• Viewing and searching files<br>• Permissions and environment variables<br>• Text editing basics<br>• Process management<br>• Shell scripting introduction | |


---

## Day 2 — Climate Data Preparation for VECTRI
**Tuesday, December 9, 2025**

### Morning Session (9:00 AM - 12:30 PM)

| Time | Topic | Type |
|------|-------|------|
| 09:00–10:30 | **Climate Data Access and Extraction** | Lecture |
|  | • Accessing ERA5 data via Copernicus Climate Data Store (CDS)<br>• Accessing CHIRPS data via Climate Hazards Center<br>• Understanding NetCDF data format and structure<br>• Using command-line tools (nco, cdo) for data manipulation<br>• Extracting Amhara region subset from global/regional datasets | |
| 10:30–10:45 | ☕ **Coffee Break** | |
| 10:45–12:30 | **Data Quality Control and Processing** | Lecture |
|  | • Checking for missing data, gaps, and anomalies<br>• Handling leap years in climate datasets<br>• Temporal aggregation: sub-daily to daily values<br>• Spatial processing: regridding and resampling<br>• Masking to Amhara region boundaries<br>• Optional: bias correction using gauge observations<br>• Comparing ERA5 vs. CHIRPS precipitation in highlands | |

### Afternoon Session (2:00 PM - 5:00 PM)

| Time | Topic | Type |
|------|-------|------|
| 14:00–15:00 | **Building VECTRI Climate Input Files** | Lecture |
|  | • VECTRI climate file requirements and structure<br>• Creating daily time series with proper dimensions and attributes<br>• Variable naming conventions: temp (°C), rain (mm/day)<br>• Ensuring data consistency and proper formatting<br>• Writing NetCDF files with appropriate metadata | |
| 15:00–15:15 | ☕ **Coffee Break** | |
| 15:15–17:00 | **Lab 2: Climate Data Preparation** | Hands-on |
|  | • Download ERA5 2-m temperature for Amhara (2013-2019)<br>• Download CHIRPS precipitation for Amhara (2013-2019)<br>• Quality control checks and visualization<br>• Temporal aggregation to daily values<br>• Spatial resampling to target grid (0.05° or 0.1°)<br>• Mask to Amhara boundaries<br>• Combine temperature and rainfall into single NetCDF file<br>• Create `climate_amhara_2013_2019.nc`<br>• Validate output file structure and content<br>• Generate summary plots (time series, spatial maps) | |

---

## Day 3 — Environmental Factors and VECTRI Data File
**Wednesday, December 10, 2025**

### Morning Session (9:00 AM - 12:30 PM)

| Time | Topic | Type |
|------|-------|------|
| 09:00–10:30 | **Population Data for Malaria Modeling** | Lecture |
|  | • Role of population in transmission dynamics<br>• Population density and human biting rate scaling<br>• WorldPop dataset overview and access<br>• Population data resolution and accuracy<br>• Temporal considerations: static vs. time-varying population<br>• Resampling population data to model grid<br>• Creating population layer for VECTRI | |
| 10:30–10:45 | ☕ **Coffee Break** | |
| 10:45–12:30 | **Environmental Factors Affecting Transmission** | Lecture |
|  | • Land cover and land use impacts on malaria<br>• Vegetation shading effects on mosquito habitats<br>• Temperature offsets in breeding sites<br>• Elevation and topography considerations<br>• Urban vs. rural transmission dynamics<br>• Water bodies and irrigation systems<br>• Creating land cover proxy variables for VECTRI | |

### Afternoon Session (2:00 PM - 5:00 PM)

| Time | Topic | Type |
|------|-------|------|
| 14:00–15:00 | **VECTRI Environmental Data File Structure** | Lecture |
|  | • Required variables and dimensions<br>• Population density layer format<br>• Optional environmental variables<br>• Coordinate system and projection requirements<br>• Metadata and attributes<br>• Combining multiple environmental layers | |
| 15:00–15:15 | ☕ **Coffee Break** | |
| 15:15–17:00 | **Lab 3: Creating VECTRI Environmental Data File** | Hands-on |
|  | • Download WorldPop population data for Ethiopia<br>• Extract and process Amhara region population<br>• Resample to match climate data grid<br>• Handle missing data and urban centers<br>• Optional: incorporate land cover data<br>• Create VECTRI-compatible data file structure<br>• Build `data_amhara_env.nc` with population layer<br>• Validate spatial alignment with climate file<br>• Create summary maps and statistics<br>• Quality control checks | |

---

## Day 4 — Running and Evaluating VECTRI - Amhara Case Study
**Thursday, December 11, 2025**

### Morning Session (9:00 AM - 12:30 PM)

| Time | Topic | Type |
|------|-------|------|
| 09:00–10:00 | **VECTRI Model Configuration** | Lecture |
|  | • Model parameter files and configuration options<br>• Setting simulation period (2013-2019)<br>• Spin-up period considerations (1-2 years recommended)<br>• Spatial domain setup<br>• Time-step settings<br>• Output variable selection | |
| 10:00–11:00 | **Running VECTRI Simulations** | Demo |
|  | • Command-line execution syntax<br>• Input file specification<br>• Output file naming and structure<br>• Monitoring simulation progress<br>• Common errors and troubleshooting<br>• Computational requirements and runtime | |
| 11:00–11:15 | ☕ **Coffee Break** | |
| 11:15–12:30 | **VECTRI Output Analysis** | Lecture |
|  | • Understanding model outputs: EIR, HBR, Simulated cases<br>• Extracting and processing output variables<br>• Temporal patterns: daily, monthly, seasonal aggregation<br>• Spatial patterns: district-level and gridded outputs | |

### Afternoon Session (2:00 PM - 5:00 PM)

| Time | Topic | Type |
|------|-------|------|
| 14:00–15:30 | **Lab 4: Amhara Case Study Simulation** | Hands-on |
|  | • Run VECTRI for Amhara region (2013-2019)<br>• Monitor simulation and check for errors<br>• Extract EIR, HBR, and case outputs<br>• Create district-level aggregated time series<br>• Calculate monthly and seasonal averages<br>• Prepare data for validation analysis | |
| 15:30–15:45 | ☕ **Coffee Break** | |
| 15:45–17:00 | **Model Validation and Lag Analysis** | Hands-on |
|  | • Comparing simulated EIR with observed EPHI malaria cases<br>• Cross-correlation analysis: EIR vs. reported cases<br>• Identifying optimal lag periods (1-2 months expected)<br>• Calculating model performance metrics (R, RMSE, Nash-Sutcliffe)<br>• Seasonal pattern validation (Belg vs. Kiremt)<br>• Spatial pattern assessment: hotspot identification<br>• District-specific validation<br>• Estimating best-lead warnings for each zone<br>• Identifying model strengths and limitations | |

---

## Day 5 — Toward Operations - Early Warning Prototype
**Friday, December 12, 2025**

### Morning Session (9:00 AM - 12:30 PM)

| Time | Topic | Type |
|------|-------|------|
| 09:00–10:30 | **Spatial and Temporal Analysis of Model Results** | Lecture |
|  | • Creating seasonal composites (Belg and Kiremt seasons)<br>• Analyzing interannual variability (2013-2019)<br>• Climate anomaly analysis: Wet vs. dry years, Warm vs. cool periods<br>• Identifying high-risk districts and time periods<br>• Western highlands vs. eastern lowlands comparison<br>• Mapping transmission hotspots<br>• Visualizing spatio-temporal patterns | |
| 10:30–10:45 | ☕ **Coffee Break** | |
| 10:45–12:30 | **Early Warning System Concepts** | Lecture |
|  | • Components of malaria early warning systems<br>• Integrating climate forecasts (seasonal predictions)<br>• Lead time requirements for interventions<br>• Defining thresholds and triggers: EIR percentiles, Case-exceedance thresholds<br>• District-specific warning criteria<br>• Communicating risk levels to stakeholders<br>• Linking predictions to interventions (ITN distribution, IRS campaigns) | |

### Afternoon Session (2:00 PM - 5:00 PM)

| Time | Topic | Type |
|------|-------|------|
| 14:00–15:30 | **Prototyping an Early Warning Workflow** | Hands-on |
|  | • Designing a simple operational workflow for Amhara<br>• Scenario testing and sensitivity analysis<br>• Automating data processing and model runs<br>• Creating standardized output products: Risk maps, Alert bulletins, Time series dashboards<br>• Challenges and considerations for operational implementation<br>• Resource requirements and capacity building needs | |
| 15:30–15:45 | ☕ **Coffee Break** | |
| 15:45–16:45 | **Participant Presentations** | Presentations |
|  | • Groups present their analyses and findings<br>• Prototype early warning products<br>• Lessons learned and challenges encountered<br>• Discussion and feedback from trainers and peers<br>• Ideas for applying VECTRI in participants' own work | |
| 16:45–17:00 | **Workshop Closing** | Plenary |
|  | • Summary of key learning outcomes<br>• Future research and operational directions<br>• Follow-up support and resources<br>• Training evaluation and feedback<br>• Certificate distribution<br>• Closing remarks | |

---

## Important Notes

!!! tip "Daily Structure"
    - **Morning sessions:** Theory, concepts, and demonstrations
    - **Afternoon sessions:** Hands-on lab work with real Amhara data
    - **Pair work encouraged:** Participants work in pairs during lab sessions
    - **Q&A time:** Built into each session for questions and discussions

!!! info "Materials Provided"
    - All training materials in digital format
    - Code and example scripts via GitHub repository
    - Sample datasets for practice exercises
    - Reference documentation and guides

!!! warning "Preparation"
    - Complete all prerequisites before Day 1
    - Bring personal laptop (Linux preferred, WSL2 for Windows)
    - Test Python and Linux environment in advance
    - Download required software (see Prerequisites page)

---

## Contact & Support

**Questions before the workshop?**  
Email: [yonas.mersha14@gmail.com](mailto:yonas.mersha14@gmail.com)

**Technical setup issues?**  
Check the [Setup](setup.md) and [Prerequisites](prerequisites.md) pages
