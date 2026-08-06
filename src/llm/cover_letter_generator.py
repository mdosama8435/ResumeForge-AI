from typing import List
from .context_builder import ContextBuilder
from .chains import create_cover_letter_chain
from langchain_core.documents import Document
from loguru import logger

class CoverLetterGenerator:
    def __init__(self, provider_name: str = "gemini"):
        self.chain = create_cover_letter_chain()

    def generate(self, retrieved_chunks: List[Document], jd_text: str) -> str:
        logger.info("Starting Cover Letter Generation flow via LCEL.")
        context = ContextBuilder.build_optimization_context(retrieved_chunks, jd_text)
        
        result = self.chain.invoke({"context": context})
        return result.cover_letter
