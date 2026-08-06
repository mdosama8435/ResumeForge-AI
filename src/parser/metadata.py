import os
from typing import Dict, Any

class MetadataExtractor:
    @staticmethod
    def extract(file_path: str, text: str, page_count: int = 1) -> Dict[str, Any]:
        """Extract metadata like word count, reading time, etc."""
        word_count = len(text.split())
        char_count = len(text)
        reading_time_mins = max(1, word_count // 200) # avg 200 wpm
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        file_type = os.path.splitext(file_path)[1].lower() if file_path else ""
        
        return {
            "page_count": page_count,
            "word_count": word_count,
            "character_count": char_count,
            "estimated_reading_time_mins": reading_time_mins,
            "file_type": file_type,
            "file_size_bytes": file_size
        }
