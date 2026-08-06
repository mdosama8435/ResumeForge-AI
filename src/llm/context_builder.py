from typing import List, Dict, Any
import json
from loguru import logger
from langchain_core.documents import Document

class ContextBuilder:
    @staticmethod
    def build_optimization_context(retrieved_chunks: List[Document], jd_text: str, metadata: Dict[str, Any] = None) -> str:
        """Combine retrieved RAG chunks and JD into a unified context block."""
        context_parts = []
        
        context_parts.append("--- JOB DESCRIPTION ---")
        context_parts.append(jd_text[:3000]) # Cap size to avoid massive JDs blowing context
        
        context_parts.append("\\n--- CANDIDATE RESUME CONTEXT (RAG CHUNKS) ---")
        for i, doc in enumerate(retrieved_chunks):
            section_name = doc.metadata.get("section_name", "UNKNOWN SECTION")
            context_parts.append(f"[{section_name.upper()}]: {doc.page_content}")
            
        if metadata:
            context_parts.append("\\n--- CANDIDATE METADATA ---")
            context_parts.append(json.dumps(metadata, indent=2))
            
        context_str = "\\n".join(context_parts)
        logger.debug(f"Context builder generated context of size {len(context_str)} characters.")
        return context_str
