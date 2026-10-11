class Kategori:
    def __init__(self, id_kategori: str, nama_kategori: str):
        self._id_kategori: str = id_kategori
        self._nama_kategori: str = nama_kategori

    @property
    def id_kategori(self) -> str:
        return self._id_kategori

    @id_kategori.setter
    def id_kategori(self, value: str):
        self._id_kategori = value

    @property
    def nama_kategori(self) -> str:
        return self._nama_kategori

    @nama_kategori.setter
    def nama_kategori(self, value: str):
        self._nama_kategori = value

    def __str__(self) -> str:
        """+ __str__(): str: Menampilkan representasi string dari kategori."""
        return f"[{self._id_kategori}] {self._nama_kategori}"