from datetime import date
from typing import Optional

from alat import Alat
from enumKondisi import KondisiAlat

class ItemPinjam:
    def __init__(self, alat: Alat):
        alat.tandai_dipinjam()
        
        self._alat: Alat = alat
        self._sudah_kembali: bool = False
        self._tanggal_kembali: Optional[date] = None
        self._kondisi_kembali: Optional[KondisiAlat] = None
        
    @property
    def alat(self) -> Alat:
        return self._alat
    
    @property
    def sudah_kembali(self) -> bool:
        return self._sudah_kembali
    
    @property
    def tanggal_kembali(self) -> Optional[date]:
        return self._tanggal_kembali
    
    @property
    def kondisi_kembali(self) -> Optional[KondisiAlat]:
        return self._kondisi_kembali
    
    def is_dikembalikan(self) -> bool:
        return self._sudah_kembali
    
    def kembalikan(self, kondisi: KondisiAlat, tanggal: Optional[date] = None) -> None:
        if self._sudah_kembali:
            raise ValueError(
                f"Alat {self._alat.kode_alat} sudah dikembalikan sebelumnya."
            )
            
        self._alat.terima_kembali(kondisi)
        self._sudah_kembali = True
        self._kondisi_kembali = kondisi
        self._tanggal_kembali = tanggal or date.today()
        
    def __str__(self) -> str:
        if self._sudah_kembali:
            status = (f"Dikembalikan {self._tanggal_kembali} "
                      f"({self._kondisi_kembali.value})")
        else:
            status = "Belum dikembalikan"
        return f"[{self._alat.kode_alat}] {self._alat.nama_alat} | {status}"