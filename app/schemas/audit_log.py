from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditLogSchema(BaseModel):
    id: int
    date: datetime
    entitlement_type: str
    name: str
    registration_id: int
    lunch: int  # 0 for False, 1 for True
    dinner: int  # 0 for False, 1 for True
    lunch_takenon: Optional[datetime] = None
    dinner_takenon: Optional[datetime] = None

    class Config:
        from_attributes = True

class AuditLogUpdate(BaseModel):
    registrationid: str
    date: str
    lunch: Optional[bool] = None
    dinner: Optional[bool] = None
    lunch_takenon: Optional[str] = None
    dinner_takenon: Optional[str] = None 