# VECTRI Output Quick Guide (ncdump + ncview)

---

**What you'll learn:**

- Understand the structure of VECTRI NetCDF output files
- Use `ncdump` to inspect metadata and variables
- Use `ncview` for visual exploration
- Navigate NetCDF4 groups (input, hydrology, vector, disease)
- Interpret key VECTRI output variables

---

## 1) What Your `vectri.nc` Contains

### 1.1 Dimensions

| Dimension | Size | Description |
|-----------|------|-------------|
| longitude | 81 | X-axis grid points |
| latitude | 81 | Y-axis grid points |
| time | UNLIMITED (215 currently) | Time steps |

Most time-varying fields are stored on a **(time, latitude, longitude)** grid.

Static fields (no time dimension) are also present.

### 1.2 Coordinate Variables

| Variable | Dimensions | Units | Axis |
|----------|------------|-------|------|
| longitude | (longitude) | degrees_east | X |
| latitude | (latitude) | degrees_north | Y |
| time | (time) | hours since 1900-01-01 00:00:00.0 | - |

!!! note "Metadata Note"
    Your header may show `longitude:long_name = "latitude"` which is a harmless metadata typo.

### 1.3 NetCDF4 Groups

Your file is organized into thematic groups:

| Group | Description |
|-------|-------------|
| **input** | Forcing and static inputs |
| **hydrology** | Breeding habitat and water availability |
| **vector** | Mosquito life-cycle and biting dynamics |
| **disease** | P. falciparum transmission and burden |
| **interventions** | Control strategies (empty if not enabled) |

Many tools will show these groups clearly; some may display variables with group prefixes (e.g., `vector/vector`).

---

## 2) Using `ncdump`

`ncdump` is a command-line tool for inspecting NetCDF files.

### 2.1 Inspect Global Metadata + Structure

```bash
ncdump -h vectri.nc
```

To page through the header:

```bash
ncdump -h vectri.nc | less
```

### 2.2 See Global Attributes Only

Useful for reports:

```bash
ncdump -h vectri.nc | sed -n '/global attributes:/,$p'
```

### 2.3 List Variables and Dimensions

```bash
ncdump -h vectri.nc | grep -E 'dimensions:|variables:|group:'
```

### 2.4 Print a Specific Variable

**Top-level variables:**

```bash
ncdump -v time vectri.nc
```

**Grouped variables** (use the group path):

Vector group:

```bash
ncdump -v vector/vector vectri.nc
```

Disease group:

```bash
ncdump -v disease/eir vectri.nc
```

Input group:

```bash
ncdump -v input/t2m vectri.nc
```

Hydrology group:

```bash
ncdump -v hydrology/wpond vectri.nc
```

### 2.5 Quick Sanity Checks for Missing Values

Your model output uses large fill values:

| Data Type | Fill Value |
|-----------|------------|
| Model outputs | `9.96921e+36` |
| Input climate fields | `-32767` |

Check min/max quickly:

```bash
ncdump -v input/tp vectri.nc | head -n 50
```

---

## 3) Using `ncview`

`ncview` is great for fast visual scanning and animation of NetCDF data.

### 3.1 Open the File

```bash
ncview vectri.nc
```

### 3.2 Navigating Groups

Depending on your build, `ncview` may show group variables with names like:

- `vector/vector`
- `disease/eir`
- `input/tp`

Just select the variable from the list and animate through time.

### 3.3 What to Check Visually

| Variable | What to Look For |
|----------|------------------|
| `input/tp`, `input/t2m` | Realistic rainfall and temperature over your domain |
| `hydrology/wpond` | Responds to rainfall seasonality |
| `vector/larvae`, `vector/emergence` | Rise after suitable rainfall + temperature |
| `vector/vector` | Adult density follows emergence |
| `vector/hbr` | Human biting rate scales with vector density |
| `disease/eir` | Peaks after vector density increases |
| `disease/PRd`, `disease/cases` | Plausible seasonal patterns |

---

## 4) Variable-by-Variable Reference

This reference is derived from:

```bash
ncdump -h vectri.nc
```

---

### 4.1 Top-Level Coordinates

| Variable | Dimensions | Units | Meaning |
|----------|------------|-------|---------|
| longitude | (longitude) | degrees_east | **X** coordinate |
| latitude | (latitude) | degrees_north | **Y** coordinate |
| time | (time) | hours since 1900-01-01 00:00:00.0 | Model time axis |

---

### 4.2 Group: `input`

These are the **forcing** and **static inputs** used by VECTRI.

| Variable | Dimensions | Units | Meaning | Notes |
|----------|------------|-------|---------|-------|
| population | (latitude, longitude) | km^-2 | Population density | Static field |
| tp | (time, latitude, longitude) | mm day^-1 | Total precipitation | FillValue `-32767` |
| t2m | (time, latitude, longitude) | degrees C | 2 metre temperature | FillValue `-32767` |

---

### 4.3 Group: `hydrology`

Represents **breeding habitat fractions** and **temporary water availability**.

| Variable | Dimensions | Units | Meaning | Notes |
|----------|------------|-------|---------|-------|
| wperm | (latitude, longitude) | (unitless) | Permanent breeding site fraction | Static |
| wurbn | (latitude, longitude) | (unitless) | Urban breeding site fraction | Static |
| wpond | (time, latitude, longitude) | fraction | Fraction coverage temporary ponds | Dynamic water response |

!!! tip "Interpretation Tips"
    - **wperm** sets a baseline habitat that does not depend on rainfall
    - **wurbn** represents urban-specific breeding potential
    - **wpond** should show strong seasonality and respond to rainfall pulses

---

### 4.4 Group: `vector`

These represent the **mosquito life-cycle and biting dynamics**.

| Variable | Dimensions | Units | Meaning | Notes |
|----------|------------|-------|---------|-------|
| vector | (time, latitude, longitude) | m^-2 | Anopheles Gambiae vector density | Adult density |
| larvae | (time, latitude, longitude) | m^-2 | Anopheles Gambiae larvae density | Aquatic stage |
| emergence | (time, latitude, longitude) | m^-2 day^-1 | Emergence rate of new vectors per day | Daily rate |
| hbr | (time, latitude, longitude) | bites per day per person | Anopheles Gambiae human bite rate | Links vectors ↔ humans |

!!! tip "Interpretation Tips"
    - **larvae** and **wpond** often co-vary
    - **emergence** should lag favorable habitat/temperature
    - **vector** can lag **emergence** depending on survival settings
    - **hbr** scales with adult vector density and behavior parameters

---

### 4.5 Group: `disease`

These variables represent **P. falciparum transmission and burden**.

| Variable | Dimensions | Units | Meaning | Notes |
|----------|------------|-------|---------|-------|
| PRd | (time, latitude, longitude) | frac | P. falciparum detectable parasite ratio | Prevalence-like |
| cspr | (time, latitude, longitude) | frac | Circumsporozoite protein rate | Infective fraction among vectors |
| eir | (time, latitude, longitude) | infective bites per day per person | P. falciparum Entomological Inoculation Rate | Key risk indicator |
| cases | (time, latitude, longitude) | fraction | Number of new cases P. falciparum | Check post-processing interpretation |
| immunity | (time, latitude, longitude) | fraction | Immune population P. falciparum | Modelled immunity state |

!!! tip "Interpretation Tips"
    - **eir** typically peaks after increases in **vector** and **cspr**
    - **PRd** and **cases** can lag EIR depending on infection/clearance parameters
    - **immunity** builds with sustained transmission and decays over time

---

### 4.6 Group: `interventions`

This group is **empty** in a default run.

If you enable interventions in future experiments, you may see variables related to:

- Bednet coverage/effects
- Indoor biting adjustments
- SIT (Sterile Insect Technique) parameters
- Other control strategy diagnostics

---

## 5) Practical Workflow for Training Sessions

### Step 1 — Inspect Structure

```bash
ncdump -h vectri.nc | less
```

### Step 2 — Confirm Input Realism

Check precipitation:

```bash
ncdump -v input/tp vectri.nc | head -n 30
```

Check temperature:

```bash
ncdump -v input/t2m vectri.nc | head -n 30
```

### Step 3 — Visual Scan in ncview

```bash
ncview vectri.nc
```

**Suggested animation order:**

1. `input/tp`, `input/t2m` — Verify forcing data
2. `hydrology/wpond` — Check water response
3. `vector/larvae`, `vector/emergence`, `vector/vector`, `vector/hbr` — Mosquito dynamics
4. `disease/cspr`, `disease/eir`, `disease/PRd`, `disease/cases`, `disease/immunity` — Disease transmission

---

## 6) Run Configuration (Global Attributes)

Your header documents important settings worth citing in reports.

### Key Configuration Parameters

| Parameter | Description |
|-----------|-------------|
| `command` | Full VECTRI command line used |
| `wpond_rate`, `wpond_CN`, `wpond_max` | Hydrology/pond parameters |
| `rvecsurv`, temperature thresholds | Vector survival and development controls |
| Immunity gain/loss parameters | Host clearance settings |
| `nlenspinup = 365` | Spinup period (days) |
| `dt = 1` | Daily time-step |

These parameters explain *why* outputs look the way they do.

### View Global Attributes

```bash
ncdump -h vectri.nc | sed -n '/global attributes:/,$p'
```

---

## 7) Common Gotchas

!!! warning "Troubleshooting Tips"

    **Blocky maps:**
    
    - Remember S2S/forcing resolution and any regridding used before VECTRI
    
    **ncview cannot open the file:**
    
    - Ensure NetCDF4 support is compiled in
    - Check the file is not corrupted
    - Verify you have read access
    
    **Missing values:**
    
    - Model outputs use `9.96921e+36`
    - Input group uses `-32767`

---

## 8) Quick Reference Commands

### Essential ncdump Commands

View header:

```bash
ncdump -h vectri.nc
```

View specific variable:

```bash
ncdump -v VARIABLE_NAME vectri.nc
```

View grouped variable:

```bash
ncdump -v GROUP/VARIABLE vectri.nc
```

### Essential ncview Commands

Open file:

```bash
ncview vectri.nc
```

---

## 9) Summary

!!! success "Key Takeaways"
    
    The VECTRI output file is a **NetCDF4 dataset** organised into thematic groups:
    
    - **input** — Forcing data (rainfall, temperature, population)
    - **hydrology** — Breeding habitat availability
    - **vector** — Mosquito life-cycle dynamics
    - **disease** — Malaria transmission metrics
    
    Daily fields are stored on a **(time, latitude, longitude)** grid, allowing:
    
    - Rapid inspection with `ncdump`
    - Interactive animation with `ncview`

---

## 📝 Exercises

### Exercise 1: Explore File Structure

1. Open a terminal and navigate to your VECTRI output directory
2. Run `ncdump -h vectri.nc | less` to explore the file structure
3. Identify all the groups and their variables

### Exercise 2: Check Input Data

1. Use `ncdump` to examine the precipitation input
2. Verify the temperature range is reasonable for your study area
3. Check the time dimension length

### Exercise 3: Visual Exploration

1. Open the file in `ncview`
2. Animate through the `wpond` variable
3. Compare the timing of `wpond` peaks with `vector/larvae` peaks

### Exercise 4: Disease Dynamics

1. Use `ncview` to animate `disease/eir`
2. Identify the peak transmission periods
3. Compare with `disease/PRd` to see the lag relationship

---

## 🔗 Additional Resources

- [NetCDF Documentation](https://www.unidata.ucar.edu/software/netcdf/docs/)
- [ncdump User Guide](https://www.unidata.ucar.edu/software/netcdf/workshops/2011/utilities/Ncdump.html)
- [ncview Homepage](http://meteora.ucsd.edu/~pierce/ncview_home_page.html)
- [VECTRI Documentation](https://users.ictp.it/~tompkins/vectri/documentation/)

