from typing import Dict, Any
import os
from .pdf_parser import PDFParser
from .docx_parser import DOCXParser
from .txt_parser import TXTParser
from .cleaner import TextCleaner
from .section_detector import SectionDetector
from .metadata import MetadataExtractor
from exceptions.parser_exception import ParserException
from loguru import logger
import time

class ResumeParser:
    @staticmethod
    def parse(file_path: str) -> Dict[str, Any]:
        """Orchestrates the parsing of a resume."""
        if not os.path.exists(file_path):
            raise ParserException(f"File not found: {file_path}")
            
        start_time = time.time()
        logger.info(f"Initiating resume parsing workflow for {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        raw_text = ""
        page_count = 1
        
        if ext == '.pdf':
            raw_text, page_count = PDFParser.parse(file_path)
        elif ext == '.docx':
            raw_text, page_count = DOCXParser.parse(file_path)
        elif ext == '.txt':
            raw_text, page_count = TXTParser.parse(file_path)
        else:
            raise ParserException(f"Unsupported file format: {ext}")
            
        cleaned_text = TextCleaner.clean(raw_text)
        sections = SectionDetector.detect(cleaned_text)
        metadata = MetadataExtractor.extract(file_path, cleaned_text, page_count)
        
        logger.info(f"Resume parsing workflow completed in {time.time() - start_time:.2f}s")
        
        return {
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "sections": sections,
            "metadata": metadata
        }
