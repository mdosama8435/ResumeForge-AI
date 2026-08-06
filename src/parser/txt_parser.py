import time
from loguru import logger
from exceptions.parser_exception import ParserException

class TXTParser:
    @staticmethod
    def parse(file_path: str) -> tuple[str, int]:
        """Parse TXT file and return (raw_text, page_count)."""
        start_time = time.time()
        logger.info(f"Starting TXT parsing for {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                raw_text = f.read()
                
            if not raw_text.strip():
                raise ParserException(f"TXT file is empty: {file_path}")
                
            logger.info(f"TXT parsing completed in {time.time() - start_time:.2f}s")
            return raw_text, 1
            
        except Exception as e:
            logger.error(f"Error parsing TXT {file_path}: {e}")
            raise ParserException(f"TXT parsing failed: {e}")
