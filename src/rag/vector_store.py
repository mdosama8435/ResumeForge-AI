import os
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from .embedding_service import EmbeddingService
from exceptions.rag_exception import RAGException
from loguru import logger
from config.settings import settings

class FAISSVectorStore:
    def __init__(self, index_name: str = "default_index"):
        self.index_name = index_name
        self.index_path = os.path.join(settings.VECTOR_STORE_DIR, index_name)
        self.embeddings = EmbeddingService.load_model()
        self.vector_store: Optional[FAISS] = None
        os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)
        self.load_index()

    def create_index(self, documents: List[Document]):
        if not documents:
            raise RAGException("Cannot create index with empty documents.")
        try:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            logger.info(f"New FAISS index created with {len(documents)} documents.")
        except Exception as e:
            raise RAGException(f"Failed to create index: {e}")

    def save_index(self):
        if self.vector_store:
            try:
                self.vector_store.save_local(self.index_path)
                logger.info(f"FAISS index saved to {self.index_path}")
            except Exception as e:
                raise RAGException(f"Failed to save index: {e}")

    def load_index(self):
        if os.path.exists(os.path.join(self.index_path, "index.faiss")):
            try:
                self.vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
                logger.info(f"Loaded existing FAISS index from {self.index_path}")
            except Exception as e:
                logger.error(f"Corrupt index at {self.index_path}: {e}")
                self.vector_store = None
        else:
            self.vector_store = None

    def insert_documents(self, documents: List[Document]):
        if not documents:
            return
        if self.vector_store is None:
            self.create_index(documents)
        else:
            try:
                self.vector_store.add_documents(documents)
                logger.info(f"Added {len(documents)} documents to FAISS index.")
            except Exception as e:
                raise RAGException(f"Failed to insert documents: {e}")
        self.save_index()
        
    def delete_document(self, document_id: str):
        if not self.vector_store:
            return
        
        # FAISS docstore keys
        docstore = self.vector_store.docstore._dict
        keys_to_delete = []
        for key, doc in docstore.items():
            if doc.metadata.get("document_id") == document_id:
                keys_to_delete.append(key)
                
        if keys_to_delete:
            self.vector_store.delete(keys_to_delete)
            logger.info(f"Deleted {len(keys_to_delete)} chunks for document {document_id}")
            self.save_index()

    def search(self, query: str, k: int = 4, score_threshold: float = 0.0) -> List[tuple[Document, float]]:
        if not self.vector_store:
            return []
        try:
            return self.vector_store.similarity_search_with_score(query, k=k, score_threshold=score_threshold)
        except Exception as e:
            raise RAGException(f"Search failed: {e}")
            
    def as_retriever(self, k: int = 4, score_threshold: float = 0.0):
        if not self.vector_store:
            raise RAGException("Vector store is not initialized.")
        return self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": k, "score_threshold": score_threshold}
        )
