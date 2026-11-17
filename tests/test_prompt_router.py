"""
Unit tests for PromptRouter (app.agents.prompt_router).

Verifies prompt template routing hierarchy, platform defaults, case handling,
production templates (Gmail casual, SMS, WhatsApp), fallback progression using tmp_path,
OSError recovery, and ultimate hardcoded fallback.
"""

from pathlib import Path
from typing import Any
import pytest

from app.agents.prompt_router import PromptRouter

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "app" / "prompts"


@pytest.fixture
def router() -> PromptRouter:
    return PromptRouter(prompts_dir=PROMPTS_DIR)


@pytest.mark.unit
class TestPromptRouterPlatformDefaults:
    """Verifies default template filenames mapped per platform."""

    @pytest.mark.parametrize(
        ("platform", "expected_default"),
        [
            ("gmail", "formal"),
            ("instagram", "caption"),
            ("linkedin", "professional"),
            ("sms", "default"),
            ("whatsapp", "default"),
            ("slack", "default"),
            ("unknown_platform", "default"),
        ],
    )
    def test_platform_default_mappings(
        self, router: PromptRouter, platform: str, expected_default: str
    ) -> None:
        assert router._get_platform_default(platform) == expected_default


@pytest.mark.unit
class TestPromptRouterProductionTemplates:
    """Verifies that actual repository prompt templates are correctly resolved."""

    def test_routes_to_gmail_casual_template(self, router: PromptRouter) -> None:
        context = {
            "platform": "gmail",
            "relationship": "colleague",
            "tone": "casual",
        }
        prompt = router.get_prompt(context)

        assert "expert email writing assistant specializing in casual" in prompt
        assert "Platform: {{ platform }}" in prompt

    def test_routes_to_gmail_formal_template_as_platform_default(
        self, router: PromptRouter
    ) -> None:
        # Tone "formal" or unspecified tone for gmail resolves to gmail/formal.md
        context = {
            "platform": "gmail",
            "relationship": "client",
            "tone": "formal",
        }
        prompt = router.get_prompt(context)

        assert "formal" in prompt.lower()
        assert "email" in prompt.lower()

    def test_routes_to_sms_default_template(self, router: PromptRouter) -> None:
        context = {
            "platform": "sms",
            "relationship": "friend",
            "tone": "casual",
        }
        prompt = router.get_prompt(context)

        assert "You are an SMS writing assistant." in prompt
        assert "{{ message }}" in prompt

    def test_routes_to_whatsapp_default_template(
        self, router: PromptRouter
    ) -> None:
        context = {
            "platform": "whatsapp",
            "relationship": "colleague",
            "tone": "friendly",
        }
        prompt = router.get_prompt(context)

        assert "WhatsApp" in prompt
        assert "{{ message }}" in prompt

    def test_routes_to_global_default_for_unknown_platform(
        self, router: PromptRouter
    ) -> None:
        """When platform directory does not exist, routes to app/prompts/default.md."""
        context = {
            "platform": "nonexistent_platform_xyz",
            "relationship": "friend",
            "tone": "casual",
        }
        prompt = router.get_prompt(context)

        # Global default.md exists in app/prompts
        assert len(prompt) > 0
        assert "default" in prompt.lower() or "ai" in prompt.lower()


@pytest.mark.unit
class TestPromptRouterCaseHandling:
    """Verifies case normalization of platform, relationship, and tone context."""

    @pytest.mark.parametrize(
        "context",
        [
            {"platform": "GMAIL", "tone": "CASUAL"},
            {"platform": "Gmail", "tone": "Casual"},
            {"platform": "gMaIl", "tone": "cAsUaL"},
        ],
    )
    def test_case_insensitive_routing(
        self, router: PromptRouter, context: dict[str, Any]
    ) -> None:
        prompt = router.get_prompt(context)
        assert "expert email writing assistant specializing in casual" in prompt


@pytest.mark.unit
class TestPromptRouterFallbackHierarchy:
    """
    Verifies the 5-tier fallback hierarchy using isolated temporary directories
    without modifying real application templates:
      Tier 1: relationship.md
      Tier 2: tone.md
      Tier 3: platform_default.md
      Tier 4: platform/default.md
      Tier 5: global default.md
      Ultimate: Hardcoded fallback string
    """

    def test_tier_1_relationship_template_precedence(
        self, tmp_path: Path
    ) -> None:
        platform_dir = tmp_path / "custom"
        platform_dir.mkdir()

        (platform_dir / "manager.md").write_text("TIER 1: RELATIONSHIP", encoding="utf-8")
        (platform_dir / "formal.md").write_text("TIER 2: TONE", encoding="utf-8")
        (platform_dir / "default.md").write_text("TIER 4: PLATFORM DEFAULT", encoding="utf-8")

        mock_router = PromptRouter(prompts_dir=tmp_path)
        prompt = mock_router.get_prompt({
            "platform": "custom",
            "relationship": "manager",
            "tone": "formal",
        })

        assert prompt == "TIER 1: RELATIONSHIP"

    def test_tier_2_tone_template_precedence_when_relationship_absent(
        self, tmp_path: Path
    ) -> None:
        platform_dir = tmp_path / "custom"
        platform_dir.mkdir()

        # No relationship template
        (platform_dir / "respectful.md").write_text("TIER 2: TONE", encoding="utf-8")
        (platform_dir / "default.md").write_text("TIER 4: PLATFORM DEFAULT", encoding="utf-8")

        mock_router = PromptRouter(prompts_dir=tmp_path)
        prompt = mock_router.get_prompt({
            "platform": "custom",
            "relationship": "unknown_rel",
            "tone": "respectful",
        })

        assert prompt == "TIER 2: TONE"

    def test_tier_3_platform_default_precedence_when_relationship_and_tone_absent(
        self, tmp_path: Path
    ) -> None:
        gmail_dir = tmp_path / "gmail"
        gmail_dir.mkdir()

        # Default for gmail is "formal"
        (gmail_dir / "formal.md").write_text("TIER 3: GMAIL FORMAL", encoding="utf-8")
        (gmail_dir / "default.md").write_text("TIER 4: DEFAULT", encoding="utf-8")

        mock_router = PromptRouter(prompts_dir=tmp_path)
        prompt = mock_router.get_prompt({
            "platform": "gmail",
            "relationship": "unknown_rel",
            "tone": "unknown_tone",
        })

        assert prompt == "TIER 3: GMAIL FORMAL"

    def test_tier_4_platform_default_md_when_specific_absent(
        self, tmp_path: Path
    ) -> None:
        sms_dir = tmp_path / "sms"
        sms_dir.mkdir()

        (sms_dir / "default.md").write_text("TIER 4: SMS DEFAULT", encoding="utf-8")

        mock_router = PromptRouter(prompts_dir=tmp_path)
        prompt = mock_router.get_prompt({
            "platform": "sms",
            "relationship": "unknown",
            "tone": "unknown",
        })

        assert prompt == "TIER 4: SMS DEFAULT"

    def test_tier_5_global_default_when_platform_dir_has_no_matches(
        self, tmp_path: Path
    ) -> None:
        (tmp_path / "default.md").write_text("TIER 5: GLOBAL DEFAULT", encoding="utf-8")

        mock_router = PromptRouter(prompts_dir=tmp_path)
        prompt = mock_router.get_prompt({
            "platform": "unknown_chat_app",
            "relationship": "friend",
            "tone": "casual",
        })

        assert prompt == "TIER 5: GLOBAL DEFAULT"

    def test_ultimate_hardcoded_fallback_when_all_templates_missing(
        self, tmp_path: Path
    ) -> None:
        """When the prompts directory is completely empty, returns the built-in fallback string."""
        empty_dir = tmp_path / "empty_prompts"
        empty_dir.mkdir()

        mock_router = PromptRouter(prompts_dir=empty_dir)
        prompt = mock_router.get_prompt({"platform": "anything"})

        assert "You are an expert AI communication agent." in prompt
        assert "adhering strictly to the requested platform conventions" in prompt

    def test_oserror_reading_file_falls_back_to_next_candidate(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When an OSError occurs reading one template, router logs warning and attempts next."""
        platform_dir = tmp_path / "testapp"
        platform_dir.mkdir()

        cand1 = platform_dir / "friend.md"
        cand1.write_text("FIRST CANDIDATE", encoding="utf-8")

        cand2 = platform_dir / "default.md"
        cand2.write_text("SECOND CANDIDATE FALLBACK", encoding="utf-8")

        real_read_text = Path.read_text

        def mock_read_text(self_path: Path, *args: Any, **kwargs: Any) -> str:
            if self_path.name == "friend.md":
                raise OSError("Simulated filesystem I/O read failure")
            return real_read_text(self_path, *args, **kwargs)

        monkeypatch.setattr(Path, "read_text", mock_read_text)

        mock_router = PromptRouter(prompts_dir=tmp_path)
        prompt = mock_router.get_prompt({
            "platform": "testapp",
            "relationship": "friend",
        })

        assert prompt == "SECOND CANDIDATE FALLBACK"
