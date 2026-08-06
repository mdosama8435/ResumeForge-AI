from typing import Dict, Any
import os
import re
from .pdf_parser import PDFParser
from .docx_parser import DOCXParser
from .txt_parser import TXTParser
from .cleaner import TextCleaner
from exceptions.parser_exception import ParserException
from loguru import logger

class JDParser:
    @classmethod
    def parse(cls, file_path: str) -> Dict[str, Any]:
        """Parse Job Description into structured text."""
        if not os.path.exists(file_path):
            raise ParserException(f"File not found: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            raw_text, _ = PDFParser.parse(file_path)
        elif ext == '.docx':
            raw_text, _ = DOCXParser.parse(file_path)
        elif ext == '.txt':
            raw_text, _ = TXTParser.parse(file_path)
        else:
            raise ParserException(f"Unsupported file format: {ext}")
            
        cleaned_text = TextCleaner.clean(raw_text)
        
        return {
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "requirements": cls._extract_list(cleaned_text, r"requirements?|qualifications?|what you need"),
            "responsibilities": cls._extract_list(cleaned_text, r"responsibilities?|what you'll do|role"),
            "skills": cls._extract_list(cleaned_text, r"skills?|technologies"),
            "experience": cls._extract_list(cleaned_text, r"experience")
        }

    @classmethod
    def _extract_list(cls, text: str, header_regex: str) -> list:
        """Heuristically extract bullet points under a given header."""
        lines = text.split('\n')
        extracting = False
        results = []
        
        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                continue
                
            if re.match(rf"^{header_regex}:?$", line_clean, flags=re.IGNORECASE):
                extracting = True
                continue
                
            if extracting and len(line_clean) < 40 and not line_clean.startswith('-') and line_clean.istitle():
                extracting = False
                
            if extracting and line_clean.startswith('-'):
                results.append(line_clean[1:].strip())
                
        return results
