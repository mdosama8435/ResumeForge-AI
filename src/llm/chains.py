from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableParallel
from src.prompts.templates import (
    RESUME_OPTIMIZATION_PROMPT,
    INTERVIEW_PREP_PROMPT,
    COVER_LETTER_PROMPT,
    RECRUITER_FEEDBACK_PROMPT,
    CAREER_COACH_PROMPT
)
from .output_parser import Parsers
from config.settings import settings

def get_llm():
    raw_keys = settings.GEMINI_API_KEY.split(',')
    keys = [k.strip() for k in raw_keys if k.strip()]
    if not keys:
        raise ValueError("No GEMINI_API_KEY provided in .env")

    llms = [
        ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            google_api_key=key,
            temperature=settings.LLM_TEMPERATURE,
            top_p=settings.LLM_TOP_P,
            timeout=60.0,
            max_retries=1
        ) for key in keys
    ]
    
    primary_llm = llms[0]
    if len(llms) > 1:
        return primary_llm.with_fallbacks(llms[1:])
    return primary_llm

def create_resume_optimization_chain():
    llm = get_llm()
    prompt = RESUME_OPTIMIZATION_PROMPT.partial(format_instructions=Parsers.resume_parser.get_format_instructions())
    return prompt | llm | Parsers.resume_parser

def create_ats_recommendation_chain():
    # Placeholder if a separate ATS prompt exists, else reuse another
    llm = get_llm()
    # Assuming ATS uses a different prompt, but since one wasn't explicitly defined in prompts, we'll map to it if needed
    pass

def create_interview_prep_chain():
    llm = get_llm()
    prompt = INTERVIEW_PREP_PROMPT.partial(format_instructions=Parsers.interview_parser.get_format_instructions())
    return prompt | llm | Parsers.interview_parser

def create_cover_letter_chain():
    llm = get_llm()
    prompt = COVER_LETTER_PROMPT.partial(format_instructions=Parsers.cover_letter_parser.get_format_instructions())
    return prompt | llm | Parsers.cover_letter_parser

def create_recruiter_feedback_chain():
    llm = get_llm()
    prompt = RECRUITER_FEEDBACK_PROMPT.partial(format_instructions=Parsers.recruiter_review_parser.get_format_instructions())
    return prompt | llm | Parsers.recruiter_review_parser

def create_career_coach_chain():
    llm = get_llm()
    prompt = CAREER_COACH_PROMPT.partial(format_instructions=Parsers.career_coach_parser.get_format_instructions())
    return prompt | llm | Parsers.career_coach_parser

def create_parallel_execution_chain():
    """Generates Interview Questions, Cover Letter, Recruiter Review, and Career Coach in parallel."""
    return RunnableParallel(
        interview_questions=create_interview_prep_chain(),
        cover_letter=create_cover_letter_chain(),
        recruiter_feedback=create_recruiter_feedback_chain(),
        career_coach=create_career_coach_chain()
    )
