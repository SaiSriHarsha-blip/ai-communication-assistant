from typing import Optional
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from app.models.enums import Platform, Relationship, Language, Tone

class MessageContext(BaseModel):
    """
    Model representing the resolved context for a message, including both
    explicitly provided and inferred metadata, as well as clarification state.
    """
    platform: Optional[Platform] = Field(None, description="The intended communication platform.")
    relationship: Optional[Relationship] = Field(None, description="The relationship with the recipient.")
    language: Optional[Language] = Field(None, description="The language for the message.")
    tone: Optional[Tone] = Field(None, description="The requested tone.")
    purpose: Optional[str] = Field(None, description="The overall purpose of the message.")
    
    needs_clarification: bool = Field(False, description="Flag indicating if the agent needs more information from the user.")
    missing_fields: list[str] = Field(default_factory=list, description="List of missing required fields.")
    question: Optional[str] = Field(None, description="The specific question to ask the user if clarification is needed.")
