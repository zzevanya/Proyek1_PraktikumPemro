from typing import List, Optional


class Mahasiswa:
    def __init__(self, nim: str, nama: str, no_hp: str):
        self._nim: str = nim
        self._nama: str = nama
        self._no_hp: str = no_hp
        self._transaksi_aktif: List[str] = []

    @property
    def nim(self) -> str:
        return self._nim

    @property
    def nama(self) -> str:
        return self._nama

    @nama.setter
    def nama(self, nama_baru: str):
        self._nama = nama_baru

    @property
    def no_hp(self) -> str:
        return self._no_hp

    @no_hp.setter
    def no_hp(self, no_hp_baru: str):
        self._no_hp = no_hp_baru

    @property
    def transaksi_aktif(self) -> List[str]:
        return self._transaksi_aktif

    def ubah_data(self, nama: str, no_hp: str) -> None:
        """+ ubah_data(nama, no_hp): Mengubah nama dan nomor handphone mahasiswa."""
        self._nama = nama
        self._no_hp = no_hp

    def tambah_trx_aktif(self, id_transaksi: str) -> None:
        """+ tambah_trx_aktif(id): Menambahkan ID transaksi peminjaman yang sedang aktif."""
        if id_transaksi not in self._transaksi_aktif:
            self._transaksi_aktif.append(id_transaksi)

    def hapus_trx_aktif(self, id_transaksi: Optional[str] = None) -> None:
        """
        + hapus_trx_aktif(): 
        Menghapus ID transaksi dari daftar transaksi aktif saat transaksi selesai/dikembalikan.
        Bisa menghapus ID tertentu jika diberikan, atau pop item terakhir jika parameter kosong.
        """
        if id_transaksi is not None:
            if id_transaksi in self._transaksi_aktif:
                self._transaksi_aktif.remove(id_transaksi)
        elif self._transaksi_aktif:
            self._transaksi_aktif.pop()

    def jumlah_trx_aktif(self) -> int:
        """
        + jumlah_trx_aktif(): 
        Mengembalikan jumlah transaksi aktif mahasiswa (digunakan untuk validasi batas MAKS_TRANSAKSI).
        """
        return len(self._transaksi_aktif)

    def status_aktif(self) -> bool:
        """
        + status_aktif(): bool: 
        Mengembalikan True jika mahasiswa masih memiliki transaksi aktif, sebaliknya False.
        """
        return len(self._transaksi_aktif) > 0

    def __str__(self) -> str:
        status = "Meminjam" if self.status_aktif() else "Bebas Pinjaman"
        return f"[{self._nim}] {self._nama} | HP: {self._no_hp} | Status: {status} ({self.jumlah_trx_aktif()} transaksi aktif)"