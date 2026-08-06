import time
from loguru import logger
from langchain_huggingface import HuggingFaceEmbeddings
from exceptions.rag_exception import RAGException
from config.settings import settings
from typing import List

class EmbeddingService:
    _instance = None
    
    @classmethod
    def load_model(cls) -> HuggingFaceEmbeddings:
        """Singleton pattern for loading the HuggingFace embeddings model."""
        if cls._instance is None:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            try:
                start_time = time.time()
                cls._instance = HuggingFaceEmbeddings(
                    model_name=settings.EMBEDDING_MODEL
                )
                logger.info(f"Embedding model loaded in {time.time() - start_time:.2f}s")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise RAGException(f"Embedding model unavailable: {e}")
        return cls._instance

    @classmethod
    def embed_text(cls, text: str) -> List[float]:
        try:
            model = cls.load_model()
            return model.embed_query(text)
        except Exception as e:
            raise RAGException(f"Invalid embeddings for text: {e}")

    @classmethod
    def embed_documents(cls, texts: List[str]) -> List[List[float]]:
        try:
            model = cls.load_model()
            start_time = time.time()
            logger.debug(f"Embedding {len(texts)} chunks started")
            embeddings = model.embed_documents(texts)
            logger.debug(f"Embedding completed in {time.time() - start_time:.2f}s")
            return embeddings
        except Exception as e:
            raise RAGException(f"Batch embedding failed: {e}")
