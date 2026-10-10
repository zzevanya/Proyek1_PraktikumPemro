from alatManager import AlatManager
from logAktivitas import LogAktivitas
from Kategori import KategoriAlat


logger = LogAktivitas()
manager = AlatManager(logger)

data_dummy = [
    ("A001", "Laptop", KategoriAlat.ELEKTRONIK),
    ("A002", "Router MikroTik", KategoriAlat.ELEKTRONIK),
    ("A003", "Switch Jaringan", KategoriAlat.ELEKTRONIK),
    ("A004", "Kabel LAN", KategoriAlat.NON_ELEKTRONIK),
    ("A005", "Tripod Kamera", KategoriAlat.NON_ELEKTRONIK),
    ("A006", "Obeng Set", KategoriAlat.PERKAKAS),
    ("A007", "Tang Potong", KategoriAlat.PERKAKAS),
    ("A008", "Alkohol 70%", KategoriAlat.BAHAN_KIMIA),
]

for kode, nama, kategori in data_dummy:
    berhasil = manager.tambah_alat(kode, nama, kategori)

    if berhasil:
        print(f"Berhasil menambahkan {nama}")
    else:
        print(f"Gagal menambahkan {nama}")

print("\n=== DAFTAR KATEGORI ===")
for kategori in manager.tampilkan_kategori_alat():
    print("-", kategori.value)

print("\n=== SEMUA ALAT ===")
for kode, nama, kategori in data_dummy:
    alat = manager.cari_alat(kode)

    if alat is not None:
        print(alat)

# Cari berdasarkan kategori
print("\n=== ALAT ELEKTRONIK ===")
hasil = manager.cari_alat_berdasarkan_kategori(
    KategoriAlat.ELEKTRONIK
)

for alat in hasil:
    print(alat)

print("\n=== LOG AKTIVITAS ===")
logger.tampilkan()