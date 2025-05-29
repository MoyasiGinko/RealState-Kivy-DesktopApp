@echo off
REM Real Estate Management System - Windows Startup Script
REM Author: Luay Alkawaz
REM Version: 1.0.0

echo Starting Real Estate Management System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import kivy, pillow" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create necessary directories
if not exist "property_photos" mkdir property_photos
if not exist "property_photos\thumbnails" mkdir property_photos\thumbnails
if not exist "backups" mkdir backups
if not exist "reports" mkdir reports
if not exist "logs" mkdir logs

REM Run the application
echo Starting application...
python main.py

echo.
echo Application closed.
pause
