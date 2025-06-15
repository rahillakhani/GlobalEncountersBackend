from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Union, Any

class DetailResponse(BaseModel):
    detail: str

class ParticipantData(BaseModel):
    registrant_id: int
    participant_type: Optional[str] = None
    date: datetime

    class Config:
        from_attributes = True

class FoodLogBase(BaseModel):
    name: Optional[str] = None
    registration_id: Optional[Union[str, int]] = None
    date: Optional[datetime] = None
    lunch: Optional[int] = None
    dinner: Optional[int] = None
    lunch_takenon: Optional[datetime] = None
    dinner_takenon: Optional[datetime] = None

    @validator('registration_id', pre=True)
    def convert_registration_id(cls, v):
        # Convert to string if it's not None
        return str(v) if v is not None else v

    class Config:
        from_attributes = True

class FoodLogCreate(FoodLogBase):
    registration_id: Union[str, int]  # Accept both string and int
    date: datetime

class FoodLogUpdate(FoodLogBase):
    registration_id: Union[str, int]  # Accept both string and int
    date: datetime

class FoodLogSchema(FoodLogBase):
    registration_id: Union[str, int]  # Accept both string and int
    date: datetime

    class Config:
        from_attributes = True

# Removed FoodLogResponse as FoodLogSchema will be used directly
# class FoodLogResponse(FoodLogBase):
#     class Config:
#         from_attributes = True

class FoodLogListResponse(BaseModel):
    food_logs: List[FoodLogSchema]
    detail: Optional[str] = None
    access_token: str

    class Config:
        from_attributes = True 