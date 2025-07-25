# 🎤 Speech Recognition App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://speech-recognition-app.streamlit.app)

A comprehensive speech recognition application with multiple API support, built with Python and Streamlit.

## 🌟 Features

- **🔄 Multiple APIs**: Google, Google Cloud, Wit.ai, Microsoft Azure, Bing
- **🌍 Multi-language**: 13+ supported languages
- **🎤 Web Interface**: Modern Streamlit-based UI
- **📱 Audio Recording**: Browser-based recording
- **📁 File Upload**: Support for WAV, MP3, FLAC, M4A, OGG
- **💾 Export Options**: TXT, JSON, CSV formats
- **⏸️ Pause/Resume**: Control recording process
- **📊 Statistics**: Track transcriptions and usage

## 🚀 Quick Start

### 🌐 Try it Online
👉 **[Launch Streamlit App](https://speech-recognition-app.streamlit.app)**

### 💻 Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JohnHika/Speech-Recognition-App.git
   cd Speech-Recognition-App
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app_improved.py
   ```

4. **Or run the command-line version:**
   ```bash
   python speech_recognition_app.py
   ```

## 📋 Requirements

- Python 3.7+
- Microphone (for recording)
- Internet connection (for cloud APIs)

## 🔧 API Configuration

### Free Option (No API key needed)
- **Google Speech Recognition**: Works out of the box

### Premium Options (API key required)
- **Google Cloud Speech**: Get key from [Google Cloud Console](https://console.cloud.google.com/)
- **Wit.ai**: Get key from [Wit.ai](https://wit.ai/)
- **Microsoft Azure**: Get key from [Azure Portal](https://portal.azure.com/)
- **Microsoft Bing**: Get key from [Microsoft Cognitive Services](https://azure.microsoft.com/services/cognitive-services/)

## 🌍 Supported Languages

English (US/UK), Spanish (Spain/Mexico), French, German, Italian, Portuguese (Brazil), Russian, Japanese, Korean, Chinese (Simplified), Arabic, and more!

## 📖 Documentation

- **[Complete Documentation](README.md)** - Detailed setup and usage guide
- **[Streamlit Guide](STREAMLIT_README.md)** - Web interface documentation

## 🎯 Use Cases

- **📝 Content Creation**: Dictate blog posts and articles
- **🎓 Education**: Transcribe lectures and meetings
- **💼 Business**: Convert voice memos to text
- **🌐 Accessibility**: Support for hearing-impaired users
- **🔬 Research**: Transcribe interviews and recordings

## 🛠️ Files Overview

### For Streamlit Cloud Deployment:
- `streamlit_app_improved.py` - **Main Streamlit app (recommended)**
- `requirements.txt` - Dependencies

### Alternative versions:
- `streamlit_app.py` - Basic Streamlit version
- `speech_recognition_app.py` - Command-line interface

### Setup files:
- `setup.sh` - Automated setup script
- `test_setup.py` - System verification
- `demo.py` - Feature demonstration

## 🚀 Deploy to Streamlit Cloud

1. **Fork this repository**
2. **Visit [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Connect your GitHub account**
4. **Select this repository**
5. **Set main file to:** `streamlit_app_improved.py`
6. **Deploy!**

## 📊 Project Structure

```
Speech-Recognition-App/
├── streamlit_app_improved.py    # 🌟 Main Streamlit app
├── streamlit_app.py             # Basic Streamlit version
├── speech_recognition_app.py    # Command-line interface
├── requirements.txt             # Dependencies
├── README.md                    # This file
├── STREAMLIT_README.md          # Detailed Streamlit docs
└── setup/                       # Setup scripts
```

## 💡 Tips for Best Results

- **🎤 Audio Quality**: Speak clearly, 6-12 inches from microphone
- **🔇 Environment**: Record in quiet environment
- **🌐 API Choice**: Start with Google (free), upgrade to Google Cloud for better accuracy
- **📁 File Format**: Use WAV for best quality, MP3 for compatibility

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⭐ Support

If you find this project helpful, please give it a star ⭐ on GitHub!

---

**Built with ❤️ using Python and Streamlit**
