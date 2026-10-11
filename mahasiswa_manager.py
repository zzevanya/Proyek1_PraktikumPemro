from mahasiswa import Mahasiswa
from logAktivitas import LogAktivitas


class MahasiswaManager:
    def __init__(self, logger: LogAktivitas = None):
        self._data_mahasiswa: dict[str, Mahasiswa] = {}
        self._logger = logger

    def tambah_mahasiswa(self, nim: str, nama: str, no_hp: str) -> bool:
        if not nim.strip() or not nama.strip() or not no_hp.strip():
            return False

        if nim in self._data_mahasiswa:
            return False

        self._data_mahasiswa[nim] = Mahasiswa(nim, nama, no_hp)
        if self._logger:
            self._logger.catat(f"Tambah Mahasiswa: {nama} ({nim})")
        return True

    def edit_mahasiswa(self, nim: str, nama: str, no_hp: str) -> bool:
        mhs = self.get_mahasiswa(nim)
        if mhs is None or not nama.strip() or not no_hp.strip():
            return False

        mhs.ubah_data(nama, no_hp)
        if self._logger:
            self._logger.catat(f"Edit Mahasiswa: {nama} ({nim})")
        return True

    def hapus_mahasiswa(self, nim: str) -> bool:
        """Menolak penghapusan jika mahasiswa masih memiliki transaksi aktif."""
        mhs = self.get_mahasiswa(nim)

        if mhs is None:
            return False

        # Ini pemeriksaan utama untuk Skenario 6.
        if mhs.jumlah_trx_aktif() > 0:
            return False

        del self._data_mahasiswa[nim]
        if self._logger:
            self._logger.catat(f"Hapus Mahasiswa: {nim}")
        return True

    def cari_mahasiswa(self, keyword: str) -> list[Mahasiswa]:
        keyword = keyword.lower().strip()
        return [
            mhs for mhs in self._data_mahasiswa.values()
            if keyword in mhs.nama.lower() or keyword in mhs.nim.lower()
        ]

    def get_mahasiswa(self, nim: str):
        return self._data_mahasiswa.get(nim)