from typing import List
from .context_builder import ContextBuilder
from .chains import create_interview_prep_chain
from langchain_core.documents import Document
from loguru import logger

class InterviewGenerator:
    def __init__(self, provider_name: str = "gemini"):
        self.chain = create_interview_prep_chain()

    def generate(self, retrieved_chunks: List[Document], jd_text: str) -> list:
        logger.info("Starting Interview Generation flow via LCEL.")
        context = ContextBuilder.build_optimization_context(retrieved_chunks, jd_text)
        
        result = self.chain.invoke({"context": context})
        return result.questions
