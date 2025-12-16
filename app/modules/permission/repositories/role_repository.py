from sqlalchemy.orm import Session, joinedload
from app.modules.permission.models.role import Role
from app.modules.permission.models.user_role import UserRole
from app.modules.permission.models.role_group import RoleGroup
from app.modules.permission.models.permission import Permission
from app.modules.permission.models.permission_group import PermissionGroup
from app.modules.permission.models.permission_group_permission import PermissionGroupPermission
from app.modules.permission.models.role_permission import RolePermission

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str):
        role = Role(name=name)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def get_all(self):
        return self.db.query(Role).all()

    def get_all_roles(self):
        return self.db.query(Role).options(
            joinedload(Role.groups)
            .joinedload(RoleGroup.group)
            .joinedload(PermissionGroup.permissions)
            .joinedload(PermissionGroupPermission.permission)
        ).all()

    def get(self, role_id: int):
        return self.db.query(Role).filter(Role.id == role_id).first()

    def update(self, role_id: int, name: str):
        role = self.get(role_id)
        if role:
            role.name = name
            self.db.commit()
            self.db.refresh(role)
        return role

    def delete(self, role_id: int):
        role = self.get(role_id)
        if role:
            self.db.delete(role)
            self.db.commit()
        return role

    # Assignments
    def assign_role_to_user(self, user_id: int, role_id: int):
        ur = UserRole(user_id=user_id, role_id=role_id)
        self.db.add(ur)
        self.db.commit()

    def remove_user_roles(self, user_id: int):
        self.db.query(UserRole).filter(UserRole.user_id == user_id).delete()
        self.db.commit()

    def assign_group_to_role(self, role_id: int, group_id: int):
        rg = RoleGroup(role_id=role_id, group_id=group_id)
        self.db.add(rg)
        self.db.commit()

    def remove_role_groups(self, role_id: int):
        self.db.query(RoleGroup).filter(RoleGroup.role_id == role_id).delete()
        self.db.commit()

    def assign_permission_to_role(self, role_id: int, permission_id: int):
        rp = RolePermission(role_id=role_id, permission_id=permission_id)
        self.db.add(rp)
        self.db.commit()

    def remove_role_permissions(self, role_id: int):
        self.db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        self.db.commit()

    def get_all_roles_with_groups(self):
        roles = self.db.query(Role).all()
        result = []

        for role in roles:
            # Ambil group terkait role
            role_groups = (
                self.db.query(PermissionGroup)
                .join(RoleGroup, RoleGroup.group_id == PermissionGroup.id)
                .filter(RoleGroup.role_id == role.id)
                .all()
            )

            group_list = []

            for group in role_groups:
                # Ambil permission di group
                group_permissions = (
                    self.db.query(Permission)
                    .join(PermissionGroupPermission, PermissionGroupPermission.permission_id == Permission.id)
                    .filter(PermissionGroupPermission.group_id == group.id)
                    .all()
                )

                group_list.append({
                    "id": group.id,
                    "name": group.name,
                    "permissions": group_permissions
                })

            result.append({
                "id": role.id,
                "name": role.name,
                "groups": group_list
            })

        return result