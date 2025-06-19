# FSLeyes via Docker - Working Setup

This branch contains a working Docker setup for FSLeyes (neuroimaging viewer).

## Quick Start

### Option 1: Simple Docker Run (Recommended)
```bash
./run-fsleyes-simple.sh
```

### Option 2: Docker Compose
```bash
./run-fsleyes.sh
```

## What's included:

- `run-fsleyes-simple.sh` - Simple script using direct docker run
- `run-fsleyes.sh` - Script using docker compose
- `docker-compose.fsleyes.yml` - Docker compose configuration
- `Dockerfile.fsleyes` - Custom Dockerfile for building your own image

## Tested and Working ✅

This setup has been tested and confirmed working on:
- Linux 6.8.0-60-generic
- Docker version 28.2.2
- Docker Compose version v2.36.2

The GUI forwarding works correctly via X11. 