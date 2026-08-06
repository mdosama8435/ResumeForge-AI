from langchain_core.output_parsers import PydanticOutputParser
from .validator import (
    OptimizedResumeSchema,
    ATSRecommendationSchema,
    InterviewQuestionsSchema,
    CoverLetterSchema,
    RecruiterReviewSchema,
    CareerCoachRoadmapSchema
)

class Parsers:
    resume_parser = PydanticOutputParser(pydantic_object=OptimizedResumeSchema)
    ats_parser = PydanticOutputParser(pydantic_object=ATSRecommendationSchema)
    interview_parser = PydanticOutputParser(pydantic_object=InterviewQuestionsSchema)
    cover_letter_parser = PydanticOutputParser(pydantic_object=CoverLetterSchema)
    recruiter_review_parser = PydanticOutputParser(pydantic_object=RecruiterReviewSchema)
    career_coach_parser = PydanticOutputParser(pydantic_object=CareerCoachRoadmapSchema)
