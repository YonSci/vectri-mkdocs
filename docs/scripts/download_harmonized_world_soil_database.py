#!/usr/bin/env python
"""
Extract topsoil sand/silt/clay fractions from HWSD-based NetCDF
(e.g. hwsd_soil_data_all_land.nc), crop to a region (Ethiopia by
default), convert to fractions (0–1), and optionally regrid to a
template model grid (e.g. VECTRI forcing grid).

NEW: If the HWSD NetCDF does not exist locally, the script can
optionally download it from ISIMIP using a direct URL
(--download-url, or a built-in default).

Expected input:
  - HWSD-derived NetCDF with variables:
        sand  : topsoil sand fraction in %
        silt  : topsoil silt fraction in %
        clay  : topsoil clay fraction in %
    and coordinates lat/lon (or latitude/longitude).

Output:
  - NetCDF with variables:
        sandfrac(lat, lon or model_lat, model_lon)
        siltfrac(...)
        clayfrac(...)
    all as fractions (0–1) for the topsoil layer (0–30 cm).

Dependencies:
  - numpy
  - xarray
  - requests
"""

import argparse
from pathlib import Path

import numpy as np
import xarray as xr
import requests


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Default ISIMIP URL for hwsd_soil_data_all_land.nc.
# NOTE: If this URL ever changes or requires authentication,
# you can override it with --download-url.
HWS_DEFAULT_URL = (
    "https://files.isimip.org/ISIMIP3a/InputData/geo_conditions/soil/"
    "hwsd_soil_data_all_land.nc"
)


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------

def download_file(url: str, out_path: Path, chunk_size: int = 2**20,
                  max_retries: int = 4, timeout: int = 60) -> Path:
    """
    Robust downloader with retries and partial-file cleanup.

    - Always overwrites any existing file at out_path.
    - Verifies downloaded size vs Content-Length if available.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, max_retries + 1):
        if out_path.exists():
            out_path.unlink()  # remove any partial file

        print(f"[info] Downloading {url} (attempt {attempt}/{max_retries})")

        try:
            with requests.get(url, stream=True, timeout=timeout) as r:
                r.raise_for_status()
                total = int(r.headers.get("Content-Length", 0) or 0)
                downloaded = 0

                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if not chunk:
                            continue
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total:
                            pct = 100 * downloaded / total
                            print(
                                f"\r[info] Downloaded "
                                f"{downloaded/1e6:.1f}/{total/1e6:.1f} MB ({pct:.1f}%)",
                                end="",
                            )
            print()

            # If server gave us a size, make sure we got all bytes
            if total and out_path.stat().st_size != total:
                raise IOError(
                    f"Incomplete download: got {out_path.stat().st_size} bytes, "
                    f"expected {total}"
                )

            print(f"[info] Saved to {out_path}")
            return out_path

        except Exception as e:
            print(f"\n[warn] Download failed on attempt {attempt}: {e}")
            if out_path.exists():
                out_path.unlink()
            if attempt == max_retries:
                raise RuntimeError(
                    f"Failed to download {url} after {max_retries} attempts"
                ) from e


def ensure_hwsd_file(hwsd_nc: Path, download_url: str | None = None) -> Path:
    """
    Ensure the HWSD NetCDF exists locally.

    - If it exists: do nothing.
    - If it does not exist:
        * If download_url is given, try to download.
        * Otherwise, raise a FileNotFoundError with a clear message.
    """
    hwsd_nc = Path(hwsd_nc)
    if hwsd_nc.exists():
        print(f"[info] HWSD file already present: {hwsd_nc}")
        return hwsd_nc

    if download_url is None:
        raise FileNotFoundError(
            f"HWSD file not found: {hwsd_nc}\n"
            "Please either:\n"
            "  1) Download hwsd_soil_data_all_land.nc manually from ISIMIP,\n"
            "     and point --hwsd-nc to its location, or\n"
            "  2) Re-run this script with --download-url pointing to the\n"
            "     direct 'Download file' link from the ISIMIP file page."
        )

    print(
        f"[info] HWSD file not found locally. Attempting to download from:\n"
        f"       {download_url}"
    )
    download_file(download_url, hwsd_nc)
    return hwsd_nc


# ---------------------------------------------------------------------------
# Coordinate / regridding helpers
# ---------------------------------------------------------------------------

def _find_lat_lon_names(ds, lat_guess=("lat", "latitude", "y"),
                        lon_guess=("lon", "longitude", "x")):
    """Find lat/lon coordinate names in a dataset."""
    lat_name = next((n for n in lat_guess if n in ds.coords), None)
    lon_name = next((n for n in lon_guess if n in ds.coords), None)
    if lat_name is None or lon_name is None:
        raise ValueError(
            f"Could not find lat/lon coords in dataset. Tried {lat_guess} "
            f"for lat and {lon_guess} for lon. "
            f"Available coords: {list(ds.coords)}"
        )
    return lat_name, lon_name


def _sort_lat_lon(ds, lat_name, lon_name):
    """Ensure lat & lon are ascending in the dataset."""
    if float(ds[lat_name][0]) > float(ds[lat_name][-1]):
        ds = ds.sortby(lat_name)
    if float(ds[lon_name][0]) > float(ds[lon_name][-1]):
        ds = ds.sortby(lon_name)
    return ds


# ---------------------------------------------------------------------------
# Core HWSD processing
# ---------------------------------------------------------------------------

def load_hwsd_topsoil_fractions(
    hwsd_nc: Path,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
) -> xr.Dataset:
    """
    Load HWSD-derived soil texture data, crop to a bounding box,
    and convert sand/silt/clay to fractions (0–1).

    Assumes variables 'sand', 'silt', and 'clay' in percent (%).
    """
    hwsd_nc = Path(hwsd_nc)
    print(f"[info] Opening HWSD file: {hwsd_nc}")
    ds = xr.open_dataset(hwsd_nc)

    lat_name, lon_name = _find_lat_lon_names(ds)
    ds = _sort_lat_lon(ds, lat_name, lon_name)

    print(
        f"[info] Cropping to box: "
        f"{lat_name}=[{lat_min}, {lat_max}], {lon_name}=[{lon_min}, {lon_max}]"
    )
    ds_sub = ds.sel(
        {lat_name: slice(lat_min, lat_max),
         lon_name: slice(lon_min, lon_max)}
    )

    # Check variables
    for v in ("sand", "silt", "clay"):
        if v not in ds_sub.variables:
            raise KeyError(
                f"Variable '{v}' not found in HWSD dataset. "
                f"Available variables: {list(ds_sub.data_vars)}"
            )

    sand = ds_sub["sand"]
    silt = ds_sub["silt"]
    clay = ds_sub["clay"]

    # In case there is an extra dimension like "layer" or "depth", take first
    for name, arr in (("sand", sand), ("silt", silt), ("clay", clay)):
        extra_dims = [d for d in arr.dims if d not in (lat_name, lon_name)]
        if extra_dims:
            print(
                f"[warn] Variable '{name}' has extra dims {extra_dims}, "
                "taking first index along each."
            )
            sel_dict = {d: 0 for d in extra_dims}
            ds_sub[name] = arr.isel(**sel_dict)

    sand = ds_sub["sand"]
    silt = ds_sub["silt"]
    clay = ds_sub["clay"]

    # Convert % -> fraction (0–1), clip [0, 1] to be safe
    sandfrac = (sand / 100.0).clip(0.0, 1.0).astype("float32")
    siltfrac = (silt / 100.0).clip(0.0, 1.0).astype("float32")
    clayfrac = (clay / 100.0).clip(0.0, 1.0).astype("float32")

    sandfrac.name = "sandfrac"
    siltfrac.name = "siltfrac"
    clayfrac.name = "clayfrac"

    sandfrac.attrs.update(
        {
            "units": "1",
            "long_name": "Topsoil sand fraction (0–30 cm)",
            "source": "HWSD-derived soil map (e.g. hwsd_soil_data_all_land.nc)",
        }
    )
    siltfrac.attrs.update(
        {
            "units": "1",
            "long_name": "Topsoil silt fraction (0–30 cm)",
            "source": "HWSD-derived soil map (e.g. hwsd_soil_data_all_land.nc)",
        }
    )
    clayfrac.attrs.update(
        {
            "units": "1",
            "long_name": "Topsoil clay fraction (0–30 cm)",
            "source": "HWSD-derived soil map (e.g. hwsd_soil_data_all_land.nc)",
        }
    )

    ds_out = xr.Dataset(
        {
            "sandfrac": sandfrac,
            "siltfrac": siltfrac,
            "clayfrac": clayfrac,
        }
    )
    # Keep coordinate attributes
    ds_out[lat_name].attrs.update(ds_sub[lat_name].attrs)
    ds_out[lon_name].attrs.update(ds_sub[lon_name].attrs)

    return ds_out


def regrid_to_template(
    ds: xr.Dataset,
    template_nc: Path,
    lat_name_guess=("lat", "latitude", "y"),
    lon_name_guess=("lon", "longitude", "x"),
) -> xr.Dataset:
    """
    Interpolate soil fractions to the lat/lon coordinates of template_nc.

    Assumes ds has coords named 'lat'/'lon' or similar (see _find_lat_lon_names).
    """
    template_nc = Path(template_nc)
    print(f"[info] Opening template grid: {template_nc}")
    ds_tmpl = xr.open_dataset(template_nc)

    # Coordinates in ds
    lat_name_ds, lon_name_ds = _find_lat_lon_names(ds, lat_name_guess, lon_name_guess)
    ds = _sort_lat_lon(ds, lat_name_ds, lon_name_ds)

    # Coordinates in template
    lat_name_tmpl, lon_name_tmpl = _find_lat_lon_names(
        ds_tmpl, lat_name_guess, lon_name_guess
    )
    lat_t = ds_tmpl[lat_name_tmpl]
    lon_t = ds_tmpl[lon_name_tmpl]

    print(
        f"[info] Interpolating to template grid: "
        f"{lat_name_tmpl}={lat_t.size}, {lon_name_tmpl}={lon_t.size}"
    )

    # Interpolate each variable
    ds_interp = xr.Dataset()
    for v in ("sandfrac", "siltfrac", "clayfrac"):
        if v not in ds:
            raise KeyError(
                f"Variable '{v}' not found in dataset being regridded."
            )
        da = ds[v]
        da_i = da.interp(
            {lat_name_ds: lat_t, lon_name_ds: lon_t},
            method="linear",
        )
        # Rename coords if necessary
        rename_dict = {}
        if lat_name_ds != lat_name_tmpl:
            rename_dict[lat_name_ds] = lat_name_tmpl
        if lon_name_ds != lon_name_tmpl:
            rename_dict[lon_name_ds] = lon_name_tmpl
        if rename_dict:
            da_i = da_i.rename(rename_dict)
        ds_interp[v] = da_i.astype("float32")

    # Copy coord metadata
    ds_interp[lat_name_tmpl].attrs.update(ds_tmpl[lat_name_tmpl].attrs)
    ds_interp[lon_name_tmpl].attrs.update(ds_tmpl[lon_name_tmpl].attrs)

    ds_interp.attrs.update(
        {
            "regridded_to": str(template_nc),
        }
    )

    return ds_interp


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Extract HWSD-based topsoil sand/silt/clay fractions from a "
            "NetCDF (e.g. hwsd_soil_data_all_land.nc), crop to a region "
            "(Ethiopia by default), convert to fractions (0–1), and optionally "
            "regrid to a template model grid."
        )
    )
    parser.add_argument(
        "--hwsd-nc", type=str, required=True,
        help=(
            "Path where the HWSD NetCDF (e.g. hwsd_soil_data_all_land.nc) "
            "should be located. If it does not exist, the script can try to "
            "download it using --download-url (or the built-in default)."
        ),
    )
    parser.add_argument(
        "--download-url", type=str, default=None,
        help=(
            "Optional direct URL for the HWSD NetCDF. "
            "If --hwsd-nc does not exist locally, the script will try to "
            "download from this URL. If not given, a built-in default ISIMIP "
            "URL is used, which may require you to be on a network with "
            "access / logged in."
        ),
    )
    parser.add_argument(
        "--lat-min", type=float, default=3.0,
        help="Minimum latitude of area of interest (default: 3.0 for Ethiopia)",
    )
    parser.add_argument(
        "--lat-max", type=float, default=15.0,
        help="Maximum latitude of area of interest (default: 15.0 for Ethiopia)",
    )
    parser.add_argument(
        "--lon-min", type=float, default=33.0,
        help="Minimum longitude of area of interest (default: 33.0 for Ethiopia)",
    )
    parser.add_argument(
        "--lon-max", type=float, default=48.0,
        help="Maximum longitude of area of interest (default: 48.0 for Ethiopia)",
    )
    parser.add_argument(
        "--out-nc", type=str, required=True,
        help="Output NetCDF file path.",
    )
    parser.add_argument(
        "--template-nc", type=str, default=None,
        help=(
            "Optional template NetCDF (e.g. example_sys5.nc). "
            "If provided, soil fractions will be interpolated to its "
            "lat/lon grid."
        ),
    )

    args = parser.parse_args()

    hwsd_nc = Path(args.hwsd_nc)
    out_nc = Path(args.out_nc)
    template_nc = Path(args.template_nc) if args.template_nc else None

    lat_min = args.lat_min
    lat_max = args.lat_max
    lon_min = args.lon_min
    lon_max = args.lon_max

    # Decide which URL to use if download is needed
    download_url = args.download_url if args.download_url else HWS_DEFAULT_URL

    # Ensure HWSD file exists (download if missing)
    hwsd_nc = ensure_hwsd_file(hwsd_nc, download_url=download_url)

    # Load HWSD-based fractions for the region
    ds_frac = load_hwsd_topsoil_fractions(
        hwsd_nc=hwsd_nc,
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
    )

    # Optionally interpolate to template grid
    if template_nc is not None:
        print(f"[info] Regridding soil fractions to template grid: {template_nc}")
        ds_frac = regrid_to_template(ds_frac, template_nc)

    ds_frac.attrs.update(
        {
            "title": "Topsoil (0–30 cm) sand/silt/clay fractions from HWSD-derived map",
            "history": "Created by hwsd_texture_to_vectri_soil.py",
            "comment": (
                "Sand, silt, clay topsoil mass fractions (0–1) derived from "
                "HWSD-based NetCDF (e.g. hwsd_soil_data_all_land.nc)."
            ),
        }
    )

    out_nc.parent.mkdir(parents=True, exist_ok=True)
    print(f"[info] Writing NetCDF: {out_nc}")
    ds_frac.to_netcdf(out_nc)
    print("[info] Done.")


if __name__ == "__main__":
    main()
