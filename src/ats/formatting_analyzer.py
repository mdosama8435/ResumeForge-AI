from typing import Dict, Any
import re

class FormattingAnalyzer:
    @staticmethod
    def analyze(raw_text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        if not raw_text:
            return {"score": 0, "reason": "Empty document."}
            
        score = 100
        reasons = []
        
        # Check length (ideal 400 - 1000 words)
        words = metadata.get("word_count", 0)
        if words < 300:
            score -= 20
            reasons.append("Resume is too short.")
        elif words > 1200:
            score -= 20
            reasons.append("Resume exceeds ideal length.")
        else:
            reasons.append("Optimal length.")
            
        # Check bullets
        bullets = len(re.findall(r'^- ', raw_text, re.MULTILINE))
        if bullets < 5:
            score -= 20
            reasons.append("Underutilizes bullet points.")
        else:
            reasons.append("Good use of bullet points.")
            
        return {
            "score": max(0, score),
            "reason": " ".join(reasons)
        }
