# Android Voice Assistant App

Kotlin-based Android application for voice and text interaction with the AI assistant.

## Features

- Google OAuth authentication
- Voice recording and streaming
- Text input
- Real-time transcript display
- Audio playback for AI responses
- Auto-pairing with desktop via user account
- Material Design 3 UI with Jetpack Compose

## Prerequisites

- Android Studio Hedgehog (2023.1.1) or newer
- Android SDK 24+ (targeting SDK 34)
- Kotlin 1.9+
- Gradle 8.0+

## Project Structure

```
android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/assistant/mobile/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── ui/
│   │   │   │   │   ├── screens/
│   │   │   │   │   │   ├── LoginScreen.kt
│   │   │   │   │   │   ├── ChatScreen.kt
│   │   │   │   │   │   └── SettingsScreen.kt
│   │   │   │   │   └── theme/
│   │   │   │   ├── grpc/
│   │   │   │   │   ├── GrpcClient.kt
│   │   │   │   │   └── StreamManager.kt
│   │   │   │   ├── audio/
│   │   │   │   │   ├── AudioRecorder.kt
│   │   │   │   │   └── AudioPlayer.kt
│   │   │   │   ├── auth/
│   │   │   │   │   └── AuthManager.kt
│   │   │   │   └── viewmodel/
│   │   │   │       ├── ChatViewModel.kt
│   │   │   │       └── AuthViewModel.kt
│   │   │   ├── AndroidManifest.xml
│   │   │   └── res/
│   │   └── build.gradle.kts
│   └── build.gradle.kts
└── build.gradle.kts
```

## Dependencies

Add to `app/build.gradle.kts`:

```kotlin
dependencies {
    // Core Android
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")

    // Compose
    implementation(platform("androidx.compose:compose-bom:2024.01.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.navigation:navigation-compose:2.7.6")

    // ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")

    // gRPC
    implementation("io.grpc:grpc-kotlin-stub:1.4.1")
    implementation("io.grpc:grpc-okhttp:1.60.1")
    implementation("io.grpc:grpc-protobuf-lite:1.60.1")
    implementation("com.google.protobuf:protobuf-kotlin-lite:3.25.1")

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")

    // Google OAuth
    implementation("com.google.android.gms:play-services-auth:20.7.0")

    // DataStore for preferences
    implementation("androidx.datastore:datastore-preferences:1.0.0")

    // Audio
    // Opus codec (if using Opus)
    // implementation("com.github.louiswins:opus-jni:0.1.0")

    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
}
```

## Setup Instructions

### 1. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sign-In API
4. Create OAuth 2.0 credentials:
   - Application type: Android
   - Package name: `com.assistant.mobile`
   - SHA-1 fingerprint: Get with `keytool -list -v -keystore ~/.android/debug.keystore`
5. Download `google-services.json`
6. Place in `android/app/` directory

### 2. Configure Backend URL

Edit `app/src/main/res/values/strings.xml`:

```xml
<resources>
    <string name="app_name">AI Assistant</string>
    <string name="backend_url">your-backend-url:50051</string>
</resources>
```

For Railway deployment, use the Railway URL.

### 3. Generate Protobuf Code

```bash
cd android
./gradlew generateProto
```

### 4. Build and Run

1. Open project in Android Studio
2. Sync Gradle
3. Connect Android device or start emulator
4. Click Run

## Permissions

Add to `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

## Features Implementation

### Voice Recording

```kotlin
class AudioRecorder(private val context: Context) {
    private var audioRecord: AudioRecord? = null

    fun startRecording(onAudioData: (ByteArray) -> Unit) {
        // Implementation using AudioRecord API
    }

    fun stopRecording() {
        audioRecord?.stop()
        audioRecord?.release()
    }
}
```

### gRPC Streaming

```kotlin
class GrpcClient(private val channel: ManagedChannel) {
    private val streamingStub = StreamingServiceGrpcKt.StreamingServiceCoroutineStub(channel)

    suspend fun startStream(
        userId: String,
        onPacketReceived: (Packet) -> Unit
    ) {
        val requests = flow {
            // Send registration packet
            emit(createRegistrationPacket(userId))

            // Keep stream open
            awaitCancellation()
        }

        streamingStub.stream(requests).collect { packet ->
            onPacketReceived(packet)
        }
    }
}
```

### UI Screens

**LoginScreen**: Google OAuth login
**ChatScreen**: Main UI with transcript, voice button, text input
**SettingsScreen**: API keys, preferences

## Testing

### Unit Tests

```bash
./gradlew test
```

### Instrumented Tests

```bash
./gradlew connectedAndroidTest
```

## Deployment

### Debug Build

```bash
./gradlew assembleDebug
```

APK will be in `app/build/outputs/apk/debug/`

### Release Build

1. Create keystore:
   ```bash
   keytool -genkey -v -keystore release.keystore -alias assistant -keyalg RSA -keysize 2048 -validity 10000
   ```

2. Configure signing in `app/build.gradle.kts`

3. Build:
   ```bash
   ./gradlew assembleRelease
   ```

## Architecture

```
UI Layer (Compose)
    ↓
ViewModel Layer
    ↓
Repository/Manager Layer
    ├── GrpcClient (network)
    ├── AudioRecorder (audio input)
    ├── AudioPlayer (audio output)
    └── AuthManager (authentication)
```

## Next Steps

- [ ] Implement complete UI with Jetpack Compose
- [ ] Add audio recording and playback
- [ ] Implement gRPC streaming
- [ ] Add Google OAuth
- [ ] Handle permissions properly
- [ ] Add error handling and retry logic
- [ ] Implement local caching
- [ ] Add push notifications
- [ ] Build settings screen
