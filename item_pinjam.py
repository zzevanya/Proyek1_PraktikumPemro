from datetime import date
from typing import Optional

from alat import Alat
from enumKondisi import KondisiAlat

class ItemPinjam:
    HEADER = ["kode_alat", "sudah_kembali", "tanggal_kembali", "kondisi_kembali"]

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


    def to_dict(self) -> dict:
        return {
            "kode_alat": self._alat.kode_alat,
            "sudah_kembali": "1" if self._sudah_kembali else "0",
            "tanggal_kembali": self._tanggal_kembali.isoformat() if self._tanggal_kembali else "",
            "kondisi_kembali": self._kondisi_kembali.name if self._kondisi_kembali else "",
        }

    @classmethod
    def from_dict(cls, d: dict, alat: Alat) -> "ItemPinjam":
        # Melewati __init__ karena __init__ memanggil alat.tandai_dipinjam();
        # status dipinjam dipulihkan terpisah oleh TransaksiManager.muat().
        item = cls.__new__(cls)
        item._alat = alat
        item._sudah_kembali = d["sudah_kembali"] == "1"
        item._tanggal_kembali = date.fromisoformat(d["tanggal_kembali"]) if d["tanggal_kembali"] else None
        item._kondisi_kembali = KondisiAlat[d["kondisi_kembali"]] if d["kondisi_kembali"] else None
        return item
