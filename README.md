# AI Voice Assistant System

A distributed AI assistant system with voice and text interaction through mobile devices, powered by cloud AI (OpenAI/Claude) with optional local AI support.

## Architecture

- **Android App**: Voice/text input, transcript display, audio playback
- **Desktop App (Python)**: AI brain - STT, LLM processing, TTS, subagents
- **Backend (Go)**: Minimal relay server for routing, OAuth, conversation storage
- **Database**: PostgreSQL for users and conversation history

## Project Structure

```
/
├── proto/              # Protocol Buffer definitions
├── backend/            # Go gRPC relay server
├── desktop/            # Python desktop AI application
├── android/            # Kotlin Android mobile app
├── shared/             # Shared configuration and utilities
└── docker/             # Docker configurations
```

## Features

- OAuth authentication (Google)
- Auto-pairing: Phone ↔ Desktop (1:1 per user)
- Voice input with speech-to-text (OpenAI Whisper)
- Text input support
- AI processing (OpenAI GPT/Claude API, switchable to local models)
- Text-to-speech (OpenAI TTS / local alternatives)
- Real-time transcript display
- Conversation history storage
- Subagent support for complex desktop workflows

## Technology Stack

- **Backend**: Go, gRPC, PostgreSQL
- **Desktop**: Python, gRPC, OpenAI API, PyQt/Tkinter
- **Android**: Kotlin, gRPC-Kotlin, Jetpack Compose
- **Infrastructure**: Docker, Railway/Render
- **Audio**: Opus codec, OpenAI Whisper, OpenAI TTS

## Getting Started

See individual README files in each subdirectory for setup instructions.
