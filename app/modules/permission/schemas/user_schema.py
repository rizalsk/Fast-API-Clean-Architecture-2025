from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class PermissionGroupSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class RoleSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class PermissionSchema(BaseModel):
    id: int
    name: str
    is_default: bool
    group: Optional[PermissionGroupSchema] = None
    route_group: str = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: str
    avatar: Optional[str] = None
    created_at: datetime
    roles: List[RoleSchema] = []
    permissions: List[PermissionSchema] = []

    class Config:
        from_attributes = True