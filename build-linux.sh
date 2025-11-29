#!/bin/bash

echo "===================================="
echo "GravityMaze Linux Build Script"
echo "===================================="
echo ""

# Function to check command existence
command_exists () {
    type "$1" &> /dev/null ;
}

# Check for Python 3
if ! command_exists python3; then
    echo "ERROR: Python 3 not found! Please install python3 first."
    exit 1
fi

echo "[1/6] Checking/Installing PyInstaller..."
if ! pip3 show pyinstaller > /dev/null 2>&1; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
else
    echo "PyInstaller already installed."
fi

echo ""
echo "[2/6] Checking/Installing dependencies..."
# List of required packages
PACKAGES="pillow pygame pyserial numpy"

for pkg in $PACKAGES; do
    if ! pip3 show $pkg > /dev/null 2>&1; then
        echo "Installing $pkg..."
        pip3 install $pkg
    else
        echo "$pkg already installed."
    fi
done

echo ""
echo "[3/6] Creating game icon..."
python3 create_icon.py
if [ $? -ne 0 ]; then
    echo "Warning: Could not create icon. Continuing without custom icon..."
fi

echo ""
echo "[4/6] Building executable with PyInstaller..."
echo "This may take a few minutes..."

# Clean previous builds
rm -rf build/ dist/

# Run PyInstaller
# Note: separators for add-data are ':' on Linux
pyinstaller --onefile \
    --windowed \
    --name "GravityMaze_Linux" \
    --icon "icon.ico" \
    --add-data "icon.ico:." \
    --add-data "gravitymaze.db:. " \
    --hidden-import pygame \
    --hidden-import serial \
    --hidden-import numpy \
    game.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Build failed!"
    exit 1
fi

echo ""
echo "[5/6] Build complete!"
echo ""
echo "Executable location: dist/GravityMaze_Linux"
echo ""
echo "You can now run the game by executing ./dist/GravityMaze_Linux"
echo ""
