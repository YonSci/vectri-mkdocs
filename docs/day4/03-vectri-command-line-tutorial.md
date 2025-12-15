# VECTRI Command Line Tutorial (Step-by-Step)

---

**What you'll learn:**

- Run VECTRI from the command line
- Understand all major command-line options
- Set up proper run directories
- Use options files and inline parameters
- Run ensemble simulations
- Troubleshoot common issues

---

This guide shows how to run **VECTRI** from the command line using the main options.

It is written to match the typical **tutorial folder** that contains files like:

| File | Description |
|------|-------------|
| `example_sys5.nc` / `example_sys5.grb` | Example climate data |
| `example_data.nc` | Example population/ancillary data |
| `example_data_wperm.nc` or `example_wperm.nc` | Examples with permanent breeding fraction |
| `vectri_calibrated.options` | Example options/namelist-style settings |
| `vectri_fake_clim.nc`, `vectri_fake_data.nc` | Small test files |

!!! note
    File names can vary between tutorial versions. If your filenames differ, just substitute accordingly.

---

## 1) Before You Run

### 1.1 Recommended Folder Practice

To avoid cluttering and accidental git tracking, keep separate directories for:

- **Code directory** — where you installed VECTRI
- **Run directory** — where you execute simulations

Example layout:

```
$HOME/vectri                        # code
$HOME/myruns/vectri_tutorial_run    # runs
```

Copy or symlink tutorial data into your **run** folder.

### 1.2 Check the Executable

Assuming you have an environment variable `VECTRI` set:

```bash
echo $VECTRI
```

```bash
ls $VECTRI
```

Run help to see all options:

```bash
$VECTRI/vectri -h
```

---

## 2) Command-Line Options Overview

| Option | What it does |
|--------|--------------|
| `-c` | Climate file (GRIB or NetCDF). Usually contains temperature; may also include precipitation. |
| `-d` | Data file (NetCDF). Must include **population**; may also include permanent breeding fraction, land use, etc. |
| `-o` | Output filename (default: `vectri.nc`) |
| `-p` | Separate precipitation file if not included in `-c` |
| `-a` | Options/arguments file to set model parameters (default: `./input/vectri.options`) |
| `-r` | Input directory (default: `./input`) |
| `-v` | Pass options inline without editing a file |
| `-i` | Restart/init file |
| `-e` | Ensemble number (for reproducibility) |
| `-x` | Vector species selector |
| `-n` | Namelist file path/name |
| `-z` | Redirect text output to a file |
| `-g` | Force climate file format as GRIB |
| `-u` | Debug compilation flag (advanced/developer use) |

---

## 3) Minimal Run (NetCDF Climate)

From your **run** directory (where the tutorial files are located):

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc
```

This will produce:

- `vectri.nc` (default output)
- Screen log output

---

## 4) Choose an Output Name

Use the `-o` flag to specify the output filename:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o out_example_sys5.nc
```

---

## 5) Using GRIB Climate

If your climate file is GRIB (`.grb`), VECTRI usually auto-detects the format:

```bash
$VECTRI/vectri -c example_sys5.grb -d example_data.nc -o out_example_sys5_grb.nc
```

If needed, force GRIB parsing with the `-g` flag:

```bash
$VECTRI/vectri -g -c example_sys5.grb -d example_data.nc -o out_forced_grb.nc
```

---

## 6) When Precipitation is Separate (`-p`)

If the climate file provided with `-c` contains only temperature, you can supply a separate precipitation file:

```bash
$VECTRI/vectri -c example_sys5.nc -p era_geo_an.grb -d example_data.nc -o out_temp_plus_precip.nc
```

!!! note
    If your tutorial climate file already includes precipitation, `-p` is not required.

---

## 7) Using an Options File (`-a`)

### 7.1 Default Behavior

By default VECTRI looks for:

```
./input/vectri.options
```

So if you have an `input/` directory in your run folder:

```bash
mkdir -p input
```

```bash
cp vectri_calibrated.options input/vectri.options
```

Then run:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o out_with_default_options.nc
```

### 7.2 Explicitly Set an Options File

If your options file is elsewhere:

```bash
$VECTRI/vectri -a vectri_calibrated.options -c example_sys5.nc -d example_data.nc -o out_with_calibrated_options.nc
```

---

## 8) Changing the Input Directory (`-r`)

If you want to keep inputs in a custom folder:

```bash
mkdir -p myinput
```

```bash
cp vectri_calibrated.options myinput/vectri.options
```

Run with custom input directory:

```bash
$VECTRI/vectri -r myinput -a myinput/vectri.options -c example_sys5.nc -d example_data.nc -o out_custom_inputdir.nc
```

!!! warning "Important"
    When you change the input directory with `-r`, you should also specify `-a` explicitly.

---

## 9) Passing Options Inline (`-v`)

This is handy for quick experiments without editing files:

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -v "nloopspinup=3,nlenspinup=180" -o out_inline_options.nc
```

Use this instead of editing `vectri.options` when you only need small changes.

---

## 10) Restart Runs (`-i`)

If you have a previous restart file:

```bash
$VECTRI/vectri -i restart_01.nc -c example_sys5.nc -d example_data.nc -o out_from_restart.nc
```

!!! note
    If `-i` is not set or the file does not exist, VECTRI uses artificial initial conditions.

---

## 11) Ensemble Runs (`-e`)

For reproducible ensemble members, use the `-e` flag with different numbers:

Member 1:

```bash
$VECTRI/vectri -e 1 -c example_sys5.nc -d example_data.nc -o out_member_01.nc
```

Member 2:

```bash
$VECTRI/vectri -e 2 -c example_sys5.nc -d example_data.nc -o out_member_02.nc
```

Member 3:

```bash
$VECTRI/vectri -e 3 -c example_sys5.nc -d example_data.nc -o out_member_03.nc
```

---

## 12) Vector Species Selection (`-x`)

### Default: An. gambiae

```bash
$VECTRI/vectri -x 0 -c example_sys5.nc -d example_data.nc -o out_gambiae.nc
```

### An. funestus (unvalidated)

```bash
$VECTRI/vectri -x 1 -c example_sys5.nc -d example_data.nc -o out_funestus.nc
```

### Ae. albopictus (under development)

```bash
$VECTRI/vectri -x 10 -c example_sys5.nc -d example_data.nc -o out_albopictus.nc
```

---

## 13) Using a Namelist File (`-n`)

If your setup requires a custom namelist:

```bash
$VECTRI/vectri -n my_vectri.namelist -c example_sys5.nc -d example_data.nc -o out_custom_namelist.nc
```

---

## 14) Save Text Output to a Log File (`-z`)

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o out_logged.nc -z run_log.txt
```

This is useful for troubleshooting and keeping records.

---

## 15) Complete "Best Practice" Example

A clean, reproducible command you can adapt:

Create directories:

```bash
mkdir -p outputs logs input
```

Copy options file:

```bash
cp vectri_calibrated.options input/vectri.options
```

Run VECTRI:

```bash
$VECTRI/vectri -a input/vectri.options -c example_sys5.nc -d example_data.nc -e 1 -v "nloopspinup=3,nlenspinup=180" -o outputs/ethiopia_tutorial_member01.nc -z logs/ethiopia_tutorial_member01.txt
```

---

## 16) Common Pitfalls & Quick Fixes

!!! warning "Troubleshooting"

    **"Cannot find vectri.options"**
    
    - Make sure `./input/vectri.options` exists, or provide `-a path/to/options`
    
    **Climate variables not recognized**
    
    - Confirm your climate file contains the required variables and correct units
    - Use the tutorial file first to validate your workflow
    
    **You accidentally ran inside the code folder**
    
    - Move to a separate run directory and re-run
    
    **Output too large / too many files**
    
    - Use a dedicated `outputs/` folder and name runs clearly with `-o`

---

## 17) Cheat Sheet

### Help

```bash
$VECTRI/vectri -h
```

### Minimal Run

```bash
$VECTRI/vectri -c CLIM.nc -d DATA.nc
```

### With Output Name

```bash
$VECTRI/vectri -c CLIM.nc -d DATA.nc -o OUT.nc
```

### Separate Precipitation

```bash
$VECTRI/vectri -c TEMP.nc -p PREC.nc -d DATA.nc -o OUT.nc
```

### Options File

```bash
$VECTRI/vectri -a vectri.options -c CLIM.nc -d DATA.nc -o OUT.nc
```

### Custom Input Directory

```bash
$VECTRI/vectri -r input_dir -a input_dir/vectri.options -c CLIM.nc -d DATA.nc
```

### Inline Options

```bash
$VECTRI/vectri -v "key1=val1,key2=val2" -c CLIM.nc -d DATA.nc
```

### Ensemble Member

```bash
$VECTRI/vectri -e 5 -c CLIM.nc -d DATA.nc -o member05.nc
```

### Restart Run

```bash
$VECTRI/vectri -i restart.nc -c CLIM.nc -d DATA.nc -o OUT.nc
```

### Vector Species

```bash
$VECTRI/vectri -x 0 -c CLIM.nc -d DATA.nc
```

---

## 18) Next Steps

After mastering the command line, you can:

- Explain expected **variables** inside climate and data files using `ncdump -h`
- Create a simple post-processing workflow:
    - Open `vectri.nc`
    - Map risk metrics
    - Compare months/seasons
- Develop a template for country-level runs with clipped climate inputs

---

## Appendix: Example Run Script

You can save this as `run_tutorial.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

VECTRI_EXE="${VECTRI:-$HOME/vectri}/vectri"

mkdir -p outputs logs input
cp -f vectri_calibrated.options input/vectri.options

"${VECTRI_EXE}" \
  -a input/vectri.options \
  -c example_sys5.nc \
  -d example_data.nc \
  -e 1 \
  -o outputs/tutorial_run_member01.nc \
  -z logs/tutorial_run_member01.txt

echo "Done. Output: outputs/tutorial_run_member01.nc"
```

Make it executable:

```bash
chmod +x run_tutorial.sh
```

Run the script:

```bash
./run_tutorial.sh
```

---

## 📝 Exercises

### Exercise 1: Basic Run

1. Navigate to your tutorial directory
2. Run VECTRI with the example files
3. Verify the output file was created

```bash
$VECTRI/vectri -c example_sys5.nc -d example_data.nc -o my_first_run.nc
```

```bash
ls -la my_first_run.nc
```

### Exercise 2: Ensemble Members

1. Run 3 ensemble members
2. Compare the output file sizes
3. Use `ncdump -h` to verify they have the same structure

### Exercise 3: Custom Options

1. Create an `input/` directory
2. Copy the options file
3. Modify spinup parameters using `-v`
4. Run and save output to a custom location

### Exercise 4: Logging

1. Run VECTRI with the `-z` flag
2. Examine the log file
3. Identify key information (runtime, parameters used, warnings)

---

## 🔗 Additional Resources

- [VECTRI Documentation](https://users.ictp.it/~tompkins/vectri/documentation/)
- [VECTRI Manual (PDF)](../pdfs/VECTRI_manual_v1.6.pdf)
- [NetCDF Tools Guide](https://www.unidata.ucar.edu/software/netcdf/)

