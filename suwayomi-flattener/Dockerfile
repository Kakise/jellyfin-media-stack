FROM alpine

# Install required packages
RUN apk add --no-cache inotify-tools bash shadow tzdata su-exec

# Create default user and group (will override UID/GID via entrypoint)
RUN addgroup -g 911 flattener && adduser -D -u 911 -G flattener flattener

# Set working directory
WORKDIR /

# Copy scripts
COPY sync.sh /sync.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /sync.sh /entrypoint.sh

# Use entrypoint to switch user at runtime
ENTRYPOINT ["/entrypoint.sh"]
