import os

rag_files = {
    "src/rag/__init__.py": "",

    "exceptions/rag_exception.py": '''from exceptions.base import ResumeForgeException
class RAGException(ResumeForgeException):
    pass
''',

    "src/rag/metadata.py": '''from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ChunkMetadata(BaseModel):
    chunk_id: str
    document_id: str
    document_type: str
    section_name: str
    page_number: int = 1
    chunk_index: int
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    token_estimate: int
    source_filename: str
''',

    "src/rag/chunker.py": '''from typing import List, Dict, Any
import hashlib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .metadata import ChunkMetadata
from config.settings import settings

class IntelligentChunker:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\\n\\n", "\\n", ". ", " ", ""]
        )

    def chunk_document(self, document_id: str, document_type: str, sections: Dict[str, str], source_filename: str) -> List[Dict[str, Any]]:
        """Chunk a document by semantic sections first, then by size if needed."""
        chunks = []
        chunk_index = 0
        
        for section_name, section_text in sections.items():
            if not section_text.strip():
                continue
                
            # Split large sections using RecursiveCharacterTextSplitter
            sub_chunks = self.text_splitter.split_text(section_text)
            
            for sub_chunk in sub_chunks:
                chunk_id = self._generate_chunk_id(document_id, section_name, chunk_index)
                
                # Rough token estimate (chars / 4)
                token_estimate = len(sub_chunk) // 4 
                
                metadata = ChunkMetadata(
                    chunk_id=chunk_id,
                    document_id=document_id,
                    document_type=document_type,
                    section_name=section_name,
                    chunk_index=chunk_index,
                    token_estimate=token_estimate,
                    source_filename=source_filename
                )
                
                chunks.append({
                    "text": sub_chunk,
                    "metadata": metadata.model_dump()
                })
                
                chunk_index += 1
                
        return chunks

    def _generate_chunk_id(self, document_id: str, section_name: str, index: int) -> str:
        unique_string = f"{document_id}_{section_name}_{index}"
        return hashlib.md5(unique_string.encode()).hexdigest()
''',

    "src/rag/embedding_service.py": '''import time
from loguru import logger
from langchain_community.embeddings import HuggingFaceEmbeddings
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
                    model_name=settings.EMBEDDING_MODEL,
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
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
''',

    "src/rag/vector_store.py": '''import os
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
''',

    "src/rag/similarity.py": '''from typing import List, Dict, Any
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
''',

    "src/rag/retriever.py": '''import time
from typing import List
from .vector_store import FAISSVectorStore
from .similarity import SimilarityProcessor, SimilarityResult
from loguru import logger
from config.settings import settings

class RAGRetriever:
    def __init__(self, index_name: str = "default_index"):
        self.vector_store = FAISSVectorStore(index_name)

    def retrieve(self, query: str, top_k: int = None, score_threshold: float = None) -> List[SimilarityResult]:
        """Semantic Search returning Top-K results."""
        k = top_k or settings.TOP_K
        threshold = score_threshold if score_threshold is not None else settings.SCORE_THRESHOLD
        
        start_time = time.time()
        logger.info(f"Retriever executed for query: '{query[:30]}...' with k={k}, threshold={threshold}")
        
        results = self.vector_store.search(query, k=k, score_threshold=threshold)
        
        processed_results = SimilarityProcessor.process_results(results)
        logger.info(f"Retriever returned {len(processed_results)} results in {time.time() - start_time:.2f}s")
        
        return processed_results
''',

    "src/rag/document_manager.py": '''import hashlib
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

        chunks = self.chunker.chunk_document(document_id, document_type, sections, source_filename)
        
        if not chunks:
            logger.warning(f"Empty document provided for {document_id}")
            raise RAGException("Empty documents cannot be indexed.")

        documents = [
            Document(page_content=chunk["text"], metadata=chunk["metadata"])
            for chunk in chunks
        ]
        
        self.vector_store.insert_documents(documents)
        self.indexed_hashes.add(doc_hash)
        logger.info(f"Document {document_id} successfully processed and indexed.")

    def update_document(self, document_id: str, document_type: str, sections: Dict[str, str], source_filename: str):
        self.vector_store.delete_document(document_id)
        self.add_document(document_id, document_type, sections, source_filename)
        
    def delete_document(self, document_id: str):
        self.vector_store.delete_document(document_id)
''',

    "tests/rag/test_rag.py": '''import pytest
from src.rag.chunker import IntelligentChunker
from src.rag.metadata import ChunkMetadata

def test_chunker():
    chunker = IntelligentChunker()
    sections = {
        "summary": "This is a brief summary.",
        "experience": "Worked at Company A for 5 years.\\n" * 50  # Make it long enough to split
    }
    chunks = chunker.chunk_document("doc_1", "resume", sections, "resume.pdf")
    
    assert len(chunks) > 0
    assert chunks[0]["metadata"]["document_id"] == "doc_1"
    assert chunks[0]["metadata"]["section_name"] == "summary"
'''
}

for filepath, content in rag_files.items():
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update config/settings.py to add new properties
with open('config/settings.py', 'r') as f:
    settings_code = f.read()

new_settings = """    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    TOP_K: int = 4
    SCORE_THRESHOLD: float = 0.0
    VECTOR_STORE_DIR: str = "vector_store"
"""

if "CHUNK_SIZE" not in settings_code:
    settings_code = settings_code.replace("    model_config =", f"{new_settings}    model_config =")
    with open('config/settings.py', 'w') as f:
        f.write(settings_code)

print("RAG module created successfully.")
