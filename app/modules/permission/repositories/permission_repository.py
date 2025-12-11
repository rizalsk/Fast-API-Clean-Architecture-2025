from sqlalchemy.orm import Session
from app.modules.permission.models.permission import Permission
from app.modules.permission.models.role import Role
from app.modules.permission.models.role_permission import RolePermission
from app.modules.permission.models.user_role import UserRole
from app.modules.permission.models.user_permission import UserPermission
from app.modules.permission.models.permission_group_permission import PermissionGroupPermission
from app.modules.permission.models.role_group import RoleGroup

class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_permission_by_name(self, name: str):
        return self.db.query(Permission).filter(Permission.name == name).first()

    def get_user_roles(self, user_id: int):
        return self.db.query(UserRole).filter(UserRole.user_id == user_id).all()

    def get_role_permissions(self, role_ids: list[int]):
        return self.db.query(RolePermission).filter(RolePermission.role_id.in_(role_ids)).all()

    def get_user_permissions(self, user_id: int):
        return self.db.query(UserPermission).filter(UserPermission.user_id == user_id).all()

    def get_group_permissions(self, group_id: int):
        return self.db.query(PermissionGroupPermission).filter(PermissionGroupPermission.group_id == group_id).all()

    def get_role_groups(self, role_ids: list[int]):
        return self.db.query(RoleGroup).filter(RoleGroup.role_id.in_(role_ids)).all()
