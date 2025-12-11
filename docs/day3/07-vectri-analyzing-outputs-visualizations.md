# VECTRI Hands-On: Analyzing Outputs with Maps, Time Series & Key Visualizations

---

**What you'll learn:**

- Understand VECTRI output variable groups (Vector, Disease, Hydrology)
- Use auto-detection scripts to identify variables
- Create time-mean maps and area-mean time series
- Compare baseline vs experiment outputs
- Interpret coupling patterns between hydrology, vector, and disease

---

This guide helps you **understand and visualise VECTRI output variables** with a practical, repeatable workflow.

It is designed for training and can be used with tutorial outputs such as:

- `vectri.nc`
- `outputs/*.nc`

---

## 1) Output Groups

VECTRI outputs are organized into three logical groups:

### 1.1 Vector Group

| Variable | Description |
|----------|-------------|
| **vector** | Adult vector density/abundance variables |
| **larvae** | Larval density |
| **emergence** | Emergence rate |
| **HBR** | Human biting rate |

### 1.2 Disease Group

| Variable | Description |
|----------|-------------|
| **PRd** | Parasite rate / detectable prevalence |
| **CSPR** | Circumsporozoite protein rate |
| **EIR** | Entomological inoculation rate |
| **cases** | Number of cases |
| **immunity** | Immune population fraction |

### 1.3 Hydrology Group

| Variable | Description |
|----------|-------------|
| **wperm** | Permanent breeding site fraction |
| **wurbn** | Urban breeding site fraction |
| **wpond** | Temporary pond fraction |

!!! note "Variable Names"
    Exact variable names may differ across versions/builds. This guide includes scripts that **auto-detect variables by keyword** so you can work robustly even if names vary.

---

## 2) Recommended Folder Layout

Recommended structure:

```
vectri_analysis/
  outputs/
    base.nc
    out_cold_start.nc
    ...
  figures/
    global/
    ethiopia/
  scripts/
```

Create folders:

```bash
mkdir -p outputs
```

```bash
mkdir -p figures/global
```

```bash
mkdir -p figures/ethiopia
```

```bash
mkdir -p scripts
```

Or create all at once:

```bash
mkdir -p outputs figures/global figures/ethiopia scripts
```

---

## 3) Quick Manual Inspection

Start with metadata:

```bash
ncdump -h outputs/base.nc | head -n 160
```

List variable names quickly:

```python
import xarray as xr

ds = xr.open_dataset("outputs/base.nc")
print("Variables:")
for v in ds.data_vars:
    print(" -", v)
```

Save as `list_variables.py`:

```bash
python list_variables.py
```

---

## 4) The Core Idea of This Workflow

For each variable of interest:

1. **Map** — time-mean map, or a chosen time slice
2. **Time series** — area-mean for your domain (Global or Ethiopia)
3. *(optional)* Monthly or seasonal aggregation

This gives you an immediate, interpretable picture of:

- Spatial hotspots
- Temporal seasonality
- Differences between experiments
- Hydrology–vector–disease coupling patterns

---

## 5) Ethiopia Bounds (Default)

This guide uses common Ethiopia bounds:

| Coordinate | Range |
|------------|-------|
| **lat** | 3 to 15 |
| **lon** | 33 to 48 |

Adjust as needed for your study.

---

## 6) Use the Auto-Plot Script (Recommended)

This guide comes with a companion Python script:

- `vectri_plot_outputs.py`

It can:

- Auto-detect variables by keyword
- Group into vector/disease/hydrology
- Create:
  - Time-mean maps
  - Area-mean time series
  - Monthly means (optional)
- Save figures to:
  - `figures/global/`
  - `figures/ethiopia/`

### 6.1 Basic Run (Global)

```bash
python scripts/vectri_plot_outputs.py --nc outputs/base.nc --outdir figures/global
```

### 6.2 Ethiopia-Only Run

```bash
python scripts/vectri_plot_outputs.py --nc outputs/base.nc --outdir figures/ethiopia --ethiopia
```

### 6.3 Two-File Comparison (Baseline vs Experiment)

```bash
python scripts/vectri_plot_outputs.py --nc outputs/base.nc --compare outputs/exp_temp_plus1K.nc --outdir figures/ethiopia --ethiopia
```

This produces:

- Maps + time series for each detected variable
- Simple difference summaries (where safe)

### 6.4 Custom Ethiopia Bounds

```bash
python scripts/vectri_plot_outputs.py --nc outputs/base.nc --outdir figures/ethiopia --ethiopia --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48
```

---

## 7) What the Script Looks For

The script uses keyword detection for your groups:

### 7.1 Vector Keywords

- `vector`, `adult`, `mosquito`, `hbr`, `bite`, `biting`, `larv`, `larvae`, `emerge`, `emergence`

### 7.2 Disease Keywords

- `prd`, `pr`, `cspr`, `eir`, `case`, `cases`, `immune`, `immunity`, `infection`, `infect`, `parasite`

### 7.3 Hydrology Keywords

- `wperm`, `wurbn`, `wpond`, `pond`, `water`

!!! tip "Fallback Behavior"
    If no matches are found, it will fall back to plotting the first few variables.

---

## 8) Suggested Teaching Sequence (60–90 min)

| Step | Activity | Time |
|------|----------|------|
| 1 | **Baseline output anatomy** | 10 min |
|    | - `ncdump -h` | |
|    | - List variables | |
| 2 | **Run auto-plot global** | 10 min |
| 3 | **Run Ethiopia-only** | 10 min |
| 4 | **Pick one variable per group** | 15 min |
|    | - Discuss physical/epidemiological meaning | |
| 5 | **Compare two experiments** | 15 min |
|    | - e.g., rainfall factor vs hydrology outputs | |
| 6 | **Explain coupling ideas** | 10 min |
|    | - rainfall → `wpond/wperm` → larvae → HBR/EIR/PRd | |

---

## 9) Interpretation Tips (High-Level)

### 9.1 Hydrology → Vector

- Increased ponding/permanent water often provides more breeding habitat
- Watch whether:
  - `wpond` increases align with
  - larvae/emergence increases

### 9.2 Vector → Disease

- Higher HBR or vector density can increase:
  - `EIR`
  - `PRd`
  - cases (depending on model config)

### 9.3 Immunity Feedbacks

- Changes in incidence/transmission can shift immunity metrics
- This can dampen or amplify later-season risk depending on settings

!!! note "Training vs Research"
    These are **qualitative training heuristics**. For research-grade inference, you'll validate with local epidemiology and longer evaluation windows.

---

## 10) Minimal Manual Plotting Template

If you want to teach the basics without the auto-script:

### 10.1 One Variable Map (Time Mean)

Create `plot_map.py`:

```python
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset("outputs/base.nc")
var = list(ds.data_vars)[0]
da = ds[var]

# Find a time dimension if present
time_dim = next((d for d in da.dims if "time" in d.lower()), None)
field = da.mean(time_dim) if time_dim else da

plt.figure()
field.plot()
plt.title(f"{var} time-mean")
plt.tight_layout()
plt.savefig("figures/manual_map.png", dpi=150)
plt.close()
```

Run:

```bash
python plot_map.py
```

### 10.2 One Variable Ethiopia Area-Mean Time Series

Create `plot_timeseries.py`:

```python
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset("outputs/base.nc")

# Crude coord detection
lat = next((c for c in ds.coords if "lat" in c.lower()), None)
lon = next((c for c in ds.coords if "lon" in c.lower()), None)

var = list(ds.data_vars)[0]
da = ds[var]

if lat and lon:
    ds = ds.sel({lat: slice(3, 15), lon: slice(33, 48)})

da = ds[var]

lat_dim = next((d for d in da.dims if "lat" in d.lower()), None)
lon_dim = next((d for d in da.dims if "lon" in d.lower()), None)

spatial = [d for d in [lat_dim, lon_dim] if d in da.dims]
ts = da.mean(spatial) if spatial else da

plt.figure()
ts.plot()
plt.title(f"{var} Ethiopia area-mean time series")
plt.tight_layout()
plt.savefig("figures/manual_timeseries.png", dpi=150)
plt.close()
```

Run:

```bash
python plot_timeseries.py
```

---

## 11) Outputs You'll Get

With the auto script, expect filenames like:

```
figures/ethiopia/
  vector__<varname>__map.png
  vector__<varname>__ts.png
  disease__<varname>__map.png
  disease__<varname>__ts.png
  hydro__<varname>__map.png
  hydro__<varname>__ts.png
```

If using comparison mode:

```
figures/ethiopia/
  vector__<varname>__delta_map.png
  vector__<varname>__delta_ts.png
  ...
```

This structure makes it easy to assemble slides quickly.

---

## 12) Complete Workflow Example

### Step 1: Set Up Directories

```bash
mkdir -p outputs figures/global figures/ethiopia scripts
```

### Step 2: Inspect Output Structure

```bash
ncdump -h outputs/base.nc | head -n 100
```

### Step 3: List Variables

```python
import xarray as xr

ds = xr.open_dataset("outputs/base.nc")
print("Variables:")
for v in ds.data_vars:
    print(" -", v)
```

### Step 4: Generate Global Figures

```bash
python scripts/vectri_plot_outputs.py --nc outputs/base.nc --outdir figures/global
```

### Step 5: Generate Ethiopia Figures

```bash
python scripts/vectri_plot_outputs.py --nc outputs/base.nc --outdir figures/ethiopia --ethiopia
```

### Step 6: Compare Experiments

```bash
python scripts/vectri_plot_outputs.py --nc outputs/base.nc --compare outputs/exp_temp_plus1K.nc --outdir figures/ethiopia --ethiopia
```

### Step 7: View Results

```bash
ls figures/ethiopia/
```

---

## 13) Understanding the Variable Inventory

The script creates a `variable_inventory.txt` file in the output directory:

```bash
cat figures/ethiopia/variable_inventory.txt
```

This file lists:

- Source file used
- Comparison file (if any)
- Geographic subset (if any)
- Detected variable groupings

---

## 14) Troubleshooting

!!! warning "Common Issues"

    **Script can't find variables:**
    
    - Check that your output file contains expected variable names
    - Verify the file path is correct
    - Try running with manual variable specification
    
    **Plots are empty or show errors:**
    
    - Ensure the data has spatial dimensions (lat/lon)
    - Check that time dimension exists for time series
    - Verify coordinate names match expected patterns
    
    **Comparison fails:**
    
    - Ensure both files have the same variable names
    - Check that coordinates align between files
    - Verify both files cover the same time period

---

## 15) Advanced: Custom Variable Selection

If you want to plot specific variables, you can modify the script or create a custom version that:

1. Takes a list of variable names as input
2. Plots only those variables
3. Applies custom grouping logic

Example custom script structure:

```python
import xarray as xr
import matplotlib.pyplot as plt

# Load dataset
ds = xr.open_dataset("outputs/base.nc")

# Specify variables of interest
variables = ["disease/eir", "vector/vector", "hydrology/wpond"]

# Plot each
for var in variables:
    if var in ds.data_vars:
        da = ds[var]
        # ... plotting code ...
```

---

## 📝 Exercises

### Exercise 1: Basic Visualization

1. Run the auto-plot script on your baseline output
2. Identify one variable from each group (vector, disease, hydrology)
3. Compare the spatial patterns in the maps

### Exercise 2: Regional Comparison

1. Generate global figures
2. Generate Ethiopia-specific figures
3. Compare the differences in patterns

### Exercise 3: Experiment Comparison

1. Run baseline and one experiment
2. Generate comparison figures
3. Identify which variables show the largest changes

### Exercise 4: Coupling Analysis

1. Plot `wpond` (hydrology)
2. Plot `larvae` (vector)
3. Plot `eir` (disease)
4. Discuss the temporal relationships between them

---

## 🔗 Additional Resources

- [VECTRI Output Analysis](./01-vectri-output-analysis.md)
- [VECTRI Parameter Sensitivity](./05-vectri-parameter-sensitivity.md)
- [VECTRI Hands-On Simulations](./03-vectri-hands-on-simulations.md)
- [VECTRI Documentation](https://users.ictp.it/~tompkins/vectri/documentation/)
- [Xarray Documentation](https://docs.xarray.dev/)
- [Matplotlib Documentation](https://matplotlib.org/)

