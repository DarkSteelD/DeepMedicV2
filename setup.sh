set -e  

echo "====================================="
echo "DeepMedicV2 Setup Script"
echo "====================================="

echo "Checking if Git is installed..."
if ! command -v git >/dev/null 2>&1; then
    echo "Error: Git is not installed or not in PATH"
    echo "Please install Git using your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install git"
    echo "  CentOS/RHEL:   sudo yum install git"
    echo "  Fedora:        sudo dnf install git"
    echo "  macOS:         brew install git"
    echo "After installation, try again."
    exit 1
fi

GIT_VERSION=$(git --version)
echo "Git found: $GIT_VERSION"

REPO_URL="https://github.com/DarkSteelD/DeepMedicV2.git"
PROJECT_NAME="DeepMedicV2"

echo "Cloning DeepMedicV2 repository..."
echo "Repository: $REPO_URL"
echo "Branch: master"

if [ -d "$PROJECT_NAME" ]; then
    echo "Directory $PROJECT_NAME already exists. Removing it..."
    if ! rm -rf "$PROJECT_NAME"; then
        echo "Error: Failed to remove existing directory"
        echo "Please check file permissions and try again."
        exit 1
    fi
fi

echo "Starting git clone..."
if ! git clone -b master "$REPO_URL" "$PROJECT_NAME"; then
    echo "Error: Failed to clone repository"
    echo "This could be due to:"
    echo "- Network connectivity issues"
    echo "- Repository access issues"
    echo "- Insufficient disk space"
    echo "- Firewall blocking the connection"
    echo "Please check your internet connection and try again."
    exit 1
fi

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