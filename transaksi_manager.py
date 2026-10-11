from transaksi import Transaksi
from mahasiswa_manager import MahasiswaManager
from alatManager import AlatManager
from logAktivitas import LogAktivitas
from enumKondisi import KondisiAlat
from alat import Alat

class TransaksiManager:
    MAKS_TRANSAKSI = 2
    MAKS_HARI = 7
    
    def __init__(self, mhs_manager: MahasiswaManager, alat_manager: AlatManager, logger: LogAktivitas = None):
        self._data_transaksi: dict[str, Transaksi] = {}
        self._mahasiswa_manager = mhs_manager
        self._alat_manager = alat_manager
        self._logger = logger
        
    def buat_transaksi(self, id_trx: str, nim: str, daftar_kode_alat: list[str]) -> bool:
        mhs = self._mahasiswa_manager.get_mahasiswa(nim)
        if not mhs or not mhs.boleh_pinjam():
            return False

        if not id_trx.strip() or id_trx.strip() in self._data_transaksi:
            return False

        daftar_alat = []
        for kode in daftar_kode_alat:
            alat = self._alat_manager.get_alat_by_kode(kode)
            if alat is None or not alat.is_tersedia() or alat in daftar_alat:
                return False
            daftar_alat.append(alat)

        if not daftar_alat:
            return False

        try:
            trx = Transaksi(id_trx, mhs, daftar_alat)
        except ValueError:
            return False

        self._data_transaksi[trx.id_transaksi] = trx
        if self._logger:
            self._logger.catat(f"Buat Transaksi: ID {trx.id_transaksi} oleh NIM {nim}")
        return True
    
    def proses_pengembalian(self, id_trx: str, kode_alat: str, kondsi: KondisiAlat) -> None:
        trx = self._data_transaksi.get(id_trx)
        
        if trx:
            trx.kembalikan_item(kode_alat, kondsi)
                
            if self._logger:
                self._logger.catat(f"Pengembalian Alat: {kode_alat} pada Transaksi {id_trx}")
                
    def tampilkan_transaksi(self) -> list[Transaksi]:
        return list(self._data_transaksi.values())
    
    def cari_by_mahasiswa(self, nim:str) -> list[Transaksi]:
        return [t for t in self._data_transaksi.values() if t._mahasiswa.nim == nim]
    
    def riwayat_mahasiswa(self, nim:str) -> list[Transaksi]:
        return self.cari_by_mahasiswa(nim)
    
    def ada_trx_aktif(self, nim: str) -> bool:
        return any(t.is_aktif() for t in self.cari_by_mahasiswa(nim))
    
    def alat_dipakai_aktif(self) -> list:
        alat_list = []
        for trx in self._data_transaksi.values():
            if trx.is_aktif():
                alat_list.extend(trx.item_belum_kembali())
        return alat_list