#!/bin/bash
# Real Estate Management System - Linux/Mac Startup Script
# Author: Luay Alkawaz
# Version: 1.0.0

echo "Starting Real Estate Management System..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
if ! python3 -c "import kivy" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Create necessary directories
mkdir -p property_photos/thumbnails
mkdir -p backups
mkdir -p reports
mkdir -p logs

# Run the application
echo "Starting application..."
python3 main.py

echo
echo "Application closed."
