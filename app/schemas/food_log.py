from pydantic import BaseModel
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
    registration_id: Optional[int] = None
    date: Optional[datetime] = None
    lunch: Optional[int] = None
    dinner: Optional[int] = None
    lunch_takenon: Optional[datetime] = None
    dinner_takenon: Optional[datetime] = None

    class Config:
        from_attributes = True

class FoodLogCreate(FoodLogBase):
    registration_id: int  # Make registration_id required for creation
    date: datetime  # Make date required for creation

class FoodLogUpdate(FoodLogBase):
    pass

class FoodLogSchema(FoodLogBase):
    registration_id: int  # Make registration_id required in response
    date: datetime  # Make date required in response

    class Config:
        from_attributes = True

# Removed FoodLogResponse as FoodLogSchema will be used directly
# class FoodLogResponse(FoodLogBase):
#     class Config:
#         from_attributes = True

class FoodLogListResponse(BaseModel):
    data: List[FoodLogSchema]
    detail: Optional[str] = None

    class Config:
        from_attributes = True 