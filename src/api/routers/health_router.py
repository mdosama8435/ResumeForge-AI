import time
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
