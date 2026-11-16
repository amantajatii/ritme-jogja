"""Gaya grafik seragam untuk semua notebook dan slide.

Pakai di awal notebook:
    from ritme import style
    style.apply()
    ...
    style.save(fig, "A_profil_harian")   # -> figures/A_profil_harian.png

Palet kategorikal sudah divalidasi aman untuk buta warna dalam urutan ini, jadi jangan diacak.
Lima warna pertama juga punya kontras minimal 3:1 terhadap SURFACE.
Warna mengikuti entitas (mis. kabupaten), bukan peringkat.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from ritme.io import FIGURES_DIR

# Urutan tetap. Untuk scatter/peta kategorikal, maksimal 3 warna pertama.
CATEGORICAL = [
    "#2a78d6",  # biru
    "#eb6834",  # oranye
    "#199e70",  # aqua
    "#b37600",  # kuning
    "#d55181",  # magenta
    "#008300",  # hijau
    "#6250d6",  # ungu
    "#e34948",  # merah
]

KAB_ORDER = ["YOGYAKARTA", "SLEMAN", "BANTUL", "KULON PROGO", "GUNUNGKIDUL"]
KAB_COLORS = dict(zip(KAB_ORDER, CATEGORICAL))
KAB_LABELS = {
    "YOGYAKARTA": "Kota Yogyakarta",
    "SLEMAN": "Sleman",
    "BANTUL": "Bantul",
    "KULON PROGO": "Kulon Progo",
    "GUNUNGKIDUL": "Gunungkidul",
}

# Sekuensial (besaran, mis. peta choropleth/heatmap): satu warna, terang -> gelap.
SEQUENTIAL_BLUE = LinearSegmentedColormap.from_list(
    "ritme_blue",
    ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"],
)
# Divergen (naik/turun relatif baseline): biru <-> abu netral <-> merah.
DIVERGING = LinearSegmentedColormap.from_list(
    "ritme_div", ["#184f95", "#6da7ec", "#f0efec", "#ec8a87", "#b8302f"]
)

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
EVENT_LINE = "#8a8984"

SOURCE_NOTE = "Sumber: JogjaPulse (Widyawan dkk., 2026), Zenodo 10.5281/zenodo.23157460"


def apply() -> None:
    """Terapkan gaya matplotlib bersama."""
    mpl.rcParams.update(
        {
            "figure.figsize": (10, 5.5),
            "figure.dpi": 110,
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.labelsize": 11,
            "axes.labelcolor": TEXT_SECONDARY,
            "axes.edgecolor": GRID,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "xtick.color": TEXT_SECONDARY,
            "ytick.color": TEXT_SECONDARY,
            "text.color": TEXT_PRIMARY,
            "lines.linewidth": 2,
            "legend.frameon": False,
            "axes.prop_cycle": mpl.cycler(color=CATEGORICAL),
        }
    )


def add_source(fig: plt.Figure, note: str = SOURCE_NOTE) -> None:
    """Tulis catatan sumber data kecil di pojok kiri bawah figure."""
    fig.text(0.01, -0.01, note, fontsize=8, color=TEXT_SECONDARY, ha="left", va="top")


def mark_events(
    ax: plt.Axes, events, label: bool = True, color: str = EVENT_LINE
) -> None:
    """Garis vertikal per kejadian; `events` butuh kolom tanggal_mulai dan nama."""
    for row in events.itertuples():
        ax.axvline(row.tanggal_mulai, color=color, linestyle="--", linewidth=1)
        if label:
            ax.annotate(
                row.nama,
                xy=(row.tanggal_mulai, 1),
                xycoords=("data", "axes fraction"),
                rotation=90,
                fontsize=8,
                color=TEXT_SECONDARY,
                ha="right",
                va="top",
            )


def save(fig: plt.Figure, name: str, dpi: int = 200) -> Path:
    """Simpan figure ke figures/<name>.png dan kembalikan path-nya."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path
