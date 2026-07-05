import logging
from typing import Any

from app.agents.prompt_router import PromptRouter
from app.models.message import MessageVariant
from app.services.base_llm import BaseLLM
from app.services.prompt_renderer import PromptRenderer

logger = logging.getLogger(__name__)


class MessageGenerationError(Exception):
    """Raised when message generation fails."""


class MessageGenerationService:
    """
    Responsible for AI message generation.

    Responsibilities:
    - Select the appropriate prompt template
    - Render the prompt with context
    - Call the LLM using structured output schemas
    - Extract and return validated MessageVariant objects
    """

    def __init__(
        self,
        prompt_router: PromptRouter,
        prompt_renderer: PromptRenderer,
        llm: BaseLLM,
    ) -> None:
        self.prompt_router = prompt_router
        self.prompt_renderer = prompt_renderer
        self.llm = llm

    def generate(
        self,
        message: str,
        context: dict[str, Any],
    ) -> list[MessageVariant]:
        """
        Generate multiple AI message variants.

        Args:
            message: Original user message.
            context: Resolved message context.

        Returns:
            List of generated MessageVariant objects.
        """

        logger.info("Selecting prompt template...")

        template = self.prompt_router.get_prompt(context)

        logger.info("Rendering prompt...")

        rendered_prompt = self.prompt_renderer.render(
            template=template,
            context={
                **context,
                "message": message,
            },
        )

        logger.info("Calling Gemini for structured output...")

        response = self.llm.generate(
            prompt=rendered_prompt,
        )

        logger.info("Extracting messages from GeminiResponse...")

        if not response or not response.messages:
            raise MessageGenerationError(
                "Gemini returned no message variants."
            )

        logger.info(
            "Successfully generated %d message variants.",
            len(response.messages),
        )

        return response.messages