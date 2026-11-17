"""
Unit tests for the IntentDetector agent (app.agents.intent_detector).

Verifies deterministic keyword-based metadata inference, word-boundary protection,
confidence scoring, fallback defaults, and explicit request override precedence.
"""

import pytest

from app.agents.intent_detector import IntentDetector
from app.models.enums import Language, Platform, Relationship, Tone
from app.models.message import MessageRequest


@pytest.fixture
def detector() -> IntentDetector:
    return IntentDetector()


@pytest.mark.unit
class TestIntentDetectorRelationship:
    """Tests for relationship detection from message text and explicit overrides."""

    @pytest.mark.parametrize(
        ("message", "expected_relationship"),
        [
            ("Hey mom, I will be late for dinner.", Relationship.FAMILY),
            ("Happy birthday to the best father ever!", Relationship.FAMILY),
            ("Thanks wife for helping with the groceries.", Relationship.FAMILY),
            ("My sister and brother are coming over.", Relationship.FAMILY),
            ("Hey bro, are we playing basketball tonight?", Relationship.FRIEND),
            ("Good morning buddy, how is the trip?", Relationship.FRIEND),
            ("Thanks mate, catch you later.", Relationship.FRIEND),
            ("Dear manager, please review my submission.", Relationship.MANAGER),
            ("Hey boss, here is the quick project update.", Relationship.MANAGER),
            ("Our team lead reviewed the latest code changes.", Relationship.MANAGER),
            ("Contact hr for queries on employee benefits.", Relationship.HR),
            ("The recruiter emailed me regarding the position.", Relationship.HR),
            ("Speaking with human resources regarding leave.", Relationship.HR),
            ("Dear professor, could you review my thesis draft?", Relationship.PROFESSOR),
            ("Our faculty advisor approved the submission.", Relationship.PROFESSOR),
            ("Hello teammate, let's sync up on the sprint tasks.", Relationship.COLLEAGUE),
            ("My coworker suggested this architecture.", Relationship.COLLEAGUE),
            ("The client approved the final proposal today.", Relationship.CLIENT),
            ("Our customer sent positive feedback on the launch.", Relationship.CLIENT),
        ],
    )
    def test_inferred_relationship_from_keywords(
        self,
        detector: IntentDetector,
        message: str,
        expected_relationship: Relationship,
    ) -> None:
        req = MessageRequest(message=message)
        result = detector.detect(req)

        assert result["relationship"] == expected_relationship
        assert result["relationship_confidence"] == 0.95

    def test_relationship_unknown_fallback(
        self, detector: IntentDetector
    ) -> None:
        req = MessageRequest(
            message="Please deploy the latest release to the production cluster."
        )
        result = detector.detect(req)

        assert result["relationship"] is None
        assert result["relationship_confidence"] == 0.30

    def test_explicit_relationship_overrides_inferred_keywords(
        self, detector: IntentDetector
    ) -> None:
        # Message has "mom" (Family keyword), but explicit request specifies Colleague
        req = MessageRequest(
            message="Hey mom, could you check the quarterly balance sheet?",
            relationship=Relationship.COLLEAGUE,
        )
        result = detector.detect(req)

        assert result["relationship"] == Relationship.COLLEAGUE
        assert result["relationship_confidence"] == 1.0


@pytest.mark.unit
class TestIntentDetectorTone:
    """Tests for tone detection from message text and explicit overrides."""

    @pytest.mark.parametrize(
        ("message", "expected_tone"),
        [
            ("I am so sorry for the delay in responding.", Tone.APOLOGETIC),
            ("Please accept my apologies for missing the meeting.", Tone.APOLOGETIC),
            ("Thank you so much for the assistance today.", Tone.RESPECTFUL),
            ("I really appreciate your quick turnaround.", Tone.RESPECTFUL),
            ("The official project deadline is Friday at 5 PM.", Tone.PROFESSIONAL),
            ("Please submit the quarterly report for review.", Tone.PROFESSIONAL),
            ("Hey team, what are the plans for today?", Tone.FRIENDLY),
            ("Hello everyone, hope you are having a great week.", Tone.FRIENDLY),
        ],
    )
    def test_inferred_tone_from_keywords(
        self,
        detector: IntentDetector,
        message: str,
        expected_tone: Tone,
    ) -> None:
        req = MessageRequest(message=message)
        result = detector.detect(req)

        assert result["tone"] == expected_tone
        assert result["tone_confidence"] == 0.90

    def test_tone_unknown_fallback_to_casual(
        self, detector: IntentDetector
    ) -> None:
        req = MessageRequest(
            message="The automated pipeline deployed container version 3.2.1."
        )
        result = detector.detect(req)

        assert result["tone"] == Tone.CASUAL
        assert result["tone_confidence"] == 0.60

    def test_explicit_tone_overrides_inferred_tone(
        self, detector: IntentDetector
    ) -> None:
        # Message contains "sorry" (Apologetic), but explicit tone is Formal
        req = MessageRequest(
            message="I am sorry for the delay in sending the report.",
            tone=Tone.FORMAL,
        )
        result = detector.detect(req)

        assert result["tone"] == Tone.FORMAL
        assert result["tone_confidence"] == 1.0


@pytest.mark.unit
class TestIntentDetectorPurpose:
    """Tests for message purpose inference."""

    @pytest.mark.parametrize(
        ("message", "expected_purpose"),
        [
            ("Stuck in traffic, will be 20 minutes late.", "inform_delay"),
            ("Can we schedule a Zoom call to discuss the demo?", "meeting"),
            ("Wishing you a very happy birthday and great year ahead!", "greeting"),
            ("Huge congratulations on passing the bar exam!", "congratulate"),
            ("I would like to apply for vacation leave next week.", "leave_request"),
            ("I am truly sorry for any inconvenience caused.", "apology"),
        ],
    )
    def test_inferred_purpose_from_keywords(
        self,
        detector: IntentDetector,
        message: str,
        expected_purpose: str,
    ) -> None:
        req = MessageRequest(message=message)
        result = detector.detect(req)

        assert result["purpose"] == expected_purpose
        assert result["purpose_confidence"] == 0.90

    def test_purpose_unknown_fallback_to_general(
        self, detector: IntentDetector
    ) -> None:
        req = MessageRequest(
            message="The package was dropped off at the reception desk."
        )
        result = detector.detect(req)

        assert result["purpose"] == "general"
        assert result["purpose_confidence"] == 0.50


@pytest.mark.unit
class TestIntentDetectorWordBoundaryAndRobustness:
    """Tests regex word boundary protections preventing substring false positives."""

    @pytest.mark.parametrize(
        ("message", "false_positive_candidate"),
        [
            ("The TV broadcast will air tomorrow at nine.", Relationship.FRIEND),  # "bro" in broadcast
            ("She is studying abroad for her master's degree.", Relationship.FRIEND),  # "bro" in abroad
            ("Please shred the confidential documents.", Relationship.HR),  # "hr" in shred
            ("The physical therapist recommended these exercises.", Relationship.HR),  # "hr" in therapist
            ("The movie was a box office bomb according to critics.", Relationship.FAMILY),  # "mom" in bomb
        ],
    )
    def test_word_boundaries_prevent_false_positives(
        self,
        detector: IntentDetector,
        message: str,
        false_positive_candidate: Relationship,
    ) -> None:
        req = MessageRequest(message=message)
        result = detector.detect(req)

        assert result["relationship"] != false_positive_candidate

    def test_platform_and_language_pass_through(
        self, detector: IntentDetector
    ) -> None:
        req = MessageRequest(
            message="Checking on the latest project deployment status.",
            platform=Platform.LINKEDIN,
            language=Language.TELUGU,
        )
        result = detector.detect(req)

        assert result["platform"] == Platform.LINKEDIN
        assert result["language"] == Language.TELUGU
