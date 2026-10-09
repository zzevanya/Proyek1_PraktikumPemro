
from alat import Alat
from enumKondisi import KondisiAlat
from Kategori import KategoriAlat
from logAktivitas import LogAktivitas


class AlatManager:
    def __init__(self, logger: LogAktivitas = None):
        self._data_alat = {}
        self._logger = logger

    def tambah_alat(
    self,
    kode_alat: str,
    nama_alat: str,
    kategori: KategoriAlat,
    kondisi: KondisiAlat = KondisiAlat.BAIK ):
        
        if kode_alat in self._data_alat:
            return False

        if not kode_alat.strip() or not nama_alat.strip():
            return False

        tersedia = kondisi == KondisiAlat.BAIK

        alat = Alat(
            kode_alat,
            nama_alat,
            kategori,
            kondisi,
            tersedia
        )

        self._data_alat[kode_alat] = alat

        if self._logger is not None:
            self._logger.catat(
                f"Alat {nama_alat} ({kode_alat}) ditambahkan"
            )

        return True

    def edit_alat(self, kode_alat, nama_baru, kategori_baru):
        alat = self._data_alat.get(kode_alat)

        if alat is None:
            return False

        if not nama_baru.strip():
            return False

        alat.ubah_data(nama_baru, kategori_baru)

        if self._logger is not None:
            self._logger.catat(
                f"Alat {kode_alat} diubah"
            )

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
            self._logger.catat(
                f"Alat {kode_alat} dihapus"
            )

        return True

    def cari_alat(self, kode_alat):
        return self._data_alat.get(kode_alat)

    def cari_alat_fleksibel(self, keyword):
        keyword = keyword.strip().lower()
        hasil = []

        if not keyword:
            return hasil

        for alat in self._data_alat.values():
            if (
                keyword in alat.kode_alat.lower()
                or keyword in alat.nama_alat.lower()
                or keyword in alat.kategori.value.lower()
            ):
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

        alat.terima_kembali(kondisi_baru)

        if self._logger is not None:
            self._logger.catat(
                f"Kondisi alat {kode_alat} diubah menjadi "
                f"{kondisi_baru.value}"
            )

        return True
