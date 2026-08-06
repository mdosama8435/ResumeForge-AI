from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_structured(self, prompt: str) -> str:
        """Generate structured text/JSON from the LLM provider."""
        pass
