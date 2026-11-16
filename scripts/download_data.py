"""Unduh semua file dataset JogjaPulse dari Zenodo ke data/raw/.

Pemakaian:
    python scripts/download_data.py            # unduh yang belum ada
    python scripts/download_data.py --force    # unduh ulang semuanya

Hanya memakai pustaka standar Python. Tiap file dicek checksum MD5-nya.
Kalau gagal (tidak ada internet, Zenodo down, dsb.), skrip menampilkan
instruksi unduh manual.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

RECORD_ID = "23157460"
API_URL = f"https://zenodo.org/api/records/{RECORD_ID}"
RECORD_URL = f"https://zenodo.org/records/{RECORD_ID}"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
TIMEOUT_SECONDS = 120
CHUNK_BYTES = 1 << 20
USER_AGENT = "ritme-jogja-downloader/1.0"

MANUAL_INSTRUCTIONS = f"""
------------------------------------------------------------------
Unduhan otomatis gagal. Unduh manual:
  1. Buka {RECORD_URL}
  2. Klik "Download all" (atau unduh tiap file satu per satu).
  3. Ekstrak / taruh semua file .csv dan README.md ke folder:
       {RAW_DIR}
  4. Pastikan nama file tidak berubah (mis. presence_kapanewon_hourly.csv).
------------------------------------------------------------------
"""


def _open(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS)


def fetch_file_list() -> list[dict]:
    with _open(API_URL) as response:
        record = json.load(response)
    return [
        {
            "name": f["key"],
            "size": f["size"],
            "url": f["links"]["self"],
            "md5": f.get("checksum", "").removeprefix("md5:"),
        }
        for f in record.get("files", [])
    ]


def md5_of(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_BYTES), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_valid(path: Path, expected_md5: str) -> bool:
    return path.exists() and (not expected_md5 or md5_of(path) == expected_md5)


def download(file_info: dict, force: bool) -> None:
    target = RAW_DIR / file_info["name"]
    if not force and is_valid(target, file_info["md5"]):
        print(f"  [lewati] {target.name} sudah ada dan checksum cocok")
        return

    size_mb = file_info["size"] / 1e6
    print(f"  [unduh ] {target.name} ({size_mb:.1f} MB)")
    partial = target.with_suffix(target.suffix + ".part")
    with _open(file_info["url"]) as response, partial.open("wb") as out:
        for chunk in iter(lambda: response.read(CHUNK_BYTES), b""):
            out.write(chunk)

    if not is_valid(partial, file_info["md5"]):
        partial.unlink(missing_ok=True)
        raise ValueError(f"checksum {target.name} tidak cocok")
    partial.replace(target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="unduh ulang semua file")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Mengambil daftar file dari {API_URL}")
    try:
        files = fetch_file_list()
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Gagal mengambil daftar file: {exc}", file=sys.stderr)
        print(MANUAL_INSTRUCTIONS, file=sys.stderr)
        return 1

    failures = []
    for file_info in files:
        try:
            download(file_info, args.force)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            print(f"  [gagal ] {file_info['name']}: {exc}", file=sys.stderr)
            failures.append(file_info["name"])

    if failures:
        print(f"\n{len(failures)} file gagal: {', '.join(failures)}", file=sys.stderr)
        print(MANUAL_INSTRUCTIONS, file=sys.stderr)
        return 1

    print(f"\nSelesai. {len(files)} file ada di {RAW_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
