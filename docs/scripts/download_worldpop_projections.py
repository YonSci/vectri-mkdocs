#!/usr/bin/env python
"""
Convert WorldPop Global_2015_2030 / R2025A (ETH, 1km unconstrained, constrained surface)
to population density (persons/km2) in NetCDF format.

Example:
    python worldpop_R2025A_to_vectri_pop.py \
        --year 2030 \
        --out-nc data/pop_eth_worldpop_R2025A_2030_km2.nc
"""

import argparse
from pathlib import Path

import numpy as np
import xarray as xr
import rioxarray as rxr
import requests

EARTH_RADIUS_KM = 6371.0088


def download_file(url: str, out_path: Path, chunk_size: int = 2**20) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists():
        print(f"[info] File already exists, skipping download: {out_path}")
        return out_path

    print(f"[info] Downloading {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

    print(f"[info] Saved to {out_path}")
    return out_path


def build_worldpop_R2025A_url(year: int) -> str:
    """
    Build download URL for Ethiopia R2025A 1km_ua constrained GeoTIFF.

    Pattern (example 2030):
    https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2030/ETH/v1/1km_ua/constrained/eth_pop_2030_CN_1km_R2025A_UA_v1.tif
    """
    base = "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A"
    iso3 = "ETH"
    fname = f"eth_pop_{year}_CN_1km_R2025A_UA_v1.tif"
    return f"{base}/{year}/{iso3}/v1/1km_ua/constrained/{fname}"


def compute_cell_area_km2(lat: np.ndarray, lon: np.ndarray) -> xr.DataArray:
    if lat.size < 2 or lon.size < 2:
        raise ValueError("Need at least 2 lat and 2 lon points to compute cell area.")

    lat_rad = np.deg2rad(lat)
    dlat = np.abs(lat_rad[1] - lat_rad[0])
    dlon = np.abs(np.deg2rad(lon[1] - lon[0]))

    phi1 = lat_rad - 0.5 * dlat
    phi2 = lat_rad + 0.5 * dlat

    row_areas = (EARTH_RADIUS_KM ** 2) * dlon * (np.sin(phi2) - np.sin(phi1))
    area2d = np.repeat(row_areas[:, np.newaxis], lon.size, axis=1)

    return xr.DataArray(
        area2d,
        coords={"lat": lat, "lon": lon},
        dims=("lat", "lon"),
        name="cell_area",
        attrs={"units": "km2", "long_name": "grid-cell area"},
    )


def tif_to_density_nc(tif_path: Path, out_nc: Path, var_name: str = "pop_density") -> None:
    tif_path = Path(tif_path)
    out_nc = Path(out_nc)
    out_nc.parent.mkdir(parents=True, exist_ok=True)

    print(f"[info] Reading GeoTIFF: {tif_path}")
    da = rxr.open_rasterio(tif_path, masked=True).squeeze(drop=True)
    da = da.rename({"x": "lon", "y": "lat"})

    if float(da.lat[0]) > float(da.lat[-1]):
        da = da.sortby("lat")

    if not da.rio.crs:
        da = da.rio.write_crs("EPSG:4326", inplace=True)

    area = compute_cell_area_km2(da["lat"].values, da["lon"].values)
    density = (da / area).astype("float32")
    density.name = var_name
    density.attrs.update(
        {
            "units": "persons km-2",
            "long_name": "Projected population density",
            "source": "WorldPop Global_2015_2030 R2025A (country = ETH, 1km_ua/constrained)",
        }
    )

    ds_out = density.to_dataset()
    ds_out["lat"].attrs.update(
        {"units": "degrees_north", "standard_name": "latitude"}
    )
    ds_out["lon"].attrs.update(
        {"units": "degrees_east", "standard_name": "longitude"}
    )

    encoding = {var_name: {"_FillValue": np.float32(np.nan)}}

    print(f"[info] Writing NetCDF: {out_nc}")
    ds_out.to_netcdf(out_nc, encoding=encoding)
    print("[info] Done.")


def main():
    parser = argparse.ArgumentParser(
        description="WorldPop Global_2015_2030 / R2025A → persons/km2 NetCDF for ETH"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2030,
        help="Projection year between 2015 and 2030 (default: 2030).",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="data/worldpop_eth_R2025A_1km",
        help="Directory to cache downloaded GeoTIFF (default: data/worldpop_eth_R2025A_1km)",
    )
    parser.add_argument(
        "--out-nc",
        type=str,
        required=True,
        help="Output NetCDF path (e.g. data/pop_eth_worldpop_R2025A_2030_km2.nc)",
    )
    parser.add_argument(
        "--var-name",
        type=str,
        default="pop_density",
        help="Name of output variable (default: pop_density)",
    )
    args = parser.parse_args()

    url = build_worldpop_R2025A_url(args.year)
    cache_dir = Path(args.cache_dir)
    tif_path = cache_dir / Path(url).name

    download_file(url, tif_path)
    tif_to_density_nc(tif_path, Path(args.out_nc), var_name=args.var_name)


if __name__ == "__main__":
    main()
