# Lesson Redistribution Strategy
## Based on Existing Files Only

---

## Current File Inventory

### Day 1 (8 files)
1. `01-theory_lecture.md` - Malaria-Climate Link
2. `02-use-case.md` - Use Case: Amhara Region
3. `03-setup.md` - Setup
4. `04-basic-linux-commands.md` - Basic Linux Commands
5. `05-vectri-intro.md` - VECTRI Introduction
6. `06-vectri-model-theory-and-code.md` - VECTRI Model Theory & Code
7. `vectri_model_components_larvae_to_hydrology.md` - (not in nav)
8. `vectri_single_location_explicit_equations_physical_plots.md` - (not in nav)

### Day 2 (29 files)
**Python Fundamentals (8 files):**
1. `01-Python_Setup_for_Climate_and_Meteorology_Workshop.md`
2. `02-Python_Basics_for_Climate_and_Meteorology_Workshop.md`
3. `03-Numpy_for_Climate_and_Meteorology_Workshop.md`
4. `04-Pandas_for_Climate_and_Meteorology_Workshop.md`
5. `05-Matplotlib_for_Climate_and_Meteorology_Workshop.md`
6. `06-Xarray_for_Climate_and_Meteorology_Workshop.md`
7. `07-Geopandas_for_Climate_and_Meteorology_Workshop.md`
8. `08-Cartopy_for_Climate_and_Meteorology_Workshop.md`

**Climate Data Access (1 file):**
9. `09-climate_data_access_and_extraction.md`

**Data Download Tutorials (20 files):**
10. `10-download_chirps.md`
11. `11-download_arc2.md`
12. `12-download_tamsat.md`
13. `13-download_gfs_precip_forecast.md`
14. `14-download_gfs_temp_forecast.md`
15. `15-download_ecmwf_hres_precip.md`
16. `15-download_ecmwf_hres_temp.md`
17. `16-download_ecmwf_s2s_tp_daily.md`
18. `17-download_ecmwf_s2s_t2m_daily.md`
19. `18-download_ecmwf_s2s_tp_daily_ensemble.md`
20. `19-download_ecmwf_s2s_tm_daily_ensemble.md`
21. `20-download_chc_cmip6_precip_daily.md`
22. `21-download_chc_cmip6_temp_daily.md`
23. `22-download_chirts_daily.md`
24. `23-download_era5_land_temp_daily.md`
25. `24-download_era5_temp_daily.md`
26. `25-download_worldpop_population.md`
27. `26-download_worldpop_projections.md`
28. `27-download_hwsd_soil_texture.md`
29. `28-download_c3s_seasonal_precip_ensmean_daily.md`
30. `29-download_c3s_seasonal_temp_ensmean_daily.md`

### Day 3 (7 files)
1. `01-data-processing-and-inspecting.md` - VECTRI Data Processing
2. `02-vectri-output-analysis.md` - VECTRI Output Analysis
3. `03-vectri-command-line-tutorial.md` - VECTRI Command Line
4. `04-vectri-hands-on-simulations.md` - VECTRI Hands-On Simulations
5. `05-vectri-configuring-parameters.md` - VECTRI Configuring Parameters
6. `06-vectri-parameter-sensitivity.md` - VECTRI Parameter Sensitivity
7. `07-vectri-analyzing-outputs-visualizations.md` - VECTRI Analyzing Outputs & Visualizations

**Total: 44 files**

---

## Proposed Redistribution

### Day 1: Foundations and Setup (8 lessons)
**Theme**: Introduction, Theory, Setup, and VECTRI Basics

**Keep all Day 1 files:**
1. Malaria-Climate Link (`01-theory_lecture.md`)
2. Use Case (`02-use-case.md`)
3. Setup (`03-setup.md`)
4. Basic Linux Commands (`04-basic-linux-commands.md`)
5. VECTRI Introduction (`05-vectri-intro.md`)
6. VECTRI Model Theory & Code (`06-vectri-model-theory-and-code.md`)
7. VECTRI Model Components (`vectri_model_components_larvae_to_hydrology.md`) - Add to nav
8. VECTRI Equations (`vectri_single_location_explicit_equations_physical_plots.md`) - Add to nav

**Rationale**: All foundational content stays together.

---

### Day 2: Climate Data Preparation (12 lessons)
**Theme**: Python Skills + Climate Data Access

**Python Fundamentals (8 lessons):**
1. Python Setup (`01-Python_Setup_for_Climate_and_Meteorology_Workshop.md`)
2. Python Basics (`02-Python_Basics_for_Climate_and_Meteorology_Workshop.md`)
3. NumPy (`03-Numpy_for_Climate_and_Meteorology_Workshop.md`)
4. Pandas (`04-Pandas_for_Climate_and_Meteorology_Workshop.md`)
5. Matplotlib (`05-Matplotlib_for_Climate_and_Meteorology_Workshop.md`)
6. Xarray (`06-Xarray_for_Climate_and_Meteorology_Workshop.md`)
7. GeoPandas (`07-Geopandas_for_Climate_and_Meteorology_Workshop.md`)
8. Cartopy (`08-Cartopy_for_Climate_and_Meteorology_Workshop.md`)

**Climate Data Access (4 lessons - Core sources):**
9. Climate Data Downloading (`09-climate_data_access_and_extraction.md`)
10. ERA5 Temperature (`24-download_era5_temp_daily.md`) - Primary temperature source
11. CHIRPS Data Download (`10-download_chirps.md`) - Primary precipitation source
12. ERA5-Land Temperature (`23-download_era5_land_temp_daily.md`) - Alternative temperature

**Move to Resources/Reference (16 data download tutorials):**
- ARC2, TAMSAT, GFS, ECMWF variants, C3S, CHC-CMIP6, CHIRTS, WorldPop, HWSD, C3S Seasonal
- These become reference materials, not core lessons

**Rationale**: 
- Focus on essential Python skills needed for data processing
- Keep only primary climate data sources as lessons
- Other data sources are reference materials

---

### Day 3: Environmental Data and VECTRI Setup (10 lessons)
**Theme**: Environmental Data + VECTRI Data File Creation

**Environmental Data (3 lessons):**
1. WorldPop Population (`25-download_worldpop_population.md`)
2. WorldPop Projections (`26-download_worldpop_projections.md`)
3. HWSD Soil Texture (`27-download_hwsd_soil_texture.md`)

**VECTRI Data Processing (4 lessons):**
4. VECTRI Data Processing and Inspecting (`01-data-processing-and-inspecting.md`)
5. VECTRI Command Line Tutorial (`03-vectri-command-line-tutorial.md`)
6. VECTRI Configuring Parameters (`05-vectri-configuring-parameters.md`)
7. VECTRI Hands-On Simulations (`04-vectri-hands-on-simulations.md`)

**Rationale**: 
- Day 3 schedule focuses on environmental factors and creating VECTRI data files
- These lessons directly support Lab 3

---

### Day 4: Running and Evaluating VECTRI (3 lessons)
**Theme**: Model Execution, Output Analysis, and Validation

**Output Analysis and Evaluation:**
1. VECTRI Output Analysis (`02-vectri-output-analysis.md`)
2. VECTRI Analyzing Outputs & Visualizations (`07-vectri-analyzing-outputs-visualizations.md`)
3. VECTRI Parameter Sensitivity (`06-vectri-parameter-sensitivity.md`)

**Rationale**: 
- Day 4 schedule focuses on running simulations and validation
- These lessons support Lab 4 and validation activities
- Output analysis and visualization are key for Day 4

---

### Day 5: Advanced Analysis (0 lessons - but content exists)
**Theme**: Advanced Analysis (content is in Day 4 lessons)

**Note**: The advanced analysis content (seasonality, anomalies, lag analysis) is already included in:
- `07-vectri-analyzing-outputs-visualizations.md` (Advanced Analysis section)

**Rationale**: 
- Day 5 focuses on early warning and advanced applications
- The advanced analysis content in the visualization lesson covers seasonal analysis, interannual variability, and lag analysis
- This aligns with Day 5's focus on spatial/temporal analysis

---

## Summary Table

| Day | Theme | Lessons | Files to Move |
|-----|-------|---------|---------------|
| **Day 1** | Foundations | 8 lessons | None (keep all) |
| **Day 2** | Climate Data Prep | 12 lessons | 16 data download tutorials → Resources |
| **Day 3** | Environmental Data | 10 lessons | None (redistribute from Day 2 & 3) |
| **Day 4** | Running & Evaluation | 3 lessons | From Day 3 |
| **Day 5** | Advanced Analysis | 0 lessons* | Content already in Day 4 lesson |
| **Total** | | **33 core lessons** | 16 reference materials |

*Day 5 uses advanced content from `07-vectri-analyzing-outputs-visualizations.md`

---

## File Movement Plan

### Files to Move to Resources Section (16 files)
Create a new "Data Sources Reference" subsection under Resources:
- `11-download_arc2.md`
- `12-download_tamsat.md`
- `13-download_gfs_precip_forecast.md`
- `14-download_gfs_temp_forecast.md`
- `15-download_ecmwf_hres_precip.md`
- `15-download_ecmwf_hres_temp.md`
- `16-download_ecmwf_s2s_tp_daily.md`
- `17-download_ecmwf_s2s_t2m_daily.md`
- `18-download_ecmwf_s2s_tp_daily_ensemble.md`
- `19-download_ecmwf_s2s_tm_daily_ensemble.md`
- `20-download_chc_cmip6_precip_daily.md`
- `21-download_chc_cmip6_temp_daily.md`
- `22-download_chirts_daily.md`
- `28-download_c3s_seasonal_precip_ensmean_daily.md`
- `29-download_c3s_seasonal_temp_ensmean_daily.md`

### Files to Move Between Day Folders
**From Day 2 → Day 3:**
- `25-download_worldpop_population.md`
- `26-download_worldpop_projections.md`
- `27-download_hwsd_soil_texture.md`

**From Day 3 → Day 4:**
- `02-vectri-output-analysis.md`
- `06-vectri-parameter-sensitivity.md`
- `07-vectri-analyzing-outputs-visualizations.md`

---

## Updated Navigation Structure

```yaml
- Lessons:
    # Day 1: Foundations (8 lessons)
    - Malaria-Climate Link: day1/01-theory_lecture.md
    - Use Case: day1/02-use-case.md
    - Setup: day1/03-setup.md
    - Basic Linux Commands: day1/04-basic-linux-commands.md
    - VECTRI Introduction: day1/05-vectri-intro.md
    - VECTRI Model Theory & Code: day1/06-vectri-model-theory-and-code.md
    - VECTRI Model Components: day1/vectri_model_components_larvae_to_hydrology.md
    - VECTRI Equations: day1/vectri_single_location_explicit_equations_physical_plots.md
    
    # Day 2: Climate Data Preparation (12 lessons)
    - Python Setup: day2/01-Python_Setup_for_Climate_and_Meteorology_Workshop.md
    - Python Basics: day2/02-Python_Basics_for_Climate_and_Meteorology_Workshop.md
    - NumPy: day2/03-Numpy_for_Climate_and_Meteorology_Workshop.md
    - Pandas: day2/04-Pandas_for_Climate_and_Meteorology_Workshop.md
    - Matplotlib: day2/05-Matplotlib_for_Climate_and_Meteorology_Workshop.md
    - Xarray: day2/06-Xarray_for_Climate_and_Meteorology_Workshop.md
    - GeoPandas: day2/07-Geopandas_for_Climate_and_Meteorology_Workshop.md
    - Cartopy: day2/08-Cartopy_for_Climate_and_Meteorology_Workshop.md
    - Climate Data Downloading: day2/09-climate_data_access_and_extraction.md
    - ERA5 Temperature: day2/24-download_era5_temp_daily.md
    - CHIRPS Data Download: day2/10-download_chirps.md
    - ERA5-Land Temperature: day2/23-download_era5_land_temp_daily.md
    
    # Day 3: Environmental Data and VECTRI Setup (10 lessons)
    - WorldPop Population: day3/25-download_worldpop_population.md
    - WorldPop Projections: day3/26-download_worldpop_projections.md
    - HWSD Soil Texture: day3/27-download_hwsd_soil_texture.md
    - VECTRI Data Processing: day3/01-data-processing-and-inspecting.md
    - VECTRI Command Line Tutorial: day3/03-vectri-command-line-tutorial.md
    - VECTRI Configuring Parameters: day3/05-vectri-configuring-parameters.md
    - VECTRI Hands-On Simulations: day3/04-vectri-hands-on-simulations.md
    
    # Day 4: Running and Evaluating VECTRI (3 lessons)
    - VECTRI Output Analysis: day4/02-vectri-output-analysis.md
    - VECTRI Analyzing Outputs & Visualizations: day4/07-vectri-analyzing-outputs-visualizations.md
    - VECTRI Parameter Sensitivity: day4/06-vectri-parameter-sensitivity.md

- Resources:
    - Overview: resources.md
    - Data Sources Reference:
        - ARC2 Data Download: resources/data-sources/11-download_arc2.md
        - TAMSAT Data Download: resources/data-sources/12-download_tamsat.md
        - GFS Precipitation Forecast: resources/data-sources/13-download_gfs_precip_forecast.md
        - GFS Temperature Forecast: resources/data-sources/14-download_gfs_temp_forecast.md
        - ECMWF HRES Precipitation: resources/data-sources/15-download_ecmwf_hres_precip.md
        - ECMWF HRES Temperature: resources/data-sources/15-download_ecmwf_hres_temp.md
        - ECMWF S2S Precipitation: resources/data-sources/16-download_ecmwf_s2s_tp_daily.md
        - ECMWF S2S Temperature: resources/data-sources/17-download_ecmwf_s2s_t2m_daily.md
        - ECMWF S2S Ensemble Precipitation: resources/data-sources/18-download_ecmwf_s2s_tp_daily_ensemble.md
        - ECMWF S2S Ensemble Temperature: resources/data-sources/19-download_ecmwf_s2s_tm_daily_ensemble.md
        - CHC-CMIP6 Precipitation: resources/data-sources/20-download_chc_cmip6_precip_daily.md
        - CHC-CMIP6 Temperature: resources/data-sources/21-download_chc_cmip6_temp_daily.md
        - CHIRTS Daily Temperature: resources/data-sources/22-download_chirts_daily.md
        - C3S Seasonal ECMWF Precipitation: resources/data-sources/28-download_c3s_seasonal_precip_ensmean_daily.md
        - C3S Seasonal ECMWF Temperature: resources/data-sources/29-download_c3s_seasonal_temp_ensmean_daily.md
```

---

## Implementation Steps

1. **Create day4 folder** and move 3 files from day3
2. **Move environmental data files** from day2 to day3
3. **Create resources/data-sources folder** and move 16 reference files
4. **Update mkdocs.yml** with new navigation structure
5. **Add missing Day 1 files** to navigation
6. **Update any internal links** between lessons

---

## Benefits

1. **Balanced Distribution**: 8-12 lessons per day (manageable)
2. **Logical Flow**: Foundations → Data Prep → Execution → Analysis
3. **Schedule Alignment**: Matches daily schedule topics
4. **Reduced Clutter**: Reference materials separated from core lessons
5. **Complete Coverage**: All 5 days have appropriate content
6. **No New Content Needed**: Uses only existing files
