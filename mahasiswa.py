class Mahasiswa:
    def __init__(self, nim: str, nama: str, no_hp: str):
        self._nim: str = nim
        self._nama: str = nama
        self._no_hp: str = no_hp

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

    def ubah_data(self, nama: str, no_hp: str) -> None:
        """+ ubah_data(nama, no_hp): Mengubah nama dan nomor handphone mahasiswa."""
        self._nama = nama
        self._no_hp = no_hp

    def __str__(self) -> str:
        return f"[{self._nim}] {self._nama} | HP: {self._no_hp}"