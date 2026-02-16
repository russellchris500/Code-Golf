"""Main AI Assistant logic."""

import logging
from typing import List, Optional
from ai.stt import STTProvider
from ai.llm import LLMProvider, Message
from ai.tts import TTSProvider

logger = logging.getLogger(__name__)


class AIAssistant:
    """Core AI assistant that processes input and generates responses."""

    def __init__(
        self,
        stt_provider: STTProvider,
        llm_provider: LLMProvider,
        tts_provider: TTSProvider,
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize AI Assistant.

        Args:
            stt_provider: Speech-to-text provider
            llm_provider: LLM provider
            tts_provider: Text-to-speech provider
            system_prompt: System prompt for the LLM
        """
        self.stt = stt_provider
        self.llm = llm_provider
        self.tts = tts_provider
        self.system_prompt = system_prompt or self.default_system_prompt()
        self.conversation_history: List[Message] = []

        logger.info("AI Assistant initialized")

    def default_system_prompt(self) -> str:
        """Default system prompt for the assistant."""
        return """You are a helpful AI assistant accessed via voice on a mobile device.

Keep your responses concise and conversational, as they will be converted to speech.
Avoid long lists or complex formatting.
Be friendly, clear, and helpful."""

    def process_audio_input(self, audio_bytes: bytes) -> tuple[str, str, bytes]:
        """
        Process audio input and return transcript, response text, and response audio.

        Args:
            audio_bytes: Input audio from user

        Returns:
            Tuple of (transcript, response_text, response_audio)
        """
        try:
            # 1. Speech to Text
            logger.info("Transcribing audio...")
            transcript = self.stt.transcribe(audio_bytes)
            logger.info(f"User said: {transcript}")

            # 2. Generate AI response
            response_text = self.process_text_input(transcript)

            # 3. Text to Speech
            logger.info("Synthesizing speech...")
            response_audio = self.tts.synthesize(response_text)

            return transcript, response_text, response_audio

        except Exception as e:
            logger.error(f"Error processing audio input: {e}")
            error_msg = "I'm sorry, I encountered an error processing your request."
            error_audio = self.tts.synthesize(error_msg)
            return "", error_msg, error_audio

    def process_text_input(self, text: str) -> str:
        """
        Process text input and return response.

        Args:
            text: User's text input

        Returns:
            AI response text
        """
        try:
            # Add user message to history
            self.conversation_history.append(Message("user", text))

            # Generate response
            logger.info("Generating AI response...")
            response = self.llm.generate_response(
                self.conversation_history, self.system_prompt
            )

            # Add assistant response to history
            self.conversation_history.append(Message("assistant", response))

            # Keep history manageable (last 10 messages)
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]

            logger.info(f"Assistant response: {response}")
            return response

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error generating a response."

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    def get_conversation_history(self) -> List[Message]:
        """Get conversation history."""
        return self.conversation_history.copy()

    def set_system_prompt(self, prompt: str):
        """Update system prompt."""
        self.system_prompt = prompt
        logger.info("System prompt updated")
