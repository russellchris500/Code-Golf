# System Architecture

Complete architecture documentation for the AI Voice Assistant system.

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Ecosystem                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                            ┌──────────────┐  │
│  │   Android    │◄──────────────────────────►│   Desktop    │  │
│  │     Phone    │      1:1 Auto-Paired       │   (Windows)  │  │
│  │              │                             │              │  │
│  │ - Voice      │                             │ - AI Brain   │  │
│  │ - Text       │                             │ - STT/LLM    │  │
│  │ - Transcript │                             │ - TTS        │  │
│  └──────┬───────┘                             └──────┬───────┘  │
│         │                                            │          │
│         │ gRPC/TLS                       gRPC/TLS   │          │
│         │                                            │          │
│         └────────────────┬───────────────────────────┘          │
│                          │                                       │
└──────────────────────────┼───────────────────────────────────────┘
                           │
                           │
                    ┌──────▼──────┐
                    │   Backend   │
                    │   (Go)      │
                    │             │
                    │ - Relay     │
                    │ - OAuth     │
                    │ - Minimal   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ PostgreSQL  │
                    │             │
                    │ - Users     │
                    │ - Sessions  │
                    │ - History   │
                    └─────────────┘
```

## Data Flow

### Voice Interaction Flow

```
1. USER SPEAKS
   └─► Android: AudioRecorder captures voice
        └─► Encode to Opus
             └─► gRPC Stream (Packet.audio)
                  └─► Backend: Relay receives
                       └─► Route to Desktop
                            └─► Desktop: Receive audio
                                 ├─► OpenAI Whisper: Audio → Text
                                 │    └─► Transcript
                                 ├─► Send transcript back to phone
                                 │    └─► Backend → Phone: Display transcript
                                 ├─► OpenAI GPT: Generate response
                                 │    └─► Response text
                                 └─► OpenAI TTS: Text → Audio
                                      └─► gRPC Stream (Packet.audio)
                                           └─► Backend: Relay receives
                                                └─► Route to Phone
                                                     └─► Phone: Play audio

2. USER HEARS RESPONSE
```

### Text Interaction Flow

```
1. USER TYPES
   └─► Android: Text input
        └─► gRPC Stream (Packet.text)
             └─► Backend: Relay receives
                  └─► Route to Desktop
                       └─► Desktop: Process text
                            └─► OpenAI GPT: Generate response
                                 └─► gRPC Stream (Packet.text)
                                      └─► Backend: Relay receives
                                           └─► Route to Phone
                                                └─► Phone: Display text

2. USER READS RESPONSE
```

## Component Details

### Android App (Kotlin)

**Responsibilities:**
- Capture voice input
- Display transcript in real-time
- Show text messages
- Play audio responses
- Handle authentication

**Tech Stack:**
- Kotlin
- Jetpack Compose (UI)
- gRPC-Kotlin
- Google OAuth
- AudioRecord/AudioTrack

**Key Classes:**
```
MainActivity
├── ChatViewModel
│   ├── GrpcClient
│   ├── AudioRecorder
│   └── AudioPlayer
├── AuthViewModel
│   └── AuthManager
└── Screens
    ├── LoginScreen
    ├── ChatScreen
    └── SettingsScreen
```

### Desktop App (Python)

**Responsibilities:**
- Receive audio/text from phone
- Speech-to-text conversion
- AI processing (GPT/Claude)
- Text-to-speech synthesis
- Send responses back
- Manage conversation context

**Tech Stack:**
- Python 3.10+
- gRPC Python
- OpenAI API
- Anthropic API
- PyAudio (optional for local audio)

**Key Modules:**
```
main.py
├── AIAssistant
│   ├── STTProvider (OpenAI/Local)
│   ├── LLMProvider (OpenAI/Anthropic/Local)
│   └── TTSProvider (OpenAI/Local)
├── GRPCClient
│   └── Bidirectional streaming
└── Config
    └── Environment-based configuration
```

### Backend Server (Go)

**Responsibilities:**
- Relay packets between paired devices
- Authenticate users (OAuth)
- Manage device sessions
- Store conversation history
- Handle reconnections

**Tech Stack:**
- Go 1.21+
- gRPC
- PostgreSQL
- JWT authentication

**Key Components:**
```
main.go
├── AuthService
│   ├── OAuth verification
│   ├── JWT generation
│   └── Token validation
├── StreamingService
│   └── Bidirectional streaming
├── RelayManager
│   ├── Device registration
│   ├── Packet routing
│   └── Connection management
└── Database
    ├── User management
    ├── Session tracking
    └── Conversation storage
```

## Protocol Buffers

### Message Types

**Packet** (main message):
- `packet_id`: Unique identifier
- `user_id`: User identifier
- `source`: MOBILE or DESKTOP
- `destination`: MOBILE or DESKTOP
- `type`: AUDIO_CHUNK, TEXT_MESSAGE, TRANSCRIPT, CONTROL
- `payload`: Actual data (oneof)

**AudioData**:
- `data`: Audio bytes
- `format`: PCM, OPUS, AAC
- `sample_rate`: e.g., 16000
- `channels`: 1 (mono) or 2 (stereo)
- `is_final`: Last chunk indicator

**TextData**:
- `text`: Message content
- `text_type`: USER_INPUT or AI_RESPONSE

**TranscriptData**:
- `text`: Transcribed text
- `is_final`: Complete or partial
- `confidence`: Recognition confidence

## Security

### Authentication Flow

```
1. User opens Android app
   └─► Google OAuth login
        └─► Get OAuth token
             └─► Send to Backend
                  └─► Backend verifies with Google
                       └─► Create/get user in DB
                            └─► Generate JWT
                                 └─► Return to app
                                      └─► Store JWT locally

2. Desktop app starts
   └─► User logs in (same process)
        └─► Gets JWT

3. gRPC connections
   └─► Include JWT in metadata
        └─► Backend validates JWT
             └─► Allow connection
```

### Data Security

- **In Transit**: TLS encryption for all gRPC connections
- **At Rest**: Encrypted API keys in PostgreSQL
- **Authentication**: JWT with short expiration (24h)
- **API Keys**: User-provided, stored encrypted

## Database Schema

```sql
users
  - id (UUID, PK)
  - email
  - oauth_provider
  - oauth_subject
  - created_at

user_api_keys
  - user_id (FK)
  - encrypted_keys (JSONB)

device_sessions
  - user_id (FK)
  - device_type (mobile/desktop)
  - session_id
  - last_seen

conversations
  - id (UUID, PK)
  - user_id (FK)
  - created_at

conversation_turns
  - id (UUID, PK)
  - conversation_id (FK)
  - role (user/assistant)
  - content
  - created_at
```

## Scaling Strategy

### Phase 1: MVP (1-100 users)
```
Single Server:
- 1 VM running backend
- 1 PostgreSQL instance
- Cost: $10-20/month
```

### Phase 2: Growth (100-10K users)
```
┌──────────────┐
│Load Balancer │
└──────┬───────┘
       │
   ┌───┴───┬───────┐
   │       │       │
┌──▼──┐ ┌──▼──┐ ┌──▼──┐
│gRPC │ │gRPC │ │gRPC │
│Srv 1│ │Srv 2│ │Srv 3│
└──┬──┘ └──┬──┘ └──┬──┘
   │       │       │
   └───┬───┴───┬───┘
       │       │
   ┌───▼───┐ ┌─▼──────┐
   │ Redis │ │Postgres│
   │Pub/Sub│ │        │
   └───────┘ └────────┘

Cost: $100-500/month
```

### Phase 3: Scale (10K+ users)
```
API Gateway → Auth Service
           → Streaming Service (multiple)
           → Message Broker (Kafka)
           → PostgreSQL (primary + replicas)
           → Redis Cache
           → S3 (audio storage)

Cost: $1K-5K+/month
```

## Error Handling

### Connection Loss

**Phone disconnects:**
1. Backend detects closed stream
2. Unregisters mobile device
3. Desktop continues running
4. Phone reconnects → auto-pair resumes

**Desktop disconnects:**
1. Backend detects closed stream
2. Unregisters desktop device
3. Phone shows "Desktop offline"
4. Desktop reconnects → auto-pair resumes

### API Failures

**OpenAI/Anthropic API error:**
1. Desktop catches exception
2. Logs error
3. Sends error message to phone
4. User sees friendly error
5. Option to retry

### Backend Failures

**Backend crashes:**
1. Railway auto-restarts
2. Clients reconnect automatically
3. Resume from where they left off

## Performance Considerations

### Latency Targets

- **Phone to Desktop**: < 100ms
- **Speech-to-Text**: 1-3 seconds
- **LLM Response**: 2-5 seconds
- **Text-to-Speech**: 1-2 seconds
- **Total Round Trip**: 4-10 seconds

### Optimization Strategies

1. **Audio Streaming**: Send audio in chunks, don't wait for complete recording
2. **Connection Pooling**: Reuse gRPC connections
3. **Caching**: Cache common responses
4. **Compression**: Use Opus codec for audio (efficient compression)
5. **Concurrent Processing**: Process STT while user is still speaking

## Development vs Production

### Development
- No TLS (plaintext gRPC)
- Local PostgreSQL
- Mock OAuth
- Console logging

### Production
- TLS enabled
- Railway PostgreSQL
- Real OAuth verification
- Structured logging
- Error monitoring (Sentry)
- Metrics (Prometheus)

## Future Enhancements

1. **Web Interface**: Browser-based chat
2. **Subagents**: Multiple specialized AI assistants
3. **Voice Activation**: "Hey Assistant" wake word
4. **Multi-language**: Support for languages beyond English
5. **Conversation Search**: Full-text search in history
6. **Sharing**: Share conversations between users
7. **Analytics Dashboard**: Usage statistics for users

## Code Organization

```
Agent/
├── proto/              # Protocol definitions (shared)
├── backend/            # Go server
│   ├── cmd/           # Entry points
│   ├── internal/      # Business logic
│   │   ├── auth/
│   │   ├── streaming/
│   │   ├── relay/
│   │   └── database/
│   └── pb/            # Generated code
├── desktop/            # Python app
│   ├── src/
│   │   ├── ai/        # AI providers
│   │   ├── grpc_client/
│   │   └── config.py
│   └── main.py
├── android/            # Kotlin app
│   └── app/src/main/java/com/assistant/mobile/
├── docker/             # Containerization
└── scripts/            # Build scripts
```

This architecture is designed to be simple initially but scale to millions of users! 🚀
