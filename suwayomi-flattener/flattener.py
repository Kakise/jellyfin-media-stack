import os
import shutil
import logging
import re
import time
import threading
import sqlite3
from pathlib import Path
from filelock import FileLock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Configuration
INPUT_DIR = Path(os.getenv("INPUT_DIR", "/input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/output"))
STATE_DIR = Path(os.getenv("STATE_DIR", "/state"))
LOCK_FILE = "/tmp/flattener.lock"
PROCESSED_DB_PATH = Path(os.getenv("PROCESSED_DB_PATH", STATE_DIR / "processed.db"))

CHAPTER_REGEX = re.compile(r'(?:Ch(?:apter)?|Chap)(?:[ ._-]*)(\d+(?:\.\d+)?)', re.IGNORECASE)

# --- Processed file DB logic (SQLite) ---
def init_db():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(PROCESSED_DB_PATH)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS processed_files (
                path TEXT PRIMARY KEY,
                mtime REAL
            )
        """)
    return conn

def is_file_processed(conn, path: Path) -> bool:
    mtime = path.stat().st_mtime
    result = conn.execute("SELECT mtime FROM processed_files WHERE path = ?", (str(path),)).fetchone()
    return result is not None and result[0] == mtime

def mark_file_processed(conn, path: Path):
    mtime = path.stat().st_mtime
    with conn:
        conn.execute(
            "REPLACE INTO processed_files (path, mtime) VALUES (?, ?)",
            (str(path), mtime)
        )

# --- Core flattening logic ---
def extract_chapter_number(filename: str) -> str:
    match = CHAPTER_REGEX.search(filename)
    return match.group(1) if match else None

def get_unique_filename(target_dir: Path, filename: str, parent_folder: str) -> Path:
    parent_path = target_dir / parent_folder
    new_file_path = parent_path / filename

    if new_file_path.exists():
        base, ext = new_file_path.stem, new_file_path.suffix
        counter = 1
        while (parent_path / f"{base} ({counter}){ext}").exists():
            counter += 1
        new_file_path = parent_path / f"{base} ({counter}){ext}"

    parent_path.mkdir(parents=True, exist_ok=True)
    return new_file_path

def flatten_single_cbz(cbz_path: Path, target_dir: Path, conn):
    if not cbz_path.exists() or cbz_path.suffix.lower() != ".cbz":
        return

    if is_file_processed(conn, cbz_path):
        logging.info(f"Skipping already processed: {cbz_path}")
        return

    parent_folder = cbz_path.parent.name
    chapter_number = extract_chapter_number(cbz_path.name)
    if not chapter_number:
        logging.warning(f"Could not extract chapter from {cbz_path.name}, skipping.")
        return

    new_filename = f"{parent_folder} #{chapter_number}.cbz"
    target_path = get_unique_filename(target_dir, new_filename, parent_folder)

    try:
        shutil.copy2(cbz_path, target_path)
        logging.info(f"Copied and renamed: {cbz_path} → {target_path}")
        mark_file_processed(conn, cbz_path)
    except Exception as e:
        logging.error(f"Failed to copy {cbz_path}: {e}")

def flatten_directory(source_dir: Path, target_dir: Path, conn):
    logging.info(f"Flattening directory: {source_dir}")
    for root, _, files in os.walk(source_dir):
        for file in files:
            source_path = Path(root) / file
            if source_path.suffix.lower() == ".cbz":
                flatten_single_cbz(source_path, target_dir, conn)

# --- Watchdog handler ---
class WatcherHandler(FileSystemEventHandler):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.recently_handled = {}
        self.lock = threading.Lock()
        self.debounce_seconds = 2

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".cbz"):
            return

        now = time.time()
        with self.lock:
            last_time = self.recently_handled.get(event.src_path, 0)
            if now - last_time < self.debounce_seconds:
                return
            self.recently_handled[event.src_path] = now

        logging.info(f"Detected change: {event.src_path}")
        with FileLock(LOCK_FILE):
            try:
                flatten_single_cbz(Path(event.src_path), OUTPUT_DIR, self.conn)
            except Exception as e:
                logging.error(f"Error processing {event.src_path}: {e}")

# --- Main loop ---
def start_watching(conn):
    event_handler = WatcherHandler(conn)
    observer = Observer()
    observer.schedule(event_handler, str(INPUT_DIR), recursive=True)
    observer.start()
    logging.info("Watching for changes in the source folder...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    logging.info("Starting Suwayomi flattener...")

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = init_db()

    with FileLock(LOCK_FILE):
        flatten_directory(INPUT_DIR, OUTPUT_DIR, conn)

    start_watching(conn)

if __name__ == "__main__":
    main()
