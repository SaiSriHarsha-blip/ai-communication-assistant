"""
Unit tests for PromptRenderer (app.services.prompt_renderer).

Verifies Jinja2 template rendering, production template regressions (SMS, Gmail, WhatsApp),
error handling for malformed syntax and invalid types, empty templates, missing context handling,
and unicode / multiline / quote support.
"""

from pathlib import Path
from typing import Any
import pytest

from app.services.prompt_renderer import PromptRenderer, PromptRenderError

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "app" / "prompts"


@pytest.fixture
def renderer() -> PromptRenderer:
    return PromptRenderer()


@pytest.mark.unit
class TestPromptRendererBasic:
    """Basic rendering, whitespace stripping, and empty template handling."""

    def test_valid_template_rendering(self, renderer: PromptRenderer) -> None:
        template = "Hello {{ name }}, welcome to {{ place }}!"
        context = {"name": "Alice", "place": "Wonderland"}
        result = renderer.render(template, context)

        assert result == "Hello Alice, welcome to Wonderland!"

    def test_template_output_is_stripped_of_surrounding_whitespace(
        self, renderer: PromptRenderer
    ) -> None:
        template = "   \n  Hello {{ name }}  \n\t  "
        result = renderer.render(template, {"name": "Bob"})

        assert result == "Hello Bob"

    @pytest.mark.parametrize(
        "empty_template",
        [
            "",
            "   ",
            "\n\t\n",
            " \n \t \r ",
        ],
    )
    def test_empty_and_whitespace_templates_return_empty_string(
        self, renderer: PromptRenderer, empty_template: str
    ) -> None:
        result = renderer.render(empty_template, {"message": "Test"})
        assert result == ""

    def test_rendering_with_none_context(self, renderer: PromptRenderer) -> None:
        template = "Static prompt without variables."
        result = renderer.render(template, None)
        assert result == "Static prompt without variables."


@pytest.mark.unit
class TestPromptRendererErrors:
    """Validation of error conditions, malformed Jinja2 syntax, and invalid types."""

    @pytest.mark.parametrize(
        "invalid_template",
        [
            None,
            123,
            45.6,
            ["not", "a", "string"],
            {"template": "not string"},
        ],
    )
    def test_invalid_template_types_raise_prompt_render_error(
        self, renderer: PromptRenderer, invalid_template: Any
    ) -> None:
        with pytest.raises(PromptRenderError, match="Template must be a string"):
            renderer.render(invalid_template, {})

    @pytest.mark.parametrize(
        "malformed_template",
        [
            "Hello {{ unclosed_expression",
            "Bad tag {% for x in %} hello {% endfor %}",
            "Unclosed block {% if condition %} test",
        ],
    )
    def test_malformed_jinja_syntax_raises_prompt_render_error(
        self, renderer: PromptRenderer, malformed_template: str
    ) -> None:
        with pytest.raises(PromptRenderError, match="Jinja2 error"):
            renderer.render(malformed_template, {})

    def test_unexpected_exception_during_rendering_raises_prompt_render_error(
        self, renderer: PromptRenderer, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Covers generic Exception handler in PromptRenderer."""
        import jinja2

        def mock_render(*args: Any, **kwargs: Any) -> None:
            raise RuntimeError("Unexpected internal crash")

        monkeypatch.setattr(jinja2.Template, "render", mock_render)

        with pytest.raises(PromptRenderError, match="Unable to render prompt: Unexpected internal crash"):
            renderer.render("Simple {{ message }}", {"message": "test"})


@pytest.mark.unit
class TestPromptRendererProductionTemplates:
    """Regression tests verifying actual production templates render accurately."""

    def test_sms_default_template_renders_message_placeholder(
        self, renderer: PromptRenderer
    ) -> None:
        sms_template_path = PROMPTS_DIR / "sms" / "default.md"
        assert sms_template_path.is_file(), f"Template not found: {sms_template_path}"

        template_content = sms_template_path.read_text(encoding="utf-8")
        test_message = "I will be 15 minutes late to the sync."

        rendered = renderer.render(template_content, {"message": test_message})

        assert test_message in rendered
        assert "{{ message }}" not in rendered
        assert "{{message}}" not in rendered
        assert "SMS writing assistant" in rendered

    def test_gmail_casual_template_renders_all_context_variables(
        self, renderer: PromptRenderer
    ) -> None:
        gmail_template_path = PROMPTS_DIR / "gmail" / "casual.md"
        assert gmail_template_path.is_file(), f"Template not found: {gmail_template_path}"

        template_content = gmail_template_path.read_text(encoding="utf-8")
        context = {
            "platform": "gmail",
            "relationship": "colleague",
            "language": "english",
            "tone": "casual",
            "purpose": "meeting",
            "message": "Let's grab a coffee and chat about the roadmap.",
        }

        rendered = renderer.render(template_content, context)

        # Confirm all context variables were replaced
        assert "Platform: gmail" in rendered
        assert "Relationship: colleague" in rendered
        assert "Language: english" in rendered
        assert "Tone: casual" in rendered
        assert "Purpose: meeting" in rendered
        assert context["message"] in rendered
        assert "{{" not in rendered

    def test_whatsapp_default_template_renders_cleanly(
        self, renderer: PromptRenderer
    ) -> None:
        whatsapp_template_path = PROMPTS_DIR / "whatsapp" / "default.md"
        assert whatsapp_template_path.is_file(), f"Template not found: {whatsapp_template_path}"

        template_content = whatsapp_template_path.read_text(encoding="utf-8")
        context = {
            "platform": "whatsapp",
            "relationship": "friend",
            "language": "english",
            "tone": "friendly",
            "purpose": "greeting",
            "message": "Happy birthday buddy! Hope you have a wonderful day.",
        }

        rendered = renderer.render(template_content, context)

        assert "Platform: whatsapp" in rendered
        assert "Relationship: friend" in rendered
        assert context["message"] in rendered
        assert "{{" not in rendered


@pytest.mark.unit
class TestPromptRendererContentVarieties:
    """Tests special characters, unicode, multiline strings, and missing optional variables."""

    def test_missing_variables_render_empty_by_default(
        self, renderer: PromptRenderer
    ) -> None:
        """Jinja2 default behavior replaces undefined variables with empty string."""
        template = "Message: '{{ message }}' | Extra: '{{ extra_info }}'"
        result = renderer.render(template, {"message": "Hello"})

        assert result == "Message: 'Hello' | Extra: ''"

    def test_unicode_and_telugu_characters(
        self, renderer: PromptRenderer
    ) -> None:
        template = "Language: {{ language }}\nOriginal: {{ message }}"
        context = {
            "language": "telugu",
            "message": "నమస్కారం! రేపు ఉదయం 10 గంటలకు మీటింగ్ కి రండి.",
        }
        result = renderer.render(template, context)

        assert "Language: telugu" in result
        assert "నమస్కారం! రేపు ఉదయం 10 గంటలకు మీటింగ్ కి రండి." in result

    def test_emojis_and_special_symbols(
        self, renderer: PromptRenderer
    ) -> None:
        template = "Greeting: {{ emoji }} {{ message }}"
        context = {
            "emoji": "🎉🚀🔥",
            "message": "Congratulations on the successful launch!",
        }
        result = renderer.render(template, context)

        assert "🎉🚀🔥 Congratulations on the successful launch!" in result

    def test_quotes_and_multiline_content(
        self, renderer: PromptRenderer
    ) -> None:
        template = "Input:\n\"\"\"\n{{ message }}\n\"\"\""
        multiline_msg = (
            "Line 1: He said, \"Don't worry about it.\"\n"
            "Line 2: Here's a 20% discount on orders > $50.\n"
            "Line 3: 'Single quoted string'."
        )
        result = renderer.render(template, {"message": multiline_msg})

        assert multiline_msg in result
        assert 'He said, "Don\'t worry about it."' in result
