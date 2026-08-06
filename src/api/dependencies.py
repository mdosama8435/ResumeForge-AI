from src.parser.resume_parser import ResumeParser
from src.parser.jd_parser import JDParser
from src.rag.document_manager import DocumentManager
from src.rag.retriever import RAGRetriever
from src.ats.ats_engine import ATSEngine
from src.llm.resume_optimizer import ResumeOptimizer
from src.llm.interview_generator import InterviewGenerator
from src.llm.cover_letter_generator import CoverLetterGenerator

def get_resume_parser(): return ResumeParser()
def get_jd_parser(): return JDParser()
def get_document_manager(): return DocumentManager()
def get_retriever(): return RAGRetriever()
def get_ats_engine(): return ATSEngine()
def get_resume_optimizer(): return ResumeOptimizer()
def get_interview_generator(): return InterviewGenerator()
def get_cover_letter_generator(): return CoverLetterGenerator()
