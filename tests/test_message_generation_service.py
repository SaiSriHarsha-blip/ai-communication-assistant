"""
Unit and integration tests for MessageGenerationService (app.services.message_generation_service).

Verifies prompt selection, rendering with context, LLM invocation, response extraction,
variant validation, empty/malformed response detection, and error propagation.
"""

from pathlib import Path
from typing import Any
import pytest

from app.agents.prompt_router import PromptRouter
from app.models.gemini_response import GeminiResponse
from app.models.message import MessageVariant
from app.services.base_llm import BaseLLM
from app.services.message_generation_service import (
    MessageGenerationError,
    MessageGenerationService,
)
from app.services.prompt_renderer import PromptRenderer
from tests.conftest import MockLLM

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "app" / "prompts"


@pytest.fixture
def prompt_router() -> PromptRouter:
    return PromptRouter(prompts_dir=PROMPTS_DIR)


@pytest.fixture
def prompt_renderer() -> PromptRenderer:
    return PromptRenderer()


@pytest.fixture
def generation_service(
    prompt_router: PromptRouter,
    prompt_renderer: PromptRenderer,
    mock_llm: MockLLM,
) -> MessageGenerationService:
    return MessageGenerationService(
        prompt_router=prompt_router,
        prompt_renderer=prompt_renderer,
        llm=mock_llm,
    )


@pytest.mark.unit
class TestMessageGenerationServiceSuccessfulGeneration:
    """Tests for successful message generation workflows."""

    def test_generates_three_valid_variants(
        self,
        generation_service: MessageGenerationService,
        mock_llm: MockLLM,
    ) -> None:
        context = {
            "platform": "whatsapp",
            "relationship": "colleague",
            "tone": "professional",
            "language": "english",
            "purpose": "inform_delay",
        }
        message = "I will be 20 minutes late to the sync due to traffic."

        variants = generation_service.generate(message=message, context=context)

        assert isinstance(variants, list)
        assert len(variants) == 3
        for variant in variants:
            assert isinstance(variant, MessageVariant)
            assert isinstance(variant.style, str) and len(variant.style) > 0
            assert isinstance(variant.text, str) and len(variant.text) > 0

        assert [v.style for v in variants] == ["Professional", "Friendly", "Short"]
        assert mock_llm.call_count == 1

    def test_context_and_message_propagated_to_llm_prompt(
        self,
        generation_service: MessageGenerationService,
        mock_llm: MockLLM,
    ) -> None:
        context = {
            "platform": "gmail",
            "relationship": "manager",
            "tone": "casual",
            "language": "english",
            "purpose": "meeting",
        }
        message = "Can we sync on the Q3 roadmap tomorrow?"

        generation_service.generate(message=message, context=context)

        last_prompt = mock_llm.last_prompt
        assert last_prompt is not None
        assert "Platform: gmail" in last_prompt
        assert "Relationship: manager" in last_prompt
        assert "Tone: casual" in last_prompt
        assert message in last_prompt

    def test_returns_custom_variants_when_configured(
        self,
        generation_service: MessageGenerationService,
        mock_llm: MockLLM,
        sample_custom_variants: list[MessageVariant],
    ) -> None:
        mock_llm.set_response(sample_custom_variants)
        context = {"platform": "sms", "relationship": "friend"}
        message = "See you soon!"

        variants = generation_service.generate(message=message, context=context)

        assert len(variants) == 3
        assert variants[0].style == "Formal"
        assert variants[0].text == "Custom formal response."
        assert variants[1].style == "Casual"
        assert variants[2].style == "Direct"


@pytest.mark.unit
class TestMessageGenerationServiceErrorHandling:
    """Tests empty responses, malformed responses, and LLM failure handling."""

    def test_raises_message_generation_error_when_llm_returns_none(
        self,
        prompt_router: PromptRouter,
        prompt_renderer: PromptRenderer,
        mocker: Any,
    ) -> None:
        fake_llm = mocker.Mock(spec=BaseLLM)
        fake_llm.generate.return_value = None

        service = MessageGenerationService(
            prompt_router=prompt_router,
            prompt_renderer=prompt_renderer,
            llm=fake_llm,
        )

        with pytest.raises(
            MessageGenerationError,
            match="Gemini returned no message variants.",
        ):
            service.generate("Hello", {"platform": "sms"})

    def test_raises_message_generation_error_when_messages_list_is_empty(
        self,
        prompt_router: PromptRouter,
        prompt_renderer: PromptRenderer,
        mocker: Any,
    ) -> None:
        fake_llm = mocker.Mock(spec=BaseLLM)
        fake_llm.generate.return_value = GeminiResponse(messages=[])

        service = MessageGenerationService(
            prompt_router=prompt_router,
            prompt_renderer=prompt_renderer,
            llm=fake_llm,
        )

        with pytest.raises(
            MessageGenerationError,
            match="Gemini returned no message variants.",
        ):
            service.generate("Hello", {"platform": "sms"})

    def test_propagates_llm_exception_directly(
        self,
        generation_service: MessageGenerationService,
        mock_llm: MockLLM,
    ) -> None:
        mock_llm.set_failure(RuntimeError("Gemini service connection timeout"))

        with pytest.raises(
            RuntimeError,
            match="Gemini service connection timeout",
        ):
            generation_service.generate(
                "Important message", {"platform": "whatsapp"}
            )
