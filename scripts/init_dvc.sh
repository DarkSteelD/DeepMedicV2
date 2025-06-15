#!/bin/bash

# Initialize DVC in the project directory
echo "Initializing DVC..."

# Check if DVC is already initialized
if [ ! -d ".dvc" ]; then
    echo "DVC not initialized, initializing now..."
    dvc init --no-scm
else
    echo "DVC already initialized"
fi

# Check if data is already tracked
if [ ! -f "data/raw/winequality-red.csv.dvc" ]; then
    echo "Adding data file to DVC tracking..."
    dvc add data/raw/winequality-red.csv
else
    echo "Data file already tracked by DVC"
fi

# Set up models directory
mkdir -p models
echo "models/" > models/.gitkeep

# Add models to DVC if not already tracked
if [ ! -f "models/.dvc" ]; then
    echo "Adding models directory to DVC..."
    dvc add models/ 2>/dev/null || echo "Models directory tracking setup"
fi

echo "DVC initialization complete!"

# Show DVC status
echo "Current DVC status:"
dvc status || echo "No changes detected" 