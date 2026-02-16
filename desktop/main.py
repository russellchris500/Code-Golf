"""Main entry point for desktop AI assistant application."""

import logging
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import Config
from ai.stt import create_stt_provider
from ai.llm import create_llm_provider
from ai.tts import create_tts_provider
from assistant import AIAssistant
from grpc_client.client import GRPCClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('assistant.log')
    ]
)

logger = logging.getLogger(__name__)


class DesktopApp:
    """Main desktop application."""

    def __init__(self, config: Config):
        """Initialize desktop app."""
        self.config = config
        self.assistant: Optional[AIAssistant] = None
        self.grpc_client: Optional[GRPCClient] = None

    def initialize(self):
        """Initialize all components."""
        logger.info("Initializing desktop application...")

        # Validate configuration
        errors = self.config.validate()
        if errors:
            logger.error("Configuration errors:")
            for error in errors:
                logger.error(f"  - {error}")
            sys.exit(1)

        # Initialize AI providers
        logger.info(f"Initializing AI providers: {self.config.ai_provider}")

        try:
            stt = create_stt_provider(
                self.config.stt_provider,
                self.config.openai_api_key
            )

            llm = create_llm_provider(
                self.config.ai_provider,
                self.config.openai_api_key or self.config.anthropic_api_key,
                self.config.ai_model
            )

            tts = create_tts_provider(
                self.config.tts_provider,
                self.config.openai_api_key,
                self.config.openai_tts_model,
                self.config.openai_tts_voice
            )

            self.assistant = AIAssistant(stt, llm, tts)

        except Exception as e:
            logger.error(f"Failed to initialize AI providers: {e}")
            sys.exit(1)

        # Initialize gRPC client
        logger.info(f"Connecting to backend at {self.config.backend_url}")

        try:
            self.grpc_client = GRPCClient(
                self.config.backend_url,
                self.config.user_id,
                self.config.use_tls
            )
            # Note: Connection will be established when we have protobuf generated
            # self.grpc_client.connect()

        except Exception as e:
            logger.error(f"Failed to connect to backend: {e}")
            sys.exit(1)

        logger.info("Desktop application initialized successfully")

    def handle_incoming_packet(self, packet):
        """Handle incoming packet from phone."""
        # TODO: Implement when protobuf is generated
        logger.info(f"Received packet: {packet}")

        # Check packet type
        # if packet.type == AUDIO_CHUNK:
        #     # Process audio
        #     transcript, response_text, response_audio = self.assistant.process_audio_input(packet.audio.data)
        #
        #     # Send transcript back
        #     self.grpc_client.send_packet(
        #         self.grpc_client.create_transcript_packet(transcript, is_final=True)
        #     )
        #
        #     # Send audio response
        #     self.grpc_client.send_packet(
        #         self.grpc_client.create_audio_packet(response_audio, is_final=True)
        #     )
        #
        # elif packet.type == TEXT_MESSAGE:
        #     # Process text
        #     response_text = self.assistant.process_text_input(packet.text.text)
        #
        #     # Send text response
        #     self.grpc_client.send_packet(
        #         self.grpc_client.create_text_packet(response_text)
        #     )

    def run(self):
        """Run the application."""
        logger.info("Starting desktop AI assistant...")

        try:
            # Start streaming
            # self.grpc_client.start_stream(self.handle_incoming_packet)

            logger.info("Desktop assistant is running")
            logger.info("Waiting for mobile device to connect...")

            # Keep running
            import time
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Shutting down...")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            if self.grpc_client:
                self.grpc_client.disconnect()

    def shutdown(self):
        """Cleanup and shutdown."""
        logger.info("Shutting down desktop application")
        if self.grpc_client:
            self.grpc_client.disconnect()


def main():
    """Main entry point."""
    print("=" * 60)
    print("AI Voice Assistant - Desktop Application")
    print("=" * 60)
    print()

    # Load configuration
    config = Config.from_env()

    # Create and initialize app
    app = DesktopApp(config)
    app.initialize()

    # Run app
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        app.shutdown()


if __name__ == "__main__":
    main()
