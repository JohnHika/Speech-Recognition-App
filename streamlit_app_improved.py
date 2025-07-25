#!/usr/bin/env python3
"""
Streamlit Web Interface for Speech Recognition App (Improved)
A modern, user-friendly web interface with better audio handling
"""

import streamlit as st
import speech_recognition as sr
import tempfile
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
    st.session_state.transcriptions = []
    st.session_state.recording_count = 0

def main():
    st.title("🎤 Improved Speech Recognition App")
    st.markdown("### Modern Web Interface for Multi-API Speech Recognition")
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
            st.success(f"✅ Switched to {api_names[selected_api_index]}")
        
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
                key=f"api_key_{selected_api}",
                help="This key will be saved automatically"
            )
            
            if api_key and api_key != current_key:
                st.session_state.app.api_keys[selected_api] = api_key
                st.session_state.app.save_config()
                st.success("🔐 API key updated!")
            
            if not api_key:
                st.warning("⚠️ API key required for this service")
        else:
            st.info("✅ No API key required (Free service)")
        
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
            st.success(f"🌐 Language set to {lang_names[selected_lang_index]}")
        
        # Current Settings Display
        st.subheader("📋 Current Settings")
        st.markdown(f"**API:** {api_info['name']}")
        st.markdown(f"**Language:** {st.session_state.app.supported_languages[st.session_state.app.current_language]}")
        st.markdown(f"**Transcriptions:** {len(st.session_state.transcriptions)}")
        
        # Help section
        with st.expander("ℹ️ Quick Help"):
            st.markdown("""
            **How to use:**
            1. Select your preferred API
            2. Add API key if needed
            3. Choose your language
            4. Record audio below
            5. View transcriptions
            6. Download results
            """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎙️ Speech Recording & Recognition")
        
        # Method selection
        recording_method = st.radio(
            "Choose recording method:",
            ["🎤 Browser Audio Recorder", "📁 Upload Audio File"],
            horizontal=True
        )
        
        if recording_method == "🎤 Browser Audio Recorder":
            st.subheader("🎤 Record Audio")
            st.info("Click the record button below to start recording. Speak clearly when recording.")
            
            # Audio recorder
            audio_value = st.audio_input("Record your speech:")
            
            if audio_value is not None:
                st.success("✅ Audio recorded! Processing...")
                
                # Process the recorded audio
                with st.spinner("🔄 Transcribing audio..."):
                    transcription = process_audio_data(audio_value)
                    
                if transcription:
                    st.success(f"✅ Transcription complete!")
                    st.markdown(f"**Result:** {transcription['text']}")
                    
                    # Add to session state
                    st.session_state.transcriptions.append(transcription)
                    st.session_state.recording_count += 1
                    
                    # Auto-refresh the page to show new transcription
                    st.experimental_rerun()
                else:
                    st.error("❌ Could not transcribe audio. Please try again.")
        
        else:  # Upload Audio File
            st.subheader("📁 Upload Audio File")
            uploaded_file = st.file_uploader(
                "Choose an audio file",
                type=['wav', 'mp3', 'flac', 'm4a', 'ogg'],
                help="Supported formats: WAV, MP3, FLAC, M4A, OGG"
            )
            
            if uploaded_file is not None:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                # Display file info
                st.write(f"**File size:** {len(uploaded_file.getvalue()) / 1024:.1f} KB")
                
                # Process button
                if st.button("🔄 Transcribe Uploaded File"):
                    with st.spinner("🔄 Processing uploaded file..."):
                        transcription = process_uploaded_file(uploaded_file)
                        
                    if transcription:
                        st.success(f"✅ Transcription complete!")
                        st.markdown(f"**Result:** {transcription['text']}")
                        
                        # Add to session state
                        st.session_state.transcriptions.append(transcription)
                        st.experimental_rerun()
                    else:
                        st.error("❌ Could not transcribe the uploaded file.")
        
        # Recent transcriptions
        if st.session_state.transcriptions:
            st.subheader("📝 Recent Transcriptions")
            
            # Show last 3 transcriptions
            recent_transcriptions = st.session_state.transcriptions[-3:]
            for i, trans in enumerate(reversed(recent_transcriptions)):
                with st.expander(f"🗨️ [{trans['timestamp']}] Transcription {len(st.session_state.transcriptions) - i}"):
                    st.write(trans['text'])
                    st.caption(f"API: {st.session_state.app.available_apis[trans['api']]['name']} | "
                             f"Language: {st.session_state.app.supported_languages[trans['language']]}")
    
    with col2:
        st.header("💾 Transcription Management")
        
        # Statistics
        if st.session_state.transcriptions:
            st.subheader("📊 Statistics")
            total_transcriptions = len(st.session_state.transcriptions)
            total_words = sum(len(trans['text'].split()) for trans in st.session_state.transcriptions)
            total_chars = sum(len(trans['text']) for trans in st.session_state.transcriptions)
            
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Transcriptions", total_transcriptions)
                st.metric("Total Words", total_words)
            with col_stat2:
                st.metric("Total Characters", total_chars)
                avg_words = total_words / total_transcriptions if total_transcriptions > 0 else 0
                st.metric("Avg Words/Trans", f"{avg_words:.1f}")
        
        # Download options
        if st.session_state.transcriptions:
            st.subheader("📥 Export Transcriptions")
            
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                # Text format
                txt_content = generate_txt_content(st.session_state.transcriptions)
                st.download_button(
                    label="📄 TXT",
                    data=txt_content,
                    file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                # JSON format
                json_content = json.dumps(st.session_state.transcriptions, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📊 JSON",
                    data=json_content,
                    file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col_download2:
                # CSV format
                csv_content = generate_csv_content(st.session_state.transcriptions)
                st.download_button(
                    label="📈 CSV",
                    data=csv_content,
                    file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Combined text file
                combined_content = generate_combined_text(st.session_state.transcriptions)
                st.download_button(
                    label="📋 Combined",
                    data=combined_content,
                    file_name=f"combined_transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # Clear transcriptions
        if st.session_state.transcriptions:
            st.subheader("🗑️ Clear Data")
            if st.button("🗑️ Clear All Transcriptions", type="secondary", use_container_width=True):
                st.session_state.transcriptions.clear()
                st.session_state.recording_count = 0
                st.success("🧹 Transcriptions cleared!")
                st.experimental_rerun()
    
    # Full transcription history
    if st.session_state.transcriptions:
        st.header("📚 Complete Transcription History")
        
        # Create DataFrame for better display
        df_data = []
        for i, trans in enumerate(st.session_state.transcriptions, 1):
            df_data.append({
                "#": i,
                "Time": trans['timestamp'],
                "Text": trans['text'][:100] + "..." if len(trans['text']) > 100 else trans['text'],
                "Full Text": trans['text'],
                "API": st.session_state.app.available_apis[trans['api']]['name'],
                "Language": st.session_state.app.supported_languages[trans['language']],
                "Words": len(trans['text'].split()),
                "Characters": len(trans['text'])
            })
        
        df = pd.DataFrame(df_data)
        
        # Display options
        display_option = st.radio(
            "Display format:",
            ["📊 Table View", "📝 Full Text View"],
            horizontal=True
        )
        
        if display_option == "📊 Table View":
            st.dataframe(
                df[["#", "Time", "Text", "API", "Language", "Words", "Characters"]], 
                use_container_width=True,
                hide_index=True
            )
        else:  # Full Text View
            for i, trans in enumerate(st.session_state.transcriptions, 1):
                with st.expander(f"📄 Transcription #{i} - [{trans['timestamp']}]"):
                    st.write(trans['text'])
                    st.caption(f"**API:** {st.session_state.app.available_apis[trans['api']]['name']} | "
                             f"**Language:** {st.session_state.app.supported_languages[trans['language']]} | "
                             f"**Words:** {len(trans['text'].split())} | **Characters:** {len(trans['text'])}")
    
    # Footer
    st.markdown("---")
    col_footer1, col_footer2, col_footer3 = st.columns([1, 2, 1])
    with col_footer2:
        st.markdown(
            "<div style='text-align: center'>"
            "🎤 <b>Speech Recognition App</b> | "
            "Powered by Multiple APIs | "
            "Built with Streamlit 🚀"
            "</div>", 
            unsafe_allow_html=True
        )

def process_audio_data(audio_data):
    """Process audio data from Streamlit audio input"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_data.getvalue())
            tmp_file.flush()
            
            # Use speech_recognition to process the file
            r = sr.Recognizer()
            with sr.AudioFile(tmp_file.name) as source:
                audio = r.record(source)
            
            # Transcribe using the selected API
            text = st.session_state.app.transcribe_speech(audio)
            
            # Clean up
            os.unlink(tmp_file.name)
            
            if text:
                return {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "text": text,
                    "api": st.session_state.app.current_api,
                    "language": st.session_state.app.current_language,
                    "source": "browser_recording"
                }
            
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None

def process_uploaded_file(uploaded_file):
    """Process uploaded audio file"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file.flush()
            
            # Use speech_recognition to process the file
            r = sr.Recognizer()
            with sr.AudioFile(tmp_file.name) as source:
                audio = r.record(source)
            
            # Transcribe using the selected API
            text = st.session_state.app.transcribe_speech(audio)
            
            # Clean up
            os.unlink(tmp_file.name)
            
            if text:
                return {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "text": text,
                    "api": st.session_state.app.current_api,
                    "language": st.session_state.app.current_language,
                    "source": f"uploaded_file: {uploaded_file.name}"
                }
            
    except Exception as e:
        st.error(f"Error processing uploaded file: {e}")
        return None

def generate_txt_content(transcriptions):
    """Generate TXT file content"""
    content = []
    content.append("Speech Recognition Transcription Report")
    content.append("=" * 50)
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"Total Transcriptions: {len(transcriptions)}")
    content.append("")
    
    for i, trans in enumerate(transcriptions, 1):
        api_name = st.session_state.app.available_apis[trans['api']]['name']
        lang_name = st.session_state.app.supported_languages[trans['language']]
        content.append(f"--- Transcription #{i} ---")
        content.append(f"Time: {trans['timestamp']}")
        content.append(f"API: {api_name}")
        content.append(f"Language: {lang_name}")
        content.append(f"Text: {trans['text']}")
        content.append("")
    
    return "\n".join(content)

def generate_csv_content(transcriptions):
    """Generate CSV file content"""
    data = []
    for i, trans in enumerate(transcriptions, 1):
        api_name = st.session_state.app.available_apis[trans['api']]['name']
        lang_name = st.session_state.app.supported_languages[trans['language']]
        data.append({
            "ID": i,
            "Timestamp": trans['timestamp'],
            "Text": trans['text'],
            "API": api_name,
            "Language": lang_name,
            "Word_Count": len(trans['text'].split()),
            "Character_Count": len(trans['text']),
            "Source": trans.get('source', 'unknown')
        })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

def generate_combined_text(transcriptions):
    """Generate combined text from all transcriptions"""
    combined_text = []
    combined_text.append("Combined Transcription Text")
    combined_text.append("=" * 30)
    combined_text.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    combined_text.append("")
    
    for trans in transcriptions:
        combined_text.append(trans['text'])
    
    combined_text.append("")
    combined_text.append("--- End of Transcription ---")
    
    return "\n".join(combined_text)

if __name__ == "__main__":
    main()
