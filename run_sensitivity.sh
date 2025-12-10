#!/usr/bin/env bash
set -euo pipefail

mkdir -p input outputs logs

# 0) Baseline
$VECTRI/vectri   -c example_sys5.nc   -d example_data.nc   -o outputs/base.nc   -z logs/base.log

# 1) Temperature +1K
$VECTRI/vectri   -c example_sys5.nc   -d example_data.nc   -v "rtemperature_offset=1.0"   -o outputs/exp_temp_plus1K.nc   -z logs/exp_temp_plus1K.log

# 2) Rainfall x1.2
$VECTRI/vectri   -c example_sys5.nc   -d example_data.nc   -v "rrainfall_factor=1.2"   -o outputs/exp_rain_x1p2.nc   -z logs/exp_rain_x1p2.log

# 3) Biting ratio
$VECTRI/vectri   -c example_sys5.nc   -d example_data.nc   -v "rbiteratio=0.8"   -o outputs/exp_rbiteratio_0p8.nc   -z logs/exp_rbiteratio_0p8.log

# 4) Permanent water default
$VECTRI/vectri   -c example_sys5.nc   -d example_data.nc   -v "wperm_default=1e-4"   -o outputs/exp_wperm_1e-4.nc   -z logs/exp_wperm_1e-4.log

# 5) Bednet tau
$VECTRI/vectri   -c example_sys5.nc   -d example_data.nc   -v "rbednet_tau=700"   -o outputs/exp_bednet_tau_700.nc   -z logs/exp_bednet_tau_700.log

echo "All sensitivity runs completed."