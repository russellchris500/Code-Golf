# Setup Instructions

Complete guide to set up and run the AI Voice Assistant system.

## Prerequisites

### Required Software

1. **Go 1.21+** - Download from https://go.dev/dl/
2. **Python 3.10+** - Download from https://python.org/downloads/
3. **Node.js 18+** (for protobuf tools) - Download from https://nodejs.org/
4. **Protocol Buffer Compiler** - Download from https://github.com/protocolbuffers/protobuf/releases
5. **Docker Desktop** (optional, for local backend) - Download from https://docker.com/
6. **Android Studio** (for Android app) - Download from https://developer.android.com/studio

### API Keys Needed

- **OpenAI API Key** (if using OpenAI): https://platform.openai.com/api-keys
- **Anthropic API Key** (if using Claude): https://console.anthropic.com/
- **Google OAuth Credentials**: https://console.cloud.google.com/

## Step 1: Install Go

1. Download Go installer for Windows from https://go.dev/dl/
2. Run the installer
3. Verify installation:
   ```bash
   go version
   ```

## Step 2: Install Protocol Buffer Compiler

### Windows

1. Download the latest release from https://github.com/protocolbuffers/protobuf/releases
2. Look for `protoc-<version>-win64.zip`
3. Extract to `C:\protoc`
4. Add `C:\protoc\bin` to your PATH environment variable
5. Verify installation:
   ```bash
   protoc --version
   ```

### Install Go protobuf plugins

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

## Step 3: Generate Protocol Buffer Code

```bash
cd C:\Users\csr\Code\Agent
scripts\generate_proto.bat
```

This will generate:
- Go code in `backend/pb/`
- Python code in `desktop/` (generated files will be imported by the app)

## Step 4: Set Up Backend

### Option A: Using Docker (Recommended for development)

1. Make sure Docker Desktop is running

2. Start the backend and database:
   ```bash
   cd docker
   docker-compose up -d
   ```

3. Check logs:
   ```bash
   docker-compose logs -f backend
   ```

4. Backend will be available at `localhost:50051`

### Option B: Manual Setup

1. Install PostgreSQL locally

2. Create database:
   ```sql
   CREATE DATABASE agent_db;
   CREATE USER agent_user WITH PASSWORD 'agent_password';
   GRANT ALL PRIVILEGES ON DATABASE agent_db TO agent_user;
   ```

3. Configure backend:
   ```bash
   cd backend
   copy .env.example .env
   # Edit .env with your database URL
   ```

4. Install dependencies:
   ```bash
   go mod download
   ```

5. Run backend:
   ```bash
   go run cmd/server/main.go
   ```

## Step 5: Set Up Desktop App

1. Create virtual environment:
   ```bash
   cd desktop
   python -m venv venv
   ```

2. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure app:
   ```bash
   copy .env.example .env
   ```

5. Edit `.env` and add:
   - Your OpenAI API key (or Anthropic key)
   - Backend URL (localhost:50051 for local development)
   - User ID (you'll get this after OAuth is implemented)

6. Run desktop app:
   ```bash
   python main.py
   ```

## Step 6: Set Up Android App

*Android app structure will be created next*

1. Open Android Studio
2. Open the `android` folder as a project
3. Sync Gradle dependencies
4. Configure OAuth credentials in the app
5. Build and run on device or emulator

## Step 7: Deploy Backend to Railway

### Create Railway Account

1. Go to https://railway.app/
2. Sign up with GitHub
3. Create new project

### Deploy Backend

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize project:
   ```bash
   cd backend
   railway init
   ```

4. Add PostgreSQL:
   ```bash
   railway add --plugin postgresql
   ```

5. Set environment variables:
   ```bash
   railway variables set JWT_SECRET=your-secret-key
   railway variables set ENV=production
   ```

6. Deploy:
   ```bash
   railway up
   ```

7. Get the public URL:
   ```bash
   railway open
   ```

8. Update desktop and Android app `.env` with the Railway URL

## Testing the System

### Test Backend

```bash
# Install grpcurl for testing
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest

# List services
grpcurl -plaintext localhost:50051 list

# Test auth (once OAuth is implemented)
grpcurl -plaintext -d '{"provider":"google","oauth_token":"test"}' localhost:50051 assistant.auth.AuthService/AuthenticateOAuth
```

### Test Desktop App

1. Make sure backend is running
2. Run desktop app
3. Check logs for connection status

### Test Full Flow (after Android app is built)

1. Start backend
2. Start desktop app
3. Launch Android app
4. Login with Google OAuth on both
5. Send voice message from phone
6. Check desktop logs for processing
7. Receive response on phone

## Troubleshooting

### Backend won't start

- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Check port 50051 is not in use

### Desktop app can't connect

- Verify backend is running
- Check BACKEND_URL in desktop/.env
- For Railway deployment, ensure URL uses correct protocol (with/without TLS)

### Audio not working

- Check microphone permissions on phone
- Verify OpenAI API key is valid
- Check audio format compatibility

### gRPC errors

- Ensure protobuf code is generated
- Check that all proto imports are correct
- Verify gRPC versions match across client and server

## Next Steps

- [ ] Implement full Google OAuth flow
- [ ] Build Android application
- [ ] Add conversation history storage
- [ ] Implement API key encryption
- [ ] Add more AI providers
- [ ] Build web dashboard for monitoring
- [ ] Add tests
