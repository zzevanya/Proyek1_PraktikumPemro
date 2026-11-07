import os

from logAktivitas import LogAktivitas
from penyimpanan import Penyimpanan
from Kategori import Kategori
from alat import Alat
from mahasiswa import Mahasiswa
from item_pinjam import ItemPinjam
from transaksi import Transaksi
from mahasiswa_manager import MahasiswaManager
from alatManager import AlatManager
from transaksi_manager import TransaksiManager
from enumKondisi import KondisiAlat

class MenuApp:
    def __init__(self, folder_data: str = None):
        # Folder data berada di samping main.py, bukan di folder tempat program dijalankan.
        if folder_data is None:
            folder_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self._db = Penyimpanan(folder_data)
        self._log_aktivitas = LogAktivitas(self._db)
        self._mahasiswa_manager = MahasiswaManager(logger=self._log_aktivitas)
        self._alat_manager = AlatManager(logger=self._log_aktivitas)
        self._transaksi_manager = TransaksiManager(
            self._mahasiswa_manager,
            self._alat_manager,
            logger=self._log_aktivitas
        )
        self._muat_semua()

    def _muat_semua(self):
        """Urutan penting: kategori+alat -> mahasiswa -> transaksi."""
        db = self._db
        self._alat_manager.muat(
            db.muat_csv("kategori.csv"),
            db.muat_csv("alat.csv"),
        )
        self._mahasiswa_manager.muat(db.muat_csv("mahasiswa.csv"))
        self._transaksi_manager.muat(
            db.muat_csv("transaksi.csv"),
            db.muat_csv("item_pinjam.csv"),
        )

    def _simpan_semua(self):
        db = self._db
        db.simpan_csv("kategori.csv", Kategori.HEADER, self._alat_manager.data_kategori())
        db.simpan_csv("alat.csv", Alat.HEADER, self._alat_manager.data_alat())
        db.simpan_csv("mahasiswa.csv", Mahasiswa.HEADER, self._mahasiswa_manager.data_mahasiswa())
        db.simpan_csv("transaksi.csv", Transaksi.HEADER, self._transaksi_manager.data_transaksi())
        db.simpan_csv("item_pinjam.csv", ["id_transaksi"] + ItemPinjam.HEADER, self._transaksi_manager.data_item())

    def jalankan(self):
        try:
            self._loop_utama()
        finally:
            # Tetap menyimpan walaupun program ditutup paksa (mis. Ctrl+C).
            self._simpan_semua()

    def _loop_utama(self):
        self._log_aktivitas.catat("Sistem Laboratorium Berhasil Dijalankan")
        while True:
            print("\n=== SISTEM PEMINJAMAN ALAT LAB ===")
            print("1. Kelola Data Mahasiswa")
            print("2. Kelola Data Alat & Kategori")
            print("3. Transaksi Peminjaman & Pengembalian")
            print("4. Lihat Log Aktivitas/ Laporan")
            print("0. Keluar")
            
            pilihan = input("Pilih Menu (0-4): ")
            
            if pilihan == "1":
                self.menu_mahasiswa()
            elif pilihan == "2":
                self.menu_alat()
            elif pilihan == "3":
                self.menu_transaksi()
            elif pilihan == "4":
                self.menu_laporan()
            elif pilihan == "0":
                print("Terima Kasih! Program selesai.")
                break
            else:
                print("Pilihan tidak valid, silahkan coba lagi.")
                
    def menu_mahasiswa(self):
        print("\n === MENU MAHASISWA ===")
        print("1. Tambah Mahasiswa")
        print("2. Edit Mahasiswa")
        print("3. Hapus Mahasiswa")
        print("4. Cari Mahasiswa")
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih menu (0-4): ")
        
        if pilihan == "1":
            nim = input("NIM: ")
            nama = input("Nama: ")
            no_hp = input("No HP: ")
            berhasil = self._mahasiswa_manager.tambah_mahasiswa(nim, nama, no_hp)
            if berhasil:
                self._simpan_semua()
                print("Mahasiswa berhasil ditambahkan!")
            else:
                print("Gagal menambahkan mahasiswa (NIM duplikat atau input kosong).")
            
        elif pilihan == "2":
            nim = input("Masukkan NIM Mahasiswa yang ingin diedit: ")
            mhs = self._mahasiswa_manager.get_mahasiswa(nim)
            if mhs:
                nama_baru = input(f"Nama baru ({mhs.nama}): ") or mhs.nama
                no_hp_baru = input(f"No HP baru ({mhs.no_hp}): ") or mhs.no_hp
                if self._mahasiswa_manager.edit_mahasiswa(nim, nama_baru, no_hp_baru):
                    self._simpan_semua()
                    print("Data mahasiswa berhasil diperbarui!")
                else:
                    print("Data mahasiswa gagal diperbarui.")
            else:
                print("Mahasiswa dengan NIM tersebut tidak ditemukan.")
                
        elif pilihan == "3":
            nim = input("Masukkan NIM Mahasiswa yang ingin dihapus: ")
            mhs = self._mahasiswa_manager.get_mahasiswa(nim)

            if mhs is None:
                print("Mahasiswa dengan NIM tersebut tidak ditemukan.")
            else:
                berhasil = self._mahasiswa_manager.hapus_mahasiswa(nim)
                if berhasil:
                    self._simpan_semua()
                    print("Mahasiswa berhasil dihapus!")
                elif mhs.jumlah_trx_aktif() > 0:
                    print("Penghapusan ditolak! Mahasiswa masih memiliki transaksi aktif.")
                else:
                    print("Mahasiswa gagal dihapus.")
                
        elif pilihan == "4":
            keyword = input("Masukkan kata kunci (Nama/NIM): ")
            hasil = self._mahasiswa_manager.cari_mahasiswa(keyword)
            if hasil:
                print(f"\nHasil Pencarian ({len(hasil)} ditemukan)")
                for mhs in hasil:
                    print(f"NIM : {mhs.nim}")
                    print(f"Nama: {mhs.nama}")
            else:
                print("Tidak ada mahasiswa yang cocok.")
                
        elif pilihan == "0":
            return
        else:
            print("Pilihan tidak valid, silahkan coba lagi.")
            
    def menu_alat(self):
        while True:
            print("\n--- MENU ALAT & KATEGORI ---")
            print("1. Tambah Kategori")
            print("2. Tambah Alat")
            print("3. Edit Alat")
            print("4. Hapus Alat")
            print("5. Cari Alat (Kode/ Nama/ Kategori)")
            print("6. Lihat Alat Tersedia")
            print("7. Lihat Alat Dipinjam")
            print("8. Lihat Alat Rusak")
            print("9. Ubah Kondisi Alat")
            print("0. Kembali ke Menu Utama")
            
            pilihan = input("Pilih menu (0-10): ")
            
            if pilihan == "1":
                id_kategori = input("ID Kategori: ")
                nama_kategori = input("Nama Kategori: ")
                if self._alat_manager.tambah_kategori(id_kategori, nama_kategori):
                    self._simpan_semua()
                    print("Kategori berhasil ditambahkan!")
                else:
                    print("Gagal menambahkan kategori (ID sudah dipakai).")

            elif pilihan == "2":
                kode = input("Kode Alat: ")
                nama = input("Nama Alat: ")
                id_kat = input("ID Kategori: ")
                
                kategori_obj = self._alat_manager.get_kategori(id_kat)
                
                if not kategori_obj:
                    print("Gagal: ID Kategori tidak ditemukan! Silakan tambah kategori terlebih dahulu.")
                else:
                    berhasil = self._alat_manager.tambah_alat(kode, nama, kategori_obj)
                    if berhasil:
                        self._simpan_semua()
                        print("Alat berhasil ditambahkan!")
                    else:
                        print("Gagal menambahkan alat (Kode duplikat atau input tidak valid).")

            elif pilihan == "3":
                kode = input("Masukkan Kode Alat yang akan diedit: ")
                nama = input("Nama Baru: ")
                id_kat = input("ID Kategori Baru: ")
                kategori_baru = self._alat_manager.get_kategori(id_kat)
                if kategori_baru and self._alat_manager.edit_alat(kode, nama, kategori_baru):
                    self._simpan_semua()
                    print("Data alat berhasil diubah!")
                else:
                    print("Alat atau kategori tidak ditemukan, atau nama tidak valid.")

            elif pilihan == "4":
                kode = input("Masukkan Kode Alat yang akan dihapus: ")
                if self._alat_manager.hapus_alat(kode):
                    self._simpan_semua()
                    print("Alat berhasil dihapus!")
                else:
                    print("Alat tidak ditemukan atau sedang dipinjam.")

            elif pilihan == "5":
                keyword = input("Masukkan Kata Kunci (Kode/Nama/Kategori): ")
                hasil = self._alat_manager.cari_alat_fleksibel(keyword)
                if hasil:
                    print(f"\n-- Hasil Pencarian ({len(hasil)} ditemukan) --")
                    for a in hasil:
                        if a.is_tersedia():
                            status = "Tersedia"
                        elif a.is_rusak():
                            status = "Rusak"
                        else:
                            status = "Dipinjam"
                        print(
                            f"- [{a.kode_alat}] {a.nama_alat} | "
                            f"Kategori: {a.kategori.nama_kategori} | "
                            f"Kondisi: {a.kondisi.value} | Status: {status}"
                        )
                else:
                    print("Alat tidak ditemukan.")

            elif pilihan == "6":
                print("\n-- Daftar Alat Tersedia --")
                for a in self._alat_manager.tampilkan_alat_tersedia():
                    print(f"- [{a.kode_alat}] {a.nama_alat}")

            elif pilihan == "7":
                print("\n-- Daftar Alat Dipinjam --")
                for a in self._alat_manager.tampilkan_alat_dipinjam():
                    print(f"- [{a.kode_alat}] {a.nama_alat}")

            elif pilihan == "8":
                print("\n-- Daftar Alat Rusak --")
                for a in self._alat_manager.tampilkan_alat_rusak():
                    print(f"- [{a.kode_alat}] {a.nama_alat} | Kondisi: {a._kondisi.value}")

            elif pilihan == "9":
                kode = input("Masukkan Kode Alat: ")
                print("Pilih Kondisi Baru: 1. BAIK | 2. RUSAK_RINGAN | 3. RUSAK_BERAT")
                opt = input("Pilih (1-3): ")
                kondisi = KondisiAlat.BAIK
                if opt == "2":
                    kondisi = KondisiAlat.RUSAK_RINGAN
                elif opt == "3":
                    kondisi = KondisiAlat.RUSAK_BERAT
                
                if self._alat_manager.ubah_kondisi_alat(kode, kondisi):
                    self._simpan_semua()
                    print("Kondisi alat berhasil diperbarui!")
                else:
                    print("Alat tidak ditemukan.")

            elif pilihan == "0":
                return
            else:
                print("Pilihan tidak valid.")
                
    def menu_transaksi(self):
        while True:
            print("\n=== MENU TRANSAKSI & PEMINJAMAN ===")
            print("1. Buat Transaksi Peminjaman")
            print("2. Proses Pengembalian Alat")
            print("3. Tampilkan Semua Transaksi")
            print("4. Cari / Riwayat Transaksi Mahasiswa (by NIM)")
            print("5. Cek Status Transaksi Aktif Mahasiswa")
            print("6. Lihat Daftar Alat yang Sedang Dipakai/Dipinjam")
            print("0. Kembali ke Menu Utama")
            
            pilihan = input("Pilih menu (0-6): ")
            
            if pilihan == "1":
                id_trx = input("ID Transaksi Baru: ")
                nim = input("NIM Mahasiswa: ")
                kode_input = input("Kode Alat (pisahkan dengan koma jika > 1, contoh: ALT01, ALT02): ")
                daftar_kode = [k.strip() for k in kode_input.split(",") if k.strip()]
                
                if self._transaksi_manager.buat_transaksi(id_trx, nim, daftar_kode):
                    self._simpan_semua()
                    print("Transaksi peminjaman berhasil dibuat!")
                else:
                    print("Gagal membuat transaksi! (Mahasiswa tidak ditemukan / Melebihi kuota maks transaksi / Alat tidak tersedia).")

            elif pilihan == "2":
                id_trx = input("ID Transaksi: ")
                kode_alat = input("Kode Alat yang Dikembalikan: ")
                print("Kondisi Alat saat dikembalikan:")
                print("1. BAIK | 2. RUSAK_RINGAN | 3. RUSAK_BERAT")
                opt = input("Pilih Kondisi (1-3): ")
                
                kondisi = KondisiAlat.BAIK
                if opt == "2":
                    kondisi = KondisiAlat.RUSAK_RINGAN
                elif opt == "3":
                    kondisi = KondisiAlat.RUSAK_BERAT

                berhasil = self._transaksi_manager.proses_pengembalian(id_trx, kode_alat, kondisi)
                if berhasil:
                    self._simpan_semua()
                    print("Pengembalian alat berhasil diproses!")
                else:
                    print("Pengembalian gagal. Periksa ID transaksi, kode alat, atau status pengembaliannya.")

            elif pilihan == "3":
                daftar_trx = self._transaksi_manager.tampilkan_transaksi()
                if daftar_trx:
                    print("\n--- DAFTAR SELURUH TRANSAKSI ---")
                    for t in daftar_trx:
                        print(f"- ID: {t._id_transaksi} | Mahasiswa: {t._mahasiswa.nama} ({t._mahasiswa.nim}) | Status: {t._status.value}")
                else:
                    print("Belum ada transaksi tercatat.")

            elif pilihan == "4":
                nim = input("Masukkan NIM Mahasiswa: ")
                riwayat = self._transaksi_manager.riwayat_mahasiswa(nim)
                if riwayat:
                    print(f"\n--- RIWAYAT TRANSAKSI NIM: {nim} ---")
                    for t in riwayat:
                        print(f"- ID: {t._id_transaksi} | Status: {t._status.value}")
                else:
                    print("Tidak ditemukan riwayat transaksi untuk NIM tersebut.")

            elif pilihan == "5":
                nim = input("Masukkan NIM Mahasiswa: ")
                if self._transaksi_manager.ada_trx_aktif(nim):
                    print(f"Mahasiswa dengan NIM {nim} SAAT INI MEMILIKI transaksi aktif.")
                else:
                    print(f"Mahasiswa dengan NIM {nim} TIDAK MEMILIKI transaksi aktif.")

            elif pilihan == "6":
                alat_dipakai = self._transaksi_manager.alat_dipakai_aktif()
                if alat_dipakai:
                    print("\n--- DAFTAR ALAT YANG SEDANG DIPINJAM ---")
                    for item in alat_dipakai:
                        print(f"- Kode: {item.alat.kode_alat} | Nama: {item.alat.nama_alat}")
                else:
                    print("Saat ini tidak ada alat yang sedang dipinjam.")

            elif pilihan == "0":
                return
            else:
                print("Pilihan tidak valid, silakan coba lagi.")
                
    def menu_laporan(self):
        print("\n--- LOG AKTIVITAS & LAPORAN ---")
        self._log_aktivitas.tampilkan()

if __name__ == "__main__":
    app = MenuApp()
    app.jalankan()