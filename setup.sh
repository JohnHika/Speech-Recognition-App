#!/bin/bash
# Setup script for Speech Recognition App

echo "Speech Recognition App Setup"
echo "============================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip..."
    sudo apt-get update
    sudo apt-get install python3-pip -y
fi

echo "Installing system dependencies..."

# Detect OS and install appropriate dependencies
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux - installing portaudio and development tools"
    sudo apt-get update
    sudo apt-get install -y python3-dev python3-pip portaudio19-dev build-essential
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS - installing portaudio via Homebrew"
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install it first:"
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        exit 1
    fi
    brew install portaudio
    
else
    echo "Unsupported OS. Please install portaudio manually."
fi

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Testing installation..."
python3 test_setup.py

echo ""
echo "Setup complete!"
echo "To run the app: python3 speech_recognition_app.py"
