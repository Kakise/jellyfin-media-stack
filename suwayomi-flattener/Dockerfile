# Use a Python 3.9 base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies and su-exec for user switching
RUN apt-get update && apt-get install -y \
    sudo \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create the flattener user and group
RUN groupadd -g 1000 flattener && useradd -r -u 1000 -g flattener flattener

# Copy the application files (flattener.py and entrypoint.sh)
COPY . /app

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Set environment variables (optional, you can set these from Docker Compose as well)
ENV INPUT_DIR=/input
ENV OUTPUT_DIR=/output
ENV STATE_DIR=/state

# Run the flattener script
CMD ["python", "flattener.py"]
