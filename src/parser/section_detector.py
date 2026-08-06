import re
from typing import Dict

class SectionDetector:
    SECTION_MAPPING = {
        "summary": [r"summary", r"objective", r"profile", r"about me"],
        "experience": [r"experience", r"employment", r"work history", r"professional experience"],
        "education": [r"education", r"academic background", r"qualifications"],
        "skills": [r"skills", r"core competencies", r"technologies", r"technical skills"],
        "projects": [r"projects", r"personal projects", r"academic projects"],
        "certifications": [r"certifications", r"licenses", r"certificates"],
        "achievements": [r"achievements", r"awards", r"honors"]
    }

    @classmethod
    def detect(cls, text: str) -> Dict[str, str]:
        """Detect and extract sections from raw text."""
        sections = {}
        lines = text.split('\n')
        current_section = "unclassified"
        sections[current_section] = []

        for line in lines:
            line_clean = line.strip().lower()
            if len(line_clean) < 40 and not line_clean.startswith('-'):
                detected = cls._match_header(line_clean)
                if detected:
                    current_section = detected
                    if current_section not in sections:
                        sections[current_section] = []
                    continue
            
            sections[current_section].append(line)

        return {k: "\n".join(v).strip() for k, v in sections.items() if v}

    @classmethod
    def _match_header(cls, line: str) -> str:
        for section, patterns in cls.SECTION_MAPPING.items():
            for pattern in patterns:
                if re.match(rf"^{pattern}:?$", line):
                    return section
        return ""
