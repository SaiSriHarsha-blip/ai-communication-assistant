from typing import Any

from app.models.enums import Language
from app.models.message import MessageRequest


class ContextBuilder:
    """
    Builds the final context for the AI agent by combining
    explicit user input with inferred metadata.

    It also determines whether clarification is required
    before invoking the LLM.
    """

    RELATIONSHIP_CONFIDENCE_THRESHOLD = 0.8

    CLARIFICATION_QUESTIONS = {
        "platform": (
            "Which platform should I prepare this message for? "
            "(WhatsApp, Gmail, Instagram, LinkedIn or SMS)"
        ),
        "relationship": (
            "Who is the recipient? "
            "(Friend, Family, Manager, HR, Professor, Colleague or Client)"
        ),
        "language": (
            "Which language would you like me to use? "
            "(English, Telugu, Hindi or Mixed)"
        ),
    }

    def build_context(
        self,
        request: MessageRequest,
        detected: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Merge explicit request values with detected metadata,
        validate the context, and determine whether clarification
        is required.

        Returns:
            {
                "context": {...},
                "needs_clarification": bool,
                "missing_fields": list[str],
                "question": str | None
            }
        """

        context = {
            "platform": request.platform or detected.get("platform"),
            "relationship": request.relationship or detected.get("relationship"),
            "language": request.language
            or detected.get("language")
            or Language.ENGLISH,
            "tone": request.tone or detected.get("tone"),
            "purpose": detected.get("purpose", "general"),
        }

        missing_fields: list[str] = []

        relationship_confidence = detected.get(
            "relationship_confidence",
            1.0,
        )

        if (
            context["relationship"] is None
            or relationship_confidence < self.RELATIONSHIP_CONFIDENCE_THRESHOLD
        ):
            missing_fields.append("relationship")

        if context["platform"] is None:
            missing_fields.append("platform")

        question = None

        if missing_fields:
            first_missing = missing_fields[0]
            question = self.CLARIFICATION_QUESTIONS.get(first_missing)

        return {
            "context": context,
            "needs_clarification": len(missing_fields) > 0,
            "missing_fields": missing_fields,
            "question": question,
        }