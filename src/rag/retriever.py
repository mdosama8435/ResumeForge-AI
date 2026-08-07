import time
from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document
from loguru import logger
from .vector_store import MemoryVectorStore
from exceptions.rag_exception import RAGException
from config.settings import settings

class RAGRetriever:
    def __init__(self, index_name: str = "default_index"):
        self.index_name = index_name
        self.vector_store = MemoryVectorStore(index_name)

    def get_retriever(self, top_k: int = None, score_threshold: float = None):
        """Returns a LangChain VectorStoreRetriever."""
        k = top_k or settings.TOP_K
        threshold = score_threshold if score_threshold is not None else settings.SCORE_THRESHOLD
        return self.vector_store.as_retriever(k=k, score_threshold=threshold)

    def retrieve(self, query: str, top_k: int = None, score_threshold: float = None) -> List[Document]:
        """Semantic Search returning Top-K results via LangChain retriever."""
        retriever = self.get_retriever(top_k, score_threshold)
        start_time = time.time()
        logger.info(f"LangChain Retriever executed for query: '{query[:30]}...'")
        
        results = retriever.invoke(query)
        
        logger.info(f"Retriever returned {len(results)} results in {time.time() - start_time:.2f}s")
        return results
