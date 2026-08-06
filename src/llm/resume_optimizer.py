from typing import List, Any
from .context_builder import ContextBuilder
from .chains import create_resume_optimization_chain
from .validator import OptimizedResumeSchema
from langchain_core.documents import Document
from loguru import logger

class ResumeOptimizer:
    def __init__(self, provider_name: str = "gemini"):
        # provider_name is ignored as we use LCEL chains with gemini configured
        self.chain = create_resume_optimization_chain()

    def optimize(self, retrieved_chunks: List[Document], jd_text: str) -> OptimizedResumeSchema:
        """Full orchestration flow for resume optimization using LCEL."""
        logger.info("Starting Resume Optimization flow via LCEL.")
        
        # 1. Build Context
        context = ContextBuilder.build_optimization_context(retrieved_chunks, jd_text)
        
        # 2. Invoke Chain (Prompt | LLM | Parser)
        result = self.chain.invoke({"context": context})
        
        logger.info("Resume Optimization flow completed successfully.")
        return result
