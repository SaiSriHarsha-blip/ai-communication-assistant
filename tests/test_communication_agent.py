"""
Unit and pipeline integration tests for CommunicationAgent (app.agents.communication_agent).

Verifies the end-to-end orchestration pipeline from MessageRequest through IntentDetector,
ContextBuilder, clarification gating, MessageGenerationService (with MockLLM), and MessageResponse.
"""

from typing import Any
import pytest

from app.agents.communication_agent import CommunicationAgent
from app.models.context import MessageContext
from app.models.enums import Language, Platform, Relationship, Tone
from app.models.message import MessageRequest, MessageResponse, MessageVariant
from app.services.message_generation_service import MessageGenerationError
from tests.conftest import MockLLM


@pytest.mark.unit
class TestCommunicationAgentEndToEndSuccess:
    """Tests for complete requests that successfully traverse all 5 pipeline steps."""

    def test_complete_request_generates_three_variants_and_message_response(
        self,
        mock_communication_agent: CommunicationAgent,
        mock_llm: MockLLM,
    ) -> None:
        req = MessageRequest(
            message="I will be 20 minutes late to our sync due to heavy highway traffic.",
            platform=Platform.WHATSAPP,
            relationship=Relationship.COLLEAGUE,
            tone=Tone.PROFESSIONAL,
            language=Language.ENGLISH,
        )

        response = mock_communication_agent.process(req)

        assert isinstance(response, MessageResponse)
        assert response.original_message == req.message
        assert len(response.messages) == 3
        for variant in response.messages:
            assert isinstance(variant, MessageVariant)
            assert variant.text and len(variant.text) > 0

        assert response.detected_platform == Platform.WHATSAPP
        assert response.detected_relationship == Relationship.COLLEAGUE
        assert response.detected_language == Language.ENGLISH
        assert response.detected_tone == Tone.PROFESSIONAL

        assert mock_llm.call_count == 1

    def test_explicit_relationship_overrides_inferred_in_final_response(
        self,
        mock_communication_agent: CommunicationAgent,
        mock_llm: MockLLM,
    ) -> None:
        # Message has "mom" (Family), but explicit request relationship is Colleague
        req = MessageRequest(
            message="Hey mom, could you sign off on the Q3 budget spreadsheet?",
            platform=Platform.GMAIL,
            relationship=Relationship.COLLEAGUE,
        )

        response = mock_communication_agent.process(req)

        assert isinstance(response, MessageResponse)
        assert response.detected_relationship == Relationship.COLLEAGUE
        assert mock_llm.call_count == 1

    def test_explicit_tone_and_language_preserved(
        self,
        mock_communication_agent: CommunicationAgent,
        mock_llm: MockLLM,
    ) -> None:
        req = MessageRequest(
            message="Can we schedule a call to review the new designs tomorrow?",
            platform=Platform.LINKEDIN,
            relationship=Relationship.CLIENT,
            tone=Tone.CASUAL,
            language=Language.TELUGU,
        )

        response = mock_communication_agent.process(req)

        assert isinstance(response, MessageResponse)
        assert response.detected_tone == Tone.CASUAL
        assert response.detected_language == Language.TELUGU
        assert mock_llm.call_count == 1

    def test_three_custom_variants_reach_final_response(
        self,
        mock_communication_agent: CommunicationAgent,
        mock_llm: MockLLM,
        sample_custom_variants: list[MessageVariant],
    ) -> None:
        mock_llm.set_response(sample_custom_variants)
        req = MessageRequest(
            message="Please update the deployment ticket.",
            platform=Platform.SMS,
            relationship=Relationship.COLLEAGUE,
        )

        response = mock_communication_agent.process(req)

        assert isinstance(response, MessageResponse)
        assert response.messages[0].text == "Custom formal response."
        assert response.messages[1].text == "Custom casual response."
        assert response.messages[2].text == "Custom direct response."


@pytest.mark.unit
class TestCommunicationAgentClarificationWorkflow:
    """Tests for requests requiring clarification where the workflow pauses at Step 3."""

    def test_missing_relationship_pauses_workflow_without_calling_llm(
        self,
        mock_communication_agent: CommunicationAgent,
        mock_llm: MockLLM,
    ) -> None:
        # Platform is explicit, but message has no relationship keywords
        req = MessageRequest(
            message="Please review the document by 5 PM today.",
            platform=Platform.WHATSAPP,
        )

        result = mock_communication_agent.process(req)

        assert isinstance(result, MessageContext)
        assert result.needs_clarification is True
        assert result.missing_fields == ["relationship"]
        assert "Who is the recipient?" in result.question

        # Crucial check: LLM must NEVER be called when clarification is needed
        assert mock_llm.call_count == 0

    def test_missing_platform_pauses_workflow_without_calling_llm(
        self,
        mock_communication_agent: CommunicationAgent,
        mock_llm: MockLLM,
    ) -> None:
        # Relationship is explicit, but platform is None
        req = MessageRequest(
            message="Hey boss, I have completed the assigned code review.",
            relationship=Relationship.MANAGER,
        )

        result = mock_communication_agent.process(req)

        assert isinstance(result, MessageContext)
        assert result.needs_clarification is True
        assert result.missing_fields == ["platform"]
        assert "Which platform" in result.question

        assert mock_llm.call_count == 0

    def test_both_missing_fields_follows_order_and_prioritizes_relationship_question(
        self,
        mock_communication_agent: CommunicationAgent,
        mock_llm: MockLLM,
    ) -> None:
        # Neither platform nor relationship provided or inferrable
        req = MessageRequest(
            message="Just checking in on the project status and deliverables."
        )

        result = mock_communication_agent.process(req)

        assert isinstance(result, MessageContext)
        assert result.needs_clarification is True
        assert result.missing_fields == ["relationship", "platform"]
        # In context builder, relationship is checked first and drives the question
        assert "Who is the recipient?" in result.question

        assert mock_llm.call_count == 0


@pytest.mark.unit
class TestCommunicationAgentErrorHandling:
    """Tests exception bubbling and logging in CommunicationAgent."""

    def test_re_raises_generation_service_error(
        self,
        mock_communication_agent: CommunicationAgent,
        mock_llm: MockLLM,
    ) -> None:
        # LLM failure triggers generation failure, which must be logged and re-raised
        mock_llm.set_failure(RuntimeError("Unrecoverable model error"))

        req = MessageRequest(
            message="Meeting tomorrow at 10 AM.",
            platform=Platform.GMAIL,
            relationship=Relationship.COLLEAGUE,
        )

        with pytest.raises(RuntimeError, match="Unrecoverable model error"):
            mock_communication_agent.process(req)

    def test_re_raises_message_generation_empty_error(
        self,
        mock_communication_agent: CommunicationAgent,
        mocker: Any,
    ) -> None:
        # When message_generation_service raises MessageGenerationError
        mocker.patch.object(
            mock_communication_agent.message_generation_service,
            "generate",
            side_effect=MessageGenerationError("No message variants produced"),
        )

        req = MessageRequest(
            message="Review deadline is Friday.",
            platform=Platform.SMS,
            relationship=Relationship.FRIEND,
        )

        with pytest.raises(MessageGenerationError, match="No message variants produced"):
            mock_communication_agent.process(req)
