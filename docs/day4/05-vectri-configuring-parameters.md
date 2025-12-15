# VECTRI Hands-On: Configuring Model Parameters

---

**What you'll learn:**

- Configure model parameters using command line (`-v`)
- Use `vectri.options` file for parameter management
- Understand parameter override order
- Run sensitivity experiments across different parameter categories
- Verify parameter changes in output files

---

This hands-on guide shows how to **configure, override, and test model parameters** in VECTRI using:

- **Command line input** (`-v`)
- **`vectri.options` file**

It also provides mini-experiments to **change a parameter and observe the effect** across:

- Simulation parameters
- Vector / Parasite (disease) parameters
- Hydrology parameters
- Host / Population parameters
- Intervention parameters

---

## 0) Assumptions & Example Files

You have a run directory containing tutorial-like inputs such as:

| File | Description |
|------|-------------|
| `example_sys5.nc` or `example_sys5.grb` | Climate data |
| `example_data.nc` | Population and optional ancillary fields |
| `vectri_calibrated.options` | Optional example options file |

If needed, create an input folder:

```bash
mkdir -p input
```

---

## 1) The Three Ways to Control Parameters

The manual summarizes 3 ways:

| Method | Use Case | Recommendation |
|--------|----------|----------------|
| **Command line** (`-v`) | 1–2 quick changes | Recommended for quick experiments |
| **Input file** (`vectri.options`) | Many or semi-permanent changes | Recommended for structured experiments |
| **Fortran code edits** | Advanced development | Not recommended for standard usage |

This guide focuses on methods (1) and (2).

---

## 2) Method A — Command Line Input (`-v`)

### 2.1 Syntax

Use the `-v` option with a comma-separated string:

```bash
vectri -v "param1=val,param2=val"
```

Example used in initialization:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "nloopspinup=3,nlenspinup=365" -o out_spinup_test.nc
```

### 2.2 Confirm Your Settings Were Applied

After the run, check the global attributes:

```bash
ncdump -h out_spinup_test.nc | grep -i spinup
```

You should see the parameter values in the **global attributes**.

---

## 3) Method B — `vectri.options` File

### 3.1 Where It Lives

The file should be placed at:

```
./input/vectri.options
```

Create the directory:

```bash
mkdir -p input
```

Create and open the file:

```bash
nano input/vectri.options
```

Or use your preferred editor:

```bash
vi input/vectri.options
```

### 3.2 Format

You can list parameters either:

- Comma-separated, or
- One per line (easiest to read)

**Example (one per line):**

```text
nloopspinup=3
nlenspinup=365
```

**Example (comma-separated):**

```text
nloopspinup=3,nlenspinup=365
```

Run using the file:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o out_options_file_test.nc
```

### 3.3 Warning from the Manual

!!! warning "Important"
    Because `vectri.options` is "hidden away", it's easy to forget it exists. When comparing experiments, always verify settings in the output global attributes:

```bash
ncdump -h out_options_file_test.nc | grep -i spinup
```

---

## 4) Override Order (Important)

The manual explains:

- VECTRI builds a namelist where it loads:
  1. **`vectri.options`** values first
  2. then **command line `-v`** values

So if you specify the same parameter twice, **`-v` wins**.

### 4.1 Quick Demonstration

Put this in `input/vectri.options`:

```text
nloopspinup=1
```

Then run:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "nloopspinup=3" -o out_override_demo.nc
```

Verify the override:

```bash
ncdump -h out_override_demo.nc | grep -i nloopspinup
```

You should see `3` (the command-line value, not the file value).

---

## 5) Parameter Tables

These defaults apply to **An. gambiae** and **Plas. falciparum** unless you switch vector/disease modes.

### 5.1 Simulation Parameters

| Name | Default | Units | Description / Notes |
|------|---------|-------|---------------------|
| `nloopspinup` | 0 | — | Number of spinup loops |
| `nlenspinup` | 10 | days | Length of spinup loop |
| `dt` | 1 | days | **Time step (do not change!)** |
| `nnumeric` | 2 | — | Numerical integration scheme [0–5] |
| `rtemperature_offset` | 0 | K | Toy climate change: add constant offset |
| `rtemperature_trend` | 0 | K | Toy climate change: temperature trend |
| `rrainfall_factor` | 1 | ratio | Toy climate change: multiply rainfall |

### 5.2 Vector Parameters

| Name | Default | What it controls (high-level) |
|------|---------|-------------------------------|
| `neggmn` | 60* | Eggs per batch resulting in female adults |
| `rbiteratio` | 0.6 | Biting ratio scaling |
| `rbitehighrisk` | 5 | High-risk biting multiplier |
| `rvecsurv` | 0.95 | Vector survival baseline |
| `nlarv_scheme` | 4 | Larval scheme selection |
| `nsurvival_scheme` | 2 | Survival scheme selection |
| `rtsporo` | 16 | Sporogony temperature parameter (model-specific) |
| `dsporo` | 111 | Sporogony duration parameter (model-specific) |

### 5.3 Disease (Parasite/Host Infection) Parameters

| Name | Default | What it controls (high-level) |
|------|---------|-------------------------------|
| `rhostclear` | 15 | Host clearance time/scale |
| `rhostimmuneclear` | 300 | Immune clearance scale |
| `rpthost2vect_I` | 0.25 | Transmission host→vector (infected) |
| `rpthost2vect_R` | 0.1 | Transmission host→vector (recovered) |
| `rptvect2host` | 0.15 | Transmission vector→host |
| `rhost_infectd` | 20 | Infection duration parameter |
| `rhost_detectd` | 9 | Detectable infection period |
| `rimmune_gain_eira` | 300 | Immunity gain scaling |
| `rimmune_loss_tau` | 365 | Immunity loss time scale |
| `rhost_infect_init` | 0.1 | Cold-start initial infection fraction |

### 5.4 Hydrology Parameters

| Name | Default | What it controls (high-level) |
|------|---------|-------------------------------|
| `wperm_default` | 1.e-06 | Default permanent water fraction |
| `npud_scheme` | 2 | Hydrology scheme selection |
| `wpond_rate` | 0.001 | Ponding rate |
| `wpond_CN` | 85 | Curve number (runoff proxy) |
| `wpond_min` | 1.e-06 | Minimum ponding |
| `wpond_max` | 0.2 | Maximum ponding |
| `wpond_evap` | 5 | Pond evaporation factor |
| `wpond_infil_clay` | 50 | Infiltration scaling for clay |
| `wpond_infil_sand` | 700 | Infiltration scaling for sand |
| `wpond_infil_silt` | 250 | Infiltration scaling for silt |
| `wperm_ratio` | 0.05 | Permanent water ratio modifier |
| `wurbn_ratio` | 0.05 | Urban water ratio modifier |
| `wurbn_tau` | 20 | Urban water time scale |

### 5.5 Population / Host Parameters

| Name | Default | What it controls (high-level) |
|------|---------|-------------------------------|
| `rpop_death_rate` | 0.02 | Population death rate |
| `rpopdensity_min` | 1 | Minimum population density |
| `rmigration` | 1.e-05 | Migration parameter |

### 5.6 Intervention Parameters

| Name | Default | What it controls (high-level) |
|------|---------|-------------------------------|
| `rsit_breed` | 0.56 | SIT breeding impact |
| `rsit_mortality` | 1 | SIT mortality impact |
| `rbednet_tau` | 1052 | Bednet decay time scale (approx. multi-year) |

---

## 6) Change a Parameter and See the Effect (Mini-Labs)

The goal here is not to produce definitive epidemiological conclusions, but to help you **verify that your configuration workflow works**.

### 6.1 Baseline Run

Create output directories:

```bash
mkdir -p outputs logs
```

Run baseline simulation:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o outputs/base.nc -z logs/base.log
```

Record defaults stored in the output:

```bash
ncdump -h outputs/base.nc | head -n 200
```

### 6.2 Lab A — Toy Temperature Increase

Use `rtemperature_offset`:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rtemperature_offset=1.0" -o outputs/temp_plus1K.nc -z logs/temp_plus1K.log
```

Confirm the parameter was applied:

```bash
ncdump -h outputs/temp_plus1K.nc | grep -i rtemperature_offset
```

### 6.3 Lab B — Toy Rainfall Change

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rrainfall_factor=1.2" -o outputs/rain_x1p2.nc -z logs/rain_x1p2.log
```

### 6.4 Lab C — Vector Biting Intensity

Change `rbiteratio`:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rbiteratio=0.8" -o outputs/bite_ratio_0p8.nc -z logs/bite_ratio_0p8.log
```

### 6.5 Lab D — Host Clearance

Change `rhostclear`:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rhostclear=10" -o outputs/hostclear_10.nc -z logs/hostclear_10.log
```

### 6.6 Lab E — Hydrology Sensitivity

Change `wperm_default`:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "wperm_default=1e-4" -o outputs/wperm_1e-4.nc -z logs/wperm_1e-4.log
```

### 6.7 Lab F — Intervention Decay

Change `rbednet_tau`:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rbednet_tau=700" -o outputs/bednet_tau_700.nc -z logs/bednet_tau_700.log
```

---

## 7) Checking Differences in Outputs (Quick Patterns)

Because output variable names can vary, start by listing variables:

```python
import xarray as xr

ds = xr.open_dataset("outputs/base.nc")
print(list(ds.data_vars))
```

### 7.1 Compute Simple Global Means

```python
import xarray as xr

base = xr.open_dataset("outputs/base.nc")
test = xr.open_dataset("outputs/temp_plus1K.nc")

common = sorted(set(base.data_vars).intersection(test.data_vars))
v = common[0] if common else None

print("Common variable used for demo:", v)

if v:
    print("Base mean:", float(base[v].mean()))
    print("Test mean:", float(test[v].mean()))
```

Save as `compare_outputs.py`:

```bash
python compare_outputs.py
```

---

## 8) Using `vectri.options` for a Structured Experiment Set

If you plan a block of experiments, set a "default" configuration:

```bash
cp -f vectri_calibrated.options input/vectri.options 2>/dev/null || true
```

Edit the options file:

```bash
nano input/vectri.options
```

Add, for example:

```text
nloopspinup=2
nlenspinup=365
rrainfall_factor=1.0
rtemperature_offset=0.0
```

Run with file defaults:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o outputs/options_default.nc
```

Then override one thing on the command line:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rrainfall_factor=1.1" -o outputs/options_plus_rain.nc
```

This is the "mix-n-match" workflow described in the manual.

---

## 9) Practical Tips for Teaching & Reproducibility

!!! tip "Best Practices"

    - Always run a **baseline** first
    - Change **one parameter at a time**
    - Confirm the parameter appears in global attributes:
    
    ```bash
    ncdump -h outputs/your_run.nc | grep -i your_param
    ```
    
    - Name outputs descriptively (e.g., `temp_plus1K`, `rain_x1p2`)
    - Keep logs (`-z`) for easy troubleshooting
    - Avoid changing `dt`

---

## 10) Summary

You now have a working pattern to:

| Skill | Description |
|-------|-------------|
| Quick Parameters | Set parameters quickly with `-v` |
| Structured Config | Configure many parameters with `input/vectri.options` |
| Override Order | Understand the override order (file first, then `-v`) |
| Sensitivity Tests | Run sensitivity mini-labs across:
  - Simulation settings
  - Vector/parasite dynamics
  - Hydrology
  - Population/host settings
  - Interventions |

---

## 📝 Exercises

### Exercise 1: Parameter Verification

1. Run a simulation with a custom parameter using `-v`
2. Verify the parameter appears in the output global attributes
3. Compare with the default value

### Exercise 2: Options File Workflow

1. Create an `input/vectri.options` file with 3–4 parameters
2. Run a simulation using the file
3. Override one parameter using `-v`
4. Verify the override worked

### Exercise 3: Temperature Sensitivity

1. Run baseline simulation
2. Run with `rtemperature_offset=2.0`
3. Compare EIR or vector density between runs

### Exercise 4: Hydrology Experiment

1. Run baseline
2. Run with `wperm_default=1e-5` and `wperm_default=1e-3`
3. Compare pond fraction and larval density

---

## 🔗 Additional Resources

- [VECTRI Documentation](https://users.ictp.it/~tompkins/vectri/documentation/)
- [VECTRI Manual (PDF)](../pdfs/VECTRI_manual_v1.6.pdf)
- [VECTRI Command Line Tutorial](./02-vectri-command-line-tutorial.md)

