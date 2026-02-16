"""Configuration management for desktop app."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    """Application configuration."""

    # Backend
    backend_url: str
    use_tls: bool

    # User
    user_id: str
    access_token: str

    # API Keys
    openai_api_key: Optional[str]
    anthropic_api_key: Optional[str]

    # AI Configuration
    ai_provider: str  # openai, anthropic, local
    ai_model: str
    stt_provider: str  # openai, local
    tts_provider: str  # openai, local

    # OpenAI specific
    openai_tts_voice: str
    openai_tts_model: str

    # Audio
    sample_rate: int
    chunk_size: int
    audio_format: str

    # Logging
    log_level: str

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            backend_url=os.getenv("BACKEND_URL", "localhost:50051"),
            use_tls=os.getenv("USE_TLS", "false").lower() == "true",
            user_id=os.getenv("USER_ID", ""),
            access_token=os.getenv("ACCESS_TOKEN", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            ai_provider=os.getenv("AI_PROVIDER", "openai"),
            ai_model=os.getenv("AI_MODEL", "gpt-4-turbo-preview"),
            stt_provider=os.getenv("STT_PROVIDER", "openai"),
            tts_provider=os.getenv("TTS_PROVIDER", "openai"),
            openai_tts_voice=os.getenv("OPENAI_TTS_VOICE", "alloy"),
            openai_tts_model=os.getenv("OPENAI_TTS_MODEL", "tts-1"),
            sample_rate=int(os.getenv("SAMPLE_RATE", "16000")),
            chunk_size=int(os.getenv("CHUNK_SIZE", "1024")),
            audio_format=os.getenv("AUDIO_FORMAT", "opus"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if not self.user_id:
            errors.append("USER_ID is required")

        if not self.access_token:
            errors.append("ACCESS_TOKEN is required")

        if self.ai_provider == "openai" and not self.openai_api_key:
            errors.append("OPENAI_API_KEY is required when using OpenAI")

        if self.ai_provider == "anthropic" and not self.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY is required when using Anthropic")

        return errors
