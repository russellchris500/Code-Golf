# Generating Protocol Buffer Code

Follow these steps to generate the gRPC code for the project.

## Step 1: Generate Go Code (Backend)

This generates the Go code needed for the backend server.

```bash
cd C:\Users\csr\Code\Agent
scripts\generate_proto.bat
```

This will generate Go files in `backend\pb\auth\` and `backend\pb\streaming\`.

If you get an error about missing protoc plugins, run:
```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

Then add `%USERPROFILE%\go\bin` to your PATH.

## Step 2: Generate Python Code (Desktop)

The Python code is generated when you set up the desktop virtual environment.

### Method 1: Automatic (during setup)

When you install the requirements, it will include `grpcio-tools`:

```bash
cd desktop
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Method 2: Manual Generation

If you need to regenerate Python code:

```bash
cd desktop
venv\Scripts\activate
python -m grpc_tools.protoc -I=..\proto --python_out=. --grpc_python_out=. ..\proto\auth.proto
python -m grpc_tools.protoc -I=..\proto --python_out=. --grpc_python_out=. ..\proto\streaming.proto
```

This generates:
- `auth_pb2.py` - Auth message definitions
- `auth_pb2_grpc.py` - Auth service stubs
- `streaming_pb2.py` - Streaming message definitions
- `streaming_pb2_grpc.py` - Streaming service stubs

## Verification

### Check Go Files

```bash
dir backend\pb\auth\*.go
dir backend\pb\streaming\*.go
```

You should see:
- `backend\pb\auth\auth.pb.go`
- `backend\pb\auth\auth_grpc.pb.go`
- `backend\pb\streaming\streaming.pb.go`
- `backend\pb\streaming\streaming_grpc.pb.go`

### Check Python Files

```bash
dir desktop\*_pb2*.py
```

You should see:
- `desktop\auth_pb2.py`
- `desktop\auth_pb2_grpc.py`
- `desktop\streaming_pb2.py`
- `desktop\streaming_pb2_grpc.py`

## Troubleshooting

### Error: "protoc not found"

Install protoc from https://github.com/protocolbuffers/protobuf/releases
- Download `protoc-XX.X-win64.zip`
- Extract to `C:\protoc`
- Add `C:\protoc\bin` to PATH
- Restart terminal and try again

### Error: "protoc-gen-go not found"

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

Then add `%USERPROFILE%\go\bin` to PATH.

### Error: "No module named 'grpc_tools'"

```bash
cd desktop
venv\Scripts\activate
pip install grpcio-tools
```

## Next Steps

After generating protobuf code:

1. **Test backend**:
   ```bash
   cd backend
   go run cmd/server/main.go
   ```

2. **Test desktop app**:
   ```bash
   cd desktop
   venv\Scripts\activate
   python main.py
   ```

See [NEXT_STEPS.md](NEXT_STEPS.md) for complete setup instructions.
