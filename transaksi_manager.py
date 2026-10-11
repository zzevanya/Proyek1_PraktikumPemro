from transaksi import Transaksi
from mahasiswa_manager import MahasiswaManager
from alatManager import AlatManager
from logAktivitas import LogAktivitas
from enumKondisi import KondisiAlat


class TransaksiManager:
    MAKS_TRANSAKSI = 2
    MAKS_HARI = 7

    def __init__(
        self,
        mhs_manager: MahasiswaManager,
        alat_manager: AlatManager,
        logger: LogAktivitas = None,
    ):
        self._data_transaksi: dict[str, Transaksi] = {}
        self._mahasiswa_manager = mhs_manager
        self._alat_manager = alat_manager
        self._logger = logger

    def buat_transaksi(
        self, id_trx: str, nim: str, daftar_kode_alat: list[str]
    ) -> bool:
        # Tolak ID transaksi yang kosong atau sudah digunakan.
        if not id_trx.strip() or id_trx in self._data_transaksi:
            return False

        mhs = self._mahasiswa_manager.get_mahasiswa(nim)
        if mhs is None or not mhs.boleh_pinjam():
            return False

        if not daftar_kode_alat:
            return False

        # Validasi seluruh alat terlebih dahulu agar transaksi tidak dibuat separuh.
        daftar_alat = []
        kode_dilihat = set()

        for kode in daftar_kode_alat:
            if kode in kode_dilihat:
                return False
            kode_dilihat.add(kode)

            alat = self._alat_manager.cari_alat(kode)
            if alat is None or not alat.is_tersedia():
                return False

            daftar_alat.append(alat)

        try:
            # Constructor Transaksi membutuhkan ID, mahasiswa, dan daftar objek alat.
            # Transaksi sendiri yang mencatat ID aktif pada objek Mahasiswa.
            trx = Transaksi(id_trx, mhs, daftar_alat)
        except ValueError:
            return False

        self._data_transaksi[id_trx] = trx
        if self._logger:
            self._logger.catat(f"Buat Transaksi: ID {id_trx} oleh NIM {nim}")
        return True

    def proses_pengembalian(
        self, id_trx: str, kode_alat: str, kondisi: KondisiAlat
    ) -> bool:
        trx = self._data_transaksi.get(id_trx)
        if trx is None:
            return False

        try:
            trx.kembalikan_item(kode_alat, kondisi)
        except ValueError:
            return False

        # Transaksi.perbarui_status() menghapus ID aktif jika semua item sudah kembali.
        if self._logger:
            self._logger.catat(
                f"Pengembalian Alat: {kode_alat} pada Transaksi {id_trx}"
            )
        return True

    def tampilkan_transaksi(self) -> list[Transaksi]:
        return list(self._data_transaksi.values())

    def cari_by_mahasiswa(self, nim: str) -> list[Transaksi]:
        return [
            transaksi for transaksi in self._data_transaksi.values()
            if transaksi.mahasiswa.nim == nim
        ]

    def riwayat_mahasiswa(self, nim: str) -> list[Transaksi]:
        return self.cari_by_mahasiswa(nim)

    def ada_trx_aktif(self, nim: str) -> bool:
        return any(
            transaksi.is_aktif()
            for transaksi in self.cari_by_mahasiswa(nim)
        )

    def alat_dipakai_aktif(self) -> list:
        alat_list = []
        for transaksi in self._data_transaksi.values():
            if transaksi.is_aktif():
                alat_list.extend(transaksi.item_belum_kembali())
        return alat_list
