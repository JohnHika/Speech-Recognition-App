#!/usr/bin/env python3
"""
Streamlit App Launcher
Simple launcher to test the Streamlit app
"""

import subprocess
import sys
import os

def main():
    print("🎤 Speech Recognition App - Streamlit Launcher")
    print("=" * 50)
    
    # Change to the app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    
    print(f"📁 Working directory: {app_dir}")
    
    try:
        # Check if we're in a virtual environment
        if 'venv' in sys.executable or 'VIRTUAL_ENV' in os.environ:
            print("✅ Virtual environment detected")
        else:
            print("⚠️  No virtual environment detected")
        
        # Test imports
        print("🔍 Testing imports...")
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} ready")
        
        import speech_recognition_app
        print("✅ Speech Recognition app imported")
        
        import pandas
        print(f"✅ Pandas {pandas.__version__} ready")
        
        print("\n🚀 Starting Streamlit server...")
        print("📱 The app will open in your default web browser")
        print("🌐 URL: http://localhost:8501")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Launch Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app_improved.py"])
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try running: pip install streamlit pandas")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Streamlit server stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
