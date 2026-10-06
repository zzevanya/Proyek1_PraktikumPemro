class Mahasiswa:
    def __init__(self, nim: str, nama: str, no_hp: str):
        self._nim: str = nim
        self._nama: str = nama
        self._no_hp: str = no_hp
        self._transaksi_aktif: list = []

    @property
    def nim(self) -> str:
        return self._nim

    @property
    def nama(self) -> str:
        return self._nama

    @nama.setter
    def nama(self, value: str):
        self._nama = value

    @property
    def no_hp(self) -> str:
        return self._no_hp

    @no_hp.setter
    def no_hp(self, value: str):
        self._no_hp = value

    @property
    def transaksi_aktif(self) -> list:
        return self._transaksi_aktif

    def ubah_data(self, nama: str, no_hp: str) -> None:
        """Mengubah data nama dan nomor handphone mahasiswa."""
        self._nama = nama
        self._no_hp = no_hp

    def tambah_trx_aktif(self, id_trx: str) -> None:
        """Menambahkan ID transaksi ke dalam daftar transaksi aktif."""
        if id_trx not in self._transaksi_aktif:
            self._transaksi_aktif.append(id_trx)

    def hapus_trx_aktif(self, id_trx: str = None) -> None:
        """
        Menghapus ID transaksi dari daftar transaksi aktif.
        Jika id_trx ditentukan, menghapus ID tersebut.
        Jika tidak ditentukan, menghapus item terakhir.
        """
        if id_trx is not None:
            if id_trx in self._transaksi_aktif:
                self._transaksi_aktif.remove(id_trx)
        elif self._transaksi_aktif:
            self._transaksi_aktif.pop()

    def jumlah_trx_aktif(self) -> int:
        """Mengembalikan jumlah transaksi yang sedang aktif."""
        return len(self._transaksi_aktif)

    def status_aktif(self) -> bool:
        """
        Mengecek apakah mahasiswa memiliki transaksi yang sedang berjalan/aktif.
        Mengembalikan True jika memiliki transaksi aktif, sebaliknya False.
        """
        return len(self._transaksi_aktif) > 0

    def __str__(self) -> str:
        return f"Mahasiswa(NIM: {self._nim}, Nama: {self._nama}, HP: {self._no_hp})"