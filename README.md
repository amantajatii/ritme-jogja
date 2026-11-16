# Ritme Jogja

Analisis dan visualisasi pola mobilitas manusia di DIY (Desember 2021 sampai April 2022) menggunakan dataset JogjaPulse.

Proyek kelompok mata kuliah (UGM) bertema *human mobility*. Kami ingin tahu kapan, di mana, dan dari mana orang bergerak di Daerah Istimewa Yogyakarta. Tiap anggota membahas satu sisi: ritme harian, tipe kawasan, dampak kejadian, arus asal-tujuan, dan keandalan datanya.

## Sumber data

Dataset JogjaPulse berisi jumlah perangkat seluler yang teramati di DIY dari 1 Desember 2021 sampai 30 April 2022 (151 hari). Datanya sudah diagregasi, dan baris dengan kurang dari 5 perangkat dihapus (k-anonymity, k = 5). Lisensi CC BY 4.0.

> Widyawan, Pratama, A. R., Ariansyah, A., Farda, N. M., Pramana, S., & Miller, O. (2026). *JogjaPulse: An Aggregated Spatio-Temporal Mobility Dataset for Yogyakarta, Indonesia* (Versi 1.0) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.23157460

| File | Isi | Baris | Dipakai oleh |
|---|---|---|---|
| `presence_kapanewon_hourly.csv` | Perangkat unik (`n_maids`) dan ping (`n_pings`) per kapanewon per jam | 230.418 | A, B |
| `presence_cell500m_daily.csv` | Perangkat unik per sel grid 500 m per hari (5.715 sel) | 183.548 | C |
| `od_home_visits_kapanewon_monthly.csv` | Pengunjung unik dari kapanewon rumah ke kapanewon tujuan, per bulan | 9.894 | D |
| `od_origin_homes_monthly.csv` | Perangkat yang tinggal di tiap kapanewon asal, per bulan (penyebut OD) | 390 | D |
| `home_maids_vs_population_kapanewon.csv` | Perangkat per kapanewon rumah dibanding jumlah penduduk | 78 | E |
| `validation_night_presence_kapanewon.csv` | Kehadiran malam (00.00-05.59 WIB) untuk validasi, 2 periode | 156 | E |
| `tier1_summary.csv`, `od_summary.csv` | Statistik supresi | 2 dan 1 | E |

Penjelasan tiap kolom ada di `data/raw/README.md`, yang ikut terunduh.

### Keterbatasan data yang perlu diketahui semua anggota

1. Jumlah perangkat yang teramati tidak tetap. Angkanya turun dari sekitar 87 ribu per hari (Desember 2021) ke sekitar 9 ribu per hari (April 2022), dengan lompatan turun pada 1 Januari dan 16 Februari 2022. Penurunan ini datang dari perubahan sampel, bukan perubahan perilaku. Untuk membandingkan antar waktu, pakai pangsa (`ritme.prep.add_share`) atau normalisasi lain.
2. Baris yang hilang berarti kurang dari 5 perangkat, bukan nol. Supresi lebih sering terjadi di Maret-April 2022 dan di wilayah pedesaan seperti Gunungkidul dan Kulon Progo.
3. `n_maids` tidak boleh dijumlahkan antar jam, hari, sel, atau kapanewon untuk mendapat total orang.
4. Data OD Maret-April 2022 ditandai `reduced_quality = True`. Analisis kuantitatif OD sebaiknya memakai Desember 2021 sampai Februari 2022. `n_maids` di OD menghitung pengunjung, tidak menghitung perjalanan.
5. Satu perangkat tidak sama dengan satu orang. Gondomanan, misalnya, punya lebih banyak perangkat daripada penduduk.
6. Nama kapanewon tidak unik: `JETIS` ada di Bantul dan di Kota Yogyakarta. Gabungkan data memakai pasangan (`kab_kota`, `kapanewon`) atau kode wilayah.
7. Dataset tidak menyertakan polygon batas kapanewon, jadi file batasnya perlu disiapkan sendiri di `data/external/`.

### Periode analisis per bagian

Dataset mencakup 1 Desember 2021 sampai 30 April 2022, tapi tidak semua bagian memakai seluruh periode. Mulai Maret 2022 jumlah perangkat anjlok dan jam yang tersupresi melonjak (di Gunungkidul naik dari 22% ke 40% jam), sehingga profil per jam jadi kurang andal.

| Bagian | Periode | Alasan |
|---|---|---|
| A | Desember-Februari untuk hari kerja, Sabtu, dan Minggu. Seluruh periode khusus untuk perbandingan hari libur. | Sebagian besar hari libur yang jatuh di hari kerja ada di Maret-April (Nyepi, Wafat Isa Almasih, cuti bersama 29 April). |
| B | Desember-Februari, dengan normalisasi yang sama dengan A | Klaster B dibandingkan langsung dengan profil A di video. Kalau periodenya beda, sekitar 17% kapanewon berpindah kelompok jam puncak. B bisa memakai `data/processed/A_ritme_kapanewon.csv`, yang dibuat dengan menjalankan notebook A. |
| C | Seluruh periode, dengan normalisasi harian | Ramadan ada di April dan kenaikan kasus Omicron di Februari. |
| D | Desember-Februari untuk analisis kuantitatif | Data OD Maret-April ditandai `reduced_quality = True`. |
| E | Mengikuti periode file validasi (Desember-April dan Desember-Januari) | Periodenya sudah ditetapkan pembuat dataset. Pilihan periode A-D dibahas di bagian keterbatasan. |

Semua bagian menandai tanggal anomali data dengan cara yang sama: 1 Januari 2022 dan 16 Februari 2022 (lompatan turun jumlah perangkat), serta 8 Maret 2022 (anomali satu hari).

### Jam dengan data bolong

Di luar tanggal anomali di atas, ada beberapa jam pagi yang datanya hampir kosong di seluruh DIY sekaligus, tanda gangguan pengiriman data. Kriterianya: jam 07.00-21.59 yang total ping seluruh DIY-nya di bawah 40% median jam yang sama dalam ±7 hari. Kami menetapkan ambang ini sebelum melihat hasil analisis dan tidak mengubahnya sesudahnya.

| Tanggal | Jam | Ping dibanding biasanya |
|---|---|---|
| 22 Januari 2022 (Sabtu) | 10.00 | 35% |
| 27 Januari 2022 (Kamis) | 09.00 | 34% |
| 4 Februari 2022 (Jumat) | 08.00 | 8% |
| 5 Februari 2022 (Sabtu) | 10.00 | 16% |

Kami hanya mengosongkan jam itu; jam lain di hari yang sama tetap dipakai. Notebook A menampilkan hasil dengan dan tanpa penutupan ini di bagian uji sensitivitas. Data harian (C) dan bulanan (D) tidak terkena langsung, tapi bagian yang memakai data per jam (A dan B) sebaiknya memakai daftar yang sama.

## Setup

Butuh Python 3.10 atau lebih baru.

```bash
git clone https://github.com/amantajatii/ritme-jogja.git
cd ritme-jogja
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .                   # supaya `import ritme` jalan dari folder mana pun
```

### Unduh data

```bash
python scripts/download_data.py
```

Skrip ini mengunduh semua file dari Zenodo ke `data/raw/` dan mengecek checksum MD5 tiap file. File yang sudah ada dilewati; tambahkan `--force` untuk mengunduh ulang. Kalau unduhan gagal, skrip menampilkan langkah unduh manual: buka https://zenodo.org/records/23157460, unduh semua file, lalu taruh di `data/raw/`.

`data/raw/` dan `data/processed/` ada di `.gitignore`, jadi isinya tidak ikut ter-commit.

### Jalankan notebook

```bash
jupyter lab notebooks/
```

## Struktur repo

```
ritme-jogja/
├── data/
│   ├── raw/                    # CSV dari Zenodo (tidak di-commit)
│   ├── external/               # batas wilayah, kalender kejadian
│   └── processed/              # hasil olahan antara (tidak di-commit)
├── notebooks/
│   └── A_ritme_harian.ipynb    # notebook B-E menyusul dari tiap anggota
├── src/ritme/
│   ├── io.py                   # fungsi load tiap file dan path proyek
│   ├── prep.py                 # normalisasi pangsa dan kolom kalender
│   └── style.py                # gaya grafik seragam, simpan ke figures/
├── figures/                    # gambar hasil (PNG) untuk slide
├── scripts/download_data.py
├── requirements.txt
└── pyproject.toml
```

Contoh pemakaian di notebook:

```python
from ritme import io, prep, style

style.apply()
hourly = io.load_presence_hourly().pipe(prep.add_calendar_columns)
hourly = prep.add_share(hourly, by=["date", "hour"])
...
style.save(fig, "A_profil_harian")   # tersimpan di figures/A_profil_harian.png
```

## Pembagian tugas

| Anggota | Nama | Analisis | Data | Tugas bersama |
|---|---|---|---|---|
| A | | Ritme harian: jam sibuk tiap kapanewon, perbandingan hari kerja, akhir pekan, dan hari libur | `presence_kapanewon_hourly` | Setup repo dan README |
| B | | Klasterisasi kapanewon (k-means) dari profil per jam: pusat kegiatan, perumahan, wisata | `presence_kapanewon_hourly` | Peta dasar batas kapanewon (`data/external/batas_kapanewon.geojson`, `src/ritme/maps.py`) |
| C | | Dampak kejadian (Nataru, Omicron, Ramadan 2022) pada titik ramai grid 500 m | `presence_cell500m_daily` | Kalender kejadian (`data/external/kalender_kejadian.csv`) |
| D | | Arus asal-tujuan dan daya tarik kapanewon | `od_home_visits_...`, `od_origin_homes_...` | Template gaya grafik (`src/ritme/style.py`) dan slide |
| E | | Validasi terhadap jumlah penduduk, bias, dan keterbatasan | `home_maids_...`, `validation_night_...` | Editing video |

## Aturan kolaborasi

1. Commit dari akun GitHub sendiri. Atur `git config user.name` dan `user.email` sesuai akun masing-masing, karena kontribusi dinilai dari riwayat commit.
2. Satu branch per anggota, lalu buka PR ke `main`. Jangan push langsung ke `main`.
   ```bash
   git checkout main && git pull
   git checkout -b anggota-a/ritme-harian
   # kerjakan, lalu commit
   git push -u origin anggota-a/ritme-harian
   ```
3. Review bergiliran A → B → C → D → E → A. PR milik A di-review B, PR milik B di-review C, dan seterusnya sampai PR milik E di-review A. PR baru di-merge setelah reviewer menyetujuinya.
4. Edit notebook milik sendiri saja. Semua anggota memakai `src/ritme/`, jadi perubahan di sana dibuat sebagai PR kecil terpisah dan diberitahukan ke grup.
5. Sebelum commit notebook, jalankan *Restart & Run All* supaya output berurutan dan tidak ada error.
6. Format pesan commit: `<tipe>: <deskripsi>`, misalnya `feat: profil 24 jam per kapanewon`, `fix: join pakai kab_kota`, atau `docs: temuan notebook C`.
7. Jangan commit data mentah, kredensial, atau file di atas 10 MB.

## Jadwal

- Video presentasi 5 menit dikumpulkan sebelum minggu ke-13.
- Presentasi di minggu ke-13 dan ke-14.
