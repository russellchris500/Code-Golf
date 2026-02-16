@echo off
REM Generate Protocol Buffer code for all languages

echo ========================================
echo Protocol Buffer Code Generation
echo ========================================
echo.

REM Check if protoc is installed
where protoc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: protoc not found in PATH
    echo Please install Protocol Buffer compiler from:
    echo https://github.com/protocolbuffers/protobuf/releases
    exit /b 1
)

REM Go backend
echo [1/2] Generating Go code...
protoc --go_out=backend --go_opt=paths=source_relative ^
       --go-grpc_out=backend --go-grpc_opt=paths=source_relative ^
       -I=proto proto/*.proto

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to generate Go code
    echo Make sure Go protobuf plugins are installed:
    echo   go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
    echo   go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
    exit /b 1
)

REM Organize generated Go files
if not exist "backend\pb\auth" mkdir backend\pb\auth
if not exist "backend\pb\streaming" mkdir backend\pb\streaming
move /Y backend\auth*.pb.go backend\pb\auth\ >nul 2>&1
move /Y backend\streaming*.pb.go backend\pb\streaming\ >nul 2>&1

echo   Done: Go code generated in backend\pb\auth\ and backend\pb\streaming\

REM Python desktop - Skip if grpc_tools not installed
echo.
echo [2/2] Generating Python code...
echo NOTE: Skipping Python generation for now.
echo Python protobuf will be generated when you set up the desktop app.
echo.
echo To generate Python code manually:
echo   1. cd desktop
echo   2. venv\Scripts\activate
echo   3. pip install grpcio-tools
echo   4. python -m grpc_tools.protoc -I=..\proto --python_out=. --grpc_python_out=. ..\proto\*.proto

REM Android (Java/Kotlin)
REM echo Generating Kotlin code...
REM protoc --kotlin_out=android/app/src/main/java ^
REM        --grpc-kotlin_out=android/app/src/main/java ^
REM        -I=proto proto/*.proto

echo Done!
