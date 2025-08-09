import sqlite3
import os
from datetime import datetime

class History:
    def __init__(self, db_path='~/.media_downloader'):
        # Expand user path and create directory if it doesn't exist
        self.db_dir = os.path.expanduser(db_path)
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.db_file = os.path.join(self.db_dir, 'history.db')
        self._create_table()

    def _get_connection(self):
        """Returns a new database connection."""
        return sqlite3.connect(self.db_file)

    def _create_table(self):
        """Creates the history table if it doesn't exist."""
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT NOT NULL,
                        title TEXT,
                        platform TEXT,
                        quality TEXT,
                        downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        finally:
            conn.close()

    def add_entry(self, url, title, platform, quality):
        """Adds a new download entry to the history."""
        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    "INSERT INTO history (url, title, platform, quality, downloaded_at) VALUES (?, ?, ?, ?, ?)",
                    (url, title, platform, quality, datetime.now())
                )
        finally:
            conn.close()

    def get_all(self, limit=50):
        """Retrieves all history entries, most recent first."""
        conn = self._get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM history ORDER BY downloaded_at DESC LIMIT ?", (limit,))
                return cursor.fetchall()
        finally:
            conn.close()

    def clear_all(self):
        """Clears all entries from the history table."""
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM history")
                # Also reset the autoincrement counter for a clean slate
                conn.execute("DELETE FROM sqlite_sequence WHERE name='history'")
        finally:
            conn.close()
