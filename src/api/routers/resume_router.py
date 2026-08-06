import time
from fastapi import APIRouter, Depends, Request, Body, Response
from src.api.schemas import BaseResponse
from src.api.controllers.resume_controller import ResumeController
from src.api.dependencies import get_retriever, get_resume_optimizer, get_cover_letter_generator, get_interview_generator

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

@router.post("/cover-letter", response_model=BaseResponse)
async def generate_cover_letter(
    request: Request,
    session_id: str = Body(...),
    jd_text: str = Body(...),
    retriever = Depends(get_retriever),
    generator = Depends(get_cover_letter_generator)
):
    start = time.time()
    data = ResumeController.generate_cover_letter(session_id, jd_text, retriever, generator)
    return BaseResponse(
        success=True, message="Cover letter generated successfully.", data={"cover_letter": data},
        execution_time=f"{time.time() - start:.3f}s", request_id=request.state.request_id
    )

@router.post("/interview", response_model=BaseResponse)
async def generate_interview(
    request: Request,
    session_id: str = Body(...),
    jd_text: str = Body(...),
    retriever = Depends(get_retriever),
    generator = Depends(get_interview_generator)
):
    start = time.time()
    data = ResumeController.generate_interview(session_id, jd_text, retriever, generator)
    return BaseResponse(
        success=True, message="Interview questions generated successfully.", data=data,
        execution_time=f"{time.time() - start:.3f}s", request_id=request.state.request_id
    )

from src.utils.document_generator import DocumentGenerator
from typing import Dict, Any

@router.post("/export/pdf")
async def export_pdf(opt_data: Dict[str, Any] = Body(...)):
    pdf_bytes = DocumentGenerator.generate_pdf(opt_data)
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.post("/export/docx")
async def export_docx(opt_data: Dict[str, Any] = Body(...)):
    docx_bytes = DocumentGenerator.generate_docx(opt_data)
    return Response(content=docx_bytes, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
