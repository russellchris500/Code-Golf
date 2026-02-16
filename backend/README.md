# Backend Relay Server

Minimal Go gRPC server that handles:
- OAuth authentication
- Auto-pairing of phone and desktop per user
- Relaying messages between paired devices
- Storing conversation history

## Prerequisites

- Go 1.21 or higher
- PostgreSQL (via Docker or Railway)
- Protocol Buffer compiler

## Installation

1. Install Go from https://go.dev/dl/
2. Install protoc compiler:
   ```bash
   # Windows (using chocolatey)
   choco install protoc

   # Or download from https://github.com/protocolbuffers/protobuf/releases
   ```

3. Install Go protobuf plugins:
   ```bash
   go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
   go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
   ```

## Setup

1. Initialize Go module:
   ```bash
   cd backend
   go mod init github.com/yourusername/agent/backend
   ```

2. Generate protobuf code:
   ```bash
   cd ..
   ./scripts/generate_proto.sh
   ```

3. Install dependencies:
   ```bash
   cd backend
   go mod tidy
   ```

4. Set environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the server:
   ```bash
   go run cmd/server/main.go
   ```

## Environment Variables

- `PORT`: Server port (default: 50051)
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret for signing JWTs
- `GOOGLE_OAUTH_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_OAUTH_CLIENT_SECRET`: Google OAuth client secret
