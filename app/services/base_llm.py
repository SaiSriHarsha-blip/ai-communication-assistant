from abc import ABC, abstractmethod
from app.models.gemini_response import GeminiResponse

class BaseLLM(ABC):
    """
    Abstract base class for all LLM providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_output_tokens: int = 512,
    ) -> GeminiResponse:
        """
        Generate text using an LLM.

        Args:
            prompt: Prompt to send to the model.
            temperature: Controls creativity.
            max_output_tokens: Maximum response length.

        Returns:
            GeminiResponse object containing structured output.
        """
        raise NotImplementedError