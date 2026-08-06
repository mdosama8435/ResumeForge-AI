import os

parser_files = {
    "src/parser/__init__.py": "",
    
    "src/parser/cleaner.py": '''import re

class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        """Normalize whitespace, remove duplicates, normalize bullets."""
        if not text:
            return ""
        
        # Normalize line endings
        text = text.replace('\\r\\n', '\\n').replace('\\r', '\\n')
        
        # Remove strange unicode characters, preserve standard punctuation and ASCII
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        # Normalize bullets (e.g. •, -, *)
        text = re.sub(r'^[\\s\\t]*[•\\-\\*o]\\s+', '- ', text, flags=re.MULTILINE)
        
        # Remove duplicate blank lines
        text = re.sub(r'\\n{3,}', '\\n\\n', text)
        
        # Normalize whitespace (but keep newlines)
        text = re.sub(r'[ \\t]+', ' ', text)
        
        # Trim spaces
        return text.strip()
''',

    "src/parser/metadata.py": '''import os
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
''',

    "src/parser/section_detector.py": '''import re
from typing import Dict

class SectionDetector:
    SECTION_MAPPING = {
        "summary": [r"summary", r"objective", r"profile", r"about me"],
        "experience": [r"experience", r"employment", r"work history", r"professional experience"],
        "education": [r"education", r"academic background", r"qualifications"],
        "skills": [r"skills", r"core competencies", r"technologies", r"technical skills"],
        "projects": [r"projects", r"personal projects", r"academic projects"],
        "certifications": [r"certifications", r"licenses", r"certificates"],
        "achievements": [r"achievements", r"awards", r"honors"]
    }

    @classmethod
    def detect(cls, text: str) -> Dict[str, str]:
        """Detect and extract sections from raw text."""
        sections = {}
        lines = text.split('\\n')
        current_section = "unclassified"
        sections[current_section] = []

        for line in lines:
            line_clean = line.strip().lower()
            if len(line_clean) < 40 and not line_clean.startswith('-'):
                detected = cls._match_header(line_clean)
                if detected:
                    current_section = detected
                    if current_section not in sections:
                        sections[current_section] = []
                    continue
            
            sections[current_section].append(line)

        return {k: "\\n".join(v).strip() for k, v in sections.items() if v}

    @classmethod
    def _match_header(cls, line: str) -> str:
        for section, patterns in cls.SECTION_MAPPING.items():
            for pattern in patterns:
                if re.match(rf"^{pattern}:?$", line):
                    return section
        return ""
''',

    "src/parser/pdf_parser.py": '''import fitz
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
            doc = fitz.open(file_path)
            if doc.is_encrypted:
                raise ParserException(f"PDF is encrypted: {file_path}")
            
            text_blocks = []
            page_count = len(doc)
            
            if page_count == 0:
                raise ParserException(f"PDF is empty: {file_path}")
                
            for page in doc:
                text_blocks.append(page.get_text("text"))
                
            raw_text = "\\n".join(text_blocks)
            logger.info(f"PDF parsing completed in {time.time() - start_time:.2f}s")
            return raw_text, page_count
            
        except fitz.FileDataError as e:
            logger.error(f"Corrupt PDF file {file_path}: {e}")
            raise ParserException(f"Corrupt or invalid PDF file: {e}")
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {e}")
            raise ParserException(f"PDF parsing failed: {e}")
''',

    "src/parser/docx_parser.py": '''from docx import Document
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
            doc = Document(file_path)
            text_blocks = []
            
            for para in doc.paragraphs:
                if para.text.strip():
                    if para.style.name.startswith('List'):
                        text_blocks.append(f"- {para.text}")
                    else:
                        text_blocks.append(para.text)
                        
            raw_text = "\\n".join(text_blocks)
            
            if not raw_text.strip():
                raise ParserException(f"DOCX is empty: {file_path}")
                
            logger.info(f"DOCX parsing completed in {time.time() - start_time:.2f}s")
            return raw_text, 1
            
        except Exception as e:
            logger.error(f"Error parsing DOCX {file_path}: {e}")
            raise ParserException(f"DOCX parsing failed: {e}")
''',

    "src/parser/txt_parser.py": '''import time
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
''',

    "src/parser/resume_parser.py": '''from typing import Dict, Any
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
''',

    "src/parser/jd_parser.py": '''from typing import Dict, Any
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
            "requirements": cls._extract_list(cleaned_text, r"(?i)requirements?|qualifications?|what you need"),
            "responsibilities": cls._extract_list(cleaned_text, r"(?i)responsibilities?|what you'll do|role"),
            "skills": cls._extract_list(cleaned_text, r"(?i)skills?|technologies"),
            "experience": cls._extract_list(cleaned_text, r"(?i)experience")
        }

    @classmethod
    def _extract_list(cls, text: str, header_regex: str) -> list:
        """Heuristically extract bullet points under a given header."""
        lines = text.split('\\n')
        extracting = False
        results = []
        
        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                continue
                
            if re.match(rf"^{header_regex}:?$", line_clean):
                extracting = True
                continue
                
            if extracting and len(line_clean) < 40 and not line_clean.startswith('-') and line_clean.istitle():
                extracting = False
                
            if extracting and line_clean.startswith('-'):
                results.append(line_clean[1:].strip())
                
        return results
''',

    "tests/parser/test_parser.py": '''import pytest
from src.parser.cleaner import TextCleaner
from src.parser.section_detector import SectionDetector
from src.parser.metadata import MetadataExtractor

def test_cleaner():
    raw_text = "Hello   world.\\n\\n\\n\\nThis is a bullet:\\n• Point 1\\n* Point 2"
    cleaned = TextCleaner.clean(raw_text)
    assert "Hello world." in cleaned
    assert "- Point 1" in cleaned
    assert "- Point 2" in cleaned
    assert "\\n\\n\\n" not in cleaned

def test_section_detector():
    raw_text = "Experience\\n- Developer at Google\\nEducation\\n- MIT"
    sections = SectionDetector.detect(raw_text)
    assert "experience" in sections
    assert "education" in sections
    assert "- Developer at Google" in sections["experience"]
    assert "- MIT" in sections["education"]

def test_metadata_extractor():
    meta = MetadataExtractor.extract("test.pdf", "Word word word", 2)
    assert meta["word_count"] == 3
    assert meta["page_count"] == 2
    assert meta["file_type"] == ".pdf"
'''
}

for filepath, content in parser_files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Parser module created successfully.")
