from pydantic import BaseModel, Field
from typing import List

class ATSScoreComponent(BaseModel):
    score: int
    reason: str

class ATSReport(BaseModel):
    overall_score: int
    keyword_score: int
    keyword_reason: str
    skills_score: int
    skills_reason: str
    experience_score: int
    experience_reason: str
    project_score: int
    project_reason: str
    education_score: int
    education_reason: str
    formatting_score: int
    formatting_reason: str
    matched_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    recommended_keywords: List[str] = Field(default_factory=list)
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
