# VECTRI Hands-On: Analyzing Outputs with Maps, Time Series & Key Visualizations

This guide helps you **understand and visualise VECTRI output variables** with a practical, repeatable workflow.  
It is designed for training and can be used with tutorial outputs such as:

- `vectri.nc`
- `outputs/*.nc`

We focus on three logical groups you listed:

## Output groups
### Vector
- **vector** (adult vector density/abundance variables)
- **larvae**
- **emergence**
- **HBR** (human biting rate)

### Disease
- **PRd** (parasite rate / detectable prevalence)
- **CSPR**
- **EIR**
- **cases**
- **immunity**

### Hydrology
- **wperm**
- **wurbn**
- **wpond**

> Exact variable names may differ across versions/builds.  
> This guide includes scripts that **auto-detect variables by keyword** so you can work robustly even if names vary.

---

## 1) Recommended folder layout

```bash
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
mkdir -p outputs figures/global figures/ethiopia scripts
```

---

## 2) Quick manual inspection

Start with metadata:

```bash
ncdump -h outputs/base.nc | head -n 160
```

List variable names quickly:

```bash
python - <<'PY'
import xarray as xr
ds = xr.open_dataset("outputs/base.nc")
print("Variables:")
for v in ds.data_vars:
    print(" -", v)
PY
```

---

## 3) The core idea of this workflow

For each variable of interest:

1) **Map**  
   - time-mean map, or a chosen time slice  
2) **Time series**  
   - area-mean for your domain (Global or Ethiopia)  
3) *(optional)* Monthly or seasonal aggregation

This gives you an immediate, interpretable picture of:

- spatial hotspots
- temporal seasonality
- differences between experiments
- hydrology–vector–disease coupling patterns

---

## 4) Ethiopia bounds (default)

This guide uses common Ethiopia bounds:

- **lat:** 3 to 15  
- **lon:** 33 to 48

Adjust as needed for your study.

---

## 5) Use the auto-plot script (recommended)

This guide comes with a companion Python script:

- `vectri_plot_outputs.py`

It can:

- auto-detect variables by keyword
- group into vector/disease/hydrology
- create:
  - time-mean maps
  - area-mean time series
  - monthly means (optional)
- save figures to:
  - `figures/global/`
  - `figures/ethiopia/`

### 5.1 Basic run (global)

```bash
python scripts/vectri_plot_outputs.py   --nc outputs/base.nc   --outdir figures/global
```

### 5.2 Ethiopia-only run

```bash
python scripts/vectri_plot_outputs.py   --nc outputs/base.nc   --outdir figures/ethiopia   --ethiopia
```

### 5.3 Two-file comparison (baseline vs experiment)

```bash
python scripts/vectri_plot_outputs.py   --nc outputs/base.nc   --compare outputs/exp_temp_plus1K.nc   --outdir figures/ethiopia   --ethiopia
```

This produces:

- maps + time series for each detected variable
- simple difference summaries (where safe)

---

## 6) What the script looks for

The script uses keyword detection for your groups:

### 6.1 Vector keywords
- `vector`, `adult`, `mosquito`, `hbr`, `bite`, `larv`, `larvae`, `emerge`, `emergence`

### 6.2 Disease keywords
- `prd`, `pr`, `cspr`, `eir`, `case`, `cases`, `immune`, `immunity`, `infection`, `infect`

### 6.3 Hydrology keywords
- `wperm`, `wurbn`, `wpond`, `pond`, `water`

If no matches are found, it will fall back to plotting the first few variables.

---

## 7) Suggested teaching sequence (60–90 min)

1) **Baseline output anatomy**  
   - `ncdump -h`
   - list variables  
2) **Run auto-plot global**  
3) **Run Ethiopia-only**  
4) **Pick one variable per group**  
   - discuss physical/epidemiological meaning  
5) **Compare two experiments**  
   - e.g., rainfall factor vs hydrology outputs  
6) **Explain coupling ideas**  
   - rainfall → `wpond/wperm` → larvae → HBR/EIR/PRd

---

## 8) Interpretation tips (high-level)

### Hydrology → Vector
- Increased ponding/permanent water often provides more breeding habitat.
- Watch whether:
  - `wpond` increases align with
  - larvae/emergence increases.

### Vector → Disease
- Higher HBR or vector density can increase:
  - `EIR`
  - `PRd`
  - cases (depending on model config).

### Immunity feedbacks
- Changes in incidence/transmission can shift immunity metrics.
- This can dampen or amplify later-season risk depending on settings.

> These are **qualitative training heuristics**.  
> For research-grade inference, you’ll validate with local epidemiology and longer evaluation windows.

---

## 9) Minimal manual plotting template (if you want to teach the basics)

### 9.1 One variable map (time mean)

```bash
python - <<'PY'
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
plt.show()
PY
```

### 9.2 One variable Ethiopia area-mean time series

```bash
python - <<'PY'
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset("outputs/base.nc")

# crude coord detection
lat = next((c for c in ds.coords if "lat" in c.lower()), None)
lon = next((c for c in ds.coords if "lon" in c.lower()), None)

var = list(ds.data_vars)[0]
da = ds[var]

if lat and lon:
    ds = ds.sel({lat: slice(3,15), lon: slice(33,48)})

da = ds[var]

lat_dim = next((d for d in da.dims if "lat" in d.lower()), None)
lon_dim = next((d for d in da.dims if "lon" in d.lower()), None)

spatial = [d for d in [lat_dim, lon_dim] if d in da.dims]
ts = da.mean(spatial) if spatial else da

plt.figure()
ts.plot()
plt.title(f"{var} Ethiopia area-mean time series")
plt.tight_layout()
plt.show()
PY
```

---

## 10) Outputs you’ll get

With the auto script, expect filenames like:

```text
figures/ethiopia/
  vector__<varname>__map.png
  vector__<varname>__ts.png
  disease__<varname>__map.png
  disease__<varname>__ts.png
  hydro__<varname>__map.png
  hydro__<varname>__ts.png
```

This structure makes it easy to assemble slides quickly.

---

## 11) Next enhancements (if you want them)

I can create an additional companion that:

- builds a **single PDF-style figure pack** for a run
- creates:
  - a 2x2 “hydrology → larvae → HBR → EIR” narrative panel
  - country-level seasonal summaries
- includes a short text auto-narrative for outlook bulletins