from typing import Dict, Any
import re

class ProjectAnalyzer:
    @staticmethod
    def analyze(resume_sections: Dict[str, str], jd_text: str) -> Dict[str, Any]:
        proj_text = resume_sections.get("projects", "").lower()
        
        if not proj_text:
            # Not all JDs require projects
            if "project" in jd_text.lower():
                return {"score": 0, "reason": "JD mentions projects but none found in resume."}
            return {"score": 100, "reason": "No projects section required or found."}
            
        metrics = len(re.findall(r'\\d+', proj_text))
        score = min(100, 50 + (metrics * 10))
        reason = f"Projects section exists with {metrics} measurable data points."
        
        return {
            "score": score,
            "reason": reason
        }
