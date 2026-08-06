import pypdf
import time
from loguru import logger
from exceptions.parser_exception import ParserException

class PDFParser:
    @staticmethod
    def parse(file_path: str) -> tuple[str, int]:
        """Parse PDF file and return (raw_text, page_count)."""
        start_time = time.time()
        logger.info(f"Starting PDF parsing for {file_path}")
        
        try:
            reader = pypdf.PdfReader(file_path)
            if reader.is_encrypted:
                raise ParserException(f"PDF is encrypted: {file_path}")
            
            text_blocks = []
            page_count = len(reader.pages)
            
            if page_count == 0:
                raise ParserException(f"PDF is empty: {file_path}")
                
            for page in reader.pages:
                text_blocks.append(page.extract_text() or "")
                
            raw_text = "\n".join(text_blocks)
            logger.info(f"PDF parsing completed in {time.time() - start_time:.2f}s")
            return raw_text, page_count
            
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {e}")
            raise ParserException(f"PDF parsing failed: {e}")
