import zipfile
import xml.etree.ElementTree as ET
import time
from loguru import logger
from exceptions.parser_exception import ParserException

class DOCXParser:
    @staticmethod
    def parse(file_path: str) -> tuple[str, int]:
        """Parse DOCX file and return (raw_text, page_count)."""
        start_time = time.time()
        logger.info(f"Starting DOCX parsing for {file_path}")
        
        try:
            with zipfile.ZipFile(file_path) as docx:
                tree = ET.XML(docx.read('word/document.xml'))
                namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                
                text_blocks = []
                for para in tree.findall('.//w:p', namespaces):
                    texts = [node.text for node in para.findall('.//w:t', namespaces) if node.text]
                    if texts:
                        text_blocks.append("".join(texts))
                        
            raw_text = "\n".join(text_blocks)
            
            if not raw_text.strip():
                raise ParserException(f"DOCX is empty: {file_path}")
                
            logger.info(f"DOCX parsing completed in {time.time() - start_time:.2f}s")
            return raw_text, 1
            
        except Exception as e:
            logger.error(f"Error parsing DOCX {file_path}: {e}")
            raise ParserException(f"DOCX parsing failed: {e}")
