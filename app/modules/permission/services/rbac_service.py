from sqlalchemy.orm import Session

from app.modules.permission.models.user_role import UserRole
from app.modules.permission.models.role_permission import RolePermission
from app.modules.permission.models.permission import Permission
from app.modules.permission.models.user_permission import UserPermission
from app.modules.permission.models.permission_group_permission import PermissionGroupPermission
from app.modules.permission.models.role_group import RoleGroup

class RBACService:
    def __init__(self, db: Session):
        self.db = db

    def has_permission(self, user_id: int, permission_name: str, group_id: int = None) -> bool:
        # Cek permission exist
        perm = self.db.query(Permission).filter(Permission.name == permission_name).first()
        if not perm:
            return False

        perm_id = perm.id

        # Jika group_id diberikan
        if group_id:
            # Cek group permission
            gp = self.db.query(PermissionGroupPermission).filter_by(group_id=group_id, permission_id=perm_id).first()
            if gp:
                return True
            # Cek user individual permission di group
            up = self.db.query(UserPermission).filter_by(user_id=user_id, group_id=group_id, permission_id=perm_id).first()
            if up:
                return True
            # Cek role permission di group
            roles = self.db.query(UserRole).filter_by(user_id=user_id).all()
            for r in roles:
                role_group = self.db.query(RoleGroup).filter_by(role_id=r.role_id, group_id=group_id).first()
                if role_group:
                    role_perm = self.db.query(RolePermission).filter_by(role_id=r.role_id, permission_id=perm_id).first()
                    if role_perm:
                        return True
            return False
        else:
            # Cek user individual permission tanpa group
            up = self.db.query(UserPermission).filter_by(user_id=user_id, group_id=None, permission_id=perm_id).first()
            if up:
                return True
            # Cek role permission tanpa group
            roles = self.db.query(UserRole).filter_by(user_id=user_id).all()
            for r in roles:
                role_perm = self.db.query(RolePermission).filter_by(role_id=r.role_id, permission_id=perm_id).first()
                if role_perm:
                    return True
            return False
