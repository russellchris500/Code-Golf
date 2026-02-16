# Next Steps - Action Plan

Your AI Voice Assistant foundation is built! Here's what to do next.

## Immediate Actions (Do These First)

### 1. Install Go (if not already installed)

```bash
# Download from https://go.dev/dl/
# After installation, verify:
go version
```

### 2. Install Protocol Buffer Compiler

**Windows:**
1. Download from https://github.com/protocolbuffers/protobuf/releases
2. Look for `protoc-XX.X-win64.zip`
3. Extract to `C:\protoc`
4. Add `C:\protoc\bin` to PATH
5. Verify: `protoc --version`

### 3. Install Go Protobuf Plugins

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

Add Go bin to PATH if needed: `%USERPROFILE%\go\bin`

### 4. Generate Protobuf Code

```bash
cd C:\Users\csr\Code\Agent
scripts\generate_proto.bat
```

This generates:
- `backend/pb/auth/*.pb.go`
- `backend/pb/streaming/*.pb.go`
- `desktop/auth_pb2.py` and `streaming_pb2.py`

### 5. Install Backend Dependencies

```bash
cd backend
go mod download
```

## Testing the Backend

### Option 1: Docker (Easiest)

```bash
cd docker
docker-compose up
```

Backend will run on `localhost:50051` with PostgreSQL.

### Option 2: Manual

1. Install and start PostgreSQL locally
2. Create database:
   ```sql
   CREATE DATABASE agent_db;
   ```
3. Update `backend/.env`:
   ```bash
   copy .env.example .env
   # Edit DATABASE_URL
   ```
4. Run:
   ```bash
   cd backend
   go run cmd/server/main.go
   ```

## Testing the Desktop App

```bash
cd desktop
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
# Edit .env with your OpenAI key

python main.py
```

## Critical TODOs

### Backend

- [ ] **Fix protobuf imports in Go files**: After generating code, update import paths
- [ ] **Implement full OAuth**: Currently using mock auth
  - Add Google OAuth token verification
  - Implement token validation with Google
- [ ] **API key encryption**: Encrypt user API keys in database
- [ ] **Conversation storage**: Complete database save/retrieve functions

### Desktop

- [ ] **Update gRPC client**: Uncomment protobuf imports after generation
- [ ] **Test audio pipeline**: Record audio → STT → LLM → TTS
- [ ] **Add error handling**: Retry logic, connection recovery
- [ ] **Implement conversation saving**: Send history to backend

### Android

- [ ] **Create Android Studio project**: Set up Gradle and dependencies
- [ ] **Implement UI**: LoginScreen, ChatScreen, SettingsScreen
- [ ] **Add Google OAuth**: Login flow
- [ ] **Audio recording**: Use AudioRecord API
- [ ] **gRPC client**: Streaming connection to backend
- [ ] **Audio playback**: Play TTS responses

### Infrastructure

- [ ] **Deploy to Railway**: Follow SETUP.md Railway section
- [ ] **Set up OAuth credentials**: Google Cloud Console
- [ ] **Configure TLS**: For production security
- [ ] **Add monitoring**: Logging and metrics

## Development Workflow

**Daily development:**

1. Start backend:
   ```bash
   cd docker && docker-compose up
   ```

2. Start desktop app:
   ```bash
   cd desktop
   venv\Scripts\activate
   python main.py
   ```

3. Work on Android app in Android Studio

**Testing changes:**

1. Update `.proto` files if needed
2. Regenerate code: `scripts\generate_proto.bat`
3. Rebuild backend: `go build`
4. Restart services

## Known Issues to Fix

### Backend

1. **Import paths in generated code**: May need to adjust after protoc generation
2. **OAuth verification**: Currently mocked, needs real Google token validation
3. **API key storage**: Not encrypted, needs proper encryption

### Desktop

1. **gRPC imports**: Commented out until protobuf is generated
2. **Audio format**: Need to decide on PCM vs Opus encoding
3. **Error handling**: Basic implementation, needs improvement

### Android

1. **Project not created yet**: Need to set up Android Studio project
2. **No UI**: Need to implement Compose screens

## Quick Verification Tests

### Test Backend Connectivity

```bash
# Install grpcurl
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest

# Test connection
grpcurl -plaintext localhost:50051 list

# Should see:
# assistant.auth.AuthService
# assistant.streaming.StreamingService
```

### Test Desktop AI (without gRPC)

```python
# In Python console from desktop directory
from src.ai.llm import create_llm_provider, Message

llm = create_llm_provider("openai", "your-key", "gpt-4-turbo-preview")
response = llm.generate_response([Message("user", "Hello!")])
print(response)
```

## Project Milestones

### Milestone 1: Backend + Desktop Working ✅ (Current)
- [x] Backend relay server
- [x] Desktop AI processing
- [ ] Generate and test protobuf
- [ ] End-to-end desktop testing

### Milestone 2: Android App (Next)
- [ ] Android project setup
- [ ] OAuth login
- [ ] Voice recording
- [ ] gRPC connection
- [ ] UI implementation

### Milestone 3: Full Integration
- [ ] Phone → Desktop → Phone flow working
- [ ] Conversation history saved
- [ ] Multiple users supported

### Milestone 4: Production Ready
- [ ] Deployed to Railway
- [ ] Full OAuth implemented
- [ ] API keys encrypted
- [ ] Error handling robust
- [ ] Testing complete

## Resources

- **gRPC Go Tutorial**: https://grpc.io/docs/languages/go/quickstart/
- **gRPC Python**: https://grpc.io/docs/languages/python/
- **OpenAI API Docs**: https://platform.openai.com/docs
- **Anthropic API**: https://docs.anthropic.com/
- **Jetpack Compose**: https://developer.android.com/jetpack/compose
- **Railway Docs**: https://docs.railway.app/

## Getting Unstuck

**If protobuf generation fails:**
- Check `protoc --version` works
- Verify Go plugins are installed and in PATH
- Check proto file syntax

**If backend won't start:**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Check port 50051 is available

**If desktop can't connect:**
- Ensure backend is running
- Check BACKEND_URL matches backend address
- For Railway, use the public URL

**If OpenAI API errors:**
- Verify API key is valid
- Check you have credits in your account
- Ensure correct model names

## Support

Created files for reference:
- `README.md` - Project overview
- `SETUP.md` - Detailed setup instructions
- `QUICKSTART.md` - Fast start guide
- `NEXT_STEPS.md` - This file
- `backend/README.md` - Backend specifics
- `desktop/README.md` - Desktop app details
- `android/README.md` - Android app guide

Start with generating protobuf code, then test the backend! 🚀
