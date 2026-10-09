# Proyek1_PraktikumPemro
# 🧰 Sistem Pengelolaan Peminjaman Peralatan Laboratorium

Aplikasi **Sistem Pengelolaan Peminjaman Peralatan Laboratorium** berbasis Python yang dikembangkan untuk tugas **Proyek I Praktikum Pemrograman Dasar**.

Program ini menerapkan konsep **Object-Oriented Programming (OOP)** dan menggunakan struktur data **List dan Dictionary** untuk mengelola data mahasiswa, peralatan laboratorium, transaksi peminjaman, serta pengembalian alat.

Aplikasi ini dirancang untuk membantu pencatatan peminjaman peralatan secara terstruktur, memantau ketersediaan alat, mencatat kondisi peralatan setelah dikembalikan, dan mengelola riwayat aktivitas sistem.

---

## 👥 Anggota Kelompok

| NIM | Nama | GitHub | Bagian |
|---|---|---|---|
| K3525078 | ZEFA | [@zzevanya] https://github.com/zzevanya | MenuApp, mahasiswa_manager, TransaksiManager |
| K3525021 | REA | [@aurreadaffa17] https://github.com/aurreadaffa17 | Mahasiswa, enumStatus, Alat |
| K3525064 | SANDI | [@shandyeka491-stack] https://github.com/shandyeka491-stack | Kategori, ItemPinjam, Transaksi |
| K3525028 | IMMEL | [@lmmelda] https://github.com/lmmelda | enumKondisi, AlatManager, LogAktivitas |

---

## 🗂️ Struktur Project

```text
Proyek1_PraktikumPemro/
│
├── main.py
├── README.md
│
├── enumsStatus.py
├── enumKondisi.py
├── Kategori.py
├── logAktivitas.py
│
├── mahasiswa.py
├── mahasiswa_manager.py
│
├── alat.py
├── alatManager.py
│
├── itemPinjam.py
├── transaksi.py
└── transaksiManager.py
```

---

## ✨ Fitur Program

- 👨‍🎓 Mengelola data mahasiswa: tambah, edit, hapus, dan cari.
- 🧰 Mengelola data alat: tambah, edit, hapus, dan cari.
- 📦 Membuat transaksi peminjaman yang dapat berisi beberapa alat.
- 🔄 Memproses pengembalian alat, termasuk pengembalian sebagian.
- ✅ Menampilkan daftar alat yang tersedia untuk dipinjam.
- 📋 Menampilkan daftar alat yang sedang dipinjam.
- ⚠️ Menampilkan daftar alat yang mengalami kerusakan.
- 🔎 Mencari transaksi berdasarkan mahasiswa.
- 🕘 Menampilkan riwayat peminjaman mahasiswa.
- 📝 Mencatat aktivitas yang terjadi di dalam sistem.

### Aturan Peminjaman

Sistem dirancang untuk menerapkan aturan berikut:

- Mahasiswa maksimal memiliki dua transaksi peminjaman aktif.
- Alat yang sedang dipinjam tidak dapat dipinjam kembali.
- Batas waktu pengembalian maksimal tujuh hari.
- Pengembalian sebagian diperbolehkan.
- Alat dengan kondisi baik dapat kembali tersedia.
- Alat rusak ringan atau rusak berat tidak dihitung sebagai alat tersedia.
- Mahasiswa dan alat yang masih tercatat dalam transaksi aktif tidak boleh dihapus.

---

## 🚀 Cara Menjalankan Program

Pastikan Python sudah terpasang pada perangkat.

### 1. Clone Repository

```bash
git clone https://github.com/zzevanya/Proyek1_PraktikumPemro.git
```

### 2. Masuk ke Folder Project

```bash
cd Proyek1_PraktikumPemro
```

### 3. Jalankan Program

```bash
python main.py
```

Program akan menampilkan menu utama yang dapat digunakan untuk mengelola data mahasiswa, peralatan, peminjaman, dan pengembalian.

---

## 🛠️ Konsep Pemrograman yang Digunakan

Konsep yang diterapkan dalam pengembangan program meliputi:

- **Object-Oriented Programming (OOP)** → Mengorganisasi program menggunakan class dan objek.
- **Encapsulation** → Mengelola atribut serta akses dan perubahan data melalui method.
- **Class dan Object** → Merepresentasikan mahasiswa, alat, transaksi, dan komponen pengelolaan sistem.
- **Enum** → Menentukan pilihan status transaksi dan kondisi alat secara konsisten.
- **List** → Menyimpan kumpulan data, detail peminjaman, dan log aktivitas.
- **Dictionary** → Mengelola data berdasarkan kunci seperti NIM, kode alat, dan ID transaksi.
- **Modular Programming** → Memisahkan implementasi ke beberapa file Python berdasarkan tanggung jawabnya.
- **Git dan GitHub** → Mendukung pengembangan kolaboratif, pencatatan perubahan, dan integrasi kode.

---

## 📌 Menu Program

Menu utama dirancang untuk menyediakan fitur berikut:

```text
1. Kelola Data Mahasiswa
2. Kelola Data Alat
3. Buat Transaksi Peminjaman
4. Tampilkan Transaksi
5. Proses Pengembalian Alat
6. Cari Transaksi Berdasarkan Mahasiswa
7. Tampilkan Alat Tersedia
8. Tampilkan Alat yang Sedang Dipinjam
9. Tampilkan Alat Rusak
10. Tampilkan Riwayat Peminjaman Mahasiswa
11. Keluar
```

---

## 🧪 Pengujian Program

Pengujian dilakukan untuk memastikan bahwa fitur dan aturan bisnis berjalan sesuai kebutuhan, meliputi:

- Penambahan data mahasiswa dan peralatan.
- Peminjaman beberapa alat dalam satu transaksi.
- Penolakan peminjaman alat yang tidak tersedia.
- Pengembalian sebagian alat.
- Pembaruan kondisi dan ketersediaan alat.
- Penolakan penghapusan mahasiswa yang masih memiliki transaksi aktif.
- Pencatatan aktivitas sistem.

---

## 📚 Dokumentasi Proyek

Dokumentasi pengembangan meliputi:

- UML Class Diagram setiap anggota.
- UML Class Diagram final kelompok.
- Dokumen Keputusan Desain.
- Dokumentasi source code dan repository GitHub.
- Dokumen Hasil Pengujian.
- Dokumen Cross-Group Code Review.
- Dokumen Refleksi dan Rencana Perbaikan.

---

**Proyek I — Praktikum Pemrograman Dasar**  
Sistem Pengelolaan Peminjaman Peralatan Laboratorium  
Kelompok 2