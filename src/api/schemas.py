from typing import Any, Optional, Dict
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
