import logging
from typing import Any
# pyrefly: ignore [missing-import]
from jinja2 import Template, TemplateError

logger = logging.getLogger(__name__)

class PromptRenderError(Exception):
    """Raised when prompt rendering fails."""

class PromptRenderer:
    """
    Renders prompt templates using Jinja2, replacing placeholders (e.g. {{ message }})
    with context values.
    """

    def render(
        self,
        template: str,
        context: dict[str, Any] | None = None,
    ) -> str:
        """
        Render a prompt template.

        Args:
            template: The Jinja2 prompt template string.
            context: Dictionary containing values for placeholders.

        Returns:
            Fully rendered prompt string.

        Raises:
            PromptRenderError: If template rendering fails.
        """
        if not isinstance(template, str):
            raise PromptRenderError("Template must be a string.")

        if not template.strip():
            logger.warning("Received an empty prompt template.")
            return ""

        context = context or {}

        try:
            logger.debug("Rendering prompt template using Jinja2...")
            jinja_template = Template(template)
            rendered_prompt = jinja_template.render(**context).strip()
            logger.debug("Prompt rendered successfully.")
            return rendered_prompt
        except TemplateError as exc:
            logger.exception("Jinja2 template syntax or rendering error.")
            raise PromptRenderError(f"Jinja2 error: {exc}") from exc
        except Exception as exc:
            logger.exception("Prompt rendering failed due to an unexpected error.")
            raise PromptRenderError(f"Unable to render prompt: {exc}") from exc