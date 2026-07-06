import logging

from app.agents.context_builder import ContextBuilder
from app.agents.intent_detector import IntentDetector

from app.models.context import MessageContext
from app.models.message import (
    MessageRequest,
    MessageResponse,
)

from app.services.message_generation_service import (
    MessageGenerationService,
)

logger = logging.getLogger(__name__)


class CommunicationAgentError(Exception):
    """Raised when the communication workflow fails."""


class CommunicationAgent:
    """
    Orchestrates the complete communication workflow.

    Responsibilities:
        1. Detect intent
        2. Build context
        3. Request clarification if needed
        4. Generate AI messages
        5. Return structured response
    """

    def __init__(
        self,
        intent_detector: IntentDetector,
        context_builder: ContextBuilder,
        message_generation_service: MessageGenerationService,
    ) -> None:
        self.intent_detector = intent_detector
        self.context_builder = context_builder
        self.message_generation_service = message_generation_service

    def process(
        self,
        request: MessageRequest,
    ) -> MessageContext | MessageResponse:
        """
        Execute the complete communication workflow.
        """

        logger.info("=" * 60)
        logger.info("Communication Agent started.")

        try:
            # -------------------------------------------------
            # Step 1 — Intent Detection
            # -------------------------------------------------
            logger.info("Step 1/5 → Detect Intent")

            detected = self.intent_detector.detect(request)

            # -------------------------------------------------
            # Step 2 — Context Building
            # -------------------------------------------------
            logger.info("Step 2/5 → Build Context")

            context_result = self.context_builder.build_context(
                request=request,
                detected=detected,
            )

            context = context_result["context"]

            message_context = MessageContext(
                platform=context.get("platform"),
                relationship=context.get("relationship"),
                language=context.get("language"),
                tone=context.get("tone"),
                purpose=context.get("purpose"),
                needs_clarification=context_result.get(
                    "needs_clarification",
                    False,
                ),
                missing_fields=context_result.get(
                    "missing_fields",
                    [],
                ),
                question=context_result.get("question"),
            )

            # -------------------------------------------------
            # Step 3 — Clarification Check
            # -------------------------------------------------
            logger.info("Step 3/5 → Check Clarification")

            if message_context.needs_clarification:
                logger.info("Clarification required.")
                logger.info(
                    "Workflow paused until user provides missing information."
                )

                return message_context

            logger.info("Context complete. Continuing workflow.")

            # -------------------------------------------------
            # Step 4 — AI Message Generation
            # -------------------------------------------------
            logger.info("Step 4/5 → Generate AI Messages")

            generated_messages = (
                self.message_generation_service.generate(
                    message=request.message,
                    context=message_context.model_dump(
                        exclude_none=True,
                    ),
                )
            )

            logger.info(
                "Generated %d message variants.",
                len(generated_messages),
            )

            # -------------------------------------------------
            # Step 5 — Return Structured Response
            # -------------------------------------------------
            logger.info("Step 5/5 → Returning structured response")
            logger.info("Communication workflow completed successfully.")
            logger.info("=" * 60)

            return MessageResponse(
                original_message=request.message,
                messages=generated_messages,
                detected_platform=message_context.platform,
                detected_relationship=message_context.relationship,
                detected_language=message_context.language,
                detected_tone=message_context.tone,
            )

        except Exception:
            logger.exception("Communication workflow failed.")

            raise