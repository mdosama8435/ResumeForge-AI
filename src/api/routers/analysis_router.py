import time
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
