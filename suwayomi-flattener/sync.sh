#!/bin/bash

SOURCE="/mnt/FOLDER"
DEST="/media"

mkdir -p "$DEST"

sync_files() {
  echo "Syncing structure..."

  # Optional: clean old sync (or use rsync instead for more control)
  rm -rf "$DEST"/*
  
  # Find all leaf folders two levels deep and copy their contents to /media
  find "$SOURCE" -mindepth 3 -type f | while read -r filepath; do
    foldername=$(basename "$(dirname "$filepath")")
    targetdir="$DEST/$foldername"
    mkdir -p "$targetdir"
    cp "$filepath" "$targetdir/"
  done

  echo "Sync complete."
}

# Initial sync
sync_files

# Watch for changes and re-sync
inotifywait -mrq -e create,delete,modify,move "$SOURCE" | while read -r _; do
  sync_files
done
