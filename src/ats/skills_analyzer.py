from typing import Dict, Any, List
import re

class SkillsAnalyzer:
    # Deterministic dictionary
    TECH_SKILLS = {"python", "java", "c++", "react", "node", "aws", "azure", "docker", "kubernetes", "sql", "git", "machine learning", "fastapi"}
    SOFT_SKILLS = {"leadership", "communication", "teamwork", "problem solving", "management", "agile"}

    @classmethod
    def analyze(cls, resume_sections: Dict[str, str], jd_text: str) -> Dict[str, Any]:
        jd_lower = jd_text.lower()
        res_text = "\\n".join(resume_sections.values()).lower()
        
        # Find skills requested in JD
        jd_tech = {s for s in cls.TECH_SKILLS if s in jd_lower}
        jd_soft = {s for s in cls.SOFT_SKILLS if s in jd_lower}
        jd_all = jd_tech.union(jd_soft)
        
        if not jd_all:
            return {"score": 100, "reason": "No predefined skills identified in JD.", "missing": []}
            
        # Find skills present in Resume
        res_all = {s for s in cls.TECH_SKILLS.union(cls.SOFT_SKILLS) if s in res_text}
        
        matched = jd_all.intersection(res_all)
        missing = jd_all - res_all
        
        coverage = len(matched) / len(jd_all)
        score = int(coverage * 100)
        
        reason = f"Candidate possesses {len(matched)} of {len(jd_all)} key skills identified in the JD."
        
        return {
            "score": score,
            "reason": reason,
            "missing": list(missing)
        }
