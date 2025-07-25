#!/usr/bin/env python3
"""
Streamlit Web Interface for Speech Recognition App
Main entry point for Streamlit Cloud deployment
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
    page_title="Speech Recognition App",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

class StreamlitSpeechApp:
    def __init__(self):
        # Initialize session state
        if 'app' not in st.session_state:
            st.session_state.app = SpeechRecognitionApp()
        if 'transcriptions' not in st.session_state:
            st.session_state.transcriptions = []
        if 'is_recording' not in st.session_state:
            st.session_state.is_recording = False
        
        self.app = st.session_state.app

    def show_header(self):
        """Display the application header"""
        st.title("🎤 Speech Recognition App")
        st.markdown("Convert speech to text using multiple AI-powered APIs")
        
        # Display current configuration
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current API", self.app.current_api)
        with col2:
            st.metric("Language", self.app.current_language)
        with col3:
            st.metric("Transcriptions", len(st.session_state.transcriptions))

    def show_settings_sidebar(self):
        """Display settings in the sidebar"""
        st.sidebar.header("⚙️ Settings")
        
        # API Selection
        api_options = {
            'google': 'Google Speech Recognition (Free)',
            'google_cloud': 'Google Cloud Speech (API Key Required)',
            'wit': 'Wit.ai (API Key Required)',
            'azure': 'Microsoft Azure (API Key Required)',
            'bing': 'Microsoft Bing (API Key Required)'
        }
        
        selected_api = st.sidebar.selectbox(
            "Select Speech Recognition API:",
            options=list(api_options.keys()),
            format_func=lambda x: api_options[x],
            index=0
        )
        
        if selected_api != self.app.current_api:
            self.app.set_api(selected_api)
        
        # Language Selection
        language_options = {
            'en-US': 'English (US)',
            'en-GB': 'English (UK)', 
            'es-ES': 'Spanish (Spain)',
            'es-MX': 'Spanish (Mexico)',
            'fr-FR': 'French',
            'de-DE': 'German',
            'it-IT': 'Italian',
            'pt-BR': 'Portuguese (Brazil)',
            'ru-RU': 'Russian',
            'ja-JP': 'Japanese',
            'ko-KR': 'Korean',
            'zh-CN': 'Chinese (Simplified)',
            'ar-SA': 'Arabic'
        }
        
        selected_language = st.sidebar.selectbox(
            "Select Language:",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=0
        )
        
        if selected_language != self.app.current_language:
            self.app.set_language(selected_language)
        
        # API Key Configuration
        st.sidebar.subheader("🔑 API Keys")
        if selected_api != 'google':
            api_key = st.sidebar.text_input(
                f"Enter {api_options[selected_api].split('(')[0].strip()} API Key:",
                type="password",
                help="Required for premium APIs"
            )
            if api_key:
                self.app.set_api_key(selected_api, api_key)

    def show_audio_recorder(self):
        """Display audio recording interface"""
        st.header("🎤 Record Audio")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔴 Start Recording", disabled=st.session_state.is_recording):
                self.start_recording()
        
        with col2:
            if st.button("⏹️ Stop Recording", disabled=not st.session_state.is_recording):
                self.stop_recording()
        
        if st.session_state.is_recording:
            st.info("🎤 Recording... Speak now!")
        
        # Audio recording using Streamlit's audio input
        st.subheader("🎙️ Browser Audio Recording")
        audio_bytes = st.audio_input("Record your voice")
        
        if audio_bytes:
            # Save the audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_file_path = tmp_file.name
            
            # Process the audio
            if st.button("🔄 Transcribe Audio"):
                with st.spinner("Transcribing audio..."):
                    result = self.process_audio_file(tmp_file_path)
                    if result:
                        st.success("✅ Transcription completed!")
                        self.add_transcription(result)
                    
                # Clean up temporary file
                os.unlink(tmp_file_path)

    def show_file_upload(self):
        """Display file upload interface"""
        st.header("📁 Upload Audio File")
        
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=['wav', 'mp3', 'flac', 'm4a', 'ogg'],
            help="Supported formats: WAV, MP3, FLAC, M4A, OGG"
        )
        
        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/wav')
            
            if st.button("🔄 Transcribe Uploaded File"):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                
                with st.spinner("Transcribing uploaded audio..."):
                    result = self.process_audio_file(tmp_file_path)
                    if result:
                        st.success("✅ File transcription completed!")
                        self.add_transcription(result)
                
                # Clean up temporary file
                os.unlink(tmp_file_path)

    def process_audio_file(self, file_path: str) -> Optional[Dict]:
        """Process an audio file and return transcription result"""
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(file_path) as source:
                audio = recognizer.record(source)
            
            # Get transcription using current API
            text = self.app.transcribe_audio(audio)
            
            if text:
                return {
                    'text': text,
                    'api': self.app.current_api,
                    'language': self.app.current_language,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': 'file_upload'
                }
            return None
            
        except Exception as e:
            st.error(f"❌ Error processing audio: {str(e)}")
            return None

    def start_recording(self):
        """Start audio recording"""
        st.session_state.is_recording = True
        st.rerun()

    def stop_recording(self):
        """Stop audio recording"""
        st.session_state.is_recording = False
        st.rerun()

    def add_transcription(self, result: Dict):
        """Add a transcription result to the session state"""
        st.session_state.transcriptions.append(result)

    def show_transcriptions(self):
        """Display transcription history"""
        st.header("📝 Transcription Results")
        
        if not st.session_state.transcriptions:
            st.info("No transcriptions yet. Record some audio or upload a file to get started!")
            return
        
        # Display latest transcription prominently
        if st.session_state.transcriptions:
            latest = st.session_state.transcriptions[-1]
            st.subheader("🆕 Latest Transcription")
            st.success(f"**Text**: {latest['text']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**API**: {latest['api']}")
            with col2:
                st.info(f"**Language**: {latest['language']}")
            with col3:
                st.info(f"**Time**: {latest['timestamp']}")
        
        # Display all transcriptions
        if len(st.session_state.transcriptions) > 1:
            st.subheader("📚 All Transcriptions")
            
            # Create DataFrame for better display
            df = pd.DataFrame(st.session_state.transcriptions)
            st.dataframe(df, use_container_width=True)

    def show_export_options(self):
        """Display export options for transcriptions"""
        if not st.session_state.transcriptions:
            return
        
        st.header("💾 Export Transcriptions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export as TXT"):
                txt_content = self.export_as_txt()
                st.download_button(
                    label="Download TXT",
                    data=txt_content,
                    file_name=f"transcriptions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("📊 Export as JSON"):
                json_content = self.export_as_json()
                st.download_button(
                    label="Download JSON",
                    data=json_content,
                    file_name=f"transcriptions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("📈 Export as CSV"):
                csv_content = self.export_as_csv()
                st.download_button(
                    label="Download CSV",
                    data=csv_content,
                    file_name=f"transcriptions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

    def export_as_txt(self) -> str:
        """Export transcriptions as plain text"""
        content = []
        content.append("Speech Recognition Transcriptions")
        content.append("=" * 50)
        content.append("")
        
        for i, trans in enumerate(st.session_state.transcriptions, 1):
            content.append(f"Transcription {i}:")
            content.append(f"Time: {trans['timestamp']}")
            content.append(f"API: {trans['api']}")
            content.append(f"Language: {trans['language']}")
            content.append(f"Text: {trans['text']}")
            content.append("-" * 30)
            content.append("")
        
        return "\n".join(content)

    def export_as_json(self) -> str:
        """Export transcriptions as JSON"""
        export_data = {
            'export_date': datetime.now().isoformat(),
            'total_transcriptions': len(st.session_state.transcriptions),
            'transcriptions': st.session_state.transcriptions
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)

    def export_as_csv(self) -> str:
        """Export transcriptions as CSV"""
        df = pd.DataFrame(st.session_state.transcriptions)
        return df.to_csv(index=False)

    def show_statistics(self):
        """Display usage statistics"""
        if not st.session_state.transcriptions:
            return
        
        st.header("📊 Statistics")
        
        # Basic stats
        total_transcriptions = len(st.session_state.transcriptions)
        total_characters = sum(len(t['text']) for t in st.session_state.transcriptions)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Transcriptions", total_transcriptions)
        
        with col2:
            st.metric("Total Characters", f"{total_characters:,}")
        
        with col3:
            avg_length = total_characters / total_transcriptions if total_transcriptions > 0 else 0
            st.metric("Avg Length", f"{avg_length:.1f}")
        
        with col4:
            apis_used = len(set(t['api'] for t in st.session_state.transcriptions))
            st.metric("APIs Used", apis_used)
        
        # API usage chart
        if total_transcriptions > 0:
            df = pd.DataFrame(st.session_state.transcriptions)
            api_counts = df['api'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("API Usage")
                st.bar_chart(api_counts)
            
            with col2:
                st.subheader("Language Usage")
                lang_counts = df['language'].value_counts()
                st.bar_chart(lang_counts)

    def run(self):
        """Main application runner"""
        self.show_header()
        self.show_settings_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎤 Record", "📁 Upload", "📝 Results", "💾 Export", "📊 Stats"
        ])
        
        with tab1:
            self.show_audio_recorder()
        
        with tab2:
            self.show_file_upload()
        
        with tab3:
            self.show_transcriptions()
        
        with tab4:
            self.show_export_options()
        
        with tab5:
            self.show_statistics()
        
        # Footer
        st.markdown("---")
        st.markdown(
            "🎤 **Speech Recognition App** | "
            "Built with ❤️ using Python & Streamlit | "
            "[GitHub](https://github.com/JohnHika/Speech-Recognition-App)"
        )

def main():
    """Main entry point"""
    try:
        app = StreamlitSpeechApp()
        app.run()
    except Exception as e:
        st.error(f"❌ Application Error: {str(e)}")
        st.info("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
