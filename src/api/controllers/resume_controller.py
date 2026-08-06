from typing import Dict, Any
from src.rag.retriever import RAGRetriever
from src.llm.resume_optimizer import ResumeOptimizer

class ResumeController:
    @staticmethod
    def generate_resume(session_id: str, jd_text: str, retriever: RAGRetriever, optimizer: ResumeOptimizer) -> Dict[str, Any]:
        # 1. Retrieve Context
        retrieved_chunks = retriever.retrieve(query=jd_text)
        
        # 2. Optimize
        optimized_data = optimizer.optimize(retrieved_chunks, jd_text)
        return optimized_data.model_dump()

    @staticmethod
    def generate_cover_letter(session_id: str, jd_text: str, retriever: RAGRetriever, generator) -> str:
        retrieved_chunks = retriever.retrieve(query=jd_text)
        return generator.generate(retrieved_chunks, jd_text)

    @staticmethod
    def generate_interview(session_id: str, jd_text: str, retriever: RAGRetriever, generator) -> Dict[str, Any]:
        retrieved_chunks = retriever.retrieve(query=jd_text)
        questions = generator.generate(retrieved_chunks, jd_text)
        return {"questions": questions}
