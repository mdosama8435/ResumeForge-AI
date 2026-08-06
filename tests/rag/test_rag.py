import pytest
from src.rag.chunker import IntelligentChunker
from src.rag.metadata import ChunkMetadata

def test_chunker():
    chunker = IntelligentChunker()
    sections = {
        "summary": "This is a brief summary.",
        "experience": "Worked at Company A for 5 years.\n" * 50  # Make it long enough to split
    }
    chunks = chunker.chunk_document("doc_1", "resume", sections, "resume.pdf")
    
    assert len(chunks) > 0
    assert chunks[0].metadata["document_id"] == "doc_1"
    assert chunks[0].metadata["section_name"] == "summary"
