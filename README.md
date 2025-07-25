# Improved Speech Recognition App

A comprehensive Python-based speech recognition application with multiple API support, language selection, pause/resume functionality, and file saving capabilities.

## Features

### 🎯 Core Features
- **Multiple Speech Recognition APIs**: Support for Google, Google Cloud, Wit.ai, Microsoft Azure, and Bing
- **Language Selection**: 13+ supported languages including English, Spanish, French, German, Chinese, Japanese, and more
- **Pause/Resume**: Control speech recognition process with pause and resume functionality
- **Save Transcriptions**: Export transcriptions to both TXT and JSON formats
- **Enhanced Error Handling**: Meaningful error messages with suggestions for resolution
- **Configuration Persistence**: Settings and API keys are saved automatically

### 🌍 Supported Languages
- English (US/UK)
- Spanish (Spain/Mexico)
- French
- German
- Italian
- Portuguese (Brazil)
- Russian
- Japanese
- Korean
- Chinese (Simplified)
- Arabic

### 🔧 Supported APIs
1. **Google Speech Recognition** (Free, no API key required)
2. **Google Cloud Speech** (Requires API key)
3. **Wit.ai** (Requires API key)
4. **Microsoft Azure Speech** (Requires API key)
5. **Microsoft Bing Voice Recognition** (Requires API key)

## Installation

### Prerequisites
- Python 3.7 or higher
- A working microphone
- Internet connection (for cloud-based APIs)

### System Dependencies (Linux/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip portaudio19-dev
```

### System Dependencies (macOS)
```bash
brew install portaudio
```

### System Dependencies (Windows)
PyAudio wheels are available for Windows, so no additional system dependencies are typically required.

### Python Dependencies
```bash
pip install -r requirements.txt
```

### Alternative Installation (if PyAudio fails)
If you encounter issues with PyAudio installation:

**Linux:**
```bash
sudo apt-get install python3-pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

## Usage

### Running the Application
```bash
python3 speech_recognition_app.py
```

### Main Menu Options
1. **Start Speech Recognition** - Begin listening and transcribing speech
2. **Select Speech Recognition API** - Choose from available APIs
3. **Select Language** - Choose recognition language
4. **View Current Transcription** - Display all transcribed text
5. **Save Transcription to File** - Export transcriptions
6. **Clear Transcription** - Remove all transcribed text
7. **Settings & Configuration** - View current settings
8. **Help** - Display help information
0. **Exit** - Close the application

### During Speech Recognition
- Type `p` + Enter to **pause** recognition
- Type `r` + Enter to **resume** recognition
- Type `q` + Enter to **quit** recognition
- Press `Ctrl+C` to force stop

## Configuration

### API Keys Setup
The application will prompt you to enter API keys when selecting APIs that require them. Keys are automatically saved in `config.json`.

#### Getting API Keys

**Google Cloud Speech:**
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Speech-to-Text API
3. Create credentials (API key or service account)

**Wit.ai:**
1. Visit [Wit.ai](https://wit.ai/)
2. Create an app
3. Copy the Server Access Token

**Microsoft Azure Speech:**
1. Visit [Azure Portal](https://portal.azure.com/)
2. Create a Speech service resource
3. Copy the API key from Keys and Endpoint

**Microsoft Bing Voice Recognition:**
1. Visit [Microsoft Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/)
2. Subscribe to Bing Speech API
3. Copy the subscription key

### Configuration File
Settings are automatically saved in `config.json`:
```json
{
  "api_keys": {
    "google_cloud": "your-google-cloud-key",
    "wit": "your-wit-ai-key",
    "azure": "your-azure-key",
    "bing": "your-bing-key"
  },
  "default_api": "google",
  "default_language": "en-US"
}
```

## Output Files

### Transcription Files
When saving transcriptions, two files are created:
- `transcription_YYYYMMDD_HHMMSS.txt` - Human-readable format
- `transcription_YYYYMMDD_HHMMSS.json` - Machine-readable format with metadata

### JSON Format Example
```json
[
  {
    "timestamp": "14:30:25",
    "text": "Hello, this is a test transcription.",
    "api": "google",
    "language": "en-US"
  }
]
```

## Error Handling

The application provides enhanced error handling with meaningful messages:

- **Network Issues**: Suggestions to check internet connection
- **API Quota Exceeded**: Recommendations to check quotas or try different APIs
- **Authentication Errors**: Guidance on API key configuration
- **Audio Issues**: Microphone setup troubleshooting

## Troubleshooting

### Common Issues

**1. PyAudio Installation Failed**
```bash
# Linux
sudo apt-get install python3-dev python3-pip portaudio19-dev

# macOS
brew install portaudio

# Windows
pip install pipwin
pipwin install pyaudio
```

**2. Microphone Not Working**
- Check system audio settings
- Ensure microphone permissions are granted
- Test microphone with other applications

**3. API Errors**
- Verify API keys are correct
- Check internet connection
- Ensure API quotas are not exceeded

**4. Recognition Not Working**
- Speak clearly and close to microphone
- Check selected language matches spoken language
- Try different APIs if one fails

### Dependencies Issues

If you encounter issues with specific packages:

```bash
# Reinstall speech_recognition
pip uninstall speech_recognition
pip install speech_recognition

# For Google Cloud Speech issues
pip install google-cloud-speech

# For Azure Speech issues
pip install azure-cognitiveservices-speech
```

## Development

### Project Structure
```
Speech-Recognition-App/
├── speech_recognition_app.py  # Main application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── config.json              # Configuration (created automatically)
└── transcription_*.txt      # Saved transcriptions
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Testing
To test the application:
1. Run with different APIs
2. Test with different languages
3. Verify pause/resume functionality
4. Test file saving features
5. Test error handling scenarios

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Review error messages for suggestions
3. Consult API documentation for specific services
4. Join the community discussions

## Changelog

### Version 2.0 (Current)
- ✅ Multiple API support (Google, Google Cloud, Wit.ai, Azure, Bing)
- ✅ Enhanced error handling with meaningful messages
- ✅ File saving functionality (TXT and JSON formats)
- ✅ Language selection (13+ languages)
- ✅ Pause/resume functionality
- ✅ Configuration persistence
- ✅ Improved user interface
- ✅ Background audio processing
- ✅ Comprehensive documentation

## Future Enhancements

Potential future improvements:
- Real-time audio visualization
- Custom vocabulary/phrases
- Audio file transcription
- Batch processing
- Web interface
- Voice activity detection
- Custom model training support
