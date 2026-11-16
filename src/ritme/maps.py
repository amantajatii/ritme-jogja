"""Batas kapanewon DIY dan penggabungan data berdasarkan kode BPS."""

from __future__ import annotations

import geopandas as gpd
import pandas as pd

from ritme.io import EXTERNAL_DIR

BOUNDARY_PATH = EXTERNAL_DIR / "batas_kapanewon.geojson"
BOUNDARY_SOURCE = (
    "https://geoportal.jogjaprov.go.id/server/rest/services/ADMIN_BATASWILAYAH/"
    "DIY_34_ADMINISTRASIKEC_AR/FeatureServer/0"
)
KAPANEWON_CODE = "kapanewon_code"


def load_kapanewon_boundaries() -> gpd.GeoDataFrame:
    """Baca batas DIY (EPSG:4326); `kapanewon_code` berasal dari `kdcbps`."""
    if not BOUNDARY_PATH.is_file():
        raise FileNotFoundError(f"{BOUNDARY_PATH} belum ada. Sumber: {BOUNDARY_SOURCE}")

    batas = gpd.read_file(BOUNDARY_PATH)
    kode = batas["kdcbps"].astype("string").str.strip()
    if not kode.str.fullmatch(r"\d{2}\.\d{2}\.\d{2}", na=False).all() or not kode.is_unique:
        raise ValueError("GeoJSON harus berisi satu poligon atau multipoligon per kode BPS yang valid.")
    if not batas.geom_type.isin(["Polygon", "MultiPolygon"]).all() or batas.geometry.is_empty.any():
        raise ValueError("GeoJSON berisi geometri kapanewon yang kosong atau bukan poligon.")
    return batas.assign(**{KAPANEWON_CODE: kode}).to_crs(epsg=4326).sort_values(KAPANEWON_CODE)


def join_kapanewon_boundaries(
    data: pd.DataFrame,
    *,
    code_col: str = KAPANEWON_CODE,
    boundaries: gpd.GeoDataFrame | None = None,
) -> gpd.GeoDataFrame:
    """Gabungkan satu baris data per kode; pertahankan poligon yang belum punya data.

    Pakai ``code_col="origin_code"`` atau ``"dest_code"`` untuk data OD yang
    sudah disaring atau diringkas menjadi satu baris per kapanewon.
    """
    batas = load_kapanewon_boundaries() if boundaries is None else boundaries
    tabel = data.assign(**{code_col: data[code_col].astype("string").str.strip()})
    kode = tabel[code_col]
    if kode.isna().any() or kode.eq("").any() or not kode.is_unique:
        raise ValueError(f"{code_col} harus berisi kode yang terisi dan unik.")
    asing = sorted(set(kode) - set(batas[KAPANEWON_CODE]))
    if asing:
        raise ValueError(f"Kode data tanpa batas wilayah: {', '.join(asing)}")

    return batas.merge(
        tabel, left_on=KAPANEWON_CODE, right_on=code_col, how="left", validate="one_to_one"
    )
