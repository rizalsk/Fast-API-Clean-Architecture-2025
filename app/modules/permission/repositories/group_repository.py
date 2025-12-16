# app/modules/permission/repositories/group_repository.py
from sqlalchemy.orm import Session, joinedload
from app.modules.permission.models.permission_group import PermissionGroup
from app.modules.permission.models.permission_group_permission import PermissionGroupPermission
from app.modules.permission.models.role_group import RoleGroup

class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_groups(self):
        return self.db.query(PermissionGroup).options(
            joinedload(PermissionGroup.permissions).joinedload(PermissionGroupPermission.permission),
            joinedload(PermissionGroup.roles).joinedload(RoleGroup.role)
        ).all()