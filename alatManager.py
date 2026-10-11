
from alat import Alat
from enumKondisi import KondisiAlat
from Kategori import Kategori
from logAktivitas import LogAktivitas


class AlatManager:
    def __init__(self, logger: LogAktivitas = None):
        self._data_alat = {}
        self._data_kategori = {}
        self._logger = logger

    def tambah_alat(
        self,
        kode_alat: str,
        nama_alat: str,
        kategori: Kategori,
        kondisi: KondisiAlat = KondisiAlat.BAIK
    ):
        if kode_alat in self._data_alat:
            return False

        if not kode_alat.strip() or not nama_alat.strip():
            return False

        if not isinstance(kategori, Kategori):
            return False

        if not isinstance(kondisi, KondisiAlat):
            return False

        alat = Alat(kode_alat, nama_alat, kategori, kondisi)
        self._data_alat[kode_alat] = alat

        if self._logger is not None:
            self._logger.catat(
                f"Alat {nama_alat} ({kode_alat}) ditambahkan"
            )

        return True
    
    def tambah_kategori(self, id_kategori: str, nama_kategori: str) -> bool:
        if id_kategori in self._data_kategori:
            return False
        
        kategori_baru = Kategori(id_kategori, nama_kategori)
        self._data_kategori[id_kategori] = kategori_baru
        
        if self._logger:
            self._logger.catat(f"Kategori {nama_kategori} '{id_kategori}' berhasil ditambahkan.")
        return True

    def edit_alat(self, kode_alat, nama_baru, kategori_baru):
        alat = self._data_alat.get(kode_alat)

        if alat is None:
            return False

        if not nama_baru.strip():
            return False

        if not isinstance(kategori_baru, Kategori):
            return False

        alat.ubah_data(nama_baru, kategori_baru)

        if self._logger is not None:
            self._logger.catat(f"Alat {kode_alat} diubah")

        return True

    def hapus_alat(
        self,
        kode_alat,
        masih_dalam_transaksi_aktif=False
    ):
        alat = self._data_alat.get(kode_alat)

        if alat is None:
            return False

        if masih_dalam_transaksi_aktif:
            return False

        if not alat.tersedia and not alat.is_rusak():
            return False

        del self._data_alat[kode_alat]

        if self._logger is not None:
            self._logger.catat(f"Alat {kode_alat} dihapus")

        return True

    def cari_alat(self, kode_alat):
        return self._data_alat.get(kode_alat)

    def get_alat_by_kode(self, kode_alat):
        return self.cari_alat(kode_alat)
    
    def get_kategori(self, id_kategori: str):
        return self._data_kategori.get(id_kategori, None)

    def cari_alat_fleksibel(self, keyword):
        keyword = keyword.strip().lower()
        hasil = []

        if not keyword:
            return hasil

        for alat in self._data_alat.values():
            if (
                keyword in alat.kode_alat.lower()
                or keyword in alat.nama_alat.lower()
                or keyword in alat.kategori.nama_kategori.lower()
            ):
                hasil.append(alat)

        return hasil

    def tampilkan_kategori_alat(self):
        return list(Kategori)

    def cari_alat_berdasarkan_kategori(self, kategori):
        hasil = []

        for alat in self._data_alat.values():
            if alat.kategori == kategori:
                hasil.append(alat)

        return hasil

    def tampilkan_alat_tersedia(self):
        hasil = []

        for alat in self._data_alat.values():
            if alat.is_tersedia():
                hasil.append(alat)

        return hasil

    def tampilkan_alat_dipinjam(self):
        hasil = []

        for alat in self._data_alat.values():
            if not alat.tersedia and not alat.is_rusak():
                hasil.append(alat)

        return hasil

    def tampilkan_alat_rusak(self):
        hasil = []

        for alat in self._data_alat.values():
            if alat.is_rusak():
                hasil.append(alat)

        return hasil

    def ubah_kondisi_alat(self, kode_alat, kondisi_baru):
        alat = self._data_alat.get(kode_alat)

        if alat is None:
            return False

        if not isinstance(kondisi_baru, KondisiAlat):
            return False

        alat.kondisi = kondisi_baru

        if self._logger is not None:
            self._logger.catat(
                f"Kondisi alat {kode_alat} diubah menjadi "
                f"{kondisi_baru.value}"
            )

        return True
