from enumKondisi import KondisiAlat
from Kategori import KategoriAlat


class Alat:
    def __init__(
        self,
        kode_alat: str,
        nama_alat: str,
        kategori: KategoriAlat,
        kondisi: KondisiAlat = KondisiAlat.BAIK
    ):
        self._kode_alat: str = kode_alat
        self._nama_alat: str = nama_alat
        self._kategori: KategoriAlat = kategori
        self._kondisi: KondisiAlat = kondisi
        self._sedang_dipinjam: bool = False

    @property
    def kode_alat(self) -> str:
        return self._kode_alat

    @property
    def nama_alat(self) -> str:
        return self._nama_alat

    @nama_alat.setter
    def nama_alat(self, value: str):
        self._nama_alat = value

    @property
    def kategori(self) -> KategoriAlat:
        return self._kategori

    @kategori.setter
    def kategori(self, value: KategoriAlat):
        self._kategori = value

    @property
    def kondisi(self) -> KondisiAlat:
        return self._kondisi

    @kondisi.setter
    def kondisi(self, value: KondisiAlat):
        self._kondisi = value

    @property
    def tersedia(self) -> bool:
        """Dihitung dinamis: Tersedia hanya jika tidak sedang dipinjam dan tidak rusak."""
        return (not self._sedang_dipinjam) and (not self.is_rusak())

    def is_tersedia(self) -> bool:
        """+ is_tersedia(): bool: Mengembalikan hasil evaluasi ketersediaan dinamis."""
        return self.tersedia

    def tandai_dipinjam(self) -> None:
        """+ tandai_dipinjam(): Menandai alat sedang dipinjam."""
        self._sedang_dipinjam = True

    def terima_kembali(self, kondisi: KondisiAlat) -> None:
        """+ terima_kembali(kondisi): Mengembalikan status pinjam dan memperbarui kondisi fisik."""
        self._sedang_dipinjam = False
        self._kondisi = kondisi

    def is_rusak(self) -> bool:
        """+ is_rusak(): bool: Mengecek apakah kondisi alat rusak (ringan atau berat)."""
        return self._kondisi in (KondisiAlat.RUSAK_RINGAN, KondisiAlat.RUSAK_BERAT)

    def ubah_data(self, nama: str, kat: KategoriAlat) -> None:
        """+ ubah_data(nama, kat): Memperbarui nama dan kategori alat."""
        self._nama_alat = nama
        self._kategori = kat

    def __str__(self) -> str:
        if self._sedang_dipinjam:
            status_teks = "Dipinjam"
        elif self.is_rusak():
            status_teks = "Tidak Tersedia (Rusak)"
        else:
            status_teks = "Tersedia"

        kat_val = self._kategori.value if isinstance(self._kategori, KategoriAlat) else str(self._kategori)
        kon_val = self._kondisi.value if isinstance(self._kondisi, KondisiAlat) else str(self._kondisi)
        return f"[{self._kode_alat}] {self._nama_alat} | Kategori: {kat_val} | Kondisi: {kon_val} | Status: {status_teks}"