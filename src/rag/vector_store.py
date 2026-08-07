import os
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from .embedding_service import EmbeddingService
from exceptions.rag_exception import RAGException
from loguru import logger
from config.settings import settings

class MemoryVectorStore:
    def __init__(self, index_name: str = "default_index"):
        from langchain_core.vectorstores import InMemoryVectorStore
        self.InMemoryVectorStore = InMemoryVectorStore
        
        self.index_name = index_name
        self.embeddings = EmbeddingService.load_model()
        self.vector_store = None

    def create_index(self, documents: List[Document]):
        if not documents:
            raise RAGException("Cannot create index with empty documents.")
        try:
            self.vector_store = self.InMemoryVectorStore.from_documents(documents, self.embeddings)
            logger.info(f"New Memory index created with {len(documents)} documents.")
        except Exception as e:
            raise RAGException(f"Failed to create index: {e}")

    def insert_documents(self, documents: List[Document]):
        if not documents:
            return
        if self.vector_store is None:
            self.create_index(documents)
        else:
            try:
                self.vector_store.add_documents(documents)
                logger.info(f"Added {len(documents)} documents to Memory index.")
            except Exception as e:
                raise RAGException(f"Failed to insert documents: {e}")
        
    def delete_document(self, document_id: str):
        if not self.vector_store:
            return
        
        # InMemoryVectorStore docstore keys
        docstore = self.vector_store.store
        keys_to_delete = []
        for key, doc in docstore.items():
            if doc.metadata.get("document_id") == document_id:
                keys_to_delete.append(key)
                
        if keys_to_delete:
            self.vector_store.delete(keys_to_delete)
            logger.info(f"Deleted {len(keys_to_delete)} chunks for document {document_id}")

    def search(self, query: str, k: int = 4, score_threshold: float = 0.0) -> List[tuple[Document, float]]:
        if not self.vector_store:
            return []
        try:
            return self.vector_store.similarity_search_with_score(query, k=k)
        except Exception as e:
            raise RAGException(f"Search failed: {e}")
            
    def as_retriever(self, k: int = 4, score_threshold: float = 0.0):
        if not self.vector_store:
            raise RAGException("Vector store is not initialized.")
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )

