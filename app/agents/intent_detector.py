import re
from typing import Any

from app.models.enums import Relationship, Tone
from app.models.message import MessageRequest


class IntentDetector:
    """
    Detects user intent and infers metadata using deterministic rules.

    This component performs lightweight NLP before invoking any LLM.
    """

    RELATIONSHIP_KEYWORDS = {
        Relationship.FAMILY: [
            "mom", "mother", "dad", "father",
            "brother", "sister", "parents",
            "wife", "husband", "uncle", "aunt"
        ],
        Relationship.FRIEND: [
            "friend", "buddy", "bro", "mate"
        ],
        Relationship.MANAGER: [
            "manager", "boss", "lead", "team lead"
        ],
        Relationship.HR: [
            "hr", "human resources", "recruiter"
        ],
        Relationship.PROFESSOR: [
            "professor", "teacher", "faculty", "mentor"
        ],
        Relationship.COLLEAGUE: [
            "colleague", "coworker", "teammate"
        ],
        Relationship.CLIENT: [
            "client", "customer"
        ],
    }

    TONE_KEYWORDS = {
        Tone.APOLOGETIC: [
            "sorry", "apologize", "apologies"
        ],
        Tone.RESPECTFUL: [
            "thank you", "thanks", "appreciate"
        ],
        Tone.PROFESSIONAL: [
            "meeting", "deadline", "project",
            "report", "official"
        ],
        Tone.FRIENDLY: [
            "hey", "hi", "hello"
        ]
    }

    PURPOSE_KEYWORDS = {
        "inform_delay": [
            "late", "delay", "traffic"
        ],
        "meeting": [
            "meeting", "call", "zoom"
        ],
        "greeting": [
            "birthday", "anniversary"
        ],
        "congratulate": [
            "congratulations", "congrats"
        ],
        "leave_request": [
            "leave", "vacation"
        ],
        "apology": [
            "sorry", "apologize"
        ]
    }

    def _contains_keyword(self, text: str, keywords: list[str]) -> bool:
        """Return True if any keyword exists in text."""
        text = text.lower()

        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                return True

        return False

    def _detect_relationship(self, text: str) -> tuple[Relationship | None, float]:
        """Infer relationship and confidence."""

        for relationship, keywords in self.RELATIONSHIP_KEYWORDS.items():
            if self._contains_keyword(text, keywords):
                return relationship, 0.95

        return None, 0.30

    def _detect_tone(self, text: str) -> tuple[Tone, float]:
        """Infer tone and confidence."""

        for tone, keywords in self.TONE_KEYWORDS.items():
            if self._contains_keyword(text, keywords):
                return tone, 0.90

        return Tone.CASUAL, 0.60

    def _detect_purpose(self, text: str) -> tuple[str, float]:
        """Infer message purpose."""

        for purpose, keywords in self.PURPOSE_KEYWORDS.items():
            if self._contains_keyword(text, keywords):
                return purpose, 0.90

        return "general", 0.50

    def detect(self, request: MessageRequest) -> dict[str, Any]:
        """
        Analyze the request and infer metadata.

        Returns structured information for downstream agents.
        """

        relationship, relationship_conf = (
            (request.relationship, 1.0)
            if request.relationship
            else self._detect_relationship(request.message)
        )

        tone, tone_conf = (
            (request.tone, 1.0)
            if request.tone
            else self._detect_tone(request.message)
        )

        purpose, purpose_conf = self._detect_purpose(request.message)

        return {
            "platform": request.platform,
            "relationship": relationship,
            "relationship_confidence": relationship_conf,
            "language": request.language,
            "tone": tone,
            "tone_confidence": tone_conf,
            "purpose": purpose,
            "purpose_confidence": purpose_conf,
        }