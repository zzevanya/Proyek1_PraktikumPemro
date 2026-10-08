from mahasiswa import Mahasiswa
from logAktivitas import LogAktivitas

class MahasiswaManager:
    def __init__(self, logger: LogAktivitas = None):
        self._data_mahasiswa: dict[str, Mahasiswa] = {}
        self._logger = logger
        
    def tambah_mahasiswa(self, nim: str, nama: str, no_hp:str) -> None:
        if nim not in self._data_mahasiswa:
            self._data_mahasiswa[nim] = Mahasiswa(nim, nama, no_hp)
            if self._logger:
                self._logger.catat(f"Tambah Mahasiswa: {nama} ({nim})")
                
    def edit_mahasiswa(self, nim:str, nama:str, no_hp:str)-> None:
        mhs = self.get_mahasiswa(nim)
        if mhs:
            mhs.ubah_data(nama, no_hp)
            if self._logger:
                self._logger.catat(f"Edit Mahasiswa: {nama} ({nim})")
                
    def hapus_mahasiswa(self, nim:str) -> None:
        if nim in self._data_mahasiswa:
            del self._data_mahasiswa[nim]
            if self._logger:
                self._logger.catat(f"Hapus Mahasiswa: {nim}")
                
    def cari_mahasiswa(self, keyword: str) -> list[Mahasiswa]:
        return[
            mhs for mhs in self._data_mahasiswa.values()
            if keyword.lower() in mhs.nama.lower() or keyword in mhs.nim
        ]
        
    def get_mahasiswa(self, nim:str)-> Mahasiswa:
        return self._data_mahasiswa.get(nim)