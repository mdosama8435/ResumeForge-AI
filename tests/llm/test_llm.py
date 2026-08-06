import pytest
from src.llm.output_parser import Parsers
from pydantic import ValidationError

def test_validate_resume_schema():
    valid_json = """{
        "summary": "Great dev",
        "skills": ["python"],
        "experience": ["did things"],
        "projects": ["app"],
        "ats_score": 95,
        "missing_keywords": ["java"],
        "suggestions": ["add java"]
    }"""
    validated = Parsers.resume_parser.parse(valid_json)
    assert validated.ats_score == 95
    assert "python" in validated.skills

def test_validate_resume_schema_invalid():
    invalid_json = '{"summary": "Missing fields"}'
    with pytest.raises(Exception): # LangChain raises OutputParserException which wraps ValidationError
        Parsers.resume_parser.parse(invalid_json)
