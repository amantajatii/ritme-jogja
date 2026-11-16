"""Praproses bersama: normalisasi dan kolom kalender.

Jumlah perangkat turun dari ~87 ribu/hari (Des 2021) ke ~9 ribu/hari (Apr 2022)
karena sampel data berubah, jadi bandingkan antar waktu memakai pangsa, bukan angka mentah.
"""

from __future__ import annotations

import pandas as pd

WEEKDAY_NAMES_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


def add_calendar_columns(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Tambah kolom weekday (0=Senin), weekday_name, is_weekend, month."""
    dates = pd.to_datetime(df[date_col])
    return df.assign(
        weekday=dates.dt.day_of_week,
        weekday_name=dates.dt.day_of_week.map(dict(enumerate(WEEKDAY_NAMES_ID))),
        is_weekend=dates.dt.day_of_week >= 5,
        month=dates.dt.strftime("%Y-%m"),
    )


def add_share(
    df: pd.DataFrame,
    by: list[str],
    value_col: str = "n_maids",
    share_col: str = "share",
) -> pd.DataFrame:
    """Tambah kolom pangsa: value / jumlah value dalam grup `by`.

    Contoh: add_share(hourly, by=["date", "hour"]) memberi pangsa tiap kapanewon
    pada jam yang sama. Jumlah n_maids hanya dipakai sebagai penyebut, bukan jumlah orang.
    """
    totals = df.groupby(by)[value_col].transform("sum")
    return df.assign(**{share_col: df[value_col] / totals})
