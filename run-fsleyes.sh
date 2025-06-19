#!/bin/bash

# Script to run FSLeyes via Docker with GUI support

# Allow X11 forwarding
xhost +local:docker

# Set display environment variable
export DISPLAY=${DISPLAY:-:0}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Run FSLeyes using Docker Compose (newer syntax without hyphen)
echo "Starting FSLeyes via Docker..."
docker compose -f docker-compose.fsleyes.yml up --rm fsleyes

# Clean up X11 permissions
xhost -local:docker

echo "FSLeyes session ended." 