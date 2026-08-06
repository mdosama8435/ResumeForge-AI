import pytest
from src.ats.keyword_matcher import KeywordMatcher
from src.ats.skills_analyzer import SkillsAnalyzer
from src.ats.score_calculator import ScoreCalculator

def test_keyword_matcher():
    res = "I have experience with python and docker."
    jd = "Need python, docker, and kubernetes."
    result = KeywordMatcher.analyze(res, jd)
    assert result["score"] < 100
    assert "kubernetes" in result["missing"]

def test_skills_analyzer():
    sections = {"skills": "python, java"}
    jd = "Seeking python and aws"
    result = SkillsAnalyzer.analyze(sections, jd)
    assert "aws" in result["missing"]

def test_score_calculator():
    sub_scores = {
        "keyword": 100,
        "skills": 100,
        "experience": 100,
        "projects": 100,
        "education": 100,
        "formatting": 100
    }
    assert ScoreCalculator.calculate_overall(sub_scores) == 100
