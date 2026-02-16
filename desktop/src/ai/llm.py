"""LLM module supporting multiple AI providers."""

import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from openai import OpenAI
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class Message:
    """Represents a conversation message."""

    def __init__(self, role: str, content: str):
        self.role = role  # 'user' or 'assistant'
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_response(
        self, messages: List[Message], system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate AI response.

        Args:
            messages: Conversation history
            system_prompt: Optional system prompt

        Returns:
            AI response text
        """
        pass


class OpenAILLM(LLMProvider):
    """OpenAI GPT for AI responses."""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """
        Initialize OpenAI LLM.

        Args:
            api_key: OpenAI API key
            model: GPT model to use
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        logger.info(f"Initialized OpenAI LLM with model {model}")

    def generate_response(
        self, messages: List[Message], system_prompt: Optional[str] = None
    ) -> str:
        """Generate response using OpenAI GPT."""
        try:
            # Build messages list
            api_messages = []

            if system_prompt:
                api_messages.append({"role": "system", "content": system_prompt})

            api_messages.extend([msg.to_dict() for msg in messages])

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model, messages=api_messages, temperature=0.7
            )

            text = response.choices[0].message.content
            logger.info(f"Generated response: {text[:100]}...")
            return text

        except Exception as e:
            logger.error(f"LLM error: {e}")
            raise


class AnthropicLLM(LLMProvider):
    """Anthropic Claude for AI responses."""

    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        """
        Initialize Anthropic LLM.

        Args:
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        logger.info(f"Initialized Anthropic LLM with model {model}")

    def generate_response(
        self, messages: List[Message], system_prompt: Optional[str] = None
    ) -> str:
        """Generate response using Anthropic Claude."""
        try:
            # Build messages list
            api_messages = [msg.to_dict() for msg in messages]

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt or "You are a helpful AI assistant.",
                messages=api_messages,
            )

            text = response.content[0].text
            logger.info(f"Generated response: {text[:100]}...")
            return text

        except Exception as e:
            logger.error(f"LLM error: {e}")
            raise


class LocalLLM(LLMProvider):
    """Local LLM (placeholder for local models)."""

    def __init__(self, model_path: Optional[str] = None):
        """Initialize local LLM."""
        logger.info("Initialized Local LLM (not implemented)")
        # TODO: Implement local model (e.g., llama.cpp, Ollama)

    def generate_response(
        self, messages: List[Message], system_prompt: Optional[str] = None
    ) -> str:
        """Generate response using local LLM."""
        # TODO: Implement local generation
        logger.warning("Local LLM not implemented, returning placeholder")
        return "Local LLM not implemented yet. Please configure a cloud provider."


def create_llm_provider(
    provider: str, api_key: Optional[str] = None, model: Optional[str] = None
) -> LLMProvider:
    """
    Factory function to create LLM provider.

    Args:
        provider: Provider name ('openai', 'anthropic', or 'local')
        api_key: API key for cloud providers
        model: Model name

    Returns:
        LLM provider instance
    """
    if provider == "openai":
        if not api_key:
            raise ValueError("OpenAI API key required")
        return OpenAILLM(api_key, model or "gpt-4-turbo-preview")
    elif provider == "anthropic":
        if not api_key:
            raise ValueError("Anthropic API key required")
        return AnthropicLLM(api_key, model or "claude-3-opus-20240229")
    elif provider == "local":
        return LocalLLM()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
