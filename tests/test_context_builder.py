"""
Unit tests for ContextBuilder (app.agents.context_builder).

Verifies merging of explicit user input with inferred metadata, confidence threshold
evaluation, missing field tracking order, clarification question generation, and default fallbacks.
"""

from typing import Any
import pytest

from app.agents.context_builder import ContextBuilder
from app.models.enums import Language, Platform, Relationship, Tone
from app.models.message import MessageRequest


@pytest.fixture
def builder() -> ContextBuilder:
    return ContextBuilder()


@pytest.mark.unit
class TestContextBuilderCompleteContext:
    """Tests when all required context is available (no clarification needed)."""

    def test_complete_explicit_context_requires_no_clarification(
        self, builder: ContextBuilder
    ) -> None:
        req = MessageRequest(
            message="Meeting tomorrow at 10 AM.",
            platform=Platform.GMAIL,
            relationship=Relationship.MANAGER,
            tone=Tone.PROFESSIONAL,
            language=Language.ENGLISH,
        )
        detected = {
            "platform": Platform.GMAIL,
            "relationship": Relationship.MANAGER,
            "relationship_confidence": 1.0,
            "tone": Tone.PROFESSIONAL,
            "tone_confidence": 1.0,
            "purpose": "meeting",
            "purpose_confidence": 0.90,
        }

        result = builder.build_context(req, detected)

        assert result["needs_clarification"] is False
        assert result["missing_fields"] == []
        assert result["question"] is None
        assert result["context"]["platform"] == Platform.GMAIL
        assert result["context"]["relationship"] == Relationship.MANAGER
        assert result["context"]["tone"] == Tone.PROFESSIONAL
        assert result["context"]["language"] == Language.ENGLISH
        assert result["context"]["purpose"] == "meeting"

    def test_high_confidence_inferred_relationship_requires_no_clarification(
        self, builder: ContextBuilder
    ) -> None:
        """When platform is provided and relationship is inferred with confidence >= 0.8."""
        req = MessageRequest(
            message="Hey mom, love you lots!",
            platform=Platform.WHATSAPP,
        )
        detected = {
            "platform": Platform.WHATSAPP,
            "relationship": Relationship.FAMILY,
            "relationship_confidence": 0.95,  # Above threshold 0.8
            "tone": Tone.FRIENDLY,
            "tone_confidence": 0.90,
            "purpose": "greeting",
        }

        result = builder.build_context(req, detected)

        assert result["needs_clarification"] is False
        assert result["missing_fields"] == []
        assert result["question"] is None
        assert result["context"]["relationship"] == Relationship.FAMILY


@pytest.mark.unit
class TestContextBuilderClarificationScenarios:
    """Tests for various combinations of missing context and clarification triggers."""

    def test_missing_platform_only_triggers_platform_clarification(
        self, builder: ContextBuilder
    ) -> None:
        req = MessageRequest(
            message="Hey boss, here is the report.",
            relationship=Relationship.MANAGER,
        )
        detected = {
            "platform": None,
            "relationship": Relationship.MANAGER,
            "relationship_confidence": 1.0,
            "tone": Tone.PROFESSIONAL,
            "purpose": "meeting",
        }

        result = builder.build_context(req, detected)

        assert result["needs_clarification"] is True
        assert result["missing_fields"] == ["platform"]
        assert result["question"] == ContextBuilder.CLARIFICATION_QUESTIONS["platform"]
        assert "Which platform" in result["question"]

    def test_missing_relationship_only_triggers_relationship_clarification(
        self, builder: ContextBuilder
    ) -> None:
        req = MessageRequest(
            message="Please review the document by 5 PM.",
            platform=Platform.SLACK if hasattr(Platform, "SLACK") else Platform.WHATSAPP,
        )
        detected = {
            "platform": req.platform,
            "relationship": None,
            "relationship_confidence": 0.30,  # Below threshold
            "tone": Tone.PROFESSIONAL,
            "purpose": "general",
        }

        result = builder.build_context(req, detected)

        assert result["needs_clarification"] is True
        assert result["missing_fields"] == ["relationship"]
        assert result["question"] == ContextBuilder.CLARIFICATION_QUESTIONS["relationship"]
        assert "Who is the recipient?" in result["question"]

    def test_low_confidence_relationship_triggers_clarification(
        self, builder: ContextBuilder
    ) -> None:
        """Even if relationship is inferred, if confidence < 0.8, clarification is required."""
        req = MessageRequest(
            message="Reviewing the proposal now.",
            platform=Platform.LINKEDIN,
        )
        detected = {
            "platform": Platform.LINKEDIN,
            "relationship": Relationship.CLIENT,
            "relationship_confidence": 0.79,  # Just below 0.8 threshold
            "tone": Tone.PROFESSIONAL,
            "purpose": "general",
        }

        result = builder.build_context(req, detected)

        assert result["needs_clarification"] is True
        assert "relationship" in result["missing_fields"]
        assert result["question"] == ContextBuilder.CLARIFICATION_QUESTIONS["relationship"]

    def test_both_platform_and_relationship_missing_order_and_question(
        self, builder: ContextBuilder
    ) -> None:
        """When both are missing, relationship is prioritized first in missing_fields and question."""
        req = MessageRequest(
            message="Checking on the latest project update."
        )
        detected = {
            "platform": None,
            "relationship": None,
            "relationship_confidence": 0.30,
            "tone": Tone.CASUAL,
            "purpose": "general",
        }

        result = builder.build_context(req, detected)

        assert result["needs_clarification"] is True
        assert result["missing_fields"] == ["relationship", "platform"]
        # First missing field drives the question
        assert result["question"] == ContextBuilder.CLARIFICATION_QUESTIONS["relationship"]


@pytest.mark.unit
class TestContextBuilderPrecedenceAndDefaults:
    """Tests explicit override precedence, language fallback, and purpose propagation."""

    def test_explicit_fields_override_detected_fields(
        self, builder: ContextBuilder
    ) -> None:
        req = MessageRequest(
            message="Hey mom, see you soon.",
            platform=Platform.SMS,
            relationship=Relationship.COLLEAGUE,
            tone=Tone.FORMAL,
            language=Language.HINDI,
        )
        detected = {
            "platform": Platform.WHATSAPP,
            "relationship": Relationship.FAMILY,
            "relationship_confidence": 0.95,
            "tone": Tone.FRIENDLY,
            "language": Language.ENGLISH,
            "purpose": "greeting",
        }

        result = builder.build_context(req, detected)

        context = result["context"]
        assert context["platform"] == Platform.SMS
        assert context["relationship"] == Relationship.COLLEAGUE
        assert context["tone"] == Tone.FORMAL
        assert context["language"] == Language.HINDI
        assert context["purpose"] == "greeting"

    def test_language_defaults_to_english_when_unspecified(
        self, builder: ContextBuilder
    ) -> None:
        req = MessageRequest(
            message="Hello there!",
            platform=Platform.WHATSAPP,
            relationship=Relationship.FRIEND,
            language=None,
        )
        detected: dict[str, Any] = {
            "platform": Platform.WHATSAPP,
            "relationship": Relationship.FRIEND,
            "relationship_confidence": 1.0,
        }

        result = builder.build_context(req, detected)

        assert result["context"]["language"] == Language.ENGLISH

    def test_purpose_defaults_to_general_when_missing_from_detected(
        self, builder: ContextBuilder
    ) -> None:
        req = MessageRequest(
            message="Status report for sprint 4.",
            platform=Platform.GMAIL,
            relationship=Relationship.MANAGER,
        )
        detected: dict[str, Any] = {
            "platform": Platform.GMAIL,
            "relationship": Relationship.MANAGER,
            "relationship_confidence": 1.0,
            # No purpose in detected
        }

        result = builder.build_context(req, detected)

        assert result["context"]["purpose"] == "general"

    def test_clarification_questions_dictionary_contents(self) -> None:
        """Verifies the predefined clarification questions for each supported field."""
        questions = ContextBuilder.CLARIFICATION_QUESTIONS
        assert "platform" in questions
        assert "relationship" in questions
        assert "language" in questions
        assert ContextBuilder.RELATIONSHIP_CONFIDENCE_THRESHOLD == 0.8
