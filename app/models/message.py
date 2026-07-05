# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field

from app.models.enums import (
    Language,
    Platform,
    Relationship,
    Tone,
)


class MessageRequest(BaseModel):
    """
    Incoming request from the client.
    """

    message: str = Field(
        ...,
        min_length=1,
        description="Original user message.",
        examples=[
            "Tell my manager I'll be 20 minutes late because of traffic."
        ],
    )

    platform: Platform | None = Field(
        default=None,
        description="Target communication platform.",
    )

    relationship: Relationship | None = Field(
        default=None,
        description="Relationship with the recipient.",
    )

    language: Language | None = Field(
        default=Language.ENGLISH,
        description="Preferred language.",
    )

    tone: Tone | None = Field(
        default=None,
        description="Preferred tone.",
    )


class MessageVariant(BaseModel):
    """
    Represents one AI-generated message variant.
    """

    style: str = Field(
        ...,
        description="Variant style.",
    )

    text: str = Field(
        ...,
        description="Generated message.",
    )


class MessageResponse(BaseModel):
    """
    Final response returned by the AI Communication Agent.
    """

    original_message: str = Field(
        ...,
        description="Original user message.",
    )

    messages: list[MessageVariant] = Field(
        ...,
        description="AI-generated message variants.",
    )

    detected_platform: Platform = Field(
        ...,
        description="Detected or selected platform.",
    )

    detected_relationship: Relationship = Field(
        ...,
        description="Detected relationship.",
    )

    detected_language: Language = Field(
        ...,
        description="Detected language.",
    )

    detected_tone: Tone = Field(
        ...,
        description="Detected tone.",
    )