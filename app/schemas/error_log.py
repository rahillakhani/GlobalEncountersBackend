from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List, Union
import re

class DetailResponse(BaseModel):
    detail: str

class ErrorLogBase(BaseModel):
    user_id: int
    registrant_id: Union[str, int]
    error: str
    error_code: str
    scan_time: datetime

    @validator('error_code')
    def validate_error_code(cls, v):
        if not re.match(r'^[0-9]{2}$', v):
            raise ValueError('Error code must be a two-digit number (e.g., 01, 02, 03)')
        return v

class ErrorLogCreate(ErrorLogBase):
    pass

class ErrorLogSchema(ErrorLogBase):
    id: int

    class Config:
        from_attributes = True

class ErrorLogResponse(BaseModel):
    userid: int
    registrant_id: int
    error: str
    error_code: str
    scan_time: datetime
    access_token: str

    class Config:
        from_attributes = True

class ErrorLogListResponse(BaseModel):
    error_logs: List[ErrorLogResponse]
    detail: Optional[str] = None
    access_token: str

    class Config:
        from_attributes = True 