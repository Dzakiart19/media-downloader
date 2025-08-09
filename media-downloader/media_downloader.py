#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from modules.ui import UI
from modules.downloader import Downloader
from modules.history import History
from modules.config import Config

class DzeckDownloader:
    def __init__(self):
        self.config = Config()
        self.ui = UI(self.config)
        self.history = History()
        self.downloader = Downloader(self.config, self.ui)
        self.queue = []

    def run(self):
        while True:
            self.ui.display_header()
            choice = self.ui.display_main_menu()

            if choice == '1':
                self.download_new()
            elif choice == '2':
                self.show_queue()
            elif choice == '3':
                self.show_history()
            elif choice == '4':
                self.settings_menu()
            elif choice == '5' or choice == '6':
                self.handle_adult_content(choice)
            elif choice == '7':
                self.ui.print_message("Terima kasih telah menggunakan Dzeck!", style="info")
                sys.exit(0)
            else:
                self.ui.print_message("Pilihan tidak valid, silakan coba lagi.", style="error")
                self.ui.pause()

    def download_new(self, use_cookies=False):
        cookies_file = None
        if use_cookies:
            self.ui.print_message(
                "Mode Download dengan Cookies. Ini memungkinkan akses ke konten yang memerlukan login.\n"
                "Anda perlu menyediakan file 'cookies.txt' dari browser Anda.\n"
                "Ekstensi browser seperti 'Get cookies.txt' dapat membantu mengekspor file ini.",
                "info"
            )
            cookies_file_input = self.ui.get_input("Masukkan path lengkap ke file cookies.txt (biarkan kosong untuk batal):")
            if cookies_file_input and os.path.exists(cookies_file_input):
                cookies_file = cookies_file_input
            elif cookies_file_input:
                self.ui.print_message("File cookies tidak ditemukan di path tersebut. Melanjutkan tanpa cookies.", "warning")

        urls_input = self.ui.get_input("Masukkan satu atau beberapa URL (pisahkan dengan spasi):")
        if not urls_input:
            return

        urls = urls_input.split()

        for url in urls:
            self.ui.print_message(f"Memproses URL: {url}", style="info")

            # Simple validation
            if not url.startswith(('http://', 'https://')):
                self.ui.print_message(f"URL tidak valid: {url}", style="error")
                continue

            # Preview metadata
            metadata = self.downloader.get_metadata(url)
            if not metadata:
                continue

            self.ui.display_metadata_preview(metadata)

            confirm = self.ui.get_input("Download file ini? (y/n): ", lower=True)
            if confirm == 'y':
                quality = self.ui.display_quality_menu(metadata.get('formats', []))
                if quality:
                    self.ui.print_legal_notice()
                    self.downloader.download(url, quality, cookies_file=cookies_file)
                    self.history.add_entry(
                        url=metadata.get('webpage_url'),
                        title=metadata.get('title'),
                        platform=metadata.get('extractor_key'),
                        quality=quality
                    )
            else:
                self.ui.print_message("Download dibatalkan.", style="warning")
        self.ui.pause()


    def show_queue(self):
        self.ui.print_message("Fitur antrian belum diimplementasikan sepenuhnya.", style="warning")
        # In a full implementation, this would show self.queue and manage it.
        self.ui.pause()

    def show_history(self):
        while True:
            history_entries = self.history.get_all()
            choice = self.ui.display_history(history_entries)

            if choice.lower() == 'c':
                confirm = self.ui.get_input("Anda yakin ingin menghapus semua riwayat? (y/n): ", lower=True)
                if confirm == 'y':
                    self.history.clear_all()
                    self.ui.print_message("Riwayat telah dihapus.", style="success")
            elif choice.lower() == 'o':
                download_path = self.config.get('download_path')
                self.ui.print_message(f"Mencoba membuka folder: {download_path}", style="info")
                try:
                    # Termux command to open a directory
                    os.system(f'termux-open "{download_path}"')
                except Exception as e:
                    self.ui.print_message(f"Gagal membuka folder: {e}", style="error")
            elif choice.lower() == 'b':
                break
            else:
                self.ui.print_message("Pilihan tidak valid.", style="error")
            self.ui.pause()


    def settings_menu(self):
        while True:
            current_config = self.config.get_all()
            choice = self.ui.display_settings_menu(current_config)

            if choice == '1':
                new_path = self.ui.get_input(f"Path download saat ini: {current_config['download_path']}\nMasukkan path baru: ")
                # Basic validation for Termux storage
                if new_path.startswith('/data/data/com.termux/files/home/storage/'):
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)
                    self.config.set('download_path', new_path)
                    self.ui.print_message("Path download berhasil diubah.", style="success")
                else:
                    self.ui.print_message("Path tidak valid. Harus berada di dalam storage Termux.", style="error")
            elif choice == '2':
                new_format = self.ui.get_input(f"Format nama file saat ini: {current_config['filename_template']}\nMasukkan format baru: ")
                self.config.set('filename_template', new_format)
                self.ui.print_message("Format nama file berhasil diubah.", style="success")
            elif choice == '3':
                current_theme = self.config.get('theme')
                new_theme = 'dark' if current_theme == 'light' else 'light'
                self.config.set('theme', new_theme)
                self.ui.update_theme()
                self.ui.print_message(f"Tema diubah ke {new_theme}.", style="success")
            elif choice == '4':
                new_ua = self.ui.get_input(f"User-Agent saat ini: {current_config['user_agent']}\nMasukkan User-Agent baru (biarkan kosong untuk batal): ")
                if new_ua:
                    self.config.set('user_agent', new_ua)
                    self.ui.print_message("User-Agent berhasil diubah.", style="success")
            elif choice == '5':
                current_status = self.config.get('check_certificate')
                self.config.set('check_certificate', not current_status)
                new_status_text = "diaktifkan" if not current_status else "dinonaktifkan"
                self.ui.print_message(f"Verifikasi sertifikat SSL telah {new_status_text}.", style="success")
                if new_status_text == "dinonaktifkan":
                    self.ui.print_message("PERINGATAN: Menonaktifkan ini adalah risiko keamanan.", style="warning")
            elif choice == '6':
                break
            else:
                self.ui.print_message("Pilihan tidak valid.", style="error")
            self.ui.pause()

    def handle_adult_content(self, choice):
        self.ui.display_adult_warning()
        confirm = self.ui.get_input("Apakah Anda berusia 18 tahun atau lebih dan setuju dengan persyaratan di atas? (y/n): ", lower=True)
        if confirm == 'y':
            self.ui.print_message("Persetujuan diterima untuk sesi ini.", style="info")
            if choice == '5':
                self.ui.print_message("Mode Dewasa Standar: Menggunakan User-Agent khusus.", "info")
                self.download_new(use_cookies=False)
            elif choice == '6':
                self.ui.print_message("Mode Dewasa Lanjutan: Menggunakan file Cookies.", "info")
                self.download_new(use_cookies=True)
        else:
            self.ui.print_message("Anda harus menyetujui persyaratan untuk melanjutkan.", style="warning")
        self.ui.pause()


if __name__ == '__main__':
    try:
        app = DzeckDownloader()
        app.run()
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh pengguna. Keluar.")
        sys.exit(0)
    except Exception as e:
        print(f"\nTerjadi error yang tidak terduga: {e}")
        # Optionally log to a file
        with open("error.log", "a") as f:
            import traceback
            f.write(f"--- ERROR ---\n")
            f.write(str(e) + "\n")
            f.write(traceback.format_exc())
            f.write("--------------\n\n")
        sys.exit(1)
