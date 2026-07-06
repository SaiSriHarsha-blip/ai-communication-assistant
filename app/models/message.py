from app.models.enums import (
    Language,
    Platform,
    Relationship,
    Tone,
)

# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field, field_validator

class MessageRequest(BaseModel):
    """
    Incoming request from the client.
    """

    message: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="The user's raw message.",
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