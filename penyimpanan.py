import csv
import os


class Penyimpanan:
    """Membaca dan menulis berkas fisik (CSV untuk data, TXT untuk log)."""

    def __init__(self, folder: str = "data"):
        self._folder = folder
        os.makedirs(self._folder, exist_ok=True)

    def _path(self, nama_file: str) -> str:
        return os.path.join(self._folder, nama_file)

    # ---------- CSV ----------
    def simpan_csv(self, nama_file: str, header: list[str], daftar_dict: list[dict]) -> None:
        """Menulis ulang seluruh isi CSV. Ditulis ke file sementara dahulu agar
        file asli tidak rusak jika program terhenti di tengah penulisan."""
        path = self._path(nama_file)
        sementara = path + ".tmp"
        with open(sementara, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(daftar_dict)
        os.replace(sementara, path)

    def muat_csv(self, nama_file: str) -> list[dict]:
        """Membaca CSV menjadi list of dict. File belum ada -> list kosong."""
        try:
            with open(self._path(nama_file), "r", newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            return []
        except (csv.Error, UnicodeDecodeError) as e:
            print(f"Peringatan: {nama_file} tidak dapat dibaca ({e}). Memakai data kosong.")
            return []

    # ---------- TXT ----------
    def tambah_baris(self, nama_file: str, teks: str) -> None:
        """Menambahkan satu baris di akhir file (mode append)."""
        with open(self._path(nama_file), "a", encoding="utf-8") as f:
            f.write(teks + "\n")

    def baca_baris(self, nama_file: str) -> list[str]:
        try:
            with open(self._path(nama_file), "r", encoding="utf-8") as f:
                return [baris.rstrip("\n") for baris in f]
        except FileNotFoundError:
            return []
