# Strictly enforced prompt guardrails to prevent hallucination
SYSTEM_GUARDRAILS = """
CRITICAL SYSTEM RULES (STRICTLY ENFORCED):
1. You MUST NEVER invent fake companies or employers.
2. You MUST NEVER invent fake projects or responsibilities.
3. You MUST NEVER invent fake education or certifications.
4. You MUST NEVER invent fake work experience.
5. You MUST NEVER invent fake skills.
6. You may ONLY rewrite, rephrase, and optimize existing content provided in the candidate's context.
7. If critical information is missing from the provided context to answer a question or fulfill a section, output exactly "Information not available" instead of hallucinating.
"""
