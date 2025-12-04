from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    name: EmailStr
    password: str
    avatar: str = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: str
    avatar: Optional[str] = None   
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None