# Ritme Jogja

**Ritme Jogja: analisis dan visualisasi pola mobilitas manusia di DIY (Des 2021–Apr 2022) menggunakan dataset JogjaPulse.**

Proyek kelompok mata kuliah (UGM) bertema *human mobility*: kapan, di mana, dan dari mana orang bergerak di Daerah Istimewa Yogyakarta.

## Sumber data

> Widyawan, Pratama, A. R., Ariansyah, A., Farda, N. M., Pramana, S., & Miller, O. (2026). *JogjaPulse: An Aggregated Spatio-Temporal Mobility Dataset for Yogyakarta, Indonesia* (Versi 1.0) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.23157460

Lisensi data: CC BY 4.0. Data tidak disimpan di repo ini.

## Unduh data

```bash
python scripts/download_data.py
```

Semua file diunduh dari Zenodo ke `data/raw/` dan dicek checksum MD5-nya. Kalau gagal, buka https://zenodo.org/records/23157460, unduh semua file, lalu taruh di `data/raw/`.

## Struktur repo

```
data/raw/          # CSV dari Zenodo (tidak di-commit)
data/external/     # batas wilayah, kalender kejadian
data/processed/    # hasil olahan antara (tidak di-commit)
notebooks/         # notebook analisis tiap anggota
src/ritme/         # modul Python bersama
figures/           # gambar hasil untuk slide
scripts/           # skrip utilitas (unduh data)
```

_README lengkap (setup, pembagian tugas, aturan kolaborasi) menyusul._
