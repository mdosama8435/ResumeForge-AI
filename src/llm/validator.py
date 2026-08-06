from pydantic import BaseModel, Field, ValidationError
from typing import List
from exceptions.llm_exception import LLMValidationException
import json
from loguru import logger

class ExplainabilityItem(BaseModel):
    section: str = Field(description="The section that was updated (e.g. 'Professional Summary', 'Skills', 'Experience')")
    reason: str = Field(description="The reason why this change was made")
    impact: str = Field(description="The impact on ATS score (Low, Medium, High, Critical)")
    confidence: str = Field(description="Confidence percentage (e.g. '95%')")

class OptimizedResumeSchema(BaseModel):
    summary: str = Field(description="Optimized professional summary")
    skills: List[str] = Field(description="List of optimized skills")
    experience: List[str] = Field(description="Optimized experience bullets")
    projects: List[str] = Field(description="Optimized projects")
    ats_score: int = Field(description="Estimated ATS match score out of 100")
    missing_keywords: List[str] = Field(description="Keywords in JD missing from resume")
    suggestions: List[str] = Field(description="Suggestions for improvement")
    explainability: List[ExplainabilityItem] = Field(description="List of reasoning items explaining major changes made to the resume")

class ATSRecommendationSchema(BaseModel):
    overall_match: str = Field(description="Overall ATS match assessment")
    strengths: List[str] = Field(description="ATS strengths")
    weaknesses: List[str] = Field(description="ATS weaknesses")
    suggestions: List[str] = Field(description="Suggestions for ATS improvement")

class InterviewQuestionItem(BaseModel):
    question: str = Field(description="The interview question")
    expected_answer: str = Field(description="Blueprint of the expected answer")
    difficulty: str = Field(description="Difficulty level (Easy, Medium, Hard)")
    category: str = Field(description="Category (e.g. System Design, Behavioral, Algorithm)")
    estimated_time: str = Field(description="Estimated time to answer (e.g. '5 mins')")

class InterviewQuestionsSchema(BaseModel):
    questions: List[InterviewQuestionItem] = Field(description="List of targeted interview questions")

class CoverLetterSchema(BaseModel):
    cover_letter: str = Field(description="The full generated cover letter text")

class RecruiterReviewSchema(BaseModel):
    overall_match: str = Field(description="Overall match against the job description")
    strengths: List[str] = Field(description="Strengths of the candidate")
    weaknesses: List[str] = Field(description="Weaknesses or red flags")
    hiring_recommendation: str = Field(description="Hiring recommendation")
    risk_analysis: str = Field(description="Risk analysis of hiring this candidate")

class CareerCoachRoadmapSchema(BaseModel):
    learning_roadmap: List[str] = Field(description="Steps for learning roadmap")
    missing_skills: List[str] = Field(description="Missing skills to acquire")
    courses: List[str] = Field(description="Suggested courses")
    projects_to_build: List[str] = Field(description="Suggested projects to build")
    interview_preparation_plan: List[str] = Field(description="Interview preparation plan steps")
