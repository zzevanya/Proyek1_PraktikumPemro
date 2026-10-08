from enumKondisi import KondisiAlat
from Kategori import KategoriAlat


class Alat:
    def __init__(
        self,
        kode_alat: str,
        nama_alat: str,
        kategori: KategoriAlat,
        kondisi: KondisiAlat = KondisiAlat.BAIK,
        tersedia: bool = True
    ):
        self._kode_alat: str = kode_alat
        self._nama_alat: str = nama_alat
        self._kategori: KategoriAlat = kategori
        self._kondisi: KondisiAlat = kondisi
        self._tersedia: bool = tersedia

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
        return self._tersedia

    @tersedia.setter
    def tersedia(self, value: bool):
        self._tersedia = value

    def is_tersedia(self) -> bool:
        """+ is_tersedia(): bool: Mengecek apakah alat siap dipinjam."""
        return self._tersedia and not self.is_rusak()

    def tandai_dipinjam(self) -> None:
        """+ tandai_dipinjam(): Mengubah ketersediaan alat menjadi sedang dipinjam (False)."""
        self._tersedia = False

    def terima_kembali(self, kondisi: KondisiAlat) -> None:
        """+ terima_kembali(kondisi): Menerima alat kembali dan memperbarui kondisi fisiknya."""
        self._kondisi = kondisi
        self._tersedia = (kondisi != KondisiAlat.RUSAK_BERAT)

    def is_rusak(self) -> bool:
        """+ is_rusak(): bool: Mengecek apakah alat dalam kondisi rusak ringan atau berat."""
        return self._kondisi in (KondisiAlat.RUSAK_RINGAN, KondisiAlat.RUSAK_BERAT)

    def ubah_data(self, nama: str, kat: KategoriAlat) -> None:
        """+ ubah_data(nama, kat): Mengubah nama dan kategori alat."""
        self._nama_alat = nama
        self._kategori = kat

    def __str__(self) -> str:
        status_pinjam = "Tersedia" if self._tersedia else "Dipinjam"
        kat_val = self._kategori.value if isinstance(self._kategori, KategoriAlat) else str(self._kategori)
        kon_val = self._kondisi.value if isinstance(self._kondisi, KondisiAlat) else str(self._kondisi)
        return f"[{self._kode_alat}] {self._nama_alat} | Kategori: {kat_val} | Kondisi: {kon_val} | Status: {status_pinjam}"