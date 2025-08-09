# Media Downloader v1.0.0

Sebuah skrip downloader media multi-platform yang interaktif dan kaya fitur untuk Termux. Dibuat untuk memberikan pengalaman pengguna yang lebih baik daripada skrip CLI dasar.

**Dibuat oleh:** AI Agent Jules

**Peringatan Legal:** Skrip ini ditujukan untuk penggunaan pribadi dan legal. Pastikan Anda memiliki hak untuk mengunduh konten dari URL yang Anda masukkan. Mengunduh materi berhak cipta tanpa izin adalah ilegal. Pengguna bertanggung jawab penuh atas tindakan mereka.

---

## Fitur Utama

- **UI Interaktif:** Menu berbasis teks dengan warna, animasi, dan header ASCII art.
- **Multi-Platform:** Ditenagai oleh `yt-dlp`, mendukung YouTube, TikTok, Instagram, Facebook, dan banyak lagi.
- **Manajemen Kualitas:** Pilih kualitas video (1080p, 720p) atau unduh audio saja (mp3).
- **Download Cepat:** Menggunakan `aria2c` untuk unduhan multi-threaded yang dipercepat.
- **Riwayat Download:** Menyimpan catatan unduhan Anda dalam database SQLite lokal.
- **Kustomisasi:**
    - Atur folder penyimpanan kustom.
    - Tentukan format nama file Anda sendiri.
    - Ganti antara tema warna terang dan gelap.
- **Penanganan Konten Dewasa:** Gerbang usia (age-gate) untuk mengakses konten yang dibatasi usia, dengan persetujuan per sesi.
- **Notifikasi:** Memberi tahu Anda saat unduhan selesai menggunakan `termux-api`.
- **Metadata:** Menyimpan file `.json` di samping media Anda dengan detail lengkap.

## Prasyarat

- **Termux:** Skrip ini dirancang khusus untuk lingkungan Termux di Android.
- **Termux:API:** Aplikasi pendamping Termux:API harus diinstal dari F-Droid atau Play Store agar notifikasi dan pembukaan file berfungsi dengan benar.
- **Koneksi Internet:** Tentu saja :)

---

## Instalasi (Otomatis)

Proses instalasi sangat mudah. Cukup jalankan skrip `install.sh`.

1.  **Buka Termux** di perangkat Android Anda.

2.  **Izinkan Akses Penyimpanan:**
    Jalankan perintah ini terlebih dahulu untuk memberikan izin Termux mengakses penyimpanan internal Anda.
    ```bash
    termux-setup-storage
    ```
    Setujui permintaan izin yang muncul.

3.  **Kloning Repositori (Jika dari Git) atau Salin File:**
    Jika Anda mendapatkan ini dari git, kloning repositori. Jika Anda menyalin file secara manual, pastikan seluruh folder `media-downloader` ada di direktori home Termux Anda (`/data/data/com.termux/files/home`).

4.  **Jalankan Skrip Instalasi:**
    Navigasikan ke direktori proyek dan jalankan `install.sh`.
    ```bash
    cd media-downloader
    bash install.sh
    ```
    Skrip akan secara otomatis:
    - Memperbarui paket Termux Anda.
    - Menginstal `python`, `ffmpeg`, `aria2c`, dan `termux-api`.
    - Menginstal pustaka Python `yt-dlp`.
    - Membuat skrip `media-downloader` dapat dieksekusi.
    - Membuat symlink agar Anda dapat menjalankan skrip dari direktori mana pun.

---

## Cara Menjalankan

Setelah instalasi, Anda dapat menjalankan skrip dari mana saja di Termux dengan mengetik:
```bash
media-downloader
```
Atau, jika Anda berada di dalam folder proyek:
```bash
./media-downloader
```

### Alur Kerja Penggunaan

1.  **Menu Utama:** Anda akan disambut dengan menu utama.
2.  **Download Baru:** Pilih opsi '1'. Tempelkan URL video (misalnya, dari YouTube).
3.  **Pratinjau Metadata:** Skrip akan menampilkan judul, uploader, dan durasi.
4.  **Konfirmasi & Pilih Kualitas:** Konfirmasi unduhan (y) dan pilih kualitas yang Anda inginkan.
5.  **Tonton Prosesnya:** Progress bar akan menunjukkan kemajuan unduhan.
6.  **Selesai:** Notifikasi akan muncul saat selesai. File Anda akan berada di folder unduhan yang dikonfigurasi (default: `~/storage/downloads/MediaDownloader`).

---

## Konfigurasi

Saat pertama kali dijalankan, skrip akan membuat file konfigurasi di `~/.media_downloader/config.json`. Anda dapat mengeditnya secara manual atau melalui menu **Pengaturan** di dalam aplikasi.

-   `download_path`: Lokasi penyimpanan file.
-   `filename_template`: Pola untuk nama file. Lihat `config.json.example` untuk detailnya.
-   `theme`: Tema warna (`dark` atau `light`).

---

## Pemecahan Masalah (Troubleshooting)

-   **Error "Permission Denied" saat menyimpan file:**
    Pastikan Anda telah menjalankan `termux-setup-storage` dan memberikan izin. Juga, periksa kembali `download_path` di pengaturan Anda untuk memastikan itu adalah lokasi yang valid dan dapat ditulis (misalnya, di bawah `~/storage/`).

-   **Perintah `media-downloader` tidak ditemukan:**
    Instalasi mungkin gagal membuat symlink. Coba jalankan skrip langsung dari foldernya: `cd ~/media-downloader && ./media-downloader`.

-   **Download sangat lambat atau gagal:**
    Beberapa situs (terutama YouTube) membatasi kecepatan unduh. Skrip menggunakan `aria2c` untuk mempercepat, tetapi mungkin tidak selalu efektif. Coba kualitas yang berbeda. Jika terus gagal, situs tersebut mungkin telah mengubah cara mereka menyajikan konten. `yt-dlp` sering diperbarui untuk mengatasi ini, jadi pastikan Anda memiliki versi terbaru (`pip install --upgrade yt-dlp`).

-   **Notifikasi tidak muncul:**
    Pastikan Anda telah menginstal aplikasi **Termux:API** dari Play Store/F-Droid dan paket `termux-api` di dalam Termux (`pkg install termux-api`).

---

## Contoh Sesi CLI

**Sesi Download YouTube:**
```
$ media-downloader

[... Header ASCII Art ...]

MENU UTAMA
  1. Download Baru
  ...
  7. Keluar
Pilih opsi: 1

Masukkan satu atau beberapa URL (pisahkan dengan spasi): https://www.youtube.com/watch?v=dQw4w9WgXcQ

[*] Memproses URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
[*] Mengambil metadata...
[+] Metadata Ditemukan:
  Judul: Rick Astley - Never Gonna Give You Up (Official Music Video)
  Uploader: Rick Astley
  Durasi: 00:03:32
  Platform: youtube

Download file ini? (y/n): y

[*] Pilih Kualitas Download:
  best. Kualitas terbaik (video+audio)
  1080p. Video 1080p (jika tersedia)
  720p. Video 720p
  audio. Hanya audio (format terbaik)
Masukkan pilihan kualitas: best

[*] Pastikan Anda memiliki hak untuk mengunduh konten ini...
[*] Mempersiapkan download untuk kualitas 'best'...
  [██████████████████████████████] 100.0% | 12.34 MB/s | ETA: 0s
[+] Download selesai: /data/data/com.termux/files/home/storage/downloads/MediaDownloader/youtube_Rick Astley - Never Gonna Give You Up (Official Music Video)_dQw4w9WgXcQ.mp4

Tekan Enter untuk kembali...
```

**Sesi "Konten Dewasa":**
```
$ media-downloader

[... Header ASCII Art ...]

MENU UTAMA
  ...
  5. Konten Dewasa 1
  ...
Pilih opsi: 5

[-] PERINGATAN KONTEN DEWASA & LEGAL
[*] Anda akan mengakses fitur yang mungkin mengarah pada konten yang dibatasi usia...
[-] PENGGUNA BERTANGGUNG JAWAB PENUH...

Apakah Anda berusia 18 tahun atau lebih dan setuju dengan persyaratan di atas? (y/n): y

[*] Persetujuan diterima untuk sesi ini.
[*] Fitur ini adalah placeholder. Silakan masukkan URL seperti biasa.

Masukkan satu atau beberapa URL (pisahkan dengan spasi): ...
```
