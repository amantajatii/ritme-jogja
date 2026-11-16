# Panduan bagian E

Bagian E memeriksa hubungan perangkat dengan penduduk, validasi malam, dan keterbatasan data. Notebook utamanya adalah `E_validasi_bias.ipynb`. Tidak perlu menjalankan notebook A–D.

## Membuka hasil di komputer ini

Dari PowerShell pada folder proyek:

```powershell
.\.venv\py313\Scripts\python -m jupyterlab notebooks/E_validasi_bias.ipynb
```

Lingkungan untuk bagian E memakai Python 3.13 di `.venv/py313/`, karena komponen numerik Python 3.14 diblokir kebijakan aplikasi Windows pada komputer ini.

Pilih kernel **Python (ritme-jogja)**. Untuk mengulang analisis, pilih **Restart Kernel and Run All Cells**. Semua grafik juga tersimpan sebagai `figures/E_01_...png` sampai `E_05_...png`. Tabel dan ringkasan narasi ada di `data/processed/E_*` setelah notebook dijalankan.

## Setup ulang di komputer lain

```powershell
py -3.13 -m venv .venv/py313
.\.venv\py313\Scripts\python -m pip install -r requirements.txt -c notebooks/E_constraints.txt
.\.venv\py313\Scripts\python -m pip install -e .
.\.venv\py313\Scripts\python scripts/download_data.py
.\.venv\py313\Scripts\python -m ipykernel install --prefix .venv/py313 --name ritme-jogja --display-name "Python (ritme-jogja)"
.\.venv\py313\Scripts\python -m jupyterlab notebooks/E_validasi_bias.ipynb
```

Versi laporan tanpa kode juga tersedia di `data/processed/E_laporan.html` pada komputer ini. Buka file tersebut dengan browser. File HTML ini hasil ekspor, bukan keluaran otomatis saat menjalankan notebook.

## Cara membaca grafik

1. **E_01_perangkat_vs_penduduk:** hubungan antarwilayah, dengan skala log agar wilayah kecil terlihat. Korelasi bukan bukti keterwakilan seluruh penduduk.
2. **E_02_rasio_perangkat:** delapan rasio terendah dan tertinggi. Perangkat per 100 penduduk bukan persentase penduduk yang teramati.
3. **E_03_validasi_malam:** hubungan malam dengan penduduk serta konsistensi dua periode. Periode bertumpang tindih; bukan dua sampel independen.
4. **E_04_cakupan_slot_malam:** 15 wilayah dengan cakupan Des–Apr terendah. Rerata malam hanya menggunakan slot yang terbit.
5. **E_05_supresi:** persentase baris hilang dibanding bobot hitungan yang hilang. Bobot bukan orang unik; definisi presence dan OD berbeda.

## Sebelum dikumpulkan

- Baca temuan dan batas interpretasi pada bagian akhir notebook; narasi pendek tersedia di sana.
- Konfirmasi sumber dan tahun penduduk BPS: README dataset masih memuat placeholder.
- Diskusikan implikasi hasil E dengan anggota A–D; sesuaikan slide dengan hasil akhir mereka.
- Kerjakan editing video setelah materi semua anggota tersedia.
- Jalankan ulang notebook sebelum commit. Jangan ikutkan `.venv`, data mentah, atau hasil olahan yang diabaikan Git.
- Kontribusi dikerjakan pada branch `anggota-e/validasi-bias`; PR E ditinjau anggota A.
