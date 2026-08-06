import pytest
from src.parser.cleaner import TextCleaner
from src.parser.section_detector import SectionDetector
from src.parser.metadata import MetadataExtractor

def test_cleaner():
    raw_text = "Hello   world.\n\n\n\nThis is a bullet:\n• Point 1\n* Point 2"
    cleaned = TextCleaner.clean(raw_text)
    assert "Hello world." in cleaned
    assert "- Point 1" in cleaned
    assert "- Point 2" in cleaned
    assert "\n\n\n" not in cleaned

def test_section_detector():
    raw_text = "Experience\n- Developer at Google\nEducation\n- MIT"
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
