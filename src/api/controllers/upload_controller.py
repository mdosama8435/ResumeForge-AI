from fastapi import UploadFile
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
        
        try:
            doc_manager.add_document(session_id, "resume", parsed_data.get("sections", {}), file.filename)
        except Exception as e:
            if "Duplicate document" not in str(e):
                raise e
                
        return parsed_data

    @staticmethod
    async def upload_jd(file: UploadFile, parser: JDParser, session_id: str) -> Dict[str, Any]:
        file_bytes = await file.read()
        os.makedirs("uploads", exist_ok=True)
        temp_path = f"uploads/{session_id}_jd_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
            
        parsed_data = parser.parse(temp_path)
        return parsed_data
