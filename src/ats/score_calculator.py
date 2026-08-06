from typing import Dict, Any

class ScoreCalculator:
    WEIGHTS = {
        "keyword": 0.30,
        "skills": 0.20,
        "experience": 0.20,
        "projects": 0.15,
        "education": 0.10,
        "formatting": 0.05
    }

    @classmethod
    def calculate_overall(cls, sub_scores: Dict[str, int]) -> int:
        overall = 0.0
        for key, weight in cls.WEIGHTS.items():
            overall += sub_scores.get(key, 0) * weight
        return int(round(overall))
