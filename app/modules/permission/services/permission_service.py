from sqlalchemy.orm import Session
from app.modules.permission.repositories.permission_repository import PermissionRepository

class PermissionService:
    def __init__(self, db: Session):
        self.repo = PermissionRepository(db)

    def has_permission(self, user_id: int, permission_name: str, group_id: int = None) -> bool:
        # Get user permissions
        user_perms = self.repo.get_user_permissions(user_id)
        perm_ids_user = [p.permission_id for p in user_perms if (p.group_id == group_id or (group_id is None and p.group_id is None))]

        # Get user roles
        user_roles = self.repo.get_user_roles(user_id)
        role_ids = [r.role_id for r in user_roles]

        # Role permissions
        role_perms = self.repo.get_role_permissions(role_ids)
        perm_ids_role = [rp.permission_id for rp in role_perms]

        # Role groups
        role_groups = self.repo.get_role_groups(role_ids)
        group_ids_role = [rg.group_id for rg in role_groups]

        # Group permissions
        group_perms = []
        if group_id:
            group_perms = self.repo.get_group_permissions(group_id)
        perm_ids_group = [gp.permission_id for gp in group_perms]

        # Aggregate all permissions
        all_permission_ids = set(perm_ids_user + perm_ids_role + perm_ids_group)

        # Check if permission exists
        from app.modules.permission.models.permission import Permission
        perm = self.repo.db.query(Permission).filter(Permission.name == permission_name).first()
        if not perm:
            return False

        return perm.id in all_permission_ids
