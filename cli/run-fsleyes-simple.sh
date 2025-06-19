#!/bin/bash

xhost +local:docker

export DISPLAY=${DISPLAY:-:0}

if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

PROJECT_ROOT="$(dirname "$(pwd)")"

echo "Starting FSLeyes via Docker..."
docker run --rm -it \
    --name fsleyes \
    -e DISPLAY=$DISPLAY \
    -e QT_X11_NO_MITSHM=1 \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $HOME/.Xauthority:/home/user/.Xauthority:ro \
    -v "$PROJECT_ROOT":/data:ro \
    -v "$PROJECT_ROOT":/workspace:rw \
    --network host \
    brainlife/fsleyes:latest \
    fsleyes

\xhost -local:docker

echo "FSLeyes session ended." 