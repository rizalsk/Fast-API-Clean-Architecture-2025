from fastapi import APIRouter, Request
# from app.modules.permission.middleware.permission_middleware import PermissionRequired

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal

# Schemas
from app.modules.permission.schemas.group_schema import PermissionGroupCreate, PermissionGroupUpdate
from app.modules.permission.schemas.role_schema import RoleCreate, RoleUpdate
from app.modules.permission.schemas.assign_schema import (
    AssignRoleToUser,
    AssignGroupToRole,
    AssignPermissionToRole,
    AssignPermissionToUser
)

# Services
from app.modules.permission.services.permission_group_service import PermissionGroupService
from app.modules.permission.services.role_service import RoleService
from app.modules.permission.services.user_permission_service import UserPermissionService

from typing import List
from app.modules.permission.services.group_service import GroupRepository
from app.modules.permission.repositories.role_repository import RoleRepository
from app.modules.permission.services.group_service import GroupService
from app.modules.permission.schemas.group_schema import PermissionGroupListSchema
from app.modules.permission.schemas.role_schema import (RoleWithGroupsSchema)

router = APIRouter(prefix="/permission", tags=["RBAC Permissions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= G R O U P  =================

@router.post("/groups")
def create_group(data: PermissionGroupCreate, db: Session = Depends(get_db)):
    return PermissionGroupService(db).create(data.name)

@router.put("/groups/{group_id}")
def update_group(group_id: int, data: PermissionGroupUpdate, db: Session = Depends(get_db)):
    return PermissionGroupService(db).update(group_id, data.name)

@router.delete("/groups/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    return PermissionGroupService(db).delete(group_id)

@router.get("/groups", response_model=List[PermissionGroupListSchema])
def list_groups(db: Session = Depends(get_db)):
    repo = GroupRepository(db)
    service = GroupService(repo)
    return service.list_groups()

# ================= R O L E  =================

@router.post("/roles")
def create_role(data: RoleCreate, db: Session = Depends(get_db)):
    return RoleService(db).create(data.name)

@router.put("/roles/{role_id}")
def update_role(role_id: int, data: RoleUpdate, db: Session = Depends(get_db)):
    return RoleService(db).update(role_id, data.name)

@router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    return RoleService(db).delete(role_id)

# @router.get("/roles", response_model=List[RoleListSchema])
# def list_roles(db: Session = Depends(get_db)):
#     return RoleService(db).list()

@router.get("/roles", response_model=List[RoleWithGroupsSchema])
def list_roles(db: Session = Depends(get_db)):
    repo = RoleRepository(db)
    service = RoleService(db, repo)
    return service.list_roles()

# ================= A S S I G N M E N T =================

@router.post("/assign/user-role")
def assign_role_to_user(data: AssignRoleToUser, db: Session = Depends(get_db)):
    RoleService(db).assign_roles_to_user(data.user_id, data.role_ids)
    return {"message": "Roles assigned"}

@router.post("/assign/role-group")
def assign_groups_to_role(data: AssignGroupToRole, db: Session = Depends(get_db)):
    RoleService(db).assign_groups_to_role(data.role_id, data.group_ids)
    return {"message": "Groups assigned"}

@router.post("/assign/role-permission")
def assign_permissions_to_role(data: AssignPermissionToRole, db: Session = Depends(get_db)):
    RoleService(db).assign_permissions_to_role(data.role_id, data.permission_ids)
    return {"message": "Permissions assigned"}

@router.post("/assign/user-permission")
def assign_permissions_to_user(data: AssignPermissionToUser, db: Session = Depends(get_db)):
    UserPermissionService(db).assign_permissions(
        user_id=data.user_id,
        permission_ids=data.permission_ids,
        group_id=data.group_id
    )
    return {"message": "User permissions assigned"}

