from .base_provider import BaseLLMProvider
from .gemini_provider import GeminiProvider
from exceptions.llm_exception import LLMException

class LLMFactory:
    @staticmethod
    def get_provider(provider_name: str = "gemini") -> BaseLLMProvider:
        """Factory method for instantiating the correct LLM provider."""
        provider_name = provider_name.lower()
        if provider_name == "gemini":
            return GeminiProvider()
        # Add "openai", "claude", "ollama" here in the future
        else:
            raise LLMException(f"Unsupported LLM provider: {provider_name}")
