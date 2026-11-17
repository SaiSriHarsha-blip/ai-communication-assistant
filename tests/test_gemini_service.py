"""
Unit tests for GeminiService (app.services.gemini_service) and BaseLLM (app.services.base_llm).

Verifies offline initialization, configuration, prompt validation, structured output generation,
APIError handling, and generic exception handling with genai.Client mocked (zero network calls).
"""

from typing import Any
from unittest.mock import MagicMock
from google.genai.errors import APIError
import pytest

from app.config import Settings
from app.models.gemini_response import GeminiResponse
from app.models.message import MessageVariant
from app.services.base_llm import BaseLLM
from app.services.gemini_service import GeminiService, GeminiServiceError


@pytest.fixture
def mock_genai_client(mocker: Any) -> MagicMock:
    """Mock the genai.Client constructor to ensure zero network interaction."""
    mock_cls = mocker.patch("app.services.gemini_service.genai.Client")
    mock_instance = MagicMock()
    mock_cls.return_value = mock_instance
    return mock_instance


@pytest.mark.unit
class TestGeminiServiceInitialization:
    """Tests for API key resolution, model configuration, and initialization errors."""

    def test_missing_api_key_raises_gemini_service_error(
        self, monkeypatch: pytest.MonkeyPatch, mock_genai_client: MagicMock
    ) -> None:
        from pydantic import SecretStr

        monkeypatch.setattr(
            "app.services.gemini_service.settings.GEMINI_API_KEY",
            SecretStr(""),
        )

        with pytest.raises(
            GeminiServiceError,
            match="GEMINI_API_KEY not found. Please configure your .env file.",
        ):
            GeminiService(api_key=None)

    def test_explicit_api_key_initializes_client(
        self, mock_genai_client: MagicMock, mocker: Any
    ) -> None:
        service = GeminiService(api_key="test-api-key-abc", model_name="custom-model")

        assert service.model_name == "custom-model"
        # Verify genai.Client was called with the explicit key
        from app.services.gemini_service import genai
        genai.Client.assert_called_once_with(api_key="test-api-key-abc")

    def test_initialization_exception_wrapped_in_gemini_service_error(
        self, mocker: Any
    ) -> None:
        mock_cls = mocker.patch("app.services.gemini_service.genai.Client")
        mock_cls.side_effect = ValueError("Invalid auth token format")

        with pytest.raises(
            GeminiServiceError,
            match="Gemini initialization failed: Invalid auth token format",
        ):
            GeminiService(api_key="bad-key")


@pytest.mark.unit
class TestGeminiServiceGeneration:
    """Tests prompt validation, structured generation, and error conditions."""

    @pytest.fixture
    def service(self, mock_genai_client: MagicMock) -> GeminiService:
        return GeminiService(api_key="valid-mock-key")

    @pytest.mark.parametrize(
        "invalid_prompt",
        [
            "",
            "   ",
            "\n\t\n",
        ],
    )
    def test_empty_prompt_raises_gemini_service_error(
        self, service: GeminiService, invalid_prompt: str
    ) -> None:
        with pytest.raises(GeminiServiceError, match="Prompt cannot be empty."):
            service.generate(invalid_prompt)

    def test_successful_structured_generation(
        self, service: GeminiService, mock_genai_client: MagicMock
    ) -> None:
        mock_response = MagicMock()
        expected_response = GeminiResponse(
            messages=[
                MessageVariant(style="Professional", text="Professional text"),
                MessageVariant(style="Friendly", text="Friendly text"),
                MessageVariant(style="Short", text="Short text"),
            ]
        )
        mock_response.parsed = expected_response
        mock_genai_client.models.generate_content.return_value = mock_response

        result = service.generate("Generate message", temperature=0.5, max_output_tokens=256)

        assert isinstance(result, GeminiResponse)
        assert len(result.messages) == 3
        assert result.messages[0].style == "Professional"

        # Verify call arguments
        call_kwargs = mock_genai_client.models.generate_content.call_args.kwargs
        assert call_kwargs["model"] == service.model_name
        assert call_kwargs["contents"] == "Generate message"
        config = call_kwargs["config"]
        assert config.temperature == 0.5
        assert config.max_output_tokens == 256
        assert config.response_mime_type == "application/json"
        assert config.response_schema == GeminiResponse

    def test_generation_returns_none_raises_gemini_service_error(
        self, service: GeminiService, mock_genai_client: MagicMock
    ) -> None:
        mock_genai_client.models.generate_content.return_value = None

        with pytest.raises(
            GeminiServiceError,
            match="Gemini returned no response.",
        ):
            service.generate("Valid prompt")

    def test_generation_returns_unparseable_raises_gemini_service_error(
        self, service: GeminiService, mock_genai_client: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response.parsed = None
        mock_genai_client.models.generate_content.return_value = mock_response

        with pytest.raises(
            GeminiServiceError,
            match="Gemini returned an empty or unparseable structured response.",
        ):
            service.generate("Valid prompt")

    def test_api_error_wrapped_in_gemini_service_error(
        self, service: GeminiService, mock_genai_client: MagicMock
    ) -> None:
        mock_genai_client.models.generate_content.side_effect = APIError(
            429, {"error": {"message": "Resource quota exceeded"}}
        )

        with pytest.raises(
            GeminiServiceError,
            match="Gemini API Error",
        ):
            service.generate("Valid prompt")

    def test_unexpected_exception_wrapped_in_gemini_service_error(
        self, service: GeminiService, mock_genai_client: MagicMock
    ) -> None:
        mock_genai_client.models.generate_content.side_effect = ConnectionResetError(
            "Socket connection forcibly closed by peer"
        )

        with pytest.raises(
            GeminiServiceError,
            match="Unexpected Gemini error: Socket connection forcibly closed",
        ):
            service.generate("Valid prompt")


@pytest.mark.unit
def test_base_llm_abstract_method_raises_not_implemented() -> None:
    """Verifies that invoking super().generate on BaseLLM raises NotImplementedError."""

    class ConcreteLLM(BaseLLM):
        def generate(
            self,
            prompt: str,
            temperature: float = 0.3,
            max_output_tokens: int = 512,
        ) -> GeminiResponse:
            return super().generate(prompt, temperature, max_output_tokens)

    instance = ConcreteLLM()
    with pytest.raises(NotImplementedError):
        instance.generate("test prompt")
