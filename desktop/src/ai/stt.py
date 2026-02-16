"""Speech-to-Text module supporting multiple providers."""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from openai import OpenAI
import io

logger = logging.getLogger(__name__)


class STTProvider(ABC):
    """Abstract base class for STT providers."""

    @abstractmethod
    def transcribe(self, audio_bytes: bytes, language: Optional[str] = None) -> str:
        """
        Transcribe audio to text.

        Args:
            audio_bytes: Audio data in bytes
            language: Optional language code (e.g., 'en')

        Returns:
            Transcribed text
        """
        pass


class OpenAISTT(STTProvider):
    """OpenAI Whisper API for speech-to-text."""

    def __init__(self, api_key: str, model: str = "whisper-1"):
        """
        Initialize OpenAI STT.

        Args:
            api_key: OpenAI API key
            model: Whisper model to use
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        logger.info(f"Initialized OpenAI STT with model {model}")

    def transcribe(self, audio_bytes: bytes, language: Optional[str] = None) -> str:
        """Transcribe audio using OpenAI Whisper API."""
        try:
            # Create a file-like object from bytes
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "audio.opus"  # Whisper expects a filename

            # Call Whisper API
            transcript = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                language=language,
            )

            text = transcript.text
            logger.info(f"Transcribed: {text}")
            return text

        except Exception as e:
            logger.error(f"STT error: {e}")
            raise


class LocalSTT(STTProvider):
    """Local speech-to-text (placeholder for local Whisper)."""

    def __init__(self):
        """Initialize local STT."""
        logger.info("Initialized Local STT (not implemented)")
        # TODO: Implement local Whisper model
        # import whisper
        # self.model = whisper.load_model("base")

    def transcribe(self, audio_bytes: bytes, language: Optional[str] = None) -> str:
        """Transcribe audio using local Whisper model."""
        # TODO: Implement local transcription
        logger.warning("Local STT not implemented, returning placeholder")
        return "[Local STT not implemented yet]"


def create_stt_provider(provider: str, api_key: Optional[str] = None) -> STTProvider:
    """
    Factory function to create STT provider.

    Args:
        provider: Provider name ('openai' or 'local')
        api_key: API key for cloud providers

    Returns:
        STT provider instance
    """
    if provider == "openai":
        if not api_key:
            raise ValueError("OpenAI API key required")
        return OpenAISTT(api_key)
    elif provider == "local":
        return LocalSTT()
    else:
        raise ValueError(f"Unknown STT provider: {provider}")
