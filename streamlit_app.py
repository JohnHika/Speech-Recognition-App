#!/usr/bin/env python3
"""
Streamlit Web Interface for Speech Recognition App
A modern, user-friendly web interface for the improved speech recognition application
"""

import streamlit as st
import speech_recognition as sr
import pyaudio
import threading
import time
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
import io

# Import our main application class
from speech_recognition_app import SpeechRecognitionApp

# Set page configuration
st.set_page_config(
    page_title="🎤 Speech Recognition App",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'app' not in st.session_state:
    st.session_state.app = SpeechRecognitionApp()
    st.session_state.is_listening = False
    st.session_state.is_paused = False
    st.session_state.transcriptions = []
    st.session_state.status_message = "Ready to start"

def main():
    st.title("🎤 Improved Speech Recognition App")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Selection
        st.subheader("🔧 Speech Recognition API")
        api_options = list(st.session_state.app.available_apis.keys())
        api_names = [st.session_state.app.available_apis[api]['name'] for api in api_options]
        
        current_api_index = api_options.index(st.session_state.app.current_api)
        selected_api_index = st.selectbox(
            "Select API:",
            range(len(api_options)),
            format_func=lambda x: api_names[x],
            index=current_api_index,
            key="api_selector"
        )
        
        if api_options[selected_api_index] != st.session_state.app.current_api:
            st.session_state.app.current_api = api_options[selected_api_index]
            st.session_state.app.save_config()
            st.success(f"Switched to {api_names[selected_api_index]}")
        
        # API Key Configuration
        selected_api = api_options[selected_api_index]
        api_info = st.session_state.app.available_apis[selected_api]
        
        if api_info["requires_key"]:
            st.subheader("🔑 API Key")
            current_key = st.session_state.app.api_keys.get(selected_api, "")
            api_key = st.text_input(
                f"Enter {api_info['name']} API Key:",
                value=current_key,
                type="password",
                key=f"api_key_{selected_api}"
            )
            
            if api_key and api_key != current_key:
                st.session_state.app.api_keys[selected_api] = api_key
                st.session_state.app.save_config()
                st.success("API key updated!")
            
            if not api_key:
                st.warning("API key required for this service")
        else:
            st.info("✅ No API key required")
        
        # Language Selection
        st.subheader("🌍 Language")
        lang_options = list(st.session_state.app.supported_languages.keys())
        lang_names = [st.session_state.app.supported_languages[lang] for lang in lang_options]
        
        current_lang_index = lang_options.index(st.session_state.app.current_language)
        selected_lang_index = st.selectbox(
            "Select Language:",
            range(len(lang_options)),
            format_func=lambda x: lang_names[x],
            index=current_lang_index,
            key="lang_selector"
        )
        
        if lang_options[selected_lang_index] != st.session_state.app.current_language:
            st.session_state.app.current_language = lang_options[selected_lang_index]
            st.session_state.app.save_config()
            st.success(f"Language set to {lang_names[selected_lang_index]}")
        
        # Current Settings Display
        st.subheader("📋 Current Settings")
        st.write(f"**API:** {api_info['name']}")
        st.write(f"**Language:** {st.session_state.app.supported_languages[st.session_state.app.current_language]}")
        st.write(f"**Transcriptions:** {len(st.session_state.transcriptions)}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Speech Recognition")
        
        # Status display
        status_container = st.container()
        with status_container:
            if st.session_state.is_listening:
                if st.session_state.is_paused:
                    st.warning("⏸️ Recognition Paused")
                else:
                    st.success("🎙️ Listening...")
            else:
                st.info("⏹️ Stopped")
        
        # Control buttons
        button_col1, button_col2, button_col3, button_col4 = st.columns(4)
        
        with button_col1:
            if st.button("🎙️ Start Recording", disabled=st.session_state.is_listening):
                start_recording()
        
        with button_col2:
            if st.button("⏸️ Pause", disabled=not st.session_state.is_listening or st.session_state.is_paused):
                pause_recording()
        
        with button_col3:
            if st.button("▶️ Resume", disabled=not st.session_state.is_paused):
                resume_recording()
        
        with button_col4:
            if st.button("⏹️ Stop", disabled=not st.session_state.is_listening):
                stop_recording()
        
        # Live transcription display
        st.subheader("📝 Live Transcription")
        transcription_container = st.container()
        
        # Display recent transcriptions
        if st.session_state.transcriptions:
            with transcription_container:
                for i, trans in enumerate(reversed(st.session_state.transcriptions[-10:])):  # Show last 10
                    st.write(f"**[{trans['timestamp']}]** {trans['text']}")
        else:
            with transcription_container:
                st.write("*No transcriptions yet. Click 'Start Recording' to begin.*")
    
    with col2:
        st.header("💾 Transcription Management")
        
        # Download options
        if st.session_state.transcriptions:
            st.subheader("📥 Download Transcriptions")
            
            # Text format
            txt_content = generate_txt_content(st.session_state.transcriptions)
            st.download_button(
                label="📄 Download as TXT",
                data=txt_content,
                file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
            
            # JSON format
            json_content = json.dumps(st.session_state.transcriptions, indent=2, ensure_ascii=False)
            st.download_button(
                label="📊 Download as JSON",
                data=json_content,
                file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # CSV format
            csv_content = generate_csv_content(st.session_state.transcriptions)
            st.download_button(
                label="📈 Download as CSV",
                data=csv_content,
                file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Clear transcriptions
        if st.session_state.transcriptions:
            st.subheader("🗑️ Clear Data")
            if st.button("Clear All Transcriptions", type="secondary"):
                st.session_state.transcriptions.clear()
                st.success("Transcriptions cleared!")
                st.experimental_rerun()
        
        # Statistics
        if st.session_state.transcriptions:
            st.subheader("📊 Statistics")
            total_words = sum(len(trans['text'].split()) for trans in st.session_state.transcriptions)
            total_chars = sum(len(trans['text']) for trans in st.session_state.transcriptions)
            
            st.metric("Total Transcriptions", len(st.session_state.transcriptions))
            st.metric("Total Words", total_words)
            st.metric("Total Characters", total_chars)
    
    # Full transcription history
    if st.session_state.transcriptions:
        st.header("📚 Full Transcription History")
        
        # Create DataFrame for better display
        df_data = []
        for trans in st.session_state.transcriptions:
            df_data.append({
                "Time": trans['timestamp'],
                "Text": trans['text'],
                "API": st.session_state.app.available_apis[trans['api']]['name'],
                "Language": st.session_state.app.supported_languages[trans['language']],
                "Words": len(trans['text'].split()),
                "Characters": len(trans['text'])
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
    
    # Help section
    with st.expander("ℹ️ Help & Information"):
        st.markdown("""
        ### How to Use:
        1. **Select API**: Choose your preferred speech recognition service
        2. **Configure API Key**: Enter API key if required
        3. **Select Language**: Choose the language you'll be speaking
        4. **Start Recording**: Click the microphone button to begin
        5. **Pause/Resume**: Control recording as needed
        6. **Download**: Save your transcriptions in various formats
        
        ### Supported APIs:
        - **Google Speech Recognition**: Free, no API key needed
        - **Google Cloud Speech**: Enterprise-grade, requires API key
        - **Wit.ai**: Facebook's service, requires API key
        - **Microsoft Azure Speech**: Microsoft's cloud service, requires API key
        - **Microsoft Bing Voice Recognition**: Legacy Microsoft service, requires API key
        
        ### Supported Languages:
        English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic, and more!
        
        ### Features:
        - ✅ Real-time speech recognition
        - ✅ Multiple API support
        - ✅ Multi-language support
        - ✅ Pause/Resume functionality
        - ✅ Export to TXT, JSON, CSV
        - ✅ Live transcription display
        - ✅ Statistics tracking
        """)

def start_recording():
    """Start speech recognition"""
    try:
        # Setup microphone
        if not st.session_state.app.setup_microphone():
            st.error("Failed to setup microphone!")
            return
        
        st.session_state.is_listening = True
        st.session_state.is_paused = False
        st.session_state.status_message = "Listening..."
        
        # Start background thread for continuous listening
        thread = threading.Thread(target=continuous_listening, daemon=True)
        thread.start()
        
        st.success("Started recording!")
        st.experimental_rerun()
        
    except Exception as e:
        st.error(f"Error starting recording: {e}")

def pause_recording():
    """Pause speech recognition"""
    st.session_state.is_paused = True
    st.session_state.status_message = "Paused"
    st.success("Recording paused!")
    st.experimental_rerun()

def resume_recording():
    """Resume speech recognition"""
    st.session_state.is_paused = False
    st.session_state.status_message = "Listening..."
    st.success("Recording resumed!")
    st.experimental_rerun()

def stop_recording():
    """Stop speech recognition"""
    st.session_state.is_listening = False
    st.session_state.is_paused = False
    st.session_state.status_message = "Stopped"
    st.success("Recording stopped!")
    st.experimental_rerun()

def continuous_listening():
    """Continuous listening function that runs in background"""
    # Store initial states to avoid session state issues in threads
    app = st.session_state.app
    
    while True:
        # Check if we should continue listening
        try:
            if not st.session_state.is_listening:
                break
            if st.session_state.is_paused:
                time.sleep(0.1)
                continue
        except:
            # If session state is not accessible, stop listening
            break
        
        try:
            with app.microphone as source:
                # Listen for audio with timeout
                audio = app.recognizer.listen(source, timeout=1, phrase_time_limit=5)
            
            # Process audio
            text = app.transcribe_speech(audio)
            
            if text:
                timestamp = datetime.now().strftime("%H:%M:%S")
                transcription = {
                    "timestamp": timestamp,
                    "text": text,
                    "api": app.current_api,
                    "language": app.current_language
                }
                
                # Safely add to session state
                try:
                    st.session_state.transcriptions.append(transcription)
                except:
                    # If session state not accessible, create a temporary store
                    pass
            
        except sr.WaitTimeoutError:
            # Timeout is normal, continue listening
            pass
        except Exception as e:
            print(f"Error during listening: {e}")
            time.sleep(1)

def process_audio(audio):
    """Process audio and add to transcriptions"""
    if not st.session_state.is_listening or st.session_state.is_paused:
        return
    
    text = st.session_state.app.transcribe_speech(audio)
    
    if text:
        timestamp = datetime.now().strftime("%H:%M:%S")
        transcription = {
            "timestamp": timestamp,
            "text": text,
            "api": st.session_state.app.current_api,
            "language": st.session_state.app.current_language
        }
        st.session_state.transcriptions.append(transcription)

def generate_txt_content(transcriptions):
    """Generate TXT file content"""
    content = []
    content.append("Speech Recognition Transcription")
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"Total Transcriptions: {len(transcriptions)}")
    content.append("=" * 50)
    content.append("")
    
    for trans in transcriptions:
        api_name = st.session_state.app.available_apis[trans['api']]['name']
        lang_name = st.session_state.app.supported_languages[trans['language']]
        content.append(f"[{trans['timestamp']}] ({api_name}, {lang_name})")
        content.append(trans['text'])
        content.append("")
    
    return "\n".join(content)

def generate_csv_content(transcriptions):
    """Generate CSV file content"""
    data = []
    for trans in transcriptions:
        api_name = st.session_state.app.available_apis[trans['api']]['name']
        lang_name = st.session_state.app.supported_languages[trans['language']]
        data.append({
            "Timestamp": trans['timestamp'],
            "Text": trans['text'],
            "API": api_name,
            "Language": lang_name,
            "Word_Count": len(trans['text'].split()),
            "Character_Count": len(trans['text'])
        })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

if __name__ == "__main__":
    main()
