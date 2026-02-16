"""Text-to-Speech module supporting multiple providers."""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from openai import OpenAI

logger = logging.getLogger(__name__)


class TTSProvider(ABC):
    """Abstract base class for TTS providers."""

    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        """
        Convert text to speech.

        Args:
            text: Text to convert to speech

        Returns:
            Audio data in bytes
        """
        pass


class OpenAITTS(TTSProvider):
    """OpenAI TTS for text-to-speech."""

    def __init__(
        self, api_key: str, model: str = "tts-1", voice: str = "alloy"
    ):
        """
        Initialize OpenAI TTS.

        Args:
            api_key: OpenAI API key
            model: TTS model ('tts-1' or 'tts-1-hd')
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.voice = voice
        logger.info(f"Initialized OpenAI TTS with model {model}, voice {voice}")

    def synthesize(self, text: str) -> bytes:
        """Synthesize speech using OpenAI TTS API."""
        try:
            logger.info(f"Synthesizing: {text[:100]}...")

            response = self.client.audio.speech.create(
                model=self.model, voice=self.voice, input=text
            )

            # Get audio bytes
            audio_bytes = response.content
            logger.info(f"Synthesized {len(audio_bytes)} bytes of audio")
            return audio_bytes

        except Exception as e:
            logger.error(f"TTS error: {e}")
            raise


class LocalTTS(TTSProvider):
    """Local text-to-speech (placeholder)."""

    def __init__(self):
        """Initialize local TTS."""
        logger.info("Initialized Local TTS (not implemented)")
        # TODO: Implement local TTS (e.g., pyttsx3, Coqui TTS)

    def synthesize(self, text: str) -> bytes:
        """Synthesize speech using local TTS."""
        # TODO: Implement local TTS
        logger.warning("Local TTS not implemented, returning empty audio")
        return b""


def create_tts_provider(
    provider: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    voice: Optional[str] = None,
) -> TTSProvider:
    """
    Factory function to create TTS provider.

    Args:
        provider: Provider name ('openai' or 'local')
        api_key: API key for cloud providers
        model: Model name for cloud providers
        voice: Voice name for cloud providers

    Returns:
        TTS provider instance
    """
    if provider == "openai":
        if not api_key:
            raise ValueError("OpenAI API key required")
        return OpenAITTS(api_key, model or "tts-1", voice or "alloy")
    elif provider == "local":
        return LocalTTS()
    else:
        raise ValueError(f"Unknown TTS provider: {provider}")
