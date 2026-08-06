from typing import Dict, Any
import re

class ExperienceAnalyzer:
    @staticmethod
    def analyze(resume_sections: Dict[str, str], jd_text: str) -> Dict[str, Any]:
        exp_text = resume_sections.get("experience", "").lower()
        
        if not exp_text:
            return {"score": 0, "reason": "No experience section found."}
            
        # Heuristics: check for years (e.g. 2018 - 2022)
        years = len(re.findall(r'20\\d{2}', exp_text))
        
        # Check for impact metrics (%)
        metrics = len(re.findall(r'\\d+%', exp_text))
        
        score = 50
        reason_parts = []
        
        if years >= 2:
            score += 25
            reason_parts.append("Contains measurable tenure dates.")
        if metrics > 0:
            score += 25
            reason_parts.append(f"Includes {metrics} quantifiable impact metrics.")
        else:
            reason_parts.append("Lacks quantifiable impact metrics.")
            
        score = min(100, score)
        return {
            "score": score,
            "reason": " ".join(reason_parts)
        }
