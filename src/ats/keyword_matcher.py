import json
from typing import Dict, Any, List
from loguru import logger
from src.llm.gemini_provider import GeminiProvider

class KeywordMatcher:
    @staticmethod
    def analyze(resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Extract and match keywords using an AI-driven LLM approach."""
        prompt = f"""
You are an expert technical recruiter and an advanced Applicant Tracking System (ATS).
Your task is to extract the most important technical keywords, hard skills, tools, and frameworks from the provided Job Description.
DO NOT include generic soft skills, action verbs, or common nouns (e.g., 'building', 'entire', 'handling', 'responsibilities'). Focus strictly on hard skills, technologies, and core domain concepts.

After extracting the required keywords from the Job Description, carefully analyze the provided Resume to see which of those keywords are present (exact or close synonyms).

Return ONLY a valid JSON object with the following structure:
{{
    "matched": ["keyword1", "keyword2"],
    "missing": ["keyword3", "keyword4"]
}}

Job Description:
{jd_text[:3000]}

Resume:
{resume_text[:3000]}
"""
        
        try:
            llm = GeminiProvider()
            response_text = llm.generate_structured(prompt)
            
            # Clean response text in case LLM added markdown formatting
            clean_text = response_text.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_text)
            
            matched = [str(k).upper() for k in data.get("matched", [])]
            missing = [str(k).upper() for k in data.get("missing", [])]
            
            total = len(matched) + len(missing)
            coverage = len(matched) / total if total > 0 else 1.0
            score = int(coverage * 100)
            
            reason = f"{len(matched)} out of {total} core technical keywords were found."
            
            return {
                "score": score,
                "reason": reason,
                "matched": matched,
                "missing": missing,
                "coverage": coverage
            }
            
        except Exception as e:
            logger.error(f"KeywordMatcher LLM failed: {e}")
            # Fallback to basic extraction if LLM fails
            return KeywordMatcher._fallback_analyze(resume_text, jd_text)
            
    @staticmethod
    def _fallback_analyze(resume_text: str, jd_text: str) -> Dict[str, Any]:
        import re
        stop_words = {'with', 'this', 'that', 'from', 'have', 'your', 'will', 'what', 'need', 'building', 'entire', 'into', 'help', 'about', 'time', 'handling', 'responsibilities', 'layer'}
        def extract(text):
            return set(re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())) - stop_words
            
        jd_k = extract(jd_text)
        res_k = extract(resume_text)
        
        matched = list(jd_k.intersection(res_k))
        missing = list(jd_k - res_k)
        
        coverage = len(matched) / len(jd_k) if jd_k else 1.0
        return {
            "score": int(coverage * 100),
            "reason": f"{len(matched)} out of {len(jd_k)} required keywords found.",
            "matched": matched,
            "missing": missing,
            "coverage": coverage
        }
