# Testing the Backend

Quick guide to test that the backend server is working.

## ✅ Status

- [x] Protobuf code generated
- [x] Backend compiled successfully
- [x] Dependencies installed

## Option 1: Test with Docker (Recommended)

This will start both the backend server and PostgreSQL database.

```bash
cd docker
docker-compose up
```

You should see:
```
agent_backend  | 🚀 gRPC server starting on 0.0.0.0:50051
agent_backend  | Database connection established
agent_backend  | Database schema initialized
```

The server will be available at `localhost:50051`.

## Option 2: Test Backend Only (without database)

If you don't have Docker or PostgreSQL set up yet, you can still test if the backend runs:

```bash
cd backend

# Temporarily comment out database initialization
# Then run:
.\server.exe
```

You'll see database connection errors, but the server should attempt to start.

## Testing with grpcurl

Install grpcurl to test gRPC endpoints:

```bash
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
```

List available services:
```bash
grpcurl -plaintext localhost:50051 list
```

Expected output:
```
assistant.auth.AuthService
assistant.streaming.StreamingService
grpc.reflection.v1alpha.ServerReflection
```

Test authentication (mock):
```bash
grpcurl -plaintext -d '{
  "provider": "google",
  "oauth_token": "test-token",
  "device_type": "desktop"
}' localhost:50051 assistant.auth.AuthService/AuthenticateOAuth
```

## Next Steps

1. **Set up PostgreSQL** (if using Docker, it's already running)
2. **Test desktop app connection** to backend
3. **Build Android app** for complete testing

## Troubleshooting

### "Database connection failed"

Start PostgreSQL with Docker:
```bash
cd docker
docker-compose up postgres
```

Or install PostgreSQL locally and create the database:
```sql
CREATE DATABASE agent_db;
CREATE USER agent_user WITH PASSWORD 'agent_password';
GRANT ALL PRIVILEGES ON DATABASE agent_db TO agent_user;
```

### "Port 50051 already in use"

Stop any existing server:
```bash
# Windows
netstat -ano | findstr :50051
taskkill /PID <PID> /F
```

### Backend won't start

Check the `.env` file exists and has correct values:
```bash
type backend\.env
```

## Success Indicators

✅ Server starts without errors
✅ Database connection established
✅ gRPC services listed with grpcurl
✅ Can make auth API call (returns mock response)

Once these work, you're ready to connect the desktop app!
