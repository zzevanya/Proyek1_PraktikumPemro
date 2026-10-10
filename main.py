from logAktivitas import LogAktivitas
from mahasiswa_manager import MahasiswaManager
from alatManager import AlatManager
from transaksi_manager import TransaksiManager
from enumKondisi import KondisiAlat

class MenuApp:
    def __init__(self):
        self._log_aktivitas = LogAktivitas()
        self._mahasiswa_manager = MahasiswaManager(logger=self._log_aktivitas)
        self._alat_manager = AlatManager(logger=self._log_aktivitas)
        self._transaksi_manager = TransaksiManager(
            self._mahasiswa_manager,
            self._alat_manager,
            logger=self._log_aktivitas
        )
        
    def jalankan(self):
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
            nama= input("Nama: ")
            no_hp = input("No HP: ")
            self._mahasiswa_manager.tambah_mahasiswa(nim, nama, no_hp)
            print("Mahasiswa berhasil ditambahkan!")
            
        elif pilihan == "2":
            nim = input("Masukkan NIM Mahasiswa yang ingin diedit: ")
            mhs = self._mahasiswa_manager.get_mahasiswa(nim)
            if mhs:
                nama_baru = input(f"Nama baru ({mhs.nama}): ") or mhs.nama
                no_hp_baru = input(f"No HP baru: ")
                self._mahasiswa_manager.edit_mahasiswa(nim, nama_baru, no_hp_baru)
                print("Data mahasiswa berhasil diperbarui!")
            else:
                print("Mahasiswa dengan NIM tersebut tidak ditemukan.")
                
        elif pilihan == "3":
            nim = input("Masukkan NIM Mahasiswa yang ingin dihapus: ")
            mhs = self._mahasiswa_manager.get_mahasiswa(nim)
            if mhs:
                self._mahasiswa_manager.hapus_mahasiswa(nim)
                print("Mahasiswa berhasil dihapus!")
            else:
                print("Mahasiswa tidak dengan NIM tersebut tidak ditemukan.")
                
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
            print("Kembali ke Menu Utama....")
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
            print("5. Cari Alat (by Kode)")
            print("6. Cari Alat Fleksibel (by Keyword)")
            print("7. Lihat Alat Tersedia")
            print("8. Lihat Alat Dipinjam")
            print("9. Lihat Alat Rusak")
            print("10. Ubah Kondisi Alat")
            print("0. Kembali ke Menu Utama")
            
            pilihan = input("Pilih menu (0-10): ")
            
            if pilihan == "1":
                id_kat = input("ID Kategori: ")
                nama_kat = input("Nama Kategori: ")
                self._alat_manager.tambah_kategori(id_kat, nama_kat)
                print("Kategori berhasil ditambahkan!")

            elif pilihan == "2":
                kode = input("Kode Alat: ")
                nama = input("Nama Alat: ")
                id_kat = input("ID Kategori: ")
                if self._alat_manager.tambah_alat(kode, nama, id_kat):
                    print("Alat berhasil ditambahkan!")
                else:
                    print("Gagal menambahkan alat (Kategori tidak ditemukan / Kode duplikat).")

            elif pilihan == "3":
                kode = input("Masukkan Kode Alat yang akan diedit: ")
                nama = input("Nama Baru: ")
                id_kat = input("ID Kategori Baru: ")
                if self._alat_manager.edit_alat(kode, nama, id_kat):
                    print("Data alat berhasil diubah!")
                else:
                    print("Alat atau Kategori tidak ditemukan.")

            elif pilihan == "4":
                kode = input("Masukkan Kode Alat yang akan dihapus: ")
                if self._alat_manager.hapus_alat(kode):
                    print("Alat berhasil dihapus!")
                else:
                    print("Alat tidak ditemukan.")

            elif pilihan == "5":
                kode = input("Masukkan Kode Alat: ")
                alat = self._alat_manager.get_alat_by_kode(kode)
                if alat:
                    print(f"- [{alat.kode_alat}] {alat.nama_alat} | Kategori: {alat._kategori.nama_kategori}")
                else:
                    print("Alat tidak ditemukan.")

            elif pilihan == "6":
                kw = input("Masukkan Kata Kunci: ")
                hasil = self._alat_manager.cari_alat_fleksibel(kw)
                for a in hasil:
                    print(f"- [{a.kode_alat}] {a.nama_alat} | Kategori: {a._kategori.nama_kategori}")

            elif pilihan == "7":
                print("\n-- Daftar Alat Tersedia --")
                for a in self._alat_manager.tampilkan_alat_tersedia():
                    print(f"- [{a.kode_alat}] {a.nama_alat}")

            elif pilihan == "8":
                print("\n-- Daftar Alat Dipinjam --")
                for a in self._alat_manager.tampilkan_alat_dipinjam():
                    print(f"- [{a.kode_alat}] {a.nama_alat}")

            elif pilihan == "9":
                print("\n-- Daftar Alat Rusak --")
                for a in self._alat_manager.tampilkan_alat_rusak():
                    print(f"- [{a.kode_alat}] {a.nama_alat} | Kondisi: {a._kondisi.value}")

            elif pilihan == "10":
                kode = input("Masukkan Kode Alat: ")
                print("Pilih Kondisi Baru: 1. BAIK | 2. RUSAK_RINGAN | 3. RUSAK_BERAT")
                opt = input("Pilih (1-3): ")
                kondisi = KondisiAlat.BAIK
                if opt == "2":
                    kondisi = KondisiAlat.RUSAK_RINGAN
                elif opt == "3":
                    kondisi = KondisiAlat.RUSAK_BERAT
                
                if self._alat_manager.ubah_kondisi_alat(kode, kondisi):
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

                self._transaksi_manager.proses_pengembalian(id_trx, kode_alat, kondisi)
                print("Pengembalian alat selesai diproses!")

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