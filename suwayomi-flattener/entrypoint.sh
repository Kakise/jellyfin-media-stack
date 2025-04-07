#!/bin/bash

# Default UID/GID
PUID=${PUID:-1000}
PGID=${PGID:-1000}

# Set timezone if provided
if [ -n "$TZ" ]; then
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
  echo $TZ > /etc/timezone
fi

# Create the flattener user and group if they don't exist
if ! id "flattener" &>/dev/null; then
    groupadd -g "$PGID" flattener
    useradd -r -u "$PUID" -g "$PGID" flattener
fi

# Ensure /input and /output are writable by flattener user
chown -R flattener:flattener /input /output

# Run the Python flattener script as the specified user
exec gosu flattener python /app/flattener.py
