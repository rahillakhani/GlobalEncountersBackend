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
    userid: Optional[int] = None
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
    pass

class FoodLogUpdate(FoodLogBase):
    pass

class FoodLogSchema(FoodLogBase):
    # FoodLogSchema now correctly represents the model's primary key
    userid: int # Changed from 'id' to 'userid' as per FoodLog model's primary key

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