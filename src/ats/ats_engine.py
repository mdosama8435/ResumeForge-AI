import time
from loguru import logger
from typing import Dict, Any
from .keyword_matcher import KeywordMatcher
from .semantic_matcher import SemanticMatcher
from .skills_analyzer import SkillsAnalyzer
from .experience_analyzer import ExperienceAnalyzer
from .education_analyzer import EducationAnalyzer
from .project_analyzer import ProjectAnalyzer
from .formatting_analyzer import FormattingAnalyzer
from .score_calculator import ScoreCalculator
from .report_generator import ReportGenerator
from .models import ATSReport
from exceptions.ats_exception import ATSException

class ATSEngine:
    @staticmethod
    def evaluate(resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> ATSReport:
        start_time = time.time()
        logger.info("ATS Analyzer Started.")
        
        try:
            res_raw = resume_data.get("raw_text", "")
            jd_raw = jd_data.get("raw_text", "")
            res_sections = resume_data.get("sections", {})
            metadata = resume_data.get("metadata", {})
            
            if not res_raw or not jd_raw:
                raise ATSException("Empty resume or JD provided.")
                
            results = {}
            results["keyword"] = KeywordMatcher.analyze(res_raw, jd_raw)
            # Semantic matcher is optional/enrichment, can be integrated into score later
            results["semantic"] = SemanticMatcher.analyze(res_raw, jd_raw)
            results["skills"] = SkillsAnalyzer.analyze(res_sections, jd_raw)
            results["experience"] = ExperienceAnalyzer.analyze(res_sections, jd_raw)
            results["projects"] = ProjectAnalyzer.analyze(res_sections, jd_raw)
            results["education"] = EducationAnalyzer.analyze(res_sections, jd_raw)
            results["formatting"] = FormattingAnalyzer.analyze(res_raw, metadata)
            
            sub_scores = {k: v["score"] for k, v in results.items() if "score" in v}
            results["overall_score"] = ScoreCalculator.calculate_overall(sub_scores)
            
            report = ReportGenerator.generate(results)
            
            logger.info(f"ATS Analyzer Finished in {time.time() - start_time:.2f}s. Score Generated: {report.overall_score}")
            return report
            
        except ATSException as e:
            logger.error(f"ATS evaluation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in ATS evaluation: {e}")
            raise ATSException(f"ATS Engine failed: {e}")
