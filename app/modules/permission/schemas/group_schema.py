from pydantic import BaseModel
from typing import Optional, List
from app.modules.permission.schemas.permission_schema import PermissionSchema
from app.modules.permission.schemas.role_schema import RoleSchema

class PermissionGroupCreate(BaseModel):
    name: str

class PermissionGroupUpdate(BaseModel):
    name: Optional[str] = None

class PermissionGroupSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class PermissionGroupListSchema(BaseModel):
    id: int
    name: str
    permissions: List[PermissionSchema] = []
    roles: List[RoleSchema] = []

    class Config:
        from_attributes = True
