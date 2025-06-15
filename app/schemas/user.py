from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    device_id: Optional[str] = None
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password: str 