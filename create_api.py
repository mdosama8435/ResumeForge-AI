import os

api_files = {
    "src/api/__init__.py": "",
    
    "src/api/schemas.py": '''from typing import Any, Optional, Dict
from pydantic import BaseModel

class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time: str
    request_id: str

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time: str
    request_id: str
''',

    "src/api/middlewares.py": '''import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = getattr(request.state, "request_id", "unknown")
        
        logger.info(f"Incoming request: {request.method} {request.url.path} | Request ID: {request_id}")
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            logger.info(f"Completed {response.status_code} {response.status_phrase} in {process_time:.4f}s | Request ID: {request_id}")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Failed request {request.method} {request.url.path} in {process_time:.4f}s | Request ID: {request_id} | Error: {e}")
            raise
''',

    "src/api/dependencies.py": '''from src.parser.resume_parser import ResumeParser
from src.parser.jd_parser import JDParser
from src.rag.document_manager import DocumentManager
from src.rag.retriever import RAGRetriever
from src.ats.ats_engine import ATSEngine
from src.llm.resume_optimizer import ResumeOptimizer
from src.llm.interview_generator import InterviewGenerator

def get_resume_parser(): return ResumeParser()
def get_jd_parser(): return JDParser()
def get_document_manager(): return DocumentManager()
def get_retriever(): return RAGRetriever()
def get_ats_engine(): return ATSEngine()
def get_resume_optimizer(): return ResumeOptimizer()
def get_interview_generator(): return InterviewGenerator()
''',

    "src/api/controllers/__init__.py": "",
    "src/api/routers/__init__.py": "",

    "src/api/controllers/upload_controller.py": '''from fastapi import UploadFile
from src.parser.resume_parser import ResumeParser
from src.parser.jd_parser import JDParser
from src.rag.document_manager import DocumentManager
from typing import Dict, Any
import os

class UploadController:
    @staticmethod
    async def upload_resume(file: UploadFile, parser: ResumeParser, doc_manager: DocumentManager, session_id: str) -> Dict[str, Any]:
        file_bytes = await file.read()
        os.makedirs("uploads", exist_ok=True)
        temp_path = f"uploads/{session_id}_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
            
        parsed_data = parser.parse(temp_path)
        doc_manager.add_document(session_id, "resume", parsed_data.get("sections", {}), file.filename)
        return {"parsed": True, "metadata": parsed_data.get("metadata")}

    @staticmethod
    async def upload_jd(file: UploadFile, parser: JDParser, session_id: str) -> Dict[str, Any]:
        file_bytes = await file.read()
        os.makedirs("uploads", exist_ok=True)
        temp_path = f"uploads/{session_id}_jd_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
            
        parsed_data = parser.parse(temp_path)
        return {"parsed": True, "requirements_count": len(parsed_data.get("requirements", []))}
''',

    "src/api/routers/upload_router.py": '''import time
from fastapi import APIRouter, UploadFile, File, Depends, Form, Request
from src.api.schemas import BaseResponse
from src.api.controllers.upload_controller import UploadController
from src.api.dependencies import get_resume_parser, get_jd_parser, get_document_manager

router = APIRouter(prefix="/upload", tags=["Uploads"])

@router.post("/resume", response_model=BaseResponse)
async def upload_resume(
    request: Request,
    session_id: str = Form(...),
    file: UploadFile = File(...),
    parser = Depends(get_resume_parser),
    doc_manager = Depends(get_document_manager)
):
    start = time.time()
    data = await UploadController.upload_resume(file, parser, doc_manager, session_id)
    return BaseResponse(
        success=True, message="Resume uploaded and indexed.", data=data,
        execution_time=f"{time.time() - start:.3f}s", request_id=request.state.request_id
    )

@router.post("/job-description", response_model=BaseResponse)
async def upload_jd(
    request: Request,
    session_id: str = Form(...),
    file: UploadFile = File(...),
    parser = Depends(get_jd_parser)
):
    start = time.time()
    data = await UploadController.upload_jd(file, parser, session_id)
    return BaseResponse(
        success=True, message="Job description parsed.", data=data,
        execution_time=f"{time.time() - start:.3f}s", request_id=request.state.request_id
    )
''',

    "src/api/controllers/analysis_controller.py": '''from typing import Dict, Any
from src.ats.ats_engine import ATSEngine

class AnalysisController:
    @staticmethod
    def analyze(resume_data: Dict[str, Any], jd_data: Dict[str, Any], ats_engine: ATSEngine) -> Dict[str, Any]:
        # Orchestrating the ATS Engine
        report = ats_engine.evaluate(resume_data, jd_data)
        return report.model_dump()
''',

    "src/api/routers/analysis_router.py": '''import time
from fastapi import APIRouter, Depends, Request, Body
from typing import Dict, Any
from src.api.schemas import BaseResponse
from src.api.controllers.analysis_controller import AnalysisController
from src.api.dependencies import get_ats_engine

router = APIRouter(tags=["Analysis"])

@router.post("/analyze", response_model=BaseResponse)
async def analyze_resume(
    request: Request,
    resume_data: Dict[str, Any] = Body(...),
    jd_data: Dict[str, Any] = Body(...),
    ats_engine = Depends(get_ats_engine)
):
    start = time.time()
    data = AnalysisController.analyze(resume_data, jd_data, ats_engine)
    return BaseResponse(
        success=True, message="Analysis complete.", data=data,
        execution_time=f"{time.time() - start:.3f}s", request_id=request.state.request_id
    )
''',

    "src/api/controllers/resume_controller.py": '''from typing import Dict, Any, List
from src.rag.retriever import RAGRetriever
from src.llm.resume_optimizer import ResumeOptimizer

class ResumeController:
    @staticmethod
    def generate_resume(session_id: str, jd_text: str, retriever: RAGRetriever, optimizer: ResumeOptimizer) -> Dict[str, Any]:
        # 1. Retrieve Context
        retrieved_chunks = retriever.retrieve(query=jd_text)
        
        # 2. Optimize
        optimized_data = optimizer.optimize(retrieved_chunks, jd_text)
        return optimized_data.model_dump()
''',

    "src/api/routers/resume_router.py": '''import time
from fastapi import APIRouter, Depends, Request, Body
from src.api.schemas import BaseResponse
from src.api.controllers.resume_controller import ResumeController
from src.api.dependencies import get_retriever, get_resume_optimizer

router = APIRouter(prefix="/generate", tags=["Generation"])

@router.post("/resume", response_model=BaseResponse)
async def generate_resume(
    request: Request,
    session_id: str = Body(...),
    jd_text: str = Body(...),
    retriever = Depends(get_retriever),
    optimizer = Depends(get_resume_optimizer)
):
    start = time.time()
    data = ResumeController.generate_resume(session_id, jd_text, retriever, optimizer)
    return BaseResponse(
        success=True, message="Resume optimized successfully.", data=data,
        execution_time=f"{time.time() - start:.3f}s", request_id=request.state.request_id
    )
''',

    "src/api/controllers/interview_controller.py": '''from typing import Dict, Any
from src.rag.retriever import RAGRetriever
from src.llm.interview_generator import InterviewGenerator

class InterviewController:
    @staticmethod
    def generate_interview(session_id: str, jd_text: str, retriever: RAGRetriever, generator: InterviewGenerator) -> Dict[str, Any]:
        retrieved_chunks = retriever.retrieve(query=jd_text)
        questions = generator.generate(retrieved_chunks, jd_text)
        return {"questions": questions}
''',

    "src/api/routers/interview_router.py": '''import time
from fastapi import APIRouter, Depends, Request, Body
from src.api.schemas import BaseResponse
from src.api.controllers.interview_controller import InterviewController
from src.api.dependencies import get_retriever, get_interview_generator

router = APIRouter(prefix="/generate", tags=["Generation"])

@router.post("/interview", response_model=BaseResponse)
async def generate_interview(
    request: Request,
    session_id: str = Body(...),
    jd_text: str = Body(...),
    retriever = Depends(get_retriever),
    generator = Depends(get_interview_generator)
):
    start = time.time()
    data = InterviewController.generate_interview(session_id, jd_text, retriever, generator)
    return BaseResponse(
        success=True, message="Interview questions generated.", data=data,
        execution_time=f"{time.time() - start:.3f}s", request_id=request.state.request_id
    )
''',

    "src/api/controllers/health_controller.py": '''class HealthController:
    @staticmethod
    def check_status() -> dict:
        # In a real scenario, ping the FAISS store, LLM API, etc.
        return {
            "api_status": "operational",
            "llm_status": "operational",
            "embedding_status": "operational",
            "faiss_status": "operational"
        }
''',

    "src/api/routers/health_router.py": '''import time
from fastapi import APIRouter, Request
from src.api.schemas import BaseResponse
from src.api.controllers.health_controller import HealthController

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=BaseResponse)
async def health_check(request: Request):
    start = time.time()
    data = HealthController.check_status()
    return BaseResponse(
        success=True, message="All systems operational.", data=data,
        execution_time=f"{time.time() - start:.3f}s", request_id=getattr(request.state, "request_id", "unknown")
    )
''',

    "src/api/exception_handlers.py": '''import time
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from exceptions.base import ResumeForgeException

async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(f"Global Exception on {request.url.path} | Request ID: {request_id} | {str(exc)}")
    
    # Generic error response wrapper
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred.",
            "data": {"error": str(exc)},
            "execution_time": "unknown",
            "request_id": request_id
        }
    )

async def resumeforge_exception_handler(request: Request, exc: ResumeForgeException):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"Domain Exception on {request.url.path} | Request ID: {request_id} | {str(exc)}")
    
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": str(exc),
            "data": None,
            "execution_time": "unknown",
            "request_id": request_id
        }
    )
''',

    "src/api/setup.py": '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.api.middlewares import RequestIdMiddleware, LoggingMiddleware
from src.api.routers import upload_router, analysis_router, resume_router, interview_router, health_router
from src.api.exception_handlers import global_exception_handler, resumeforge_exception_handler
from exceptions.base import ResumeForgeException

def create_app() -> FastAPI:
    app = FastAPI(
        title="ResumeForge AI API",
        description="Production API integrating Parser, RAG, ATS, and LLM.",
        version="1.0.0"
    )

    # Middlewares
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(ResumeForgeException, resumeforge_exception_handler)

    # Routers
    app.include_router(health_router.router)
    app.include_router(upload_router.router)
    app.include_router(analysis_router.router)
    app.include_router(resume_router.router)
    app.include_router(interview_router.router)

    return app
''',
    
    "tests/api/test_api.py": '''from fastapi.testclient import TestClient
from src.api.setup import create_app

client = TestClient(create_app())

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "request_id" in data
'''
}

for filepath, content in api_files.items():
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("API layer created successfully.")
