from langchain_core.prompts import PromptTemplate
from .guardrails import SYSTEM_GUARDRAILS

class PromptBuilder:
    @staticmethod
    def build_resume_optimization_prompt(context: str) -> str:
        template = f"""{SYSTEM_GUARDRAILS}

You are an expert AI Resume Writer.
Your task is to optimize the following candidate data to match the provided Job Description context.

CONTEXT (Resume Data & Job Description):
{{context}}

INSTRUCTIONS:
- Optimize the Professional Summary.
- Optimize the Experience bullets to align with the JD, keeping strictly to the facts provided.
- Suggest ATS keywords that the candidate possesses in their experience but might be missing in a dedicated skills section.

Format the output strictly as a JSON object matching the provided schema.
"""
        prompt = PromptTemplate(template=template, input_variables=["context"])
        return prompt.format(context=context)

    @staticmethod
    def build_interview_prep_prompt(context: str) -> str:
        template = f"""{SYSTEM_GUARDRAILS}

You are a Senior Technical Recruiter.
Based on the following candidate resume and target Job Description, generate 5 targeted interview questions.

CONTEXT:
{{context}}

Format the output strictly as a JSON array of strings containing the questions.
"""
        prompt = PromptTemplate(template=template, input_variables=["context"])
        return prompt.format(context=context)
