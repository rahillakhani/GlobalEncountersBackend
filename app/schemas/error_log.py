from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union

class DetailResponse(BaseModel):
    detail: str

class ErrorLogBase(BaseModel):
    user_id: int
    registrant_id: int
    error: str
    scan_time: datetime

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