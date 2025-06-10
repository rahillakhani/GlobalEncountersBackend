from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union

class DetailResponse(BaseModel):
    detail: str

class ErrorLogBase(BaseModel):
    user_id: Optional[int] = None
    registrant_id: Optional[int] = None
    error: str
    scan_time: datetime

class ErrorLogCreate(ErrorLogBase):
    pass

class ErrorLogSchema(ErrorLogBase):
    id: int

    class Config:
        from_attributes = True

class ErrorLogResponse(BaseModel):
    data: Optional[ErrorLogSchema] = None
    detail: Optional[str] = None

    class Config:
        from_attributes = True

class ErrorLogListResponse(BaseModel):
    data: Optional[List[ErrorLogSchema]] = None
    detail: Optional[str] = None

    class Config:
        from_attributes = True 