from sqlalchemy.orm import Session
from app.modules.permission.repositories.role_repository import RoleRepository
from typing import List
from app.modules.permission.repositories.role_repository import RoleRepository
from app.modules.permission.schemas.role_schema import RoleResponse, GroupSchema, PermissionSchema, RoleSchema


class RoleService:
    def __init__(self, db: Session, repo: RoleRepository):
        self.db = RoleRepository(db)
        self.repo = repo

    def create(self, name: str):
        return self.repo.create(name)

    def update(self, role_id: int, name: str):
        return self.repo.update(role_id, name)

    def delete(self, role_id: int):
        return self.repo.delete(role_id)

    def list(self):
        return self.repo.get_all()
    
    def list_roles(self):
        roles = self.repo.get_all_roles()
        result = []

        for r in roles:
            groups = []
            for rg in r.groups:
                group = rg.group
                if not group:
                    continue
                groups.append(
                    GroupSchema(
                        id=group.id,
                        name=group.name,
                        permissions=[
                            PermissionSchema(
                                id=p.permission.id,
                                name=p.permission.name,
                                is_default=p.permission.is_default
                            )
                            for p in group.permissions
                        ],
                        roles=[
                            RoleSchema(
                                id=role.role.id,
                                name=role.role.name
                            )
                            for role in group.roles
                        ]
                    )
                )

            result.append(
                RoleResponse(
                    id=r.id,
                    name=r.name,
                    groups=groups
                )
            )

        return result
    
    def list_roles_with_groups(self):
        return self.repo.get_all_roles_with_groups()

    # Assigners
    def assign_roles_to_user(self, user_id: int, role_ids: List[int]):
        self.repo.remove_user_roles(user_id)
        for rid in role_ids:
            self.repo.assign_role_to_user(user_id, rid)

    def assign_groups_to_role(self, role_id: int, group_ids: List[int]):
        self.repo.remove_role_groups(role_id)
        for gid in group_ids:
            self.repo.assign_group_to_role(role_id, gid)

    def assign_permissions_to_role(self, role_id: int, permission_ids: List[int]):
        self.repo.remove_role_permissions(role_id)
        for pid in permission_ids:
            self.repo.assign_permission_to_role(role_id, pid)
