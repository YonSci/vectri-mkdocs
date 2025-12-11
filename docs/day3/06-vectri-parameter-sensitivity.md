# VECTRI Parameter Sensitivity Mini-Pack

---

**What you'll learn:**

- Run a small sensitivity suite of experiments
- Use an auto-summary script to analyze differences
- Detect key variables automatically
- Compute baseline vs experiment differences
- Generate sensitivity reports

---

This companion handout helps you **run a small sensitivity suite** and then **auto-summarize** differences using a Python script that:

- Scans your outputs
- Detects likely *EIR / incidence / infection / vector / hydrology* variables by keyword
- Computes baseline vs experiment differences
- Optionally summarizes over **Ethiopia** (default bounds can be changed)

You can use this with the tutorial datasets you already have.

---

## 1) Folder Layout

Recommended structure:

```
vectri_param_sensitivity/
  input/
    vectri.options           # optional
  outputs/
  logs/
  scripts/
```

Create folders:

```bash
mkdir -p input
```

```bash
mkdir -p outputs
```

```bash
mkdir -p logs
```

```bash
mkdir -p scripts
```

---

## 2) Baseline Run

Run the baseline simulation:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o outputs/base.nc -z logs/base.log
```

---

## 3) One-Parameter-at-a-Time Experiments

These examples use the **command line `-v`** method for clarity.

### 3.1 Toy Warming

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rtemperature_offset=1.0" -o outputs/exp_temp_plus1K.nc -z logs/exp_temp_plus1K.log
```

### 3.2 Toy Rainfall Increase

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rrainfall_factor=1.2" -o outputs/exp_rain_x1p2.nc -z logs/exp_rain_x1p2.log
```

### 3.3 Vector Biting Intensity

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rbiteratio=0.8" -o outputs/exp_rbiteratio_0p8.nc -z logs/exp_rbiteratio_0p8.log
```

### 3.4 Hydrology Sensitivity

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "wperm_default=1e-4" -o outputs/exp_wperm_1e-4.nc -z logs/exp_wperm_1e-4.log
```

### 3.5 Intervention Decay

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rbednet_tau=700" -o outputs/exp_bednet_tau_700.nc -z logs/exp_bednet_tau_700.log
```

---

## 4) Verify Parameters Were Written

Pick any experiment and check the global attributes:

```bash
ncdump -h outputs/exp_temp_plus1K.nc | grep -i rtemperature_offset
```

Check another experiment:

```bash
ncdump -h outputs/exp_rain_x1p2.nc | grep -i rrainfall_factor
```

---

## 5) Quick Batch Runner (Optional)

Create the batch script `scripts/run_sensitivity.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

mkdir -p input outputs logs

# 0) Baseline
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o outputs/base.nc -z logs/base.log

# 1) Temperature +1K
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rtemperature_offset=1.0" -o outputs/exp_temp_plus1K.nc -z logs/exp_temp_plus1K.log

# 2) Rainfall x1.2
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rrainfall_factor=1.2" -o outputs/exp_rain_x1p2.nc -z logs/exp_rain_x1p2.log

# 3) Biting ratio
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rbiteratio=0.8" -o outputs/exp_rbiteratio_0p8.nc -z logs/exp_rbiteratio_0p8.log

# 4) Permanent water default
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "wperm_default=1e-4" -o outputs/exp_wperm_1e-4.nc -z logs/exp_wperm_1e-4.log

# 5) Bednet tau
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rbednet_tau=700" -o outputs/exp_bednet_tau_700.nc -z logs/exp_bednet_tau_700.log

echo "All sensitivity runs completed."
```

Make the script executable:

```bash
chmod +x scripts/run_sensitivity.sh
```

Run the batch script:

```bash
scripts/run_sensitivity.sh
```

---

## 6) Auto-Summary Script

This handout is paired with:

- `scripts/vectri_sensitivity_summary.py`

The script will:

1. Load `outputs/base.nc` (unless you specify another baseline)
2. Scan other `.nc` files in `outputs/`
3. Detect likely key variables using keywords:
   - `eir`, `incidence`, `infect`, `vector`, `mosquito`, `cspr`, `larv`, `water`, etc.
4. Compute:
   - Global mean change
   - Optional Ethiopia mean change
   - Percent change relative to baseline
5. Write:
   - `outputs/sensitivity_report.md`
   - `outputs/sensitivity_report.csv`

### 6.1 Run the Summary

Basic usage:

```bash
python scripts/vectri_sensitivity_summary.py --baseline outputs/base.nc --pattern "outputs/*.nc"
```

### 6.2 Ethiopia-Focused Summary (Optional)

Include Ethiopia region summary:

```bash
python scripts/vectri_sensitivity_summary.py --baseline outputs/base.nc --pattern "outputs/*.nc" --ethiopia
```

### 6.3 Customize Ethiopia Bounds

To customize the bounding box:

```bash
python scripts/vectri_sensitivity_summary.py --baseline outputs/base.nc --pattern "outputs/*.nc" --ethiopia --lat-min 3 --lat-max 15 --lon-min 33 --lon-max 48
```

### 6.4 View the Reports

Check the generated reports:

```bash
cat outputs/sensitivity_report.md
```

Or open in a text editor:

```bash
nano outputs/sensitivity_report.md
```

View the CSV:

```bash
head outputs/sensitivity_report.csv
```

---

## 7) How to Interpret the Report

This mini-pack is designed for **workflow verification and teaching**:

!!! tip "Interpretation Guidelines"

    - You should see clear differences between baseline and at least some experiments
    - The sign/magnitude of change depends on:
      - Climate regime
      - Population inputs
      - Vector species settings
      - Intervention assumptions

For operational or research conclusions, you would expand:

- Longer periods
- Multiple regions
- More realistic intervention schedules
- Validated parameter ranges

---

## 8) Suggested Classroom Sequence (45–60 min)

| Step | Activity | Time |
|------|----------|------|
| 1 | Run baseline | 5–10 min |
| 2 | Run 2–3 quick experiments | 10–20 min |
| 3 | Confirm parameters in global attributes | 5 min |
| 4 | Run the auto-summary script | 5 min |
| 5 | Discuss which variables look most sensitive and why | 10–15 min |

---

## 9) Understanding the Summary Script

### 9.1 What Variables Are Detected?

The script uses keyword matching to find important variables:

| Category | Keywords |
|----------|----------|
| Transmission / Risk | `eir`, `incidence`, `case`, `cases`, `risk` |
| Infection / Immunity | `infect`, `host`, `immune` |
| Vector / Mosquitoes | `vector`, `mosquito`, `larv`, `larva`, `egg`, `bite`, `cspr`, `spr` |
| Hydrology / Climate | `water`, `pond`, `wperm`, `rain`, `precip`, `temp`, `t2m`, `tas` |

### 9.2 What Metrics Are Computed?

For each variable and experiment:

- **Baseline mean**: Average value in baseline run
- **Experiment mean**: Average value in sensitivity run
- **Delta**: Absolute change (experiment - baseline)
- **Percent change**: Relative change ((delta / baseline) × 100)

---

## 10) Example Workflow

### Step 1: Set Up

```bash
mkdir -p input outputs logs scripts
```

### Step 2: Run Baseline

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o outputs/base.nc -z logs/base.log
```

### Step 3: Run Experiments

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rtemperature_offset=1.0" -o outputs/exp_temp_plus1K.nc -z logs/exp_temp_plus1K.log
```

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "rrainfall_factor=1.2" -o outputs/exp_rain_x1p2.nc -z logs/exp_rain_x1p2.log
```

### Step 4: Generate Summary

```bash
python scripts/vectri_sensitivity_summary.py --baseline outputs/base.nc --pattern "outputs/*.nc" --ethiopia
```

### Step 5: Review Results

```bash
cat outputs/sensitivity_report.md
```

---

## 11) Troubleshooting

!!! warning "Common Issues"

    **Script can't find files:**
    
    - Ensure you're in the correct directory
    - Check that `outputs/base.nc` exists
    - Verify the pattern matches your output files
    
    **No variables detected:**
    
    - Check that output files contain expected variable names
    - Try running with `--max-vars 10` to see more variables
    
    **Ethiopia bounds error:**
    
    - Verify your data covers the specified lat/lon range
    - Adjust bounds to match your data extent

---

## 12) Next Steps

After completing this mini-pack, you can:

| Next Step | Description |
|-----------|-------------|
| Expand Experiments | Add more parameter combinations |
| Regional Analysis | Analyze specific regions of interest |
| Time Series Analysis | Compare temporal patterns |
| Visualization | Create maps and plots of differences |
| Ensemble Analysis | Run multiple ensemble members per experiment |

---

## 📝 Exercises

### Exercise 1: Basic Sensitivity Run

1. Run baseline and 2 experiments
2. Generate summary report
3. Identify which variable shows the largest change

### Exercise 2: Parameter Verification

1. Run an experiment with a custom parameter
2. Verify it appears in global attributes
3. Check if the summary script detects the change

### Exercise 3: Regional Comparison

1. Generate global summary
2. Generate Ethiopia-specific summary
3. Compare the differences between global and regional results

### Exercise 4: Multiple Parameters

1. Run an experiment changing 2 parameters simultaneously
2. Compare with single-parameter experiments
3. Discuss non-linear interactions

---

## 🔗 Additional Resources

- [VECTRI Configuring Parameters](./04-vectri-configuring-parameters.md)
- [VECTRI Hands-On Simulations](./03-vectri-hands-on-simulations.md)
- [VECTRI Output Analysis](./01-vectri-output-analysis.md)
- [VECTRI Documentation](https://users.ictp.it/~tompkins/vectri/documentation/)

