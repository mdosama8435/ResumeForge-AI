from typing import Dict, Any
from src.ats.ats_engine import ATSEngine

class AnalysisController:
    @staticmethod
    def analyze(resume_data: Dict[str, Any], jd_data: Dict[str, Any], ats_engine: ATSEngine) -> Dict[str, Any]:
        # Orchestrating the ATS Engine
        report = ats_engine.evaluate(resume_data, jd_data)
        return report.model_dump()
