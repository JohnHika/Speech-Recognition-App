# 🎤 Speech Recognition App - Streamlit Web Interface

A modern, user-friendly web interface for the improved speech recognition application. Now you can use speech recognition directly from your web browser!

## 🌟 Features

### 🎯 Core Capabilities
- **🌐 Web-Based Interface**: No installation needed on client devices
- **🎤 Browser Audio Recording**: Record directly in your web browser
- **📁 File Upload Support**: Upload audio files (WAV, MP3, FLAC, M4A, OGG)
- **🔄 Multiple API Support**: Google, Google Cloud, Wit.ai, Azure, Bing
- **🌍 Multi-Language**: 13+ supported languages
- **💾 Export Options**: TXT, JSON, CSV, Combined formats
- **📊 Real-time Statistics**: Track words, characters, transcriptions
- **📱 Responsive Design**: Works on desktop, tablet, and mobile

### 🛠️ Technical Features
- **🔐 Secure API Key Storage**: Keys saved locally in session
- **⚙️ Configuration Persistence**: Settings automatically saved
- **🎨 Modern UI**: Clean, intuitive Streamlit interface
- **📈 Data Visualization**: Tables and statistics for transcriptions
- **🗃️ Session Management**: Transcriptions stored during session

## 🚀 Quick Start

### Method 1: Using the Launcher Script (Recommended)
```bash
cd /home/john-hika/Public/Speech-Recognition-App
source venv/bin/activate
python launch_streamlit.py
```

### Method 2: Using the Shell Script
```bash
cd /home/john-hika/Public/Speech-Recognition-App
./run_streamlit.sh
```

### Method 3: Direct Streamlit Command
```bash
cd /home/john-hika/Public/Speech-Recognition-App
source venv/bin/activate
streamlit run streamlit_app_improved.py
```

## 🌐 Accessing the App

Once started, the app will be available at:
- **Local URL**: http://localhost:8501 (or 8502 if 8501 is busy)
- **Network URL**: http://[your-ip]:8501 (accessible from other devices on your network)

The app will automatically open in your default web browser.

## 📱 How to Use

### 1. 🔧 Configuration (Sidebar)
1. **Select API**: Choose from Google, Google Cloud, Wit.ai, Azure, or Bing
2. **Enter API Key**: If required for your chosen API
3. **Select Language**: Choose from 13+ supported languages
4. **View Settings**: Check current configuration

### 2. 🎙️ Recording Methods

#### Method A: Browser Audio Recording
1. Click "Browser Audio Recorder"
2. Click the record button
3. Speak clearly into your microphone
4. Click stop when finished
5. Wait for transcription to appear

#### Method B: File Upload
1. Click "Upload Audio File"
2. Choose an audio file (WAV, MP3, FLAC, M4A, OGG)
3. Click "Transcribe Uploaded File"
4. Wait for processing

### 3. 📝 View Results
- **Recent Transcriptions**: See your latest 3 transcriptions
- **Full History**: View all transcriptions in table or text format
- **Statistics**: Track words, characters, and transcription count

### 4. 💾 Export Data
- **📄 TXT**: Human-readable format
- **📊 JSON**: Machine-readable with metadata
- **📈 CSV**: Spreadsheet-compatible format
- **📋 Combined**: All text combined into one file

## 🔧 Configuration Options

### API Selection
| API | Free/Paid | API Key Required | Features |
|-----|-----------|------------------|----------|
| Google Speech Recognition | Free | ❌ No | Basic recognition, good quality |
| Google Cloud Speech | Paid | ✅ Yes | Enterprise features, high accuracy |
| Wit.ai | Free | ✅ Yes | Facebook's service, good for apps |
| Microsoft Azure Speech | Paid | ✅ Yes | Enterprise-grade, customizable |
| Microsoft Bing Voice | Paid | ✅ Yes | Legacy service, basic features |

### Supported Languages
- 🇺🇸 English (US/UK)
- 🇪🇸 Spanish (Spain/Mexico)
- 🇫🇷 French
- 🇩🇪 German
- 🇮🇹 Italian
- 🇧🇷 Portuguese (Brazil)
- 🇷🇺 Russian
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇨🇳 Chinese (Simplified)
- 🇸🇦 Arabic

## 📊 Export Formats

### TXT Format
```
Speech Recognition Transcription Report
==================================================
Generated: 2025-07-26 12:30:45
Total Transcriptions: 3

--- Transcription #1 ---
Time: 12:30:15
API: Google Speech Recognition
Language: English (US)
Text: Hello, this is a test transcription.
```

### JSON Format
```json
[
  {
    "timestamp": "12:30:15",
    "text": "Hello, this is a test transcription.",
    "api": "google",
    "language": "en-US",
    "source": "browser_recording"
  }
]
```

### CSV Format
| ID | Timestamp | Text | API | Language | Word_Count | Character_Count | Source |
|----|-----------|------|-----|----------|------------|-----------------|---------|
| 1 | 12:30:15 | Hello, this is... | Google Speech | English (US) | 6 | 35 | browser_recording |

## 🎯 Use Cases

### 📝 Content Creation
- **Blog Writing**: Dictate your blog posts
- **Note Taking**: Convert lectures to text
- **Meeting Minutes**: Record and transcribe meetings
- **Interview Transcription**: Convert interviews to text

### 🎓 Education
- **Language Learning**: Practice pronunciation
- **Accessibility**: Help for hearing-impaired students
- **Research**: Transcribe recorded interviews
- **Documentation**: Create text from audio lectures

### 💼 Business
- **Voice Memos**: Convert voice notes to text
- **Customer Service**: Transcribe calls
- **Content Marketing**: Convert podcasts to blog posts
- **Documentation**: Create written records from audio

### 🌐 Multilingual Support
- **Translation Preparation**: Transcribe in original language
- **Language Practice**: Check pronunciation accuracy
- **International Communication**: Support multiple languages
- **Content Localization**: Prepare text for translation

## 🔒 Privacy & Security

### Data Handling
- **🏠 Local Processing**: Audio processed on your machine when possible
- **🔐 Secure API Keys**: Stored locally in session, not transmitted
- **🗑️ Session-Only Storage**: Transcriptions cleared when session ends
- **🚫 No Permanent Storage**: No data saved to disk without explicit export

### API Privacy
- **Google Free**: Audio sent to Google servers temporarily
- **Google Cloud**: Enterprise privacy controls available
- **Wit.ai**: Audio sent to Facebook servers
- **Azure**: Enterprise-grade privacy and compliance
- **Bing**: Audio sent to Microsoft servers

## 🛠️ Troubleshooting

### Common Issues

#### 🎤 Microphone Not Working
- **Check Permissions**: Allow microphone access in browser
- **Test Hardware**: Verify microphone works in other apps
- **Browser Support**: Use Chrome/Firefox for best compatibility
- **HTTPS Required**: Some browsers require HTTPS for microphone access

#### 🌐 API Errors
```
❌ Could not transcribe audio
```
**Solutions:**
- Verify API key is correct
- Check internet connection
- Ensure API quota isn't exceeded
- Try a different API

#### 📁 File Upload Issues
```
❌ Error processing uploaded file
```
**Solutions:**
- Use supported formats (WAV, MP3, FLAC, M4A, OGG)
- Check file size (keep under 10MB)
- Ensure audio quality is sufficient
- Try converting file to WAV format

#### 🔧 App Won't Start
```
❌ Import error or connection refused
```
**Solutions:**
- Ensure virtual environment is activated
- Install missing dependencies: `pip install streamlit pandas`
- Check if port 8501 is available
- Try a different port: `streamlit run app.py --server.port 8502`

### Browser Compatibility
| Browser | Audio Recording | File Upload | API Support |
|---------|-----------------|-------------|-------------|
| Chrome | ✅ Excellent | ✅ Yes | ✅ All APIs |
| Firefox | ✅ Good | ✅ Yes | ✅ All APIs |
| Safari | ⚠️ Limited | ✅ Yes | ✅ All APIs |
| Edge | ✅ Good | ✅ Yes | ✅ All APIs |

## 🎨 Interface Overview

### Sidebar Configuration
- **🔧 API Selection**: Dropdown menu for API choice
- **🔑 API Key Input**: Secure password field for keys
- **🌍 Language Selection**: Dropdown for language choice
- **📋 Current Settings**: Display of active configuration
- **ℹ️ Quick Help**: Collapsible help section

### Main Content Area
- **🎙️ Recording Section**: Audio recording and file upload
- **📝 Recent Transcriptions**: Latest 3 transcriptions with expandable details
- **💾 Management Panel**: Export options and statistics
- **📚 Full History**: Complete transcription history with table/text views

### Statistics Panel
- **📊 Metrics**: Total transcriptions, words, characters
- **📈 Averages**: Words per transcription, efficiency metrics
- **⏱️ Timing**: Session duration and activity tracking

## 🚀 Advanced Features

### Batch Processing
- Upload multiple files in sequence
- Process entire folders of audio files
- Export batch results in combined formats

### API Fallback
- Automatically try alternative APIs if primary fails
- Smart error handling with user-friendly messages
- Graceful degradation for network issues

### Performance Optimization
- Efficient audio processing
- Minimal memory usage
- Fast transcription processing
- Responsive UI updates

## 📞 Support

### Getting Help
1. **📖 Check Documentation**: Review this README thoroughly
2. **🔍 Search Issues**: Look for similar problems online
3. **🧪 Test Setup**: Run `python test_setup.py` to verify installation
4. **🎯 Reproduce Issue**: Note exact steps that cause problems
5. **📝 Gather Logs**: Check terminal output for error messages

### Useful Commands
```bash
# Test setup
python test_setup.py

# Check Streamlit version
streamlit --version

# Run with debug info
streamlit run streamlit_app_improved.py --logger.level debug

# Clear Streamlit cache
streamlit cache clear
```

## 🎯 Tips for Best Results

### 🎤 Recording Quality
- **📍 Position**: Speak 6-12 inches from microphone
- **🔇 Environment**: Record in quiet environment
- **🗣️ Speech**: Speak clearly and at moderate pace
- **⏸️ Pauses**: Allow brief pauses between sentences

### 🌐 API Selection
- **🆓 Free Usage**: Start with Google Speech Recognition
- **💼 Business**: Use Google Cloud or Azure for enterprise
- **🎯 Accuracy**: Google Cloud generally most accurate
- **💰 Cost**: Compare pricing for high-volume usage

### 📁 File Formats
- **🥇 Best**: WAV files (uncompressed, high quality)
- **✅ Good**: FLAC (lossless compression)
- **⚠️ Okay**: MP3 (lossy but widely supported)
- **❌ Avoid**: Very low bitrate or heavily compressed files

---

## 🎉 Enjoy Your Speech Recognition Experience!

The Streamlit web interface makes speech recognition accessible and user-friendly. Whether you're transcribing meetings, creating content, or building applications, this tool provides a powerful and flexible solution.

**🚀 Happy Transcribing!**
