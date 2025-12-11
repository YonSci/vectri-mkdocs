# Climate Data Processing Guide

This document provides a step-by-step explanation of the `process_climate_data.py` script. The script is designed to harmonize disparate climate, population, and soil datasets into a unified format suitable for downstream modeling (e.g., VECTRI).

## 1. Overview
The script performs the following core tasks:
- **Inspects** raw NetCDF files for meta-data (resolution, bounding box, units).
- **Standardizes** spatial dimensions (renames `lat`/`lon` to `latitude`/`longitude`).
- **Regrids** all data to match the resolution and domain of the **Precipitation** dataset.
- **Converts Units** (e.g., Kelvin to Celsius, kg/m²/s to mm/day).
- **Formats** attributes and dimensions (e.g., handles specific time dimension requirements).

## 2. Prerequisites
Ensure you have the following Python libraries installed:
```bash
pip install xarray numpy pandas netCDF4 scipy
```
*Note: `scipy` is required for interpolation.*

## 3. Usage
Run the script from the terminal. You can optionally specify the interpolation method.

```bash
# Default (Linear interpolation)
python scripts/process_climate_data.py

# Use Nearest Neighbor (better for population/categorical data)
python scripts/process_climate_data.py --method nearest
```

## 4. Step-by-Step Logic

### Step 1: Configuration & Loading
**What it does**: 
- Defines file paths for Input (Precip, Temp, Soil, Pop) and Output (`data/processed`).
- Loads all datasets using `xarray`.

### Step 2: Data Inspection (`inspect_dataset`)
**What it does**: 
Before processing, the script prints key metadata for every input file:
- **Variables**: Lists available data variables.
- **Resolution**: Calculates the grid step size (e.g., `0.25` degrees).
- **Bounding Box**: Shows the min/max Latitude and Longitude to verify coverage.
- **Time**: Shows the start/end dates and calculates the time step (e.g., `1.0 days`).
- **Units**: Checks the units attribute (e.g., `mm/day`, `Kelvin`).

### Step 3: Dimension Standardization (`standardize_dims`)
**Why this is needed**:
Different datasets often name dimensions differently (e.g., `lat` vs `latitude`, `lon` vs `longitude`). `xarray` requires matching names to regrid correctly.

**What it does**:
- Checks if a dataset uses `lon`/`lat`.
- Renames them to `longitude`/`latitude` to match the target Precipitation dataset.

### Step 4: Defining the Target Grid
**Strategy**: 
The **Precipitation** dataset (`et_pr_1991_2020.nc`) is treated as the "Master Grid".
- All other datasets (Temperature, Population, Soil) will be interpolated (regridded) to match this dataset's grid points and resolution exactly.

### Step 5: Processing Individual Datasets

#### A. Precipitation
- **Action**: The data remains on its original grid.
- **Unit Conversion**: Checks if units are `kg m-2 s-1`. If so, multiplies by `86400` to convert to `mm/day`.
- **Formatting**: Saves variable as `tp` with standard attributes (`_FillValue`, `missing_value`).

#### B. Temperature
- **Action**: Regrids to the Precipitation grid using **Linear Interpolation**.
- **Unit Conversion**: Checks if units are `Kelvin` (`K`). If so, subtracts `273.15` to convert to `deg C`.
- **Formatting**: Saves variable as `t2m`.

#### C. Population
- **Action**: Regrids to the Precipitation grid.
- **Method**: Uses `nearest` neighbor by default (or user selection) to preserve discrete population counts better than linear interpolation.
- **Dimension Handling**: **Removes the time dimension**. The output is a static map `(latitude, longitude)`.
- **attributes**: Sets units to `per km2`.

#### D. Soil Texture
- **Action**: Regrids to the Precipitation grid.
- **Variables**: Extracts `sand`, `silt`, and `clay` fractions.
- **Dimension Handling**: 
  - The script creates a **single time step** (size 1) anchored to the first date of the precipitation data.
  - It saves this time dimension as **UNLIMITED**, allowing future tools (like CDO) to append data if needed.
- **Attributes**: Sets specific physical ranges (`vmin`, `vmax`) for each soil type.

### Step 6: Saving Output
All processed files are saved to `data/processed/` as NetCDF files:
- `precip_processed.nc`
- `temp_processed.nc`
- `pop_processed.nc`
- `soil_processed.nc`

## 5. Troubleshooting
- **Error: `NetCDF: Unknown file format`**: Ensure `netCDF4` is installed (`pip install netCDF4`).
- **Regridding seems wrong**: Check the Inspection output to ensure dimension names were standardized correctly.
