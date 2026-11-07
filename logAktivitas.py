from datetime import datetime


class LogAktivitas:
    def __init__(self, penyimpanan=None):
        self._penyimpanan = penyimpanan
        self.daftar_log = penyimpanan.baca_baris("log.txt") if penyimpanan else []

    def catat(self, pesan):
        waktu = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
        baris = f"[{waktu}] {pesan}"
        self.daftar_log.append(baris)
        if self._penyimpanan is not None:
            self._penyimpanan.tambah_baris("log.txt", baris)

    def tampilkan(self):
        if not self.daftar_log:
            print("Belum ada aktivitas.")
            return

        for log in self.daftar_log:
            print(log)