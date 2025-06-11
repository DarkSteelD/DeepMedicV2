#!/bin/bash

# DeepMedicV2 Setup Script
# This script clones the DeepMedicV2 repository from GitHub

set -e  

echo "====================================="
echo "DeepMedicV2 Setup Script"
echo "====================================="

REPO_URL="https://github.com/DarkSteelD/DeepMedicV2.git"
PROJECT_NAME="DeepMedicV2"

echo "Cloning DeepMedicV2 repository..."
echo "Repository: $REPO_URL"
echo "Branch: master"

# Clone the repository
if [ -d "$PROJECT_NAME" ]; then
    echo "Directory $PROJECT_NAME already exists. Removing it..."
    rm -rf "$PROJECT_NAME"
fi

git clone -b master "$REPO_URL" "$PROJECT_NAME"

echo "Repository cloned successfully!"
echo "Project directory: $PROJECT_NAME"

cd "$PROJECT_NAME"

echo "Current directory: $(pwd)"
echo "Repository contents:"
ls -la

echo "====================================="
echo "Setup completed successfully!"
echo "====================================="
echo "To get started:"
echo "  cd $PROJECT_NAME"
echo "  # Follow the README.md for further instructions"
echo "=====================================" 