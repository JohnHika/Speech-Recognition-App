#!/bin/bash
# Run script for Speech Recognition App

cd "$(dirname "$0")"

echo "Starting Speech Recognition App..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate virtual environment and run the app
source venv/bin/activate
python speech_recognition_app.py
