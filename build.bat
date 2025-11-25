@echo off
echo ====================================
echo GravityMaze Build Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python first.
    pause
    exit /b 1
)

echo [1/5] Checking/Installing PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
) else (
    echo PyInstaller already installed.
)

echo.
echo [2/5] Checking/Installing Pillow for icon creation...
pip show pillow >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Pillow...
    pip install pillow
) else (
    echo Pillow already installed.
)

echo.
echo [3/5] Creating game icon...
python create_icon.py
if %errorlevel% neq 0 (
    echo Warning: Could not create icon. Continuing without custom icon...
)

echo.
echo [4/5] Building executable with PyInstaller...
echo This may take a few minutes...
pyinstaller --onefile ^
    --windowed ^
    --name "GravityMaze" ^
    --icon "icon.ico" ^
    --add-data "icon.ico;." ^
    --add-data "gravitymaze.db;." ^
    --hidden-import pygame ^
    --hidden-import serial ^
    --hidden-import numpy ^
    game.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [5/5] Build complete!
echo.
echo Executable location: dist\GravityMaze.exe
echo.
echo You can now run the game by executing dist\GravityMaze.exe
echo.
pause
