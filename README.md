# Ziva AI Agent

An intelligent voice-activated AI assistant built with Python, featuring speech recognition, natural language processing, and a modern PyQt5 graphical interface.

## Features

- **Voice Interaction**: Speech-to-text and text-to-speech capabilities using edge-tts
- **AI Decision Making**: Powered by Cohere's AI model for intelligent query classification
- **Real-time Search**: Integrated web search for up-to-date information
- **Task Automation**: Open/close applications, play music, system controls
- **Image Generation**: AI-powered image generation capabilities
- **Modern GUI**: Beautiful PyQt5 interface with animated graphics
- **Multi-threading**: Concurrent execution for responsive performance

## Tech Stack

- **Python 3.13+**
- **PyQt5**: Graphical user interface
- **Pygame**: Audio playback
- **Edge-tts**: Text-to-speech conversion
- **Cohere AI**: Natural language processing and decision making
- **SpeechRecognition**: Voice input processing
- **Rich**: Terminal formatting

## Project Structure

```
ziva-ai-agent/
├── Backend/
│   ├── Automation.py      # Task automation
│   ├── Chatboat.py        # AI chatbot
│   ├── ImageGeneration.py # Image generation
│   ├── Model.py           # Decision-making model
│   ├── RealtimeSearchEngine.py # Web search
│   ├── SpeechToText.py    # Voice recognition
│   └── TextToSpeech.py    # Text-to-speech
├── Frontend/
│   ├── Files/            # Temporary data files
│   ├── Graphics/          # UI assets
│   └── GUI.py             # PyQt5 interface
├── Data/                  # Chat logs and media
├── Main.py                # Entry point
├── Requirements.txt       # Dependencies
└── .env                   # Environment variables
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AnmolGhill/ziva-ai-agent.git
cd ziva-ai-agent
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r Requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the root directory with the following:
```
Username=YourName
Assistantname=Ziva
AssistantVoice=en-US-AriaNeural
CohereAPIKey=your_cohere_api_key_here
```

## Usage

Run the application:
```bash
python Main.py
```

### Voice Commands

- **General queries**: "How are you?", "What is Python?"
- **Real-time search**: "What's today's news?", "Who is the current president?"
- **Open apps**: "Open Chrome", "Open Telegram"
- **Close apps**: "Close Notepad", "Close Facebook"
- **Play music**: "Play [song name]"
- **System controls**: "Volume up", "Mute"
- **Generate images**: "Generate image of a lion"
- **Set reminders**: "Set a reminder at 9pm for my meeting"
- **Exit**: "Bye Ziva"

## Configuration

### Voice Settings
Edit the `.env` file to change the assistant voice. Available voices can be found in the edge-tts documentation.

### API Keys
You need a Cohere API key for the AI decision-making model. Get one from [Cohere](https://cohere.com/).

## Requirements

- Windows 10/11 (primary target)
- Python 3.13 or higher
- Microphone for voice input
- Speakers for audio output
- Internet connection for AI services

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

**AnmolGhill**

## Acknowledgments

- Built with inspiration from AI assistant projects
- Powered by Cohere AI and Edge TTS
- UI designed with PyQt5

---

**Note**: This is a personal project for educational and demonstration purposes.
