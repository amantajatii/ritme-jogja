"""Fungsi untuk memuat tiap file dataset JogjaPulse dari data/raw/.

Nama kolom sudah dicek terhadap README dataset (Zenodo 10.5281/zenodo.23157460).

- Kode wilayah (mis. "34.01") dibaca sebagai string supaya tidak berubah jadi float.
- Nama kapanewon tidak unik (JETIS ada di Bantul dan Kota Yogyakarta), jadi gabungkan
  antar file pakai KAPANEWON_KEY atau kode wilayah.
- Baris dengan < 5 perangkat dihapus (k-anonymity): baris hilang berarti < 5, bukan nol.
- n_maids (perangkat unik) tidak boleh dijumlahkan antar sel, jam, hari, atau kapanewon.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
EXTERNAL_DIR = ROOT / "data" / "external"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "figures"

KAPANEWON_KEY = ["kab_kota", "kapanewon"]
MONTHS_GOOD_QUALITY = ["2021-12", "2022-01", "2022-02"]

_CODE_COLUMNS = {
    "kab_code": str,
    "kapanewon_code": str,
    "origin_kab_code": str,
    "origin_code": str,
    "dest_kab_code": str,
    "dest_code": str,
    "month": str,
}


def _read(filename: str, **kwargs) -> pd.DataFrame:
    path = RAW_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"{path} belum ada. Jalankan dulu: python scripts/download_data.py"
        )
    return pd.read_csv(path, dtype=_CODE_COLUMNS, **kwargs)


def load_presence_hourly() -> pd.DataFrame:
    """Perangkat unik & ping per kapanewon per jam (230.418 baris).

    Kolom: kab_code, kab_kota, kapanewon_code, kapanewon, date (datetime),
    hour (0-23 WIB), n_maids, n_pings.
    """
    return _read("presence_kapanewon_hourly.csv", parse_dates=["date"])


def load_presence_cell_daily() -> pd.DataFrame:
    """Perangkat unik per sel grid 500 m per hari (183.548 baris, 5.715 sel).

    Kolom: cell_id, x_min_utm, y_min_utm (EPSG:32749), centroid_lon,
    centroid_lat (WGS84), date (datetime), n_maids. Tidak ada n_pings.
    """
    return _read("presence_cell500m_daily.csv", parse_dates=["date"])


def load_od_visits() -> pd.DataFrame:
    """Arus kunjungan rumah -> tujuan antar kapanewon per bulan (9.894 baris).

    Kolom: month ("YYYY-MM"), origin_kab_code, origin_kab_kota, origin_code,
    origin_kapanewon, dest_kab_code, dest_kab_kota, dest_code, dest_kapanewon,
    n_maids (jumlah pengunjung unik, bukan jumlah perjalanan), reduced_quality.
    Baris origin == dest ikut disertakan.
    """
    return _read("od_home_visits_kapanewon_monthly.csv")


def load_od_origin_homes() -> pd.DataFrame:
    """Penyebut OD: perangkat dengan rumah di tiap kapanewon asal per bulan.

    Kolom: month, origin_kab_code, origin_kab_kota, origin_code,
    origin_kapanewon, n_homed_maids, n_homed_maids_daytime (bisa kosong),
    reduced_quality.
    """
    df = _read("od_origin_homes_monthly.csv")
    return df.assign(n_homed_maids_daytime=df["n_homed_maids_daytime"].astype("Int64"))


def load_home_vs_population() -> pd.DataFrame:
    """Perangkat per kapanewon rumah vs jumlah penduduk (78 baris).

    Kolom asli KAB_KOTA / KEC_KAPN diganti jadi kab_kota / kapanewon supaya
    seragam. Kolom lain: n_users, pop_actual, ratio. Tidak ada kode wilayah.
    """
    return _read("home_maids_vs_population_kapanewon.csv").rename(
        columns={"KAB_KOTA": "kab_kota", "KEC_KAPN": "kapanewon"}
    )


def load_validation_night() -> pd.DataFrame:
    """Keberadaan malam (00-05 WIB) per kapanewon untuk validasi (156 baris).

    Dua periode: "Dec 2021 - Apr 2022" dan "Dec 2021 - Jan 2022".
    Kolom: period, kab_kota, kapanewon, night_presence, slots_published_pct,
    n_users, pop_actual.
    """
    return _read("validation_night_presence_kapanewon.csv")


def load_tier1_summary() -> pd.DataFrame:
    """Statistik supresi dua produk presence (2 baris)."""
    return _read("tier1_summary.csv")


def load_od_summary() -> pd.DataFrame:
    """Statistik supresi produk OD (1 baris)."""
    return _read("od_summary.csv")


def load_event_calendar() -> pd.DataFrame:
    """Kalender kejadian dari data/external/kalender_kejadian.csv, siap dipakai style.mark_events."""
    return pd.read_csv(
        EXTERNAL_DIR / "kalender_kejadian.csv", parse_dates=["tanggal_mulai", "tanggal_selesai"]
    ).sort_values("tanggal_mulai", ignore_index=True)


def kapanewon_lookup() -> pd.DataFrame:
    """Tabel referensi 78 kapanewon: kab_code, kab_kota, kapanewon_code, kapanewon."""
    cols = ["kab_code", "kab_kota", "kapanewon_code", "kapanewon"]
    df = _read("presence_kapanewon_hourly.csv", usecols=cols)
    return df.drop_duplicates().sort_values("kapanewon_code").reset_index(drop=True)
