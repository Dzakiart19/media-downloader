import os
import sys
import time
import textwrap

class UI:
    def __init__(self, config):
        self.config = config
        self.update_theme()

    def update_theme(self):
        theme = self.config.get('theme', 'dark')
        if theme == 'dark':
            self.colors = {
                'header': '\033[95m',  # Magenta
                'primary': '\033[96m', # Cyan
                'secondary': '\033[94m',# Blue
                'success': '\033[92m', # Green
                'warning': '\033[93m', # Yellow
                'error': '\033[91m',   # Red
                'bold': '\033[1m',
                'end': '\033[0m',
            }
        else: # light theme
            self.colors = {
                'header': '\033[35m',
                'primary': '\033[36m',
                'secondary': '\033[34m',
                'success': '\033[32m',
                'warning': '\033[33m',
                'error': '\033[31m',
                'bold': '\033[1m',
                'end': '\033[0m',
            }

    def c(self, style):
        return self.colors.get(style, '')

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def typing_effect(self, text, delay=0.01):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def display_header(self):
        self.clear_screen()
        header_lines = [
            f"{self.c('header')}",
            "  ____   ______ ______  _   _  _  __",
            " |  _ \\ |__  __|  ____|| \\ | || |/ /",
            " | |_) |   | |  | |__   |  \\| || ' / ",
            " |  _ <    | |  |  __|  | . ` ||  <  ",
            " | |_) |   | |  | |____ | |\\  || . \\ ",
            " |____/    |_|  |______||_| \\_||_|\\_\\",
            f"{self.c('end')}",
            f"{self.c('primary')}                        v1.0.0 - by DZECK{self.c('end')}"
        ]
        print("\n".join(header_lines))

    def display_main_menu(self):
        print(f"\n{self.c('bold')}{self.c('primary')}MENU UTAMA{self.c('end')}")
        menu_items = {
            "1": "Download Baru",
            "2": "Lihat Antrian",
            "3": "Riwayat Download",
            "4": "Pengaturan",
            "5": "Konten Dewasa",
            "6": "Keluar"
        }
        for key, value in menu_items.items():
            print(f"  {self.c('warning')}{key}{self.c('end')}. {self.c('secondary')}{value}{self.c('end')}")

        return self.get_input("Pilih opsi: ")

    def get_input(self, prompt, lower=False):
        full_prompt = f"\n{self.c('primary')}{prompt}{self.c('end')} "
        response = input(full_prompt)
        return response.lower().strip() if lower else response.strip()

    def print_message(self, message, style="info", wrap=True):
        color = self.c(style)
        if style == "info":
            prefix = "[*]"
        elif style == "success":
            prefix = "[+]"
        elif style == "warning":
            prefix = "[!]"
        elif style == "error":
            prefix = "[-]"
        else:
            prefix = "[>]"

        if wrap:
            wrapped_message = textwrap.fill(message, width=80)
            print(f"{color}{prefix} {wrapped_message}{self.c('end')}")
        else:
            print(f"{color}{prefix} {message}{self.c('end')}")

    def pause(self):
        input(f"\n{self.c('secondary')}Tekan Enter untuk kembali...{self.c('end')}")

    def display_metadata_preview(self, metadata):
        self.print_message("Metadata Ditemukan:", "success")
        title = metadata.get('title', 'N/A')
        uploader = metadata.get('uploader', 'N/A')
        duration = time.strftime('%H:%M:%S', time.gmtime(metadata.get('duration', 0)))

        print(f"  {self.c('bold')}Judul:{self.c('end')} {title}")
        print(f"  {self.c('bold')}Uploader:{self.c('end')} {uploader}")
        print(f"  {self.c('bold')}Durasi:{self.c('end')} {duration}")
        print(f"  {self.c('bold')}Platform:{self.c('end')} {metadata.get('extractor_key', 'N/A')}")

    def display_quality_menu(self, formats):
        self.print_message("Pilih Kualitas Download:", "info")
        print(f"  {self.c('warning')}best{self.c('end')}. {self.c('secondary')}Kualitas terbaik (video+audio){self.c('end')}")
        print(f"  {self.c('warning')}1080p{self.c('end')}. {self.c('secondary')}Video 1080p (jika tersedia){self.c('end')}")
        print(f"  {self.c('warning')}720p{self.c('end')}. {self.c('secondary')}Video 720p{self.c('end')}")
        print(f"  {self.c('warning')}audio{self.c('end')}. {self.c('secondary')}Hanya audio (format terbaik){self.c('end')}")

        return self.get_input("Masukkan pilihan kualitas: ", lower=True)

    def print_legal_notice(self):
        self.print_message(
            "Pastikan Anda memiliki hak untuk mengunduh konten ini. "
            "Skrip ini tidak ditujukan untuk membajak atau membagikan materi berhak cipta tanpa izin.",
            "warning"
        )

    def display_adult_warning(self):
        self.clear_screen()
        self.print_message("PERINGATAN KONTEN DEWASA & LEGAL", "error")
        self.print_message(
            "Anda akan mengakses fitur yang mungkin mengarah pada konten yang dibatasi usia (konten dewasa). "
            "Dengan melanjutkan, Anda mengonfirmasi bahwa Anda berusia 18 tahun atau lebih (atau usia legal di wilayah Anda).",
            "warning"
        )
        self.print_message(
            "PENGGUNA BERTANGGUNG JAWAB PENUH atas semua aktivitas yang dilakukan menggunakan skrip ini. "
            "Pengembang tidak bertanggung jawab atas penyalahgunaan. "
            "Jangan gunakan skrip ini untuk aktivitas ilegal.",
            "error"
        )

    def display_history(self, entries):
        self.clear_screen()
        self.print_message("Riwayat Download", "header")
        if not entries:
            self.print_message("Riwayat kosong.", "info")
        else:
            for i, entry in enumerate(entries):
                print(f"  {self.c('warning')}{i+1}{self.c('end')}. "
                      f"{self.c('secondary')}{entry[2]}{self.c('end')} "
                      f"({self.c('primary')}{entry[3]}{self.c('end')}) - "
                      f"{self.c('success')}{entry[5]}{self.c('end')}")

        print("\n" + "-"*30)
        print(f"  {self.c('warning')}c{self.c('end')}. {self.c('secondary')}Clear Riwayat{self.c('end')}")
        print(f"  {self.c('warning')}o{self.c('end')}. {self.c('secondary')}Buka Folder Download{self.c('end')}")
        print(f"  {self.c('warning')}b{self.c('end')}. {self.c('secondary')}Kembali ke Menu Utama{self.c('end')}")
        return self.get_input("Pilih opsi: ", lower=True)

    def display_settings_menu(self, config_data):
        self.clear_screen()
        self.print_message("Pengaturan", "header")

        cert_status = "Aktif" if config_data.get('check_certificate') else "Nonaktif"
        settings = {
            "1": f"Ubah Path Download ({config_data.get('download_path')})",
            "2": f"Ubah Format Nama File ({config_data.get('filename_template')})",
            "3": f"Ganti Tema (Saat ini: {config_data.get('theme')})",
            "4": f"Ubah User-Agent",
            "5": f"Verifikasi Sertifikat SSL (Saat ini: {cert_status})",
            "6": "Kembali ke Menu Utama"
        }

        for key, value in settings.items():
            print(f"  {self.c('warning')}{key}{self.c('end')}. {self.c('secondary')}{value}{self.c('end')}")

        return self.get_input("Pilih opsi: ")

    def download_progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                percent = d['downloaded_bytes'] / total_bytes * 100
                speed = d.get('speed')
                eta = d.get('eta')

                speed_str = f"{speed/1024/1024:.2f} MB/s" if speed else "N/A"
                eta_str = f"{eta}s" if eta else "N/A"

                bar_length = 30
                filled_length = int(bar_length * percent / 100)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)

                sys.stdout.write(f"\r  {self.c('success')}[{bar}] {percent:.1f}% | {speed_str} | ETA: {eta_str}{self.c('end')}")
                sys.stdout.flush()

        elif d['status'] == 'finished':
            sys.stdout.write("\n") # New line after download completes
            self.print_message(f"Download selesai: {d['filename']}", "success")
            self.notify_user("Download Selesai", f"File '{os.path.basename(d['filename'])}' telah berhasil diunduh.")

        elif d['status'] == 'error':
            sys.stdout.write("\n")
            self.print_message("Terjadi error saat download.", "error")

    def notify_user(self, title, message):
        # Uses termux-api for native notifications
        if os.system('command -v termux-toast > /dev/null') == 0:
            os.system(f'termux-toast "{message}"')
        elif os.system('command -v termux-notification > /dev/null') == 0:
            os.system(f'termux-notification --title "{title}" --content "{message}"')
        else:
            # Fallback for non-termux env
            pass
