# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from app.models.message import MessageVariant

class GeminiResponse(BaseModel):
    """
    Structured response returned by Gemini.
    """

    messages: list[MessageVariant]