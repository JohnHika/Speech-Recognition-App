#!/usr/bin/env python3
"""
Test script for Speech Recognition App
This script tests the basic functionality and dependencies
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✓ {package_name or module_name} - OK")
        return True
    except ImportError as e:
        print(f"✗ {package_name or module_name} - FAILED: {e}")
        return False

def test_dependencies():
    """Test all required dependencies"""
    print("Testing dependencies...")
    print("-" * 30)
    
    dependencies = [
        ("speech_recognition", "SpeechRecognition"),
        ("pyaudio", "PyAudio"),
        ("json", "JSON (built-in)"),
        ("threading", "Threading (built-in)"),
        ("datetime", "DateTime (built-in)"),
        ("os", "OS (built-in)"),
        ("time", "Time (built-in)")
    ]
    
    all_ok = True
    for module, name in dependencies:
        if not test_import(module, name):
            all_ok = False
    
    print("-" * 30)
    if all_ok:
        print("✓ All dependencies are installed!")
    else:
        print("✗ Some dependencies are missing. Please install them.")
    
    return all_ok

def test_microphone():
    """Test microphone availability"""
    print("\nTesting microphone...")
    print("-" * 20)
    
    try:
        import pyaudio
        import speech_recognition as sr
        
        # Test microphone detection
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        print(f"Audio system: {info.get('name')}")
        
        device_count = p.get_device_count()
        print(f"Audio devices found: {device_count}")
        
        # Test microphone initialization
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        print("✓ Microphone initialized successfully")
        
        # List available microphones
        mic_list = sr.Microphone.list_microphone_names()
        print(f"Available microphones: {len(mic_list)}")
        for i, name in enumerate(mic_list[:5]):  # Show first 5
            print(f"  {i}: {name}")
        
        p.terminate()
        return True
        
    except Exception as e:
        print(f"✗ Microphone test failed: {e}")
        return False

def test_speech_recognition():
    """Test basic speech recognition setup"""
    print("\nTesting speech recognition...")
    print("-" * 30)
    
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        print("✓ Recognizer created")
        
        # Test microphone
        with sr.Microphone() as source:
            print("✓ Microphone source created")
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("✓ Ambient noise adjustment complete")
        
        print("✓ Basic speech recognition setup successful")
        return True
        
    except Exception as e:
        print(f"✗ Speech recognition test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Speech Recognition App - System Test")
    print("=" * 40)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    if not deps_ok:
        print("\nPlease install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    # Test microphone
    mic_ok = test_microphone()
    
    # Test speech recognition
    sr_ok = test_speech_recognition()
    
    print("\n" + "=" * 40)
    if deps_ok and mic_ok and sr_ok:
        print("✓ All tests passed! The app should work correctly.")
        print("\nYou can now run: python3 speech_recognition_app.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        if not mic_ok:
            print("\nMicrophone issues:")
            print("- Check if microphone is connected")
            print("- Verify audio permissions")
            print("- Test microphone with other applications")
    
    return deps_ok and mic_ok and sr_ok

if __name__ == "__main__":
    main()
