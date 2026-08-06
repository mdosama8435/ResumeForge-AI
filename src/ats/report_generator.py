from typing import Dict, Any
from .models import ATSReport

class ReportGenerator:
    @staticmethod
    def generate(results: Dict[str, Any]) -> ATSReport:
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Simple heuristic for strengths/weaknesses
        for key, val in results.items():
            if isinstance(val, dict) and "score" in val:
                if val["score"] >= 80:
                    strengths.append(val["reason"])
                elif val["score"] <= 60:
                    weaknesses.append(val["reason"])
                    recommendations.append(f"Improve {key}: {val['reason']}")
                    
        return ATSReport(
            overall_score=results["overall_score"],
            keyword_score=results["keyword"]["score"],
            keyword_reason=results["keyword"]["reason"],
            skills_score=results["skills"]["score"],
            skills_reason=results["skills"]["reason"],
            experience_score=results["experience"]["score"],
            experience_reason=results["experience"]["reason"],
            project_score=results["projects"]["score"],
            project_reason=results["projects"]["reason"],
            education_score=results["education"]["score"],
            education_reason=results["education"]["reason"],
            formatting_score=results["formatting"]["score"],
            formatting_reason=results["formatting"]["reason"],
            matched_keywords=results["keyword"].get("matched", []),
            missing_keywords=results["keyword"].get("missing", []),
            recommended_keywords=results["keyword"].get("missing", [])[:5],  # Take top 5 missing as recommended
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
