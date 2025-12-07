#!/usr/bin/env python
"""
Download AfriPop / WorldPop Ethiopia 100m population raster, then convert it
to population density (per km^2 or m^2), with optional regridding to a
template NetCDF grid (e.g. VECTRI climate driver).

Data source (AfriPop Ethiopia):
  Hub page: https://hub.worldpop.org/doi/10.5258/SOTON/WP00087
  Files (served from data.worldpop.org):
    ETH10adjv5.tif  (2010, UN-adjusted counts)
    ETH10v5.tif     (2010, unadjusted counts)
    ETH15adjv5.tif  (2015, UN-adjusted counts)
    ETH15v5.tif     (2015, unadjusted counts)
Units: estimated persons per grid square (~100 m), WGS84, GeoTIFF.

Example usage:

  # 1) Download 2010 UN-adjusted AfriPop and make persons per km^2 (AfriPop grid)
  python afripop_to_vectri_pop.py ^
      --year 2010 ^
      --out-nc data/pop_eth_afripop_2010_km2.nc

  # 2) Same but persons per m^2 on VECTRI climate grid
  python afripop_to_vectri_pop.py ^
      --year 2010 ^
      --out-nc data/pop_eth_vectri_grid_2010_m2.nc ^
      --per-m2 ^
      --template-nc example_sys5.nc

  # 3) Use unadjusted counts (not UN-adjusted)
  python afripop_to_vectri_pop.py ^
      --year 2015 ^
      --unadjusted ^
      --out-nc data/pop_eth_afripop_2015_km2.nc
"""

import argparse
from pathlib import Path
from typing import Optional

import numpy as np
import requests
import xarray as xr
import rioxarray as rxr


# Base URL for AfriPop/WorldPop Ethiopia 100m population
BASE_URL = (
    "https://data.worldpop.org/"
    "GIS/Population/Individual_countries/ETH/"
    "Ethiopia_100m_Population/{filename}"
)


def build_filename(year: int, adjusted: bool) -> str:
    """
    Build AfriPop filename for Ethiopia given year and adjustment flag.

    Valid combinations (version 5):
      2010, adjusted   -> ETH10adjv5.tif
      2010, unadjusted -> ETH10v5.tif
      2015, adjusted   -> ETH15adjv5.tif
      2015, unadjusted -> ETH15v5.tif
    """
    if year not in (2010, 2015):
        raise ValueError("Only years 2010 and 2015 are available for this AfriPop set.")

    yy = str(year)[-2:]  # "10" or "15"
    if adjusted:
        return f"ETH{yy}adjv5.tif"
    else:
        return f"ETH{yy}v5.tif"


def download_afripop_file(year: int, adjusted: bool, data_dir: Path) -> Path:
    """
    Ensure the AfriPop GeoTIFF file exists locally; if not, download it.

    Returns
    -------
    tif_path : Path
        Local path to the downloaded (or already existing) GeoTIFF.
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    filename = build_filename(year, adjusted)
    tif_path = data_dir / filename

    if tif_path.exists():
        print(f"[info] AfriPop file already present: {tif_path}")
        return tif_path

    url = BASE_URL.format(filename=filename)
    print(f"[info] Downloading AfriPop from:\n       {url}")
    print(f"[info] Saving to: {tif_path}")

    with requests.get(url, stream=True) as r:
        try:
            r.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Failed to download {url} (HTTP {r.status_code}). "
                f"Check internet connection or try in browser."
            ) from exc

        total = int(r.headers.get("Content-Length", 0) or 0)
        downloaded = 0
        with open(tif_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
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

    print(f"\n[info] Download complete: {tif_path}")
    return tif_path


def compute_cell_area_km2(lat_vals, lon_vals):
    """
    Approximate spherical-Earth pixel area for each (lat, lon) cell of a
    regular lat/lon grid.

    Returns
    -------
    area_km2 : np.ndarray
        2D array with shape (nlat, nlon) giving area in km^2.
    """
    R = 6371.0  # Earth radius in km

    lat = np.asarray(lat_vals)
    lon = np.asarray(lon_vals)

    if lat.size < 2 or lon.size < 2:
        raise ValueError("Need at least 2 lat and lon points to compute grid spacing.")

    dlat_deg = float(np.abs(lat[1] - lat[0]))
    dlon_deg = float(np.abs(lon[1] - lon[0]))

    dlat = np.deg2rad(dlat_deg)
    dlon = np.deg2rad(dlon_deg)

    phi = np.deg2rad(lat)
    sin_term = np.sin(phi + dlat / 2.0) - np.sin(phi - dlat / 2.0)

    area_band_km2 = (R**2) * dlon * sin_term  # (nlat,)

    area_km2 = np.repeat(area_band_km2[:, np.newaxis], lon.size, axis=1)
    return area_km2


def afripop_to_density(
    afripop_tif: Path,
    out_nc: Path,
    per_m2: bool = False,
    template_nc: Optional[Path] = None,
    out_var_name: str = "population",
):
    """
    Convert AfriPop/WorldPop raster (counts per pixel) to population density.

    Parameters
    ----------
    afripop_tif : Path
        Path to AfriPop GeoTIFF (counts per grid cell).
    out_nc : Path
        Output NetCDF path.
    per_m2 : bool
        If True, output in persons m^-2, else persons km^-2.
    template_nc : Path or None
        If provided, interpolate density to its lat/lon grid.
    out_var_name : str
        Variable name in output NetCDF.
    """
    afripop_tif = afripop_tif.expanduser()
    if not afripop_tif.exists():
        raise FileNotFoundError(f"Input raster not found: {afripop_tif}")

    # 1. Read AfriPop raster (counts per cell), masking nodata
    #    masked=True ensures nodata becomes NaN instead of huge negative values.
    da = rxr.open_rasterio(afripop_tif, masked=True).squeeze(drop=True)

    # CRS
    if da.rio.crs is None:
        print("[warn] AfriPop file has no CRS; assuming EPSG:4326 (WGS84).")
        da = da.rio.write_crs("EPSG:4326", inplace=False)

    # Rename dimensions to lat/lon
    da = da.rename({"y": "lat", "x": "lon"})

    # Explicitly mask nodata and any negative values (no negative population)
    nodata = da.rio.nodata
    if nodata is not None:
        da = da.where(da != nodata)

    da = da.where(da >= 0)

    lat_vals = da["lat"].values
    lon_vals = da["lon"].values

    print(
        f"[info] AfriPop grid: nlat={lat_vals.size}, nlon={lon_vals.size}, "
        f"lat range=({float(lat_vals.min()):.3f}, {float(lat_vals.max()):.3f}), "
        f"lon range=({float(lon_vals.min()):.3f}, {float(lon_vals.max()):.3f})"
    )

    # 2. Compute cell area (km^2)
    area_km2 = compute_cell_area_km2(lat_vals, lon_vals)
    area_da = xr.DataArray(
        area_km2,
        coords={"lat": lat_vals, "lon": lon_vals},
        dims=("lat", "lon"),
        name="cell_area",
        attrs={"units": "km2", "long_name": "grid_cell_area"},
    )

    # 3. Density = persons / km^2
    density_km2 = da / area_da
    density_km2.name = out_var_name
    density_km2.attrs.setdefault(
        "long_name", "population density derived from AfriPop/WorldPop counts"
    )

    # Remove any non-finite values
    density_km2 = density_km2.where(np.isfinite(density_km2))

    if per_m2:
        density = density_km2 / 1e6  # 1 km^2 = 1e6 m^2
        density.attrs["units"] = "persons m-2"
    else:
        density = density_km2
        density.attrs["units"] = "persons km-2"

    # 4. Optional regridding to template grid
    if template_nc is not None:
        ds_tmpl = xr.open_dataset(template_nc)

        # Try to detect lat/lon names
        lat_name = None
        lon_name = None
        for cand in ["lat", "latitude", "y"]:
            if cand in ds_tmpl.coords:
                lat_name = cand
                break
        for cand in ["lon", "longitude", "x"]:
            if cand in ds_tmpl.coords:
                lon_name = cand
                break

        if lat_name is None or lon_name is None:
            raise ValueError(
                "Could not find latitude/longitude coordinates in template NetCDF."
            )

        lat_target = ds_tmpl[lat_name]
        lon_target = ds_tmpl[lon_name]

        print(
            f"[info] Regridding density to template grid: "
            f"{lat_name}={lat_target.size}, {lon_name}={lon_target.size}"
        )

        density_interp = density.interp(lat=lat_target, lon=lon_target)

        # Rename coords back to template names if needed
        rename_dict = {}
        if lat_name != "lat":
            rename_dict["lat"] = lat_name
        if lon_name != "lon":
            rename_dict["lon"] = lon_name
        if rename_dict:
            density_interp = density_interp.rename(rename_dict)

        density = density_interp

    # Final clean-up: keep only finite, non-negative values
    density = density.where(np.isfinite(density) & (density >= 0))

    # 5. Save to NetCDF
    out_nc.parent.mkdir(parents=True, exist_ok=True)
    ds_out = density.to_dataset(name=out_var_name)
    ds_out.to_netcdf(out_nc)
    print(f"[info] Wrote population density to {out_nc}")
    if template_nc is not None:
        print("[info] Grid matches template NetCDF.")
    else:
        print("[info] Grid matches original AfriPop raster.")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Download AfriPop/WorldPop Ethiopia 100m population (2010/2015) and "
            "convert to population density (per km^2 or m^2), with optional "
            "regridding to a template NetCDF grid."
        )
    )
    parser.add_argument(
        "--year",
        type=int,
        choices=[2010, 2015],
        default=2010,
        help="AfriPop year (2010 or 2015; default: 2010).",
    )
    parser.add_argument(
        "--unadjusted",
        action="store_true",
        help="Use UN-unadjusted counts (default: UN-adjusted).",
    )
    parser.add_argument(
        "--data-dir",
        default="data/afripop_eth",
        help="Directory to store/download AfriPop GeoTIFFs "
             "(default: data/afripop_eth).",
    )
    parser.add_argument(
        "--out-nc",
        required=True,
        help="Output NetCDF file for population density.",
    )
    parser.add_argument(
        "--per-m2",
        action="store_true",
        help="If set, output units will be persons m^-2 (default: persons km^-2).",
    )
    parser.add_argument(
        "--template-nc",
        default=None,
        help=(
            "Optional template NetCDF file; if provided, density will be "
            "interpolated to its lat/lon grid (e.g. example_sys5.nc)."
        ),
    )
    parser.add_argument(
        "--var-name",
        default="population",
        help="Name of the output variable (default: population).",
    )

    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_nc = Path(args.out_nc)
    template_nc = Path(args.template_nc) if args.template_nc else None

    # 1. Ensure AfriPop file is present (download if needed)
    tif_path = download_afripop_file(
        year=args.year,
        adjusted=not args.unadjusted,
        data_dir=data_dir,
    )

    # 2. Convert to density and write NetCDF
    afripop_to_density(
        afripop_tif=tif_path,
        out_nc=out_nc,
        per_m2=args.per_m2,
        template_nc=template_nc,
        out_var_name=args.var_name,
    )


if __name__ == "__main__":
    main()
