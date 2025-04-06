#!/bin/bash

# Default UID/GID
PUID=${PUID:-911}
PGID=${PGID:-911}

# Set timezone if provided
if [ -n "$TZ" ]; then
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
  echo $TZ > /etc/timezone
fi

# Modify flattener user/group
groupmod -o -g "$PGID" flattener
usermod -o -u "$PUID" -g "$PGID" flattener

# Make sure /media is writable
chown -R flattener:flattener /media

# Run the sync script as the specified user
exec su-exec flattener /sync.sh