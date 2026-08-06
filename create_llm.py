import os

llm_files = {
    "src/llm/__init__.py": "",

    "exceptions/llm_exception.py": '''from exceptions.base import ResumeForgeException
class LLMException(ResumeForgeException):
    pass
class LLMTimeoutException(LLMException):
    pass
class LLMRateLimitException(LLMException):
    pass
class LLMValidationException(LLMException):
    pass
''',

    "src/llm/base_provider.py": '''from abc import ABC, abstractmethod
from typing import Any

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_structured(self, prompt: str) -> str:
        """Generate structured text/JSON from the LLM provider."""
        pass
''',

    "src/llm/gemini_provider.py": '''import time
from loguru import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .base_provider import BaseLLMProvider
from exceptions.llm_exception import LLMException, LLMTimeoutException, LLMRateLimitException
from config.settings import settings

class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise LLMException("GEMINI_API_KEY is not configured.")
            
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.2, # Low temperature for deterministic factual responses
            convert_system_message_to_human=True,
            timeout=30.0
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((LLMTimeoutException, LLMRateLimitException)),
        reraise=True
    )
    def generate_structured(self, prompt: str) -> str:
        start_time = time.time()
        estimated_tokens = len(prompt) // 4
        logger.info(f"GeminiProvider starting generation. Prompt length: {len(prompt)} chars (~{estimated_tokens} tokens)")
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            duration = time.time() - start_time
            logger.info(f"GeminiProvider completed in {duration:.2f}s")
            return response.content
        except Exception as e:
            error_str = str(e).lower()
            if "timeout" in error_str or "deadline" in error_str:
                logger.warning(f"GeminiProvider timeout: {e}")
                raise LLMTimeoutException(f"Timeout connecting to Gemini: {e}")
            elif "429" in error_str or "quota" in error_str or "rate limit" in error_str:
                logger.warning(f"GeminiProvider rate limit hit: {e}")
                raise LLMRateLimitException(f"Gemini Rate Limit exceeded: {e}")
            else:
                logger.error(f"GeminiProvider generic failure: {e}")
                raise LLMException(f"GeminiProvider failed: {e}")
''',

    "src/llm/provider.py": '''from .base_provider import BaseLLMProvider
from .gemini_provider import GeminiProvider
from exceptions.llm_exception import LLMException

class LLMFactory:
    @staticmethod
    def get_provider(provider_name: str = "gemini") -> BaseLLMProvider:
        """Factory method for instantiating the correct LLM provider."""
        provider_name = provider_name.lower()
        if provider_name == "gemini":
            return GeminiProvider()
        # Add "openai", "claude", "ollama" here in the future
        else:
            raise LLMException(f"Unsupported LLM provider: {provider_name}")
''',

    "src/llm/guardrails.py": '''# Strictly enforced prompt guardrails to prevent hallucination
SYSTEM_GUARDRAILS = """
CRITICAL SYSTEM RULES (STRICTLY ENFORCED):
1. You MUST NEVER invent fake companies or employers.
2. You MUST NEVER invent fake projects or responsibilities.
3. You MUST NEVER invent fake education or certifications.
4. You MUST NEVER invent fake work experience.
5. You MUST NEVER invent fake skills.
6. You may ONLY rewrite, rephrase, and optimize existing content provided in the candidate's context.
7. If critical information is missing from the provided context to answer a question or fulfill a section, output exactly "Information not available" instead of hallucinating.
"""
''',

    "src/llm/prompt_builder.py": '''from langchain_core.prompts import PromptTemplate
from .guardrails import SYSTEM_GUARDRAILS

class PromptBuilder:
    @staticmethod
    def build_resume_optimization_prompt(context: str) -> str:
        template = f"""{SYSTEM_GUARDRAILS}

You are an expert AI Resume Writer.
Your task is to optimize the following candidate data to match the provided Job Description context.

CONTEXT (Resume Data & Job Description):
{{context}}

INSTRUCTIONS:
- Optimize the Professional Summary.
- Optimize the Experience bullets to align with the JD, keeping strictly to the facts provided.
- Suggest ATS keywords that the candidate possesses in their experience but might be missing in a dedicated skills section.

Format the output strictly as a JSON object matching the provided schema.
"""
        prompt = PromptTemplate(template=template, input_variables=["context"])
        return prompt.format(context=context)

    @staticmethod
    def build_interview_prep_prompt(context: str) -> str:
        template = f"""{SYSTEM_GUARDRAILS}

You are a Senior Technical Recruiter.
Based on the following candidate resume and target Job Description, generate 5 targeted interview questions.

CONTEXT:
{{context}}

Format the output strictly as a JSON array of strings containing the questions.
"""
        prompt = PromptTemplate(template=template, input_variables=["context"])
        return prompt.format(context=context)
''',

    "src/llm/context_builder.py": '''from typing import List, Dict, Any
import json
from loguru import logger

class ContextBuilder:
    @staticmethod
    def build_optimization_context(retrieved_chunks: List[Any], jd_text: str, metadata: Dict[str, Any] = None) -> str:
        """Combine retrieved RAG chunks and JD into a unified context block."""
        context_parts = []
        
        context_parts.append("--- JOB DESCRIPTION ---")
        context_parts.append(jd_text[:3000]) # Cap size to avoid massive JDs blowing context
        
        context_parts.append("\\n--- CANDIDATE RESUME CONTEXT (RAG CHUNKS) ---")
        for i, chunk in enumerate(retrieved_chunks):
            # Assumes chunk has matched_chunk string and section_name
            context_parts.append(f"[{chunk.section_name.upper()}]: {chunk.matched_chunk}")
            
        if metadata:
            context_parts.append("\\n--- CANDIDATE METADATA ---")
            context_parts.append(json.dumps(metadata, indent=2))
            
        context_str = "\\n".join(context_parts)
        logger.debug(f"Context builder generated context of size {len(context_str)} characters.")
        return context_str
''',

    "src/llm/validator.py": '''from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from exceptions.llm_exception import LLMValidationException
import json
from loguru import logger

class OptimizedResumeSchema(BaseModel):
    summary: str = Field(description="Optimized professional summary")
    skills: List[str] = Field(description="List of optimized skills")
    experience: List[str] = Field(description="Optimized experience bullets")
    projects: List[str] = Field(description="Optimized projects")
    ats_score: int = Field(description="Estimated ATS match score out of 100")
    missing_keywords: List[str] = Field(description="Keywords in JD missing from resume")
    suggestions: List[str] = Field(description="Suggestions for improvement")

class ResponseValidator:
    @staticmethod
    def validate_optimized_resume(json_str: str) -> OptimizedResumeSchema:
        try:
            data = json.loads(json_str)
            return OptimizedResumeSchema(**data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from LLM: {e}")
            raise LLMValidationException(f"Malformed JSON from provider: {e}")
        except ValidationError as e:
            logger.error(f"Pydantic schema validation failed: {e}")
            raise LLMValidationException(f"Invalid response structure: {e}")
''',

    "src/llm/output_parser.py": '''from typing import Any
import re
from loguru import logger
from exceptions.llm_exception import LLMValidationException

class StructuredOutputParser:
    @staticmethod
    def extract_json(raw_response: str) -> str:
        """Strip markdown ticks and return clean JSON string."""
        if not raw_response:
            raise LLMValidationException("Empty response received from LLM.")
            
        text = raw_response.strip()
        
        # Regex to find json blocks
        match = re.search(r"```(?:json)?(.*?)```", text, re.DOTALL)
        if match:
            text = match.group(1).strip()
            
        # Basic sanity check
        if not (text.startswith('{') or text.startswith('[')):
            logger.error(f"Response does not look like JSON: {text[:100]}...")
            raise LLMValidationException("Response is not JSON formatted.")
            
        return text
''',

    "src/llm/resume_optimizer.py": '''from typing import List, Any
from .provider import LLMFactory
from .context_builder import ContextBuilder
from .prompt_builder import PromptBuilder
from .output_parser import StructuredOutputParser
from .validator import ResponseValidator, OptimizedResumeSchema
from exceptions.llm_exception import LLMException
from loguru import logger

class ResumeOptimizer:
    def __init__(self, provider_name: str = "gemini"):
        self.provider = LLMFactory.get_provider(provider_name)

    def optimize(self, retrieved_chunks: List[Any], jd_text: str) -> OptimizedResumeSchema:
        """Full orchestration flow for resume optimization."""
        logger.info("Starting Resume Optimization flow.")
        
        # 1. Build Context
        context = ContextBuilder.build_optimization_context(retrieved_chunks, jd_text)
        
        # 2. Build Prompt
        prompt = PromptBuilder.build_resume_optimization_prompt(context)
        
        # 3. Request LLM Generation
        raw_response = self.provider.generate_structured(prompt)
        
        # 4. Parse & Clean Output
        clean_json = StructuredOutputParser.extract_json(raw_response)
        
        # 5. Validate Schema
        validated_data = ResponseValidator.validate_optimized_resume(clean_json)
        
        logger.info("Resume Optimization flow completed successfully.")
        return validated_data
''',

    "src/llm/cover_letter_generator.py": '''from .provider import LLMFactory
from loguru import logger

class CoverLetterGenerator:
    def __init__(self, provider_name: str = "gemini"):
        self.provider = LLMFactory.get_provider(provider_name)

    def generate(self, resume_summary: str, jd_text: str) -> str:
        # Placeholder for full implementation following the same pattern
        logger.info("Cover Letter generator initialized.")
        return "Cover Letter Generation logic goes here."
''',

    "src/llm/interview_generator.py": '''from .provider import LLMFactory
from .context_builder import ContextBuilder
from .prompt_builder import PromptBuilder
from .output_parser import StructuredOutputParser
import json
from loguru import logger

class InterviewGenerator:
    def __init__(self, provider_name: str = "gemini"):
        self.provider = LLMFactory.get_provider(provider_name)

    def generate(self, retrieved_chunks: list, jd_text: str) -> list[str]:
        logger.info("Starting Interview Generation flow.")
        context = ContextBuilder.build_optimization_context(retrieved_chunks, jd_text)
        prompt = PromptBuilder.build_interview_prep_prompt(context)
        raw_response = self.provider.generate_structured(prompt)
        clean_json = StructuredOutputParser.extract_json(raw_response)
        
        try:
            data = json.loads(clean_json)
            if isinstance(data, list):
                return [str(q) for q in data]
            return []
        except json.JSONDecodeError:
            return []
''',

    "tests/llm/test_llm.py": '''import pytest
from src.llm.output_parser import StructuredOutputParser
from src.llm.validator import ResponseValidator
from exceptions.llm_exception import LLMValidationException

def test_extract_json():
    raw_response = "Here is your response:\\n```json\\n{\\"summary\\": \\"test\\"}\\n```"
    clean = StructuredOutputParser.extract_json(raw_response)
    assert clean == '{"summary": "test"}'

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
    validated = ResponseValidator.validate_optimized_resume(valid_json)
    assert validated.ats_score == 95
    assert "python" in validated.skills

def test_validate_resume_schema_invalid():
    invalid_json = """{"summary": "Missing fields"}"""
    with pytest.raises(LLMValidationException):
        ResponseValidator.validate_optimized_resume(invalid_json)
'''
}

for filepath, content in llm_files.items():
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("LLM Orchestration module created successfully.")
