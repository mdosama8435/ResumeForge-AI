import time
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
