import yt_dlp
import os
import json
from datetime import datetime

class Downloader:
    def __init__(self, config, ui):
        self.config = config
        self.ui = ui

    def _get_yt_dlp_options(self, quality, cookies_file=None, extra_opts=None):
        """Constructs the options dictionary for yt-dlp."""
        download_path = self.config.get('download_path')
        filename_template = self.config.get('filename_template')

        # Ensure the filename template has placeholders for extension
        if not '%(ext)s' in filename_template:
            filename_template += '.%(ext)s'

        output_template = os.path.join(download_path, filename_template)

        # Format selection
        format_string = "best"
        if quality == '1080p':
            format_string = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == '720p':
            format_string = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == 'audio':
            format_string = 'bestaudio/best'

        user_agent = self.config.get('user_agent')

        opts = {
            'format': format_string,
            'outtmpl': output_template,
            'progress_hooks': [self.ui.download_progress_hook],
            'writemetadata': True,
            'external_downloader': 'aria2c',
            'http_headers': {
                'User-Agent': user_agent,
                'Referer': 'https://www.google.com' # Adding a generic referer can also help
            },
            'external_downloader_args': ['-x', '16', '-s', '16', '-k', '1M'],
            'postprocessors': [{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
            'quiet': True, # Suppress yt-dlp's own console output
            'noprogress': True, # We use our own progress hook
            'noplaylist': True, # Process only single video if playlist URL is given
        }

        if quality == 'audio':
            opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })

        if cookies_file and os.path.exists(cookies_file):
            opts['cookiefile'] = cookies_file

        if extra_opts and isinstance(extra_opts, dict):
            opts.update(extra_opts)

        return opts

    def get_metadata(self, url):
        """Fetches video metadata without downloading."""
        self.ui.print_message("Mengambil metadata...", "info")
        opts = {
            'quiet': True,
            'extract_flat': 'in_playlist',
            'skip_download': True,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                # Save metadata to a temporary file for inspection if needed
                # with open('temp_metadata.json', 'w') as f:
                #     json.dump(info_dict, f, indent=4)
                return info_dict
        except yt_dlp.utils.DownloadError as e:
            self.ui.print_message(f"Gagal mengambil metadata: {e}", "error")
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
            opts = self._get_yt_dlp_options(quality, cookies_file=cookies_file)
            with yt_dlp.YoutubeDL(opts) as ydl:
                # The actual download happens here
                ydl.download([url])
                # The success message is handled by the progress hook
        except yt_dlp.utils.DownloadError as e:
            self.ui.print_message(f"Download gagal: {e}", "error")
        except Exception as e:
            self.ui.print_message(f"Terjadi error tidak terduga saat download: {e}", "error")
