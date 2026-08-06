import hashlib
from typing import Dict, Any, List
from langchain_core.documents import Document
from .chunker import IntelligentChunker
from .vector_store import FAISSVectorStore
from exceptions.rag_exception import RAGException
from loguru import logger

class DocumentManager:
    def __init__(self, index_name: str = "default_index"):
        self.vector_store = FAISSVectorStore(index_name)
        self.chunker = IntelligentChunker()
        # In memory tracker to prevent duplicate indexing
        # In production this would be backed by Postgres or Redis
        self.indexed_hashes = set()

    def add_document(self, document_id: str, document_type: str, sections: Dict[str, str], source_filename: str):
        """Chunk a document and add it to the FAISS index."""
        # Check hash to avoid duplicate indexing
        doc_hash = hashlib.md5(f"{document_id}_{document_type}_{source_filename}".encode()).hexdigest()
        if doc_hash in self.indexed_hashes:
            logger.warning(f"Duplicate document detected: {document_id}. Skipping.")
            raise RAGException("Duplicate document detected.")

        documents = self.chunker.chunk_document(document_id, document_type, sections, source_filename)
        
        if not documents:
            logger.warning(f"Empty document provided for {document_id}")
            raise RAGException("Empty documents cannot be indexed.")
        
        self.vector_store.insert_documents(documents)
        self.indexed_hashes.add(doc_hash)
        logger.info(f"Document {document_id} successfully processed and indexed.")

    def update_document(self, document_id: str, document_type: str, sections: Dict[str, str], source_filename: str):
        self.vector_store.delete_document(document_id)
        self.add_document(document_id, document_type, sections, source_filename)
        
    def delete_document(self, document_id: str):
        self.vector_store.delete_document(document_id)
