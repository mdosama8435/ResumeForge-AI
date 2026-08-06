from typing import Optional
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
