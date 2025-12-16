from pydantic import BaseModel
from typing import Optional, List
from app.modules.permission.schemas.permission_schema import PermissionSchema
# from app.modules.permission.schemas.group_schema import PermissionGroupListSchema

class RoleCreate(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: Optional[str] = None

class RoleSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        
class RoleListSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class GroupSchema(BaseModel):
    id: int
    name: str
    permissions: List[PermissionSchema] = []

    class Config:
        from_attributes = True

class RoleResponse(BaseModel):
    id: int
    name: str
    groups: List[GroupSchema] = []

    class Config:
        from_attributes = True

class GroupPermissionSchema(BaseModel):
    id: int
    name: str
    permissions: List[PermissionSchema] = []

    class Config:
        from_attributes = True


class RoleWithGroupsSchema(BaseModel):
    id: int
    name: str
    groups: List[GroupPermissionSchema] = []

    class Config:
        from_attributes = True