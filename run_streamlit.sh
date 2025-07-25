#!/bin/bash
# Run script for Streamlit Speech Recognition App

cd "$(dirname "$0")"

echo "Starting Streamlit Speech Recognition App..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate virtual environment and run the Streamlit app
source venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Installing Streamlit dependencies..."
    pip install streamlit streamlit-webrtc pandas
fi

echo "🚀 Launching Streamlit app..."
echo "📱 The app will open in your default web browser"
echo "🌐 If it doesn't open automatically, visit: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"

streamlit run streamlit_app_improved.py
