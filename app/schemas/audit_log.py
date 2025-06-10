from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime

class AuditLogBase(BaseModel):
    registration_id: int
    entity_id: int
    action: str
    timestamp: datetime
    details: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogUpdate(BaseModel):
    registrationid: int
    date: str
    action: str
    details: Optional[str] = None

class AuditLogSchema(AuditLogBase):
    id: int

    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    data: Union[AuditLogSchema, str]
    detail: Optional[str] = None

    class Config:
        from_attributes = True

class AuditLogListResponse(BaseModel):
    data: Union[List[AuditLogSchema], str]
    detail: Optional[str] = None

    class Config:
        from_attributes = True 