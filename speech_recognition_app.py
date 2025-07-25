#!/usr/bin/env python3
"""
Improved Speech Recognition App
Features:
- Multiple speech recognition APIs
- Language selection
- Pause/Resume functionality
- Save transcriptions to file
- Enhanced error handling
"""

import speech_recognition as sr
import threading
import time
import os
from datetime import datetime
import json
from typing import Dict, List, Optional

# Try to import pyaudio, but don't fail if it's not available (for Streamlit Cloud)
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False


class SpeechRecognitionApp:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Only initialize microphone if PyAudio is available
        if PYAUDIO_AVAILABLE:
            try:
                self.microphone = sr.Microphone()
            except Exception:
                self.microphone = None
        else:
            self.microphone = None
        
        self.is_listening = False
        self.is_paused = False
        self.transcribed_text = []
        
        # Available APIs and their configurations
        self.available_apis = {
            "google": {
                "name": "Google Speech Recognition",
                "requires_key": False,
                "method": self._recognize_google
            },
            "google_cloud": {
                "name": "Google Cloud Speech",
                "requires_key": True,
                "method": self._recognize_google_cloud
            },
            "wit": {
                "name": "Wit.ai",
                "requires_key": True,
                "method": self._recognize_wit
            },
            "azure": {
                "name": "Microsoft Azure Speech",
                "requires_key": True,
                "method": self._recognize_azure
            },
            "bing": {
                "name": "Microsoft Bing Voice Recognition",
                "requires_key": True,
                "method": self._recognize_bing
            }
        }
        
        # Supported languages
        self.supported_languages = {
            "en-US": "English (US)",
            "en-GB": "English (UK)",
            "es-ES": "Spanish (Spain)",
            "es-MX": "Spanish (Mexico)",
            "fr-FR": "French",
            "de-DE": "German",
            "it-IT": "Italian",
            "pt-BR": "Portuguese (Brazil)",
            "ru-RU": "Russian",
            "ja-JP": "Japanese",
            "ko-KR": "Korean",
            "zh-CN": "Chinese (Simplified)",
            "ar-SA": "Arabic"
        }
        
        # Current settings
        self.current_api = "google"
        self.current_language = "en-US"
        self.api_keys = {}
        
        # Load configuration if exists
        self.load_config()
        
    def load_config(self):
        """Load configuration from config.json if it exists"""
        config_file = "config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.api_keys = config.get('api_keys', {})
                    self.current_api = config.get('default_api', 'google')
                    self.current_language = config.get('default_language', 'en-US')
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
    
    def save_config(self):
        """Save current configuration to config.json"""
        config = {
            'api_keys': self.api_keys,
            'default_api': self.current_api,
            'default_language': self.current_language
        }
        try:
            with open("config.json", 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
    
    def setup_microphone(self):
        """Setup and calibrate the microphone"""
        if not self.microphone:
            print("Microphone not available (PyAudio not installed)")
            return False
            
        print("Setting up microphone...")
        try:
            with self.microphone as source:
                print("Adjusting for ambient noise... Please remain quiet.")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("Microphone setup complete!")
                return True
        except Exception as e:
            print(f"Error setting up microphone: {e}")
            return False
    
    def display_available_apis(self):
        """Display available speech recognition APIs"""
        print("\nAvailable Speech Recognition APIs:")
        print("-" * 40)
        for i, (key, api_info) in enumerate(self.available_apis.items(), 1):
            status = "✓" if not api_info["requires_key"] or key in self.api_keys else "✗"
            key_req = " (API Key Required)" if api_info["requires_key"] else ""
            print(f"{i}. {api_info['name']}{key_req} {status}")
    
    def display_languages(self):
        """Display supported languages"""
        print("\nSupported Languages:")
        print("-" * 30)
        for i, (code, name) in enumerate(self.supported_languages.items(), 1):
            current = " (Current)" if code == self.current_language else ""
            print(f"{i}. {name} ({code}){current}")
    
    def select_api(self):
        """Allow user to select speech recognition API"""
        self.display_available_apis()
        
        try:
            choice = input(f"\nSelect API (1-{len(self.available_apis)}) or press Enter for current ({self.available_apis[self.current_api]['name']}): ").strip()
            
            if not choice:
                return
                
            choice_idx = int(choice) - 1
            api_keys = list(self.available_apis.keys())
            
            if 0 <= choice_idx < len(api_keys):
                selected_api = api_keys[choice_idx]
                api_info = self.available_apis[selected_api]
                
                # Check if API key is required
                if api_info["requires_key"] and selected_api not in self.api_keys:
                    api_key = input(f"Enter API key for {api_info['name']}: ").strip()
                    if api_key:
                        self.api_keys[selected_api] = api_key
                        self.save_config()
                    else:
                        print("API key required. Keeping current selection.")
                        return
                
                self.current_api = selected_api
                print(f"Selected: {api_info['name']}")
                self.save_config()
            else:
                print("Invalid selection.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Error selecting API: {e}")
    
    def select_language(self):
        """Allow user to select recognition language"""
        self.display_languages()
        
        try:
            choice = input(f"\nSelect language (1-{len(self.supported_languages)}) or press Enter for current: ").strip()
            
            if not choice:
                return
                
            choice_idx = int(choice) - 1
            lang_codes = list(self.supported_languages.keys())
            
            if 0 <= choice_idx < len(lang_codes):
                self.current_language = lang_codes[choice_idx]
                print(f"Selected: {self.supported_languages[self.current_language]} ({self.current_language})")
                self.save_config()
            else:
                print("Invalid selection.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Error selecting language: {e}")
    
    def _recognize_google(self, audio):
        """Google Speech Recognition (Free)"""
        return self.recognizer.recognize_google(audio, language=self.current_language)
    
    def _recognize_google_cloud(self, audio):
        """Google Cloud Speech API"""
        api_key = self.api_keys.get("google_cloud")
        if not api_key:
            raise Exception("Google Cloud API key not configured")
        return self.recognizer.recognize_google_cloud(audio, language=self.current_language)
    
    def _recognize_wit(self, audio):
        """Wit.ai Speech Recognition"""
        api_key = self.api_keys.get("wit")
        if not api_key:
            raise Exception("Wit.ai API key not configured")
        return self.recognizer.recognize_wit(audio, key=api_key)
    
    def _recognize_azure(self, audio):
        """Microsoft Azure Speech Recognition"""
        api_key = self.api_keys.get("azure")
        if not api_key:
            raise Exception("Azure API key not configured")
        return self.recognizer.recognize_azure(audio, key=api_key, language=self.current_language)
    
    def _recognize_bing(self, audio):
        """Microsoft Bing Voice Recognition"""
        api_key = self.api_keys.get("bing")
        if not api_key:
            raise Exception("Bing API key not configured")
        return self.recognizer.recognize_bing(audio, key=api_key, language=self.current_language)
    
    def transcribe_speech(self, audio):
        """
        Transcribe speech with enhanced error handling
        """
        try:
            # Get the recognition method for current API
            api_info = self.available_apis[self.current_api]
            recognition_method = api_info["method"]
            
            # Perform recognition
            text = recognition_method(audio)
            return text
            
        except sr.UnknownValueError:
            error_msg = f"Could not understand audio using {api_info['name']}"
            print(f"Warning: {error_msg}")
            return None
            
        except sr.RequestError as e:
            error_msg = f"Network error with {api_info['name']}: {str(e)}"
            print(f"Error: {error_msg}")
            if "quota" in str(e).lower():
                print("Suggestion: Check your API quota or try a different API")
            elif "network" in str(e).lower():
                print("Suggestion: Check your internet connection")
            return None
            
        except Exception as e:
            error_msg = f"Unexpected error with {api_info['name']}: {str(e)}"
            print(f"Error: {error_msg}")
            if "key" in str(e).lower():
                print("Suggestion: Check your API key configuration")
            return None
    
    def transcribe_audio(self, audio):
        """Transcribe audio data directly (for use with uploaded files)"""
        return self.transcribe_speech(audio)
    
    def listen_continuously(self):
        """Continuously listen for speech in a separate thread"""
        if not self.microphone:
            print("Error: Microphone not available (PyAudio not installed)")
            return
            
        print(f"\nListening with {self.available_apis[self.current_api]['name']} in {self.supported_languages[self.current_language]}...")
        print("Say something! (Press 'p' to pause, 'r' to resume, 'q' to quit)")
        
        while self.is_listening:
            if self.is_paused:
                time.sleep(0.1)
                continue
                
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Transcribe in background to avoid blocking
                threading.Thread(target=self._process_audio, args=(audio,), daemon=True).start()
                
            except sr.WaitTimeoutError:
                # Timeout is normal, continue listening
                pass
            except Exception as e:
                print(f"Error during listening: {e}")
                time.sleep(1)
    
    def _process_audio(self, audio):
        """Process audio in background thread"""
        if not self.is_listening or self.is_paused:
            return
            
        print("Processing...")
        text = self.transcribe_speech(audio)
        
        if text:
            timestamp = datetime.now().strftime("%H:%M:%S")
            transcription = {
                "timestamp": timestamp,
                "text": text,
                "api": self.current_api,
                "language": self.current_language
            }
            self.transcribed_text.append(transcription)
            print(f"[{timestamp}] You said: {text}")
    
    def pause_recognition(self):
        """Pause speech recognition"""
        if self.is_listening and not self.is_paused:
            self.is_paused = True
            print("Speech recognition paused. Press 'r' to resume.")
    
    def resume_recognition(self):
        """Resume speech recognition"""
        if self.is_listening and self.is_paused:
            self.is_paused = False
            print("Speech recognition resumed.")
    
    def stop_recognition(self):
        """Stop speech recognition"""
        self.is_listening = False
        self.is_paused = False
        print("Speech recognition stopped.")
    
    def save_transcription(self, filename=None):
        """Save transcribed text to a file"""
        if not self.transcribed_text:
            print("No transcription to save.")
            return False
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transcription_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Speech Recognition Transcription\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"API Used: {self.available_apis[self.current_api]['name']}\n")
                f.write(f"Language: {self.supported_languages[self.current_language]}\n")
                f.write("=" * 50 + "\n\n")
                
                for item in self.transcribed_text:
                    f.write(f"[{item['timestamp']}] {item['text']}\n")
                
                # Also save as JSON for programmatic access
                json_filename = filename.replace('.txt', '.json')
                with open(json_filename, 'w', encoding='utf-8') as json_file:
                    json.dump(self.transcribed_text, json_file, indent=2, ensure_ascii=False)
            
            print(f"Transcription saved to: {filename}")
            print(f"JSON format saved to: {json_filename}")
            return True
            
        except Exception as e:
            print(f"Error saving transcription: {e}")
            return False
    
    def display_transcription(self):
        """Display current transcription"""
        if not self.transcribed_text:
            print("No transcription available.")
            return
        
        print("\nCurrent Transcription:")
        print("-" * 30)
        for item in self.transcribed_text:
            print(f"[{item['timestamp']}] {item['text']}")
    
    def clear_transcription(self):
        """Clear current transcription"""
        self.transcribed_text.clear()
        print("Transcription cleared.")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 50)
        print("IMPROVED SPEECH RECOGNITION APP")
        print("=" * 50)
        print("1. Start Speech Recognition")
        print("2. Select Speech Recognition API")
        print("3. Select Language")
        print("4. View Current Transcription")
        print("5. Save Transcription to File")
        print("6. Clear Transcription")
        print("7. Settings & Configuration")
        print("8. Help")
        print("0. Exit")
        print("\nDuring recognition:")
        print("  Press 'p' + Enter to pause")
        print("  Press 'r' + Enter to resume")
        print("  Press 'q' + Enter to quit")
    
    def display_settings(self):
        """Display current settings"""
        print("\nCurrent Settings:")
        print("-" * 20)
        print(f"API: {self.available_apis[self.current_api]['name']}")
        print(f"Language: {self.supported_languages[self.current_language]}")
        print(f"Configured APIs: {', '.join(self.api_keys.keys()) if self.api_keys else 'None'}")
        print(f"Transcriptions: {len(self.transcribed_text)} items")
    
    def display_help(self):
        """Display help information"""
        print("\nHelp & Information:")
        print("-" * 20)
        print("This app supports multiple speech recognition APIs:")
        print("• Google Speech Recognition (Free, no API key needed)")
        print("• Google Cloud Speech (Requires API key)")
        print("• Wit.ai (Requires API key)")
        print("• Microsoft Azure Speech (Requires API key)")
        print("• Microsoft Bing Voice Recognition (Requires API key)")
        print("\nFeatures:")
        print("• Multiple language support")
        print("• Pause/Resume functionality")
        print("• Save transcriptions to file")
        print("• Enhanced error handling")
        print("• Configuration persistence")
        print("\nAPI Keys are stored in config.json")
        print("Transcriptions are saved as both TXT and JSON files")
    
    def run(self):
        """Main application loop"""
        print("Welcome to the Improved Speech Recognition App!")
        
        # Setup microphone
        if not self.setup_microphone():
            print("Failed to setup microphone. Exiting.")
            return
        
        # Main loop
        while True:
            self.display_menu()
            self.display_settings()
            
            try:
                choice = input("\nEnter your choice: ").strip()
                
                if choice == "1":
                    # Start speech recognition
                    self.is_listening = True
                    self.is_paused = False
                    
                    # Start listening in a separate thread
                    listen_thread = threading.Thread(target=self.listen_continuously, daemon=True)
                    listen_thread.start()
                    
                    # Handle user commands during recognition
                    while self.is_listening:
                        try:
                            cmd = input().strip().lower()
                            if cmd == 'p':
                                self.pause_recognition()
                            elif cmd == 'r':
                                self.resume_recognition()
                            elif cmd == 'q':
                                self.stop_recognition()
                                break
                        except KeyboardInterrupt:
                            self.stop_recognition()
                            break
                    
                elif choice == "2":
                    self.select_api()
                    
                elif choice == "3":
                    self.select_language()
                    
                elif choice == "4":
                    self.display_transcription()
                    
                elif choice == "5":
                    filename = input("Enter filename (or press Enter for auto-generated): ").strip()
                    self.save_transcription(filename if filename else None)
                    
                elif choice == "6":
                    confirm = input("Are you sure you want to clear transcription? (y/N): ").strip().lower()
                    if confirm == 'y':
                        self.clear_transcription()
                    
                elif choice == "7":
                    self.display_settings()
                    
                elif choice == "8":
                    self.display_help()
                    
                elif choice == "0":
                    print("Thank you for using the Speech Recognition App!")
                    break
                    
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")


if __name__ == "__main__":
    app = SpeechRecognitionApp()
    app.run()
