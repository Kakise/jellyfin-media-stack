import os
import shutil
import logging
import re
import time
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

INPUT_DIR = Path(os.getenv("INPUT_DIR", "/input"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/output"))
LOCK_FILE = "/tmp/flattener.lock"

CHAPTER_REGEX = re.compile(r'(?:Ch(?:apter)?|Chap)(?:[ ._-]*)(\d+(?:\.\d+)?)', re.IGNORECASE)

def extract_chapter_number(filename: str) -> str:
    match = CHAPTER_REGEX.search(filename)
    return match.group(1) if match else None

def get_unique_filename(target_dir: Path, filename: str, parent_folder: str) -> Path:
    """ Generate a unique filename by adding a suffix if the file exists """
    new_file_path = target_dir / parent_folder / filename
    parent_path = target_dir / parent_folder
    if new_file_path.exists():
        base, ext = new_file_path.stem, new_file_path.suffix
        counter = 1
        while (target_dir / parent_folder / f"{base} ({counter}){ext}").exists():
            counter += 1
        new_file_path = target_dir / parent_folder / f"{base} ({counter}){ext}"
    if not parent_path.exists():
        parent_path.mkdir(parents=True, exist_ok=True)
    return new_file_path

def flatten_directory(source_dir: Path, target_dir: Path):
    logging.info(f"Flattening directory: {source_dir}")
    for root, _, files in os.walk(source_dir):
        for file in files:
            source_path = Path(root) / file
            if not source_path.suffix.lower() == ".cbz":
                continue

            # Get original folder name and chapter number
            parent_folder = source_path.parent.name
            chapter_number = extract_chapter_number(file)
            if not chapter_number:
                logging.warning(f"Could not extract chapter from {file}, skipping.")
                continue

            new_filename = f"{parent_folder} #{chapter_number}.cbz"
            target_path = get_unique_filename(target_dir, new_filename, parent_folder)

            try:
                shutil.copy2(source_path, target_path)
                logging.info(f"Copied and renamed: {source_path} → {target_path}")
            except Exception as e:
                logging.error(f"Failed to copy {source_path}: {e}")

class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        """ Handle new/modified files in the input directory """
        if event.is_directory:
            return
        if event.src_path.endswith(".cbz"):
            logging.info(f"Detected change: {event.src_path}")
            with FileLock(LOCK_FILE):
                flatten_directory(INPUT_DIR, OUTPUT_DIR)

def start_watching():
    event_handler = WatcherHandler()
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

    # First run to flatten existing files
    with FileLock(LOCK_FILE):
        flatten_directory(INPUT_DIR, OUTPUT_DIR)

    # Start watching for changes
    start_watching()

if __name__ == "__main__":
    main()
