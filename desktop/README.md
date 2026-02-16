# Desktop AI Assistant Application

Python-based desktop application that processes voice/text input from mobile, interacts with AI APIs, and sends responses back.

## Features

- gRPC client connecting to relay server
- Speech-to-text (OpenAI Whisper API or local)
- AI processing (OpenAI GPT, Claude API, or local models)
- Text-to-speech (OpenAI TTS or local alternatives)
- Conversation history management
- Pluggable AI backends
- Subagent support for complex workflows

## Prerequisites

- Python 3.10 or higher
- pip
- Virtual environment (recommended)

## Installation

1. Create virtual environment:
   ```bash
   cd desktop
   python -m venv venv
   ```

2. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Generate protobuf code:
   ```bash
   cd ..
   scripts\generate_proto.bat
   ```

5. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Configuration

Edit `.env` file:
- `BACKEND_URL`: gRPC server address
- `USER_ID`: Your user ID (from OAuth)
- `OPENAI_API_KEY`: Your OpenAI API key (optional)
- `ANTHROPIC_API_KEY`: Your Anthropic API key (optional)

## Usage

```bash
python main.py
```

The app will:
1. Connect to the backend relay server
2. Auto-pair with your mobile device
3. Listen for incoming audio/text from phone
4. Process with AI
5. Send responses back to phone

## Architecture

```
Phone → Backend → Desktop App:
                    ├── Audio Receiver
                    ├── Speech-to-Text (Whisper)
                    ├── AI Processor (GPT/Claude/Local)
                    ├── Text-to-Speech
                    └── Response Sender → Backend → Phone
```
