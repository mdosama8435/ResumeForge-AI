import time
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
            status_phrase = getattr(response, "status_phrase", "")
            logger.info(f"Completed {response.status_code} {status_phrase} in {process_time:.4f}s | Request ID: {request_id}")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Failed request {request.method} {request.url.path} in {process_time:.4f}s | Request ID: {request_id} | Error: {e}")
            raise
