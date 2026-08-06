from typing import Dict, Any
from src.rag.retriever import RAGRetriever
from src.llm.interview_generator import InterviewGenerator

class InterviewController:
    @staticmethod
    def generate_interview(session_id: str, jd_text: str, retriever: RAGRetriever, generator: InterviewGenerator) -> Dict[str, Any]:
        retrieved_chunks = retriever.retrieve(query=jd_text)
        questions = generator.generate(retrieved_chunks, jd_text)
        return {"questions": questions}
