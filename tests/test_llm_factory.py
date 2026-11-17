"""
Unit tests for LLMFactory (app.services.llm_factory).

Verifies provider registration, instantiation, case-insensitivity, whitespace tolerance,
unsupported provider error handling, and factory extensibility.
"""

from typing import Any
import pytest

from app.models.gemini_response import GeminiResponse
from app.services.base_llm import BaseLLM
from app.services.gemini_service import GeminiService
from app.services.llm_factory import LLMFactory


class DummyProvider(BaseLLM):
    """Test double for BaseLLM provider registration."""

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_output_tokens: int = 512,
    ) -> GeminiResponse:
        return GeminiResponse(messages=[])


@pytest.mark.unit
class TestLLMFactory:
    """Tests for LLM provider lookup and instantiation."""

    def test_get_provider_gemini_returns_gemini_service_instance(
        self, mocker: Any
    ) -> None:
        # Mock GeminiService.__init__ to prevent requiring a live API key
        mocker.patch.object(GeminiService, "__init__", return_value=None)

        provider = LLMFactory.get_provider("gemini")

        assert isinstance(provider, GeminiService)
        assert isinstance(provider, BaseLLM)

    @pytest.mark.parametrize(
        "provider_input",
        [
            "GEMINI",
            "Gemini",
            "  gemini  ",
            " \tgEmInI\n ",
        ],
    )
    def test_get_provider_case_and_whitespace_insensitivity(
        self, mocker: Any, provider_input: str
    ) -> None:
        mocker.patch.object(GeminiService, "__init__", return_value=None)

        provider = LLMFactory.get_provider(provider_input)

        assert isinstance(provider, GeminiService)

    @pytest.mark.parametrize(
        "unsupported",
        [
            "claude",
            "openai",
            "llama",
            "deepseek",
            "unknown",
        ],
    )
    def test_get_provider_unsupported_raises_value_error(
        self, unsupported: str
    ) -> None:
        with pytest.raises(
            ValueError,
            match=f"LLM provider '{unsupported}' is not supported.",
        ) as exc_info:
            LLMFactory.get_provider(unsupported)

        assert "Supported providers: gemini" in str(exc_info.value)

    def test_custom_provider_registration_and_retrieval(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verifies extensibility of LLMFactory registry."""
        registry_copy = dict(LLMFactory._registry)
        registry_copy["dummy"] = DummyProvider
        monkeypatch.setattr(LLMFactory, "_registry", registry_copy)

        instance = LLMFactory.get_provider("dummy")
        assert isinstance(instance, DummyProvider)
        assert isinstance(instance, BaseLLM)
