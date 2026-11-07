from transaksi import Transaksi
from item_pinjam import ItemPinjam
from mahasiswa_manager import MahasiswaManager
from alatManager import AlatManager
from logAktivitas import LogAktivitas
from enumKondisi import KondisiAlat


class TransaksiManager:
    MAKS_TRANSAKSI = 2
    MAKS_HARI = 7

    def __init__(
        self,
        mhs_manager: MahasiswaManager,
        alat_manager: AlatManager,
        logger: LogAktivitas = None,
    ):
        self._data_transaksi: dict[str, Transaksi] = {}
        self._mahasiswa_manager = mhs_manager
        self._alat_manager = alat_manager
        self._logger = logger

    def buat_transaksi(
        self, id_trx: str, nim: str, daftar_kode_alat: list[str]
    ) -> bool:
        # Tolak ID transaksi yang kosong atau sudah digunakan.
        if not id_trx.strip() or id_trx in self._data_transaksi:
            return False

        mhs = self._mahasiswa_manager.get_mahasiswa(nim)
        if mhs is None or not mhs.boleh_pinjam():
            return False

        if not daftar_kode_alat:
            return False

        # Validasi seluruh alat terlebih dahulu agar transaksi tidak dibuat separuh.
        daftar_alat = []
        kode_dilihat = set()

        for kode in daftar_kode_alat:
            if kode in kode_dilihat:
                return False
            kode_dilihat.add(kode)

            alat = self._alat_manager.cari_alat(kode)
            if alat is None or not alat.is_tersedia():
                return False

            daftar_alat.append(alat)

        try:
            # Constructor Transaksi membutuhkan ID, mahasiswa, dan daftar objek alat.
            # Transaksi sendiri yang mencatat ID aktif pada objek Mahasiswa.
            trx = Transaksi(id_trx, mhs, daftar_alat)
        except ValueError:
            return False

        self._data_transaksi[id_trx] = trx
        if self._logger:
            self._logger.catat(f"Buat Transaksi: ID {id_trx} oleh NIM {nim}")
        return True

    def proses_pengembalian(
        self, id_trx: str, kode_alat: str, kondisi: KondisiAlat
    ) -> bool:
        trx = self._data_transaksi.get(id_trx)
        if trx is None:
            return False

        try:
            trx.kembalikan_item(kode_alat, kondisi)
        except ValueError:
            return False

        # Transaksi.perbarui_status() menghapus ID aktif jika semua item sudah kembali.
        if self._logger:
            self._logger.catat(
                f"Pengembalian Alat: {kode_alat} pada Transaksi {id_trx}"
            )
        return True

    def tampilkan_transaksi(self) -> list[Transaksi]:
        return list(self._data_transaksi.values())

    def cari_by_mahasiswa(self, nim: str) -> list[Transaksi]:
        return [
            transaksi for transaksi in self._data_transaksi.values()
            if transaksi.mahasiswa.nim == nim
        ]

    def riwayat_mahasiswa(self, nim: str) -> list[Transaksi]:
        return self.cari_by_mahasiswa(nim)

    def ada_trx_aktif(self, nim: str) -> bool:
        return any(
            transaksi.is_aktif()
            for transaksi in self.cari_by_mahasiswa(nim)
        )

    def alat_dipakai_aktif(self) -> list:
        alat_list = []
        for transaksi in self._data_transaksi.values():
            if transaksi.is_aktif():
                alat_list.extend(transaksi.item_belum_kembali())
        return alat_list


    # ---------- Persistensi ----------
    def data_transaksi(self) -> list[dict]:
        return [t.to_dict() for t in self._data_transaksi.values()]

    def data_item(self) -> list[dict]:
        baris = []
        for trx in self._data_transaksi.values():
            for item in trx.daftar_item:
                d = item.to_dict()
                d["id_transaksi"] = trx.id_transaksi
                baris.append(d)
        return baris

    def muat(self, data_transaksi: list[dict], data_item: list[dict]) -> None:
        """Harus dipanggil SETELAH mahasiswa dan alat dimuat.
        Sekaligus memulihkan status "sedang dipinjam" pada alat dan
        daftar transaksi aktif pada mahasiswa dari data transaksi."""
        self._data_transaksi = {}

        item_per_trx: dict[str, list[dict]] = {}
        for d in data_item:
            item_per_trx.setdefault(d.get("id_transaksi", ""), []).append(d)

        for d in data_transaksi:
            try:
                mhs = self._mahasiswa_manager.get_mahasiswa(d["nim"])
                if mhs is None:
                    raise ValueError(f"mahasiswa {d['nim']} tidak ditemukan")

                daftar_item = []
                for di in item_per_trx.get(d["id_transaksi"], []):
                    alat = self._alat_manager.cari_alat(di["kode_alat"])
                    if alat is None:
                        raise ValueError(f"alat {di['kode_alat']} tidak ditemukan")
                    daftar_item.append(ItemPinjam.from_dict(di, alat))
                if not daftar_item:
                    raise ValueError("transaksi tanpa item")

                trx = Transaksi.from_dict(d, mhs, daftar_item)
                if trx.is_aktif():
                    mhs.tambah_trx_aktif(trx.id_transaksi)
            except (KeyError, ValueError) as e:
                print(f"Peringatan: transaksi {d.get('id_transaksi', '?')} dilewati ({e})")
                continue

            if trx.is_aktif():
                for item in trx.item_belum_kembali():
                    item.alat.tandai_dipinjam()
            self._data_transaksi[trx.id_transaksi] = trx
