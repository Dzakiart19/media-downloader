import yt_dlp
import os
import json
from datetime import datetime
from urllib.parse import urlparse

class Downloader:
    def __init__(self, config, ui):
        self.config = config
        self.ui = ui

    def _build_headers(self, url: str) -> dict:
        parsed = urlparse(url)
        referer = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else 'https://www.google.com'
        return {
            'User-Agent': self.config.get('user_agent'),
            'Referer': referer,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def _convert_filename_template(self, template: str) -> str:
        """Converts custom placeholder template to yt-dlp outtmpl.
        Supported placeholders: {platform}, {title}, {title_short}, {id}
        """
        result = template
        result = result.replace('{platform}', '%(extractor_key)s')
        result = result.replace('{title_short}', '%(title).50B')
        result = result.replace('{title}', '%(title)s')
        result = result.replace('{id}', '%(id)s')
        if '%(ext)s' not in result:
            result += '.%(ext)s'
        return result

    def _get_yt_dlp_options(self, quality, cookies_file=None, extra_opts=None):
        """Constructs the options dictionary for yt-dlp."""
        download_path = self.config.get('download_path')
        filename_template = self.config.get('filename_template')

        # Convert user template to yt-dlp's outtmpl format
        output_template = os.path.join(download_path, self._convert_filename_template(filename_template))

        # Format selection
        format_string = "best"
        if quality == '1080p':
            format_string = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == '720p':
            format_string = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == 'audio':
            format_string = 'bestaudio/best'

        opts = {
            'format': format_string,
            'outtmpl': output_template,
            'progress_hooks': [self.ui.download_progress_hook],
            'writemetadata': True,
            'external_downloader': 'aria2c',
            # network robustness
            'retries': 10,
            'fragment_retries': 10,
            'socket_timeout': 30,
            'http_chunk_size': 1048576,
            'concurrent_fragment_downloads': 1,
            'external_downloader_args': ['-x', '16', '-s', '16', '-k', '1M'],
            'postprocessors': [{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
            'quiet': True, # Suppress yt-dlp's own console output
            'noprogress': True, # We use our own progress hook
            'noplaylist': True, # Process only single video if playlist URL is given
        }

        proxy = self.config.get('proxy')
        if proxy:
            opts['proxy'] = proxy

        if quality == 'audio':
            opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })

        if cookies_file and os.path.exists(cookies_file):
            opts['cookiefile'] = cookies_file

        # Add the no-check-certificate option based on config
        if not self.config.get('check_certificate', False):
            opts['nocheckcertificate'] = True

        if extra_opts and isinstance(extra_opts, dict):
            opts.update(extra_opts)

        return opts

    def get_metadata(self, url):
        """Fetches video metadata without downloading."""
        self.ui.print_message("Mengambil metadata...", "info", wrap=False)
        opts = {
            'quiet': True,
            'extract_flat': 'in_playlist',
            'skip_download': True,
            'noplaylist': True,
            'http_headers': self._build_headers(url),
        }
        if not self.config.get('check_certificate', False):
            opts['nocheckcertificate'] = True
        proxy = self.config.get('proxy')
        if proxy:
            opts['proxy'] = proxy
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                # Save metadata to a temporary file for inspection if needed
                # with open('temp_metadata.json', 'w') as f:
                #     json.dump(info_dict, f, indent=4)
                return info_dict
        except yt_dlp.utils.DownloadError as e:
            self.ui.print_message(f"Gagal mengambil metadata: {e}", "error")
            if 'Connection reset by peer' in str(e) and not self.config.get('proxy'):
                self.ui.print_message("Situs mungkin memblokir koneksi langsung. Coba atur Proxy di menu Pengaturan.", "warning")
            return None
        except Exception as e:
            self.ui.print_message(f"Terjadi error tidak terduga saat mengambil metadata: {e}", "error")
            return None

    def download(self, url, quality, cookies_file=None):
        """Downloads the video with the specified quality."""
        self.ui.print_message(f"Mempersiapkan download untuk kualitas '{quality}'...", "info")
        if cookies_file:
            self.ui.print_message("Menggunakan file cookies...", "info")

        try:
            # Update headers to match target domain for better compatibility with adult sites
            extra_opts = {
                'http_headers': self._build_headers(url)
            }
            opts = self._get_yt_dlp_options(quality, cookies_file=cookies_file, extra_opts=extra_opts)
            with yt_dlp.YoutubeDL(opts) as ydl:
                # The actual download happens here
                ydl.download([url])
                # The success message is handled by the progress hook
        except yt_dlp.utils.DownloadError as e:
            self.ui.print_message(f"Download gagal: {e}", "error")
            if 'Connection reset by peer' in str(e) and not self.config.get('proxy'):
                self.ui.print_message("Situs mungkin memblokir koneksi langsung. Coba atur Proxy di menu Pengaturan.", "warning")
        except Exception as e:
            self.ui.print_message(f"Terjadi error tidak terduga saat download: {e}", "error")
