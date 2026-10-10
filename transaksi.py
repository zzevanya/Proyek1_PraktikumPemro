from datetime import date, timedelta
from typing import Optional

from alat import Alat
from enumKondisi import KondisiAlat
from enumsStatus import StatusTransaksi
from item_pinjam import ItemPinjam
from mahasiswa import Mahasiswa

class Transaksi:
    MAKS_HARI = 7
    
    def __init__(
        self,
        id_transaksi : str,
        mahasiswa: Mahasiswa,
        daftar_alat: list[Alat],
        tanggal_pinjam: Optional[date] = None,
        lama_hari: int = MAKS_HARI,
    ):
        if not id_transaksi.strip():
            raise ValueError("ID transaksi tidak boleh kosong.")
        if not mahasiswa.boleh_pinjam():
            raise ValueError(
                f"Mahasiswa {mahasiswa.nim} sudah memiliki "
                f"{Mahasiswa.MAKS_TRANSAKSI} transaksi aktif."
            )
        if not daftar_alat:
            raise ValueError("Transaksi harus berisi minimal satu alat.")
        if not 1 <= lama_hari <= self.MAKS_HARI:
            raise ValueError(f"Lama peminjaman harus 1-{self.MAKS_HARI} hari.")
        
        kode_terlihat = set()
        for alat in daftar_alat:
            if alat.kode_alat in kode_terlihat:
                raise ValueError(f"Alat {alat.kode_alat} dimasukkan lebih dari sekali.")
            kode_terlihat.add(alat.kode_alat)
            if not alat.is_tersedia():
                raise ValueError(f"Alat {alat.kode_alat} ({alat.nama_alat}) tidak tersedia.")
    
        self._id_transaksi: str = id_transaksi.strip()
        self._mahasiswa: Mahasiswa = mahasiswa
        self._daftar_item: list[ItemPinjam] = [ItemPinjam(a) for a in daftar_alat]
        self._tanggal_pinjam: date = tanggal_pinjam or date.today()
        self._batas_kembali: date = self._tanggal_pinjam + timedelta(days=lama_hari)
        self._status: StatusTransaksi = StatusTransaksi.DIPINJAM
        
        mahasiswa.tambah_trx_aktif(self._id_transaksi)
        
    @property
    def id_transaksi(self) -> str:
        return self._id_transaksi
    
    @property
    def mahasiswa(self)  -> Mahasiswa:
        return self._mahasiswa
    
    @property
    def daftar_item(self) -> list[ItemPinjam]:
        return list(self._daftar_item)
    
    @property
    def tanggal_pinjam(self) -> date:
        return self._tanggal_pinjam
    
    @property
    def batas_kembali(self) -> date:
        return self._batas_kembali
    
    @property
    def status(self) -> StatusTransaksi:
        return self._status
    
    
    def is_aktif(self) -> bool:
        return self._status != StatusTransaksi.SELESAI
    
    def item_belum_kembali(self) -> list[ItemPinjam]:
        return [i for i in self._daftar_item if not i.is_dikembalikan()]
    
    def item_sudah_dikembalikan(self) -> list[ItemPinjam]:
        return [i for i in self._daftar_item if i.is_dikembalikan()]
    
    def punya_alat(self, kode_alat: str) -> bool:
        return any(i.alat.kode_alat == kode_alat for i in self._daftar_item)
    
    def is_terlambat(self, hari_ini: Optional[date] = None) -> bool:
        hari_ini = hari_ini or date.today()
        for item in self._daftar_item:
            pembanding = item.tanggal_kembali if item.is_dikembalikan() else hari_ini
            if pembanding > self._batas_kembali:
                return True
        return False
    
    def kembalikan_item(
        self,
        kode_alat: str,
        kondisi: KondisiAlat,
        tanggal: Optional[date] = None,
    ) -> None:
        item = self._cari_item(kode_alat)
        if item is None:
            raise ValueError(
                f"Alat {kode_alat} tidak ada dalam transaksi {self._id_transaksi}."
            )
            
        tanggal = tanggal or date.today()
        if tanggal < self._tanggal_pinjam:
            raise ValueError("Tanggal pengembalian tidak boleh sebelum tanggal peminjaman.")
        
        item.kembalikan(kondisi, tanggal)
        self.perbarui_status()
        
    
    def perbarui_status(self) -> None:
        jumlah_kembali = len(self.item_sudah_dikembalikan())
        
        if jumlah_kembali ==0:
            self._status = StatusTransaksi.DIPINJAM
        elif jumlah_kembali < len(self._daftar_item):
            self._status = StatusTransaksi.SEBAGIAN_DIKEMBALIKAN
        else:
            self._status = StatusTransaksi.SELESAI
            self._mahasiswa.hapus_trx_aktif(self.id_transaksi)
            
    def _cari_item(self, kode_alat: str) -> Optional[ItemPinjam]:
        for item in self._daftar_item:
            if item.alat.kode_alat == kode_alat:
                return item
        return None
        
    def __str__(self) -> str:
        baris = [
            f"Transaksi {self._id_transaksi} | {self._mahasiswa.nama} ({self._mahasiswa.nim})",
            f"Pinjam: {self._tanggal_pinjam} | Batas: {self._batas_kembali} | "
            f"Status: {self._status.value}",
        ]
        baris += [f" - {item}" for item in self._daftar_item]
        return "\n".join(baris)