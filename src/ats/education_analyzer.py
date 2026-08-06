from typing import Dict, Any

class EducationAnalyzer:
    @staticmethod
    def analyze(resume_sections: Dict[str, str], jd_text: str) -> Dict[str, Any]:
        edu_text = resume_sections.get("education", "").lower()
        jd_lower = jd_text.lower()
        
        if not edu_text:
            return {"score": 0, "reason": "No education section found."}
            
        score = 70
        reason_parts = ["Education section present."]
        
        # Check degree mentions in JD
        degrees = {"bachelor", "master", "phd", "b.s", "b.a", "m.s"}
        jd_degrees = {d for d in degrees if d in jd_lower}
        
        if jd_degrees:
            res_degrees = {d for d in degrees if d in edu_text}
            if jd_degrees.intersection(res_degrees):
                score = 100
                reason_parts.append("Matches degree requirements.")
            else:
                score = 50
                reason_parts.append("May not match degree requirements.")
        else:
            score = 100
            
        return {
            "score": score,
            "reason": " ".join(reason_parts)
        }
