from typing import Union
import logging

# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.context import MessageContext
from app.models.message import MessageRequest, MessageResponse

from app.agents.communication_agent import CommunicationAgent
from app.agents.context_builder import ContextBuilder
from app.agents.intent_detector import IntentDetector
from app.agents.prompt_router import PromptRouter

from app.services.prompt_renderer import PromptRenderer
from app.services.llm_factory import LLMFactory
from app.services.message_generation_service import (
    MessageGenerationService,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Messages"])


def get_communication_agent() -> CommunicationAgent:
    """
    Dependency provider for CommunicationAgent.
    """

    llm = LLMFactory().get_provider("gemini")

    message_generation_service = MessageGenerationService(
        prompt_router=PromptRouter(),
        prompt_renderer=PromptRenderer(),
        llm=llm,
    )

    return CommunicationAgent(
        intent_detector=IntentDetector(),
        context_builder=ContextBuilder(),
        message_generation_service=message_generation_service,
    )


@router.post(
    "/generate-message",
    response_model=Union[MessageContext, MessageResponse],
    summary="Generate AI Message",
)
async def generate_message(
    request: MessageRequest,
    communication_agent: CommunicationAgent = Depends(
        get_communication_agent
    ),
):
    """
    Complete AI Communication workflow.
    """

    try:
        logger.info("=" * 60)
        logger.info("Incoming Request")
        logger.info(request.model_dump())

        response = communication_agent.process(request)

        logger.info("Workflow completed successfully.")
        logger.info("=" * 60)

        return response

    except Exception as exc:
        logger.exception("Message generation failed.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )