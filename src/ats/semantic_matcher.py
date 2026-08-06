from typing import Dict, Any
from src.rag.embedding_service import EmbeddingService
import numpy as np
from loguru import logger

class SemanticMatcher:
    @staticmethod
    def analyze(resume_text: str, jd_text: str) -> Dict[str, Any]:
        if not resume_text.strip() or not jd_text.strip():
            return {"score": 0, "reason": "Empty text provided."}
            
        try:
            res_emb = np.array(EmbeddingService.embed_text(resume_text[:2000]))
            jd_emb = np.array(EmbeddingService.embed_text(jd_text[:2000]))
            
            similarity = np.dot(res_emb, jd_emb) / (np.linalg.norm(res_emb) * np.linalg.norm(jd_emb))
            score = max(0, min(100, int(similarity * 100)))
            
            return {
                "score": score,
                "reason": f"Semantic similarity match: {score}%",
                "similarity": similarity
            }
        except Exception as e:
            logger.warning(f"Semantic match failed: {e}")
            return {"score": 50, "reason": "Semantic match unavailable."}
