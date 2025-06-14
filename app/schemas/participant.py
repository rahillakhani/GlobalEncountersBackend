from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union

# Schema for detail responses when no data is found
class DetailResponse(BaseModel):
    detail: str

class ParticipantData(BaseModel):
    registrant_id: int
    participant_type: Optional[str] = None
    date: datetime

    class Config:
        from_attributes = True

# ParticipantResponse and ParticipantDataResponse seem redundant given ParticipantListResponse and DetailResponse pattern
# I will keep them for now, but will make sure the endpoint uses the appropriate union type.

class ParticipantResponse(BaseModel):
    data: Union[ParticipantData, str]
    detail: Optional[str] = None

    class Config:
        from_attributes = True

class ParticipantDataResponse(BaseModel):
    data: Union[ParticipantData, str]
    detail: Optional[str] = None

    class Config:
        from_attributes = True

class ParticipantBase(BaseModel):
    registrant_id: int
    date: datetime
    participant_type: str

class ParticipantCreate(ParticipantBase):
    pass

class ParticipantUpdate(ParticipantBase):
    pass

class ParticipantListResponse(BaseModel):
    userid: Optional[int] = None
    name: Optional[str] = None
    registration_id: Optional[str] = None
    date: Optional[datetime] = None
    detail: Optional[str] = None
    access_token: Optional[str] = None

    class Config:
        from_attributes = True 