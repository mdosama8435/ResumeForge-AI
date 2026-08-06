from fastapi import FastAPI
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
