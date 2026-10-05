from datetime import datetime


class LogAktivitas:
    def __init__(self):
        self.daftar_log = []

    def catat(self, pesan):
        waktu = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
        self.daftar_log.append(f"[{waktu}] {pesan}")

    def tampilkan(self):
        if not self.daftar_log:
            print("Belum ada aktivitas.")
            return

        for log in self.daftar_log:
            print(log)