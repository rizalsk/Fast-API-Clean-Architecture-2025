from pydantic import BaseModel
from typing import List, Optional

class AssignRoleToUser(BaseModel):
    user_id: int
    role_ids: List[int]

class AssignGroupToRole(BaseModel):
    role_id: int
    group_ids: List[int]

class AssignPermissionToRole(BaseModel):
    role_id: int
    permission_ids: List[int]

class AssignPermissionToUser(BaseModel):
    user_id: int
    permission_ids: List[int]
    group_id: Optional[int] = None
