"""
MessagePilot — Pytest Shared Fixtures and Test Infrastructure (Phase 4, Step 1).

This module defines shared fixtures, mock objects, and configuration for testing
the MessagePilot backend services, agents, pipelines, and FastAPI endpoints.
All LLM operations are mocked in-memory with zero network or external API dependency.
"""

from collections.abc import Generator
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient
import pytest

from app.agents.communication_agent import CommunicationAgent
from app.agents.context_builder import ContextBuilder
from app.agents.intent_detector import IntentDetector
from app.agents.prompt_router import PromptRouter
from app.api.message import get_communication_agent
from app.core.rate_limiter import limiter
from app.main import app
from app.models.gemini_response import GeminiResponse
from app.models.message import MessageVariant
from app.services.base_llm import BaseLLM
from app.services.message_generation_service import MessageGenerationService
from app.services.prompt_renderer import PromptRenderer

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "app" / "prompts"


# ---------------------------------------------------------------------------
# Mock LLM Implementation
# ---------------------------------------------------------------------------


class MockLLM(BaseLLM):
    """
    In-memory mock for BaseLLM.

    Features:
    - Zero network calls; safe for offline/isolated execution.
    - Returns deterministic GeminiResponse with 3 valid message variants.
    - Tracks call count, invocation parameters, and full prompt history.
    - Configurable responses and simulated failure triggers.
    """

    def __init__(
        self,
        default_variants: list[MessageVariant] | None = None,
        should_fail: bool = False,
        failure_exception: Exception | None = None,
    ) -> None:
        if default_variants is None:
            self._default_variants = [
                MessageVariant(
                    style="Professional",
                    text=(
                        "Dear team, please be advised that the project milestone "
                        "has been completed according to the updated schedule."
                    ),
                ),
                MessageVariant(
                    style="Friendly",
                    text=(
                        "Hey everyone! Great news — we've officially completed the "
                        "project milestone on time."
                    ),
                ),
                MessageVariant(
                    style="Short",
                    text="Project milestone completed on schedule.",
                ),
            ]
        else:
            self._default_variants = default_variants

        self.custom_response: GeminiResponse | None = None
        self.should_fail: bool = should_fail
        self.failure_exception: Exception = failure_exception or RuntimeError(
            "Simulated LLM service failure."
        )
        self.calls: list[dict[str, Any]] = []
        self.prompts_history: list[str] = []

    @property
    def call_count(self) -> int:
        """Total number of times generate() has been called."""
        return len(self.calls)

    @property
    def last_prompt(self) -> str | None:
        """The most recent prompt passed to generate(), or None if not called."""
        return self.prompts_history[-1] if self.prompts_history else None

    def set_response(self, variants: list[MessageVariant]) -> None:
        """Configure custom message variants to return from generate()."""
        self.custom_response = GeminiResponse(messages=variants)

    def set_failure(self, exception: Exception | None = None) -> None:
        """Configure the mock to raise an exception on next generate() invocation."""
        self.should_fail = True
        if exception is not None:
            self.failure_exception = exception

    def reset_state(self) -> None:
        """Reset call recording, history, custom responses, and failure state."""
        self.calls.clear()
        self.prompts_history.clear()
        self.custom_response = None
        self.should_fail = False
        self.failure_exception = RuntimeError("Simulated LLM service failure.")

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_output_tokens: int = 512,
    ) -> GeminiResponse:
        """
        Record invocation and return deterministic structured response.
        Raises configured exception if should_fail is True.
        """
        self.calls.append(
            {
                "prompt": prompt,
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            }
        )
        self.prompts_history.append(prompt)

        if self.should_fail:
            raise self.failure_exception

        if self.custom_response is not None:
            return self.custom_response

        return GeminiResponse(messages=list(self._default_variants))


# ---------------------------------------------------------------------------
# Core Pytest Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_llm() -> MockLLM:
    """
    Provides a fresh, isolated MockLLM instance.
    """
    return MockLLM()


@pytest.fixture
def mock_communication_agent(mock_llm: MockLLM) -> CommunicationAgent:
    """
    Constructs a real CommunicationAgent wired with actual production sub-components
    (IntentDetector, ContextBuilder, PromptRouter, PromptRenderer) and injects
    MockLLM into MessageGenerationService.
    """
    prompt_router = PromptRouter(prompts_dir=PROMPTS_DIR)
    prompt_renderer = PromptRenderer()

    generation_service = MessageGenerationService(
        prompt_router=prompt_router,
        prompt_renderer=prompt_renderer,
        llm=mock_llm,
    )

    return CommunicationAgent(
        intent_detector=IntentDetector(),
        context_builder=ContextBuilder(),
        message_generation_service=generation_service,
    )


@pytest.fixture
def client(
    mock_communication_agent: CommunicationAgent,
) -> Generator[TestClient, None, None]:
    """
    FastAPI TestClient with get_communication_agent dependency overridden
    to use mock_communication_agent. Ensures clean dependency override teardown.
    """
    original_override = app.dependency_overrides.get(get_communication_agent)
    app.dependency_overrides[get_communication_agent] = (
        lambda: mock_communication_agent
    )

    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client

    if original_override is not None:
        app.dependency_overrides[get_communication_agent] = original_override
    else:
        app.dependency_overrides.pop(get_communication_agent, None)


@pytest.fixture(autouse=True)
def reset_rate_limiter() -> Generator[None, None, None]:
    """
    Autouse fixture that resets the SlowAPI in-memory limiter before and after
    each test execution to avoid cross-test rate limit contamination.
    """
    limiter.reset()
    yield
    limiter.reset()


# ---------------------------------------------------------------------------
# Data Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_valid_request_payload() -> dict[str, Any]:
    """
    Standard valid request payload providing all context explicitly.
    """
    return {
        "message": (
            "I will be 20 minutes late to the team sync due to heavy traffic."
        ),
        "platform": "whatsapp",
        "relationship": "colleague",
        "tone": "professional",
        "language": "english",
    }


@pytest.fixture
def sample_clarification_request_payload() -> dict[str, Any]:
    """
    Vague request payload that triggers context clarification (missing relationship and platform).
    """
    return {
        "message": "Hey there just checking in on the project status.",
    }


@pytest.fixture
def sample_custom_variants() -> list[MessageVariant]:
    """
    Sample custom variants for testing custom response overrides.
    """
    return [
        MessageVariant(style="Formal", text="Custom formal response."),
        MessageVariant(style="Casual", text="Custom casual response."),
        MessageVariant(style="Direct", text="Custom direct response."),
    ]
