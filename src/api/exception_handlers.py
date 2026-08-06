import time
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
