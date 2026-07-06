# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field

from app.models.enums import (
    Language,
    Platform,
    Relationship,
    Tone,
)

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class MessageRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="The user's raw message."
    )

    platform: Optional[Platform] = None

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty.")

        return value

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