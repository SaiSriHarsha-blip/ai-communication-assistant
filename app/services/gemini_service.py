import logging
import os
from pathlib import Path

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
# pyrefly: ignore [missing-import]
from google.genai.errors import APIError

from app.models.gemini_response import GeminiResponse
from app.services.base_llm import BaseLLM

load_dotenv(Path(".env"))

logger = logging.getLogger(__name__)


class GeminiServiceError(Exception):
    """Raised when Gemini service encounters an error."""


class GeminiService(BaseLLM):
    """
    Google Gemini implementation.

    Responsibilities:
    - Initialize Gemini client
    - Generate responses using structured output schemas
    - Handle API errors
    """

    DEFAULT_MODEL = "gemini-2.5-flash"

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise GeminiServiceError(
                "GEMINI_API_KEY not found. Please configure your .env file."
            )

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            self.DEFAULT_MODEL,
        )

        try:
            self.client = genai.Client(api_key=api_key)

            logger.info(
                "Gemini initialized successfully (%s)",
                self.model_name,
            )

        except Exception as exc:
            logger.exception("Failed to initialize Gemini.")

            raise GeminiServiceError(
                f"Gemini initialization failed: {exc}"
            ) from exc

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_output_tokens: int = 1024,
    ) -> GeminiResponse:
        """
        Generate structured response using Gemini.
        """

        if not prompt.strip():
            raise GeminiServiceError(
                "Prompt cannot be empty."
            )

        logger.info("Sending prompt to Gemini for structured output...")

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                    response_mime_type="application/json",
                    response_schema=GeminiResponse,
                ),
            )

            if response is None:
                raise GeminiServiceError(
                    "Gemini returned no response."
                )

            parsed = getattr(response, "parsed", None)

            if not parsed:
                raise GeminiServiceError(
                    "Gemini returned an empty or unparseable structured response."
                )

            logger.info("Gemini structured generation successful.")

            return parsed

        except APIError as exc:
            logger.exception("Gemini API Error")

            raise GeminiServiceError(
                f"Gemini API Error: {exc}"
            ) from exc

        except Exception as exc:
            logger.exception("Unexpected Gemini error")

            raise GeminiServiceError(
                f"Unexpected Gemini error: {exc}"
            ) from exc