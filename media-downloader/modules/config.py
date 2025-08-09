import json
import os

class Config:
    def __init__(self, config_path='~/.media_downloader/config.json'):
        self.config_file = os.path.expanduser(config_path)
        self.config_dir = os.path.dirname(self.config_file)

        # Default storage path for Termux
        default_download_path = os.path.expanduser('~/storage/downloads/MediaDownloader')

        self.defaults = {
            'download_path': default_download_path,
            'filename_template': '{platform}_{title_short}_{id}',
            'theme': 'dark', # 'dark' or 'light'
            'show_legal_notice': True,
            'default_quality': 'best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'check_certificate': False, # Security risk: set to True to enforce SSL checks
        }

        self._load_config()
        self._ensure_download_path_exists()

    def _load_config(self):
        """Loads config from file, or creates it if it doesn't exist."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                # Merge user config with defaults, user config takes precedence
                self.config = {**self.defaults, **user_config}
            except json.JSONDecodeError:
                # If config is corrupted, load defaults
                self.config = self.defaults
        else:
            self.config = self.defaults

        self._save_config() # Save to ensure all keys are present in file

    def _save_config(self):
        """Saves the current configuration to the file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def _ensure_download_path_exists(self):
        """Creates the download directory if it doesn't exist."""
        path = self.get('download_path')
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                # This can happen on Android if storage permission is not granted
                print(f"Warning: Could not create download directory: {path}")
                print(f"Error: {e}")
                print("Please ensure you have granted storage permission to Termux.")

    def get(self, key, default=None):
        """Gets a config value by key."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Sets a config value and saves it."""
        self.config[key] = value
        self._save_config()
        # Special handling for path changes
        if key == 'download_path':
            self._ensure_download_path_exists()

    def get_all(self):
        """Returns the entire config dictionary."""
        return self.config.copy()
