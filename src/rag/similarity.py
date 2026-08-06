from typing import List, Dict, Any
from pydantic import BaseModel
from langchain_core.documents import Document

class SimilarityResult(BaseModel):
    similarity_score: float
    matched_chunk: str
    section_name: str
    metadata: Dict[str, Any]

class SimilarityProcessor:
    @staticmethod
    def process_results(faiss_results: List[tuple[Document, float]]) -> List[SimilarityResult]:
        """Convert FAISS results (L2 distance) into structured response models."""
        processed = []
        for doc, score in faiss_results:
            # Note: FAISS typically returns L2 distance. Lower is better.
            # Depending on index (e.g. inner product), score meaning changes. 
            # We wrap it directly for now.
            processed.append(SimilarityResult(
                similarity_score=score,
                matched_chunk=doc.page_content,
                section_name=doc.metadata.get("section_name", "unknown"),
                metadata=doc.metadata
            ))
        return processed
