#!/bin/bash

# Simple script to run FSLeyes via Docker using direct docker run command

# Allow X11 forwarding
xhost +local:docker

# Set display environment variable
export DISPLAY=${DISPLAY:-:0}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Run FSLeyes using direct docker run
echo "Starting FSLeyes via Docker..."
docker run --rm -it \
    --name fsleyes \
    -e DISPLAY=$DISPLAY \
    -e QT_X11_NO_MITSHM=1 \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $HOME/.Xauthority:/home/user/.Xauthority:ro \
    -v $(pwd):/data:ro \
    -v $(pwd):/workspace:rw \
    --network host \
    brainlife/fsleyes:latest \
    fsleyes

# Clean up X11 permissions
xhost -local:docker

echo "FSLeyes session ended." 