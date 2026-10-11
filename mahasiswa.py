class Mahasiswa:
    MAKS_TRANSAKSI = 2

    def __init__(self, nim: str, nama: str, no_hp: str):
        self._nim: str = nim
        self._nama: str = nama
        self._no_hp: str = no_hp
        # Menyimpan ID transaksi yang masih aktif.
        self._transaksi_aktif: list[str] = []

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
    def transaksi_aktif(self) -> list[str]:
        # Mengembalikan salinan agar list internal tidak diubah dari luar.
        return list(self._transaksi_aktif)

    def ubah_data(self, nama: str, no_hp: str) -> None:
        """Mengubah nama dan nomor handphone mahasiswa."""
        self._nama = nama
        self._no_hp = no_hp

    def jumlah_trx_aktif(self) -> int:
        """Mengembalikan jumlah transaksi yang belum selesai."""
        return len(self._transaksi_aktif)

    def boleh_pinjam(self) -> bool:
        """Mahasiswa boleh meminjam jika belum mencapai batas transaksi aktif."""
        return self.jumlah_trx_aktif() < self.MAKS_TRANSAKSI

    def tambah_trx_aktif(self, id_transaksi: str) -> None:
        """Mencatat ID transaksi aktif tanpa menyimpan ID yang sama dua kali."""
        if id_transaksi in self._transaksi_aktif:
            return

        if not self.boleh_pinjam():
            raise ValueError(
                f"Mahasiswa {self._nim} sudah mencapai batas "
                f"{self.MAKS_TRANSAKSI} transaksi aktif."
            )

        self._transaksi_aktif.append(id_transaksi)

    def hapus_trx_aktif(self, id_transaksi: str) -> None:
        """Menghapus ID transaksi dari daftar ketika transaksi selesai."""
        if id_transaksi in self._transaksi_aktif:
            self._transaksi_aktif.remove(id_transaksi)

    def status_aktif(self) -> bool:
        """True jika mahasiswa masih mempunyai transaksi aktif."""
        return self.jumlah_trx_aktif() > 0

    def __str__(self) -> str:
        status = "Memiliki transaksi aktif" if self.status_aktif() else "Tidak memiliki transaksi aktif"
        return (
            f"[{self._nim}] {self._nama} | HP: {self._no_hp} | "
            f"{status} ({self.jumlah_trx_aktif()} transaksi)"
        )
