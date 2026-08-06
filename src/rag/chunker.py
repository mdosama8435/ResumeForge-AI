from typing import List, Dict, Any
import hashlib
from langchain_core.documents import Document
from .metadata import ChunkMetadata
from config.settings import settings

class IntelligentChunker:
    def __init__(self):
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def chunk_document(self, document_id: str, document_type: str, sections: Dict[str, str], source_filename: str) -> List[Document]:
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
                
                chunks.append(Document(page_content=sub_chunk, metadata=metadata.model_dump()))
                
                chunk_index += 1
                
        return chunks

    def _generate_chunk_id(self, document_id: str, section_name: str, index: int) -> str:
        unique_string = f"{document_id}_{section_name}_{index}"
        return hashlib.md5(unique_string.encode()).hexdigest()
