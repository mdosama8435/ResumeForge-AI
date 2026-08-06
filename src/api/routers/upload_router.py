import time
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
