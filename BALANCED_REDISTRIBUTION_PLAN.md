# Balanced Lesson Redistribution Plan

## Current Distribution (Unbalanced)
- Day 1: 8 lessons
- Day 2: 9 lessons  
- Day 3: 4 lessons
- Day 4: 3 lessons
- Day 5: 0 lessons
**Total: 24 lessons**

## Target Distribution (Balanced)
- Day 1: 5 lessons (Foundations)
- Day 2: 5 lessons (Python Basics + Setup)
- Day 3: 5 lessons (Advanced Python + Climate Data)
- Day 4: 5 lessons (VECTRI Setup + Running)
- Day 5: 4 lessons (Output Analysis + Advanced)
**Total: 24 lessons**

## Proposed Redistribution

### Day 1: Foundations (5 lessons)
**Theme**: Core Theory and VECTRI Introduction
1. Malaria-Climate Link
2. Use Case: Amhara Region Study
3. VECTRI Introduction
4. VECTRI Model Theory & Code
5. VECTRI Model Components

**Move OUT:**
- Setup → Day 2
- Basic Linux Commands → Day 2
- VECTRI Equations → Day 1 (keep, it's theory)

### Day 2: Setup and Python Basics (5 lessons)
**Theme**: Environment Setup and Python Fundamentals
1. Setup
2. Basic Linux Commands
3. Python Setup
4. Python Basics
5. NumPy

**Move IN:**
- Setup (from Day 1)
- Basic Linux Commands (from Day 1)

**Move OUT:**
- Pandas → Day 3
- Matplotlib → Day 3
- Xarray → Day 3
- GeoPandas → Day 3
- Cartopy → Day 3
- Climate Data Downloading → Day 3

### Day 3: Advanced Python and Climate Data (5 lessons)
**Theme**: Data Processing Libraries and Climate Data Access
1. Pandas
2. Matplotlib
3. Xarray
4. GeoPandas
5. Cartopy
6. Climate Data Downloading (Data acquisition)

**Move IN:**
- Pandas, Matplotlib, Xarray, GeoPandas, Cartopy (from Day 2)
- Climate Data Downloading (from Day 2)

**Note**: 6 lessons is acceptable for Day 3 as it's a heavy data processing day

### Day 4: VECTRI Setup and Running (5 lessons)
**Theme**: VECTRI Configuration and Execution
1. VECTRI Data Processing and Inspecting
2. VECTRI Command Line Tutorial
3. VECTRI Configuring Parameters
4. VECTRI Hands-On Simulations
5. VECTRI Output Analysis

**Move IN:**
- VECTRI Output Analysis (from Day 4 - keep it here)

### Day 5: Advanced Analysis (4 lessons)
**Theme**: Output Analysis, Visualization, and Advanced Topics
1. VECTRI Analyzing Outputs & Visualizations
2. VECTRI Parameter Sensitivity
3. (Advanced analysis content from Analyzing Outputs lesson)

**Move IN:**
- VECTRI Analyzing Outputs & Visualizations (from Day 4)
- VECTRI Parameter Sensitivity (from Day 4)

## File Movements Required

### From Day 1 → Day 2:
- `03-setup.md`
- `04-basic-linux-commands.md`

### From Day 2 → Day 3:
- `04-Pandas_for_Climate_and_Meteorology_Workshop.md`
- `05-Matplotlib_for_Climate_and_Meteorology_Workshop.md`
- `06-Xarray_for_Climate_and_Meteorology_Workshop.md`
- `07-Geopandas_for_Climate_and_Meteorology_Workshop.md`
- `08-Cartopy_for_Climate_and_Meteorology_Workshop.md`
- `09-climate_data_access_and_extraction.md`

### From Day 4 → Day 5:
- `07-vectri-analyzing-outputs-visualizations.md`
- `06-vectri-parameter-sensitivity.md`

### From Day 4 → Day 4 (reorganize):
- `02-vectri-output-analysis.md` (keep in Day 4)

## Final Distribution

### Day 1: Foundations (5 lessons)
1. Malaria-Climate Link
2. Use Case
3. VECTRI Introduction
4. VECTRI Model Theory & Code
5. VECTRI Model Components
6. VECTRI Equations

### Day 2: Setup and Python Basics (5 lessons)
1. Setup
2. Basic Linux Commands
3. Python Setup
4. Python Basics
5. NumPy

### Day 3: Advanced Python and Climate Data (6 lessons)
1. Pandas
2. Matplotlib
3. Xarray
4. GeoPandas
5. Cartopy
6. Climate Data Downloading

### Day 4: VECTRI Setup and Running (5 lessons)
1. VECTRI Data Processing and Inspecting
2. VECTRI Command Line Tutorial
3. VECTRI Configuring Parameters
4. VECTRI Hands-On Simulations
5. VECTRI Output Analysis

### Day 5: Advanced Analysis (3 lessons)
1. VECTRI Analyzing Outputs & Visualizations
2. VECTRI Parameter Sensitivity

**Total: 24 lessons**

## Benefits
- More balanced workload (4-6 lessons per day)
- Better alignment with schedule topics
- Logical progression: Foundations → Setup → Data Processing → Model Execution → Analysis
- Day 5 now has content for advanced analysis and early warning

