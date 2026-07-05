from typing import Dict, Type
from app.services.base_llm import BaseLLM
from app.services.gemini_service import GeminiService

class LLMFactory:
    """
    Factory for instantiating LLM service implementations.
    Provides extensibility to support Gemini, Claude, OpenAI, etc.
    """

    _registry: Dict[str, Type[BaseLLM]] = {
        "gemini": GeminiService,
        # Placeholder registry entries for future expansion:
        # "claude": ClaudeService,
        # "openai": OpenAIService,
    }

    @classmethod
    def get_provider(cls, provider: str) -> BaseLLM:
        """
        Returns an instance of the requested LLM provider.

        Args:
            provider: The string key of the provider (e.g., 'gemini').

        Returns:
            An instance of a class implementing BaseLLM.

        Raises:
            ValueError: If the requested provider is not registered.
        """
        provider_key = provider.strip().lower()
        provider_class = cls._registry.get(provider_key)

        if not provider_class:
            supported = ", ".join(cls._registry.keys())
            raise ValueError(
                f"LLM provider '{provider}' is not supported. "
                f"Supported providers: {supported}"
            )

        return provider_class()
