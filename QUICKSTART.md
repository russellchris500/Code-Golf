# Quick Start Guide

Get the AI Voice Assistant system up and running in minutes.

## What We Built

A **voice-enabled AI assistant system** with:
- 📱 **Android app**: Voice/text input, shows transcript, plays audio responses
- 🖥️ **Desktop app (Python)**: AI brain with STT, LLM processing (OpenAI/Claude), TTS
- ☁️ **Backend (Go)**: Minimal relay server for routing between phone and desktop
- 🗄️ **PostgreSQL**: User accounts and conversation storage

## System Flow

```
📱 User speaks into phone
    ↓
☁️ Backend relays audio to user's desktop
    ↓
🖥️ Desktop: Whisper STT → GPT/Claude → OpenAI TTS
    ↓
☁️ Backend relays response back
    ↓
📱 Phone displays transcript and plays audio
```

## Prerequisites Checklist

- [ ] Windows computer for desktop app
- [ ] Android phone
- [ ] OpenAI API key (https://platform.openai.com/api-keys)
- [ ] Railway or Render account (free tier works)
- [ ] 30 minutes for setup

## Fast Setup (3 Steps)

### Step 1: Install Required Software

**On Windows:**

1. **Install Go**: https://go.dev/dl/ → Download and run installer
2. **Install Python**: https://python.org → Download 3.10+ and run installer
3. **Install protoc**:
   - Download from https://github.com/protocolbuffers/protobuf/releases
   - Extract to `C:\protoc`
   - Add `C:\protoc\bin` to PATH

4. Verify installations:
   ```bash
   go version
   python --version
   protoc --version
   ```

### Step 2: Set Up Backend (Choose one)

#### Option A: Local with Docker (Fastest)

```bash
cd C:\Users\csr\Code\Agent\docker
docker-compose up -d
```

Backend runs at `localhost:50051`

#### Option B: Deploy to Railway (Production)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
cd C:\Users\csr\Code\Agent\backend
railway login
railway init
railway add --plugin postgresql
railway up

# Get your URL
railway open
```

### Step 3: Set Up Desktop App

```bash
cd C:\Users\csr\Code\Agent\desktop

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
copy .env.example .env
notepad .env
```

Edit `.env`:
```
BACKEND_URL=localhost:50051  # or your Railway URL
USER_ID=test-user-123
OPENAI_API_KEY=sk-your-key-here
AI_PROVIDER=openai
```

Run:
```bash
python main.py
```

## Current Status

✅ **Completed:**
- Project structure and monorepo
- Protocol Buffer definitions for gRPC
- Go backend with relay service
- Basic authentication (OAuth to be enhanced)
- Python desktop app with AI integration
- OpenAI Whisper STT
- OpenAI/Claude LLM support
- OpenAI TTS
- Docker setup
- Documentation

🚧 **Next Steps:**
1. **Generate protobuf code**: Run `scripts\generate_proto.bat`
2. **Implement full OAuth**: Add Google OAuth token verification
3. **Build Android app**: Complete mobile application in Kotlin
4. **Test end-to-end**: Phone → Desktop → Phone flow
5. **Add conversation storage**: Save history to PostgreSQL
6. **Encrypt API keys**: Secure user API keys in database

## File Structure

```
Agent/
├── README.md           ← Project overview
├── SETUP.md           ← Detailed setup guide
├── QUICKSTART.md      ← This file
├── proto/             ← gRPC definitions
│   ├── auth.proto
│   └── streaming.proto
├── backend/           ← Go relay server
│   ├── cmd/server/
│   ├── internal/
│   └── pb/           ← Generated protobuf code (after running script)
├── desktop/          ← Python AI app
│   ├── main.py
│   ├── src/
│   │   ├── ai/      ← STT, LLM, TTS
│   │   ├── grpc_client/
│   │   └── config.py
│   └── requirements.txt
├── android/          ← Kotlin mobile app (to be built)
├── docker/           ← Docker setup
│   ├── docker-compose.yml
│   └── Dockerfile.backend
└── scripts/          ← Build scripts
    └── generate_proto.bat
```

## Testing Without Android App

You can test the desktop AI components independently:

```python
# In Python console
from src.ai.stt import create_stt_provider
from src.ai.llm import create_llm_provider
from src.ai.tts import create_tts_provider

# Test STT (with audio file)
stt = create_stt_provider("openai", "your-api-key")
# transcript = stt.transcribe(audio_bytes)

# Test LLM
llm = create_llm_provider("openai", "your-api-key")
from src.ai.llm import Message
response = llm.generate_response([Message("user", "Hello!")])
print(response)

# Test TTS
tts = create_tts_provider("openai", "your-api-key")
audio = tts.synthesize("Hello, this is a test.")
# Play or save audio
```

## Immediate Next Actions

**To get the system working:**

1. **Generate protobuf code**:
   ```bash
   cd C:\Users\csr\Code\Agent
   scripts\generate_proto.bat
   ```

2. **Install Go dependencies**:
   ```bash
   cd backend
   go mod download
   ```

3. **Start backend** (if using Docker):
   ```bash
   cd docker
   docker-compose up
   ```

4. **Start desktop app**:
   ```bash
   cd desktop
   venv\Scripts\activate
   python main.py
   ```

5. **Build Android app** (see android/README.md)

## Getting Help

- **Backend issues**: Check [backend/README.md](backend/README.md)
- **Desktop issues**: Check [desktop/README.md](desktop/README.md)
- **Android issues**: Check [android/README.md](android/README.md)
- **Full setup**: See [SETUP.md](SETUP.md)

## Architecture Decisions

**Why this architecture?**
- **Desktop does AI processing**: More powerful hardware, easier to switch AI providers, keeps user API keys local
- **Backend is minimal relay**: Scalable, simple, just routes packets
- **1:1 pairing**: Each user has their own desktop and phone, auto-paired by user ID
- **Pluggable AI**: Easy to switch between OpenAI, Claude, or local models

**Scaling path:**
- Phase 1 (MVP): Single backend server, ~100 users
- Phase 2: Multiple backend servers + Redis pub/sub
- Phase 3: Microservices architecture with message brokers

## Cost Estimates

**Development/Testing (per month):**
- Railway/Render backend: $0 (free tier)
- OpenAI API: $5-20 (depending on usage)
- **Total**: ~$5-20/month

**Production (per 1000 users):**
- Backend hosting: $20-50
- Database: $15-30
- OpenAI API (user-paid): $0 for you
- **Total**: ~$35-80/month

## What Makes This Project Scalable

1. **Stateless backend**: Can add more servers easily
2. **gRPC**: Efficient binary protocol
3. **User-provided API keys**: No centralized AI costs
4. **Minimal relay**: Backend doesn't process AI, just routes
5. **Protocol Buffers**: Versioned API contracts
6. **Docker**: Easy deployment and scaling

Enjoy building your AI voice assistant! 🚀
