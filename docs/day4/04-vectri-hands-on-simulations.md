# VECTRI Hands-On: Running Simulations & Analyzing Outputs

---

**What you'll learn:**

- Cold Start initialization
- Spinning up the model
- Restarting the model
- Creating a constant climate driver file
- Creating ensemble runs
- Quick output analysis techniques

---

This practical guide walks you through **simulation initialization workflows** in VECTRI and gives a lightweight, repeatable approach to **checking and analyzing outputs**.

You can follow these steps using the **tutorial data** (e.g., `example_sys5.nc`, `example_sys5.grb`, `example_data.nc`, `vectri_calibrated.options`, etc.).

!!! note
    If your files have different names, just substitute accordingly.

---

## 0) Suggested Folder Setup

Keep your **code** and **runs** separated:

```
$HOME/vectri                       # code directory (example)
$HOME/myruns/vectri_sim_tutorial   # run directory
```

Navigate to your run folder:

```bash
cd $HOME/myruns/vectri_sim_tutorial
```

List the files:

```bash
ls
```

You should see files similar to:

| File | Description |
|------|-------------|
| `example_sys5.nc` / `example_sys5.grb` | Climate data |
| `example_data.nc` | Population/ancillary data |
| `vectri_calibrated.options` | Model options |
| `example_data_wperm.nc`, `example_wperm.nc` | (optional) Permanent breeding fraction |

---

## 1) Quick Refresher: Essential Options

| Option | Description |
|--------|-------------|
| `-c` | Climate file (GRIB or NetCDF) |
| `-d` | Data file (NetCDF with population; optional land-use/PBF) |
| `-o` | Output filename |
| `-a` | Options file |
| `-r` | Input directory |
| `-v` | Inline options string |
| `-i` | Restart/init file |
| `-e` | Ensemble number |
| `-x` | Vector selection |
| `-z` | Redirect text output to file |

Check help:

```bash
$VECTRI/vectri -h
```

---

## 2) Simulation Initialization Principles

VECTRI can be used for:

- **Seasonal forecasting** (typically 3–6 months)
- **Longer-term present-day modeling**
- **Future climate scenario experiments**

Initialization options determine how the model starts its internal human/vector states.

---

## 3) Cold Start

### 3.1 What It Means

A cold start is the **default** method when you do not set `-i` or custom initialization parameters.

Based on the tutorial:

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `rhost_infect_init` | 10% | Human infection initialization |
| `rvect_min` | Background minimum | Vector population density |
| CSPR rate | 10% | Initial sporozoite rate |

### 3.2 Hands-On: Basic Cold Start

Run a minimal cold-start simulation:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o out_cold_start.nc
```

### 3.3 Hands-On: Cold Start with Logging

Add a log file:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o out_cold_start.nc -z cold_start.log
```

### 3.4 Verify Output

Confirm output exists:

```bash
ls -lh out_cold_start.nc
```

```bash
ls -lh cold_start.log
```

---

## 4) Spinning Up the Model

### 4.1 Why Spin Up?

The tutorial notes that initial conditions are typically "forgotten" within **6–24 months**, depending on temperature (longer adjustment at colder temperatures).

Rather than discarding the first 1–2 years of output, VECTRI can **spin up** internally.

### 4.2 Key Parameters

| Parameter | Description |
|-----------|-------------|
| `nlenspinup` | Length of the spin-up window (in days) |
| `nloopspinup` | Number of times that window is repeated |

**Mechanism:**

1. Model starts from cold start
2. Uses the first `nlenspinup` days of the climate file
3. Repeats this segment `nloopspinup` times
4. Discards these spin-up integrations
5. Saves output from the next integration onward

### 4.3 Example 1: One-Year Spin-Up Repeated Twice

If your climate file contains many years:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "nlenspinup=365,nloopspinup=2" -o out_spinup_365x2.nc -z spinup_365x2.log
```

**Interpretation:**

- First year is looped twice (2 years of internal spin-up)
- Output length matches the original driving period
- Initial state in the saved output is "warmed up"

### 4.4 Example 2: Seasonal File Workaround

If you only have a short seasonal driver, you can increase the loop count:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "nlenspinup=30,nloopspinup=12" -o out_spinup_30x12.nc -z spinup_30x12.log
```

This approximates a one-year spin-up using repeated first-month conditions.

---

## 5) Restarting the Model

### 5.1 Why Restarts?

For forecasting, initial conditions should reflect conditions just before the forecast start.

A **restart** is often more realistic than pure spin-up.

### 5.2 How VECTRI Creates Restart Files

After a run completes, VECTRI typically writes:

| File | Description |
|------|-------------|
| Main output | `vectri.nc` (or your `-o` name) |
| Restart dump | `./input/restart_vectri.nc` |

Create the input folder:

```bash
mkdir -p input
```

### 5.3 Hands-On: Generate a Restart File

Run a baseline simulation:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o out_for_restart_build.nc -z build_restart.log
```

Check for the restart file:

```bash
ls -lh input/restart_vectri.nc
```

### 5.4 Hands-On: Start a New Run from Restart

```bash
$VECTRI/vectri -i input/restart_vectri.nc -c example_sys5.nc -d example_data.nc -o out_from_restart.nc -z restart_run.log
```

### 5.5 Tip: "Chunked" Climate Experiments

Restart files are also useful when:

- Your climate data is split into multiple files
- You want continuity without re-running entire long periods

### 5.6 Note on Bit Reproducibility

!!! warning
    The tutorial warns that while restart was designed for bit reproducibility, this may not always hold after new developments. If exact bit-for-bit matching matters for your work, test it explicitly.

---

## 6) Creating a Constant Climate Driver File

A constant climate file is useful for:

- Sensitivity experiments
- Debugging
- Isolating non-climatic effects

The idea is to create a driver where temperature (and optionally precipitation) are held constant over time.

### 6.1 Strategy

Use a known-good climate template (same grid, coordinates, time axis), then overwrite variable values with constants.

### 6.2 Python/xarray Method

Create `make_constant_climate.py`:

```python
#!/usr/bin/env python3
import xarray as xr
import numpy as np

# 1) Load an existing climate file as template
ds = xr.open_dataset("example_sys5.nc")

# 2) Inspect variable names
print("Variables:", list(ds.data_vars))

# ---- EDIT THESE to match your file ----
# If you know the temperature variable name, set it explicitly.
TEMP_VAR = list(ds.data_vars)[0]
CONST_TEMP = 298.15  # example: 25°C in Kelvin (adjust to your units)

# 3) Make temperature constant across all times/space
ds[TEMP_VAR] = xr.full_like(ds[TEMP_VAR], CONST_TEMP)

# 4) (Optional) Make precip constant too if it exists
# PREC_VAR = "pr"
# CONST_PR = 0.0
# if PREC_VAR in ds:
#     ds[PREC_VAR] = xr.full_like(ds[PREC_VAR], CONST_PR)

# 5) Save
ds.to_netcdf("clim_constant.nc")
print("Wrote clim_constant.nc")
```

Run the script:

```bash
python make_constant_climate.py
```

Verify the output:

```bash
ncdump -h clim_constant.nc | head -n 80
```

### 6.3 Test Run with Constant Climate

```bash
$VECTRI/vectri -c clim_constant.nc -d example_data.nc -o out_constant_clim.nc -z constant_clim.log
```

---

## 7) Creating an Ensemble Run

Ensembles help you:

- Quantify uncertainty
- Improve robustness of risk signals
- Ensure reproducibility via controlled random seeds

### 7.1 Simple Loop

Create output directories:

```bash
mkdir -p outputs logs
```

Run 5 ensemble members:

```bash
for m in 1 2 3 4 5; do
  $VECTRI/vectri -e $m -c example_sys5.nc -d example_data.nc -o outputs/ens_member_${m}.nc -z logs/ens_member_${m}.log
done
```

### 7.2 Individual Member Commands

Alternatively, run each member separately:

**Member 1:**

```bash
$VECTRI/vectri -e 1 -c example_sys5.nc -d example_data.nc -o outputs/ens_member_1.nc -z logs/ens_member_1.log
```

**Member 2:**

```bash
$VECTRI/vectri -e 2 -c example_sys5.nc -d example_data.nc -o outputs/ens_member_2.nc -z logs/ens_member_2.log
```

**Member 3:**

```bash
$VECTRI/vectri -e 3 -c example_sys5.nc -d example_data.nc -o outputs/ens_member_3.nc -z logs/ens_member_3.log
```

### 7.3 Ensemble with Spin-Up

Create directories:

```bash
mkdir -p outputs logs
```

Run ensemble with spin-up:

```bash
for m in 1 2 3; do
  $VECTRI/vectri -e $m -c example_sys5.nc -d example_data.nc -v "nlenspinup=365,nloopspinup=2" -o outputs/ens_spinup_member_${m}.nc -z logs/ens_spinup_member_${m}.log
done
```

---

## 8) Analyzing Outputs (Quick, Hands-On)

This section focuses on **fast checks** you can do immediately after running.

### 8.1 Check File Structure

```bash
ncdump -h out_cold_start.nc
```

Look for:

- Dimensions (`time`, `latitude`, `longitude` or similar)
- Variable names
- Units and long_name attributes

### 8.2 Quick Visual Inspection

If you have `ncview`:

```bash
ncview out_cold_start.nc
```

### 8.3 Minimal Python Exploration

Create `quick_check_output.py`:

```python
#!/usr/bin/env python3
import xarray as xr

ds = xr.open_dataset("out_cold_start.nc")

print(ds)
print("\nVariables:")
for v in ds.data_vars:
    print(" -", v, ds[v].dims)

# Basic time coverage
if "time" in ds:
    print("\nTime range:",
          str(ds["time"].values[0]),
          "to",
          str(ds["time"].values[-1]))

# Simple spatial mean for the first variable
v0 = list(ds.data_vars)[0]
print("\nExample variable:", v0)
print("Mean:", float(ds[v0].mean().values))
```

Run the script:

```bash
python quick_check_output.py
```

### 8.4 Quick Ensemble Sanity Check

```python
import xarray as xr

files = ["outputs/ens_member_1.nc", "outputs/ens_member_2.nc", "outputs/ens_member_3.nc"]
datasets = [xr.open_dataset(f) for f in files]
v = list(datasets[0].data_vars)[0]
means = [float(ds[v].mean()) for ds in datasets]
print("Variable:", v)
print("Means:", means)
```

---

## 9) Mini-Exercises

### Exercise 1: Cold Start vs Spin-Up

1. Run both cold start and spin-up simulations
2. Compare monthly means of a key output variable

**Cold start:**

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o ex1_cold.nc
```

**With spin-up:**

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "nlenspinup=365,nloopspinup=2" -o ex1_spinup.nc
```

### Exercise 2: Restart Realism Test

1. Run a short "historical" period to build a restart
2. Use that restart to initiate a new "forecast" segment

**Build restart:**

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o ex2_historical.nc
```

**Use restart:**

```bash
$VECTRI/vectri -i input/restart_vectri.nc -c example_sys5.nc -d example_data.nc -o ex2_forecast.nc
```

### Exercise 3: Constant Climate Sensitivity

1. Create `clim_constant.nc` using the Python script
2. Compare outputs to the original climate-driven run

### Exercise 4: Ensemble Summary

1. Run 5 ensemble members
2. Compute ensemble mean and spread in Python

---

## 10) Clean "All-in-One" Example Command

Create directories:

```bash
mkdir -p input outputs logs
```

Copy calibrated options:

```bash
cp -f vectri_calibrated.options input/vectri.options
```

Run complete simulation:

```bash
$VECTRI/vectri -a input/vectri.options -c example_sys5.nc -d example_data.nc -v "nlenspinup=365,nloopspinup=2" -e 1 -o outputs/tutorial_member01_spinup.nc -z logs/tutorial_member01_spinup.log
```

---

## 11) Troubleshooting Checkpoints

!!! warning "Common Issues"

    **VECTRI can't find the options file:**
    
    - Create `input/` and place `vectri.options` inside, or use `-a`
    
    **Changed input directory with `-r`:**
    
    - Also specify `-a` with the correct path
    
    **Outputs look empty or too uniform:**
    
    - Confirm climate variable names/units
    - Confirm the data file contains required population fields

---

## 12) Summary: What You Can Now Do

After completing this hands-on, you can:

| Skill | Description |
|-------|-------------|
| Cold Start | Start VECTRI runs using cold-start defaults |
| Spin-Up | Improve initialization quality using spin-up controls |
| Restarts | Build and use restarts for realistic forecast initial states |
| Constant Climate | Create controlled constant-climate experiments |
| Ensembles | Generate ensembles with reproducible seeds |
| Output Analysis | Perform quick sanity checks using `ncdump`, `ncview`, and Python |

---

## 🔗 Additional Resources

- [VECTRI Documentation](https://users.ictp.it/~tompkins/vectri/documentation/)
- [VECTRI Manual (PDF)](../pdfs/VECTRI_manual_v1.6.pdf)
- [NetCDF Tools Guide](https://www.unidata.ucar.edu/software/netcdf/)
- [Xarray Documentation](https://docs.xarray.dev/)

