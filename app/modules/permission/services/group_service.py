# app/modules/permission/services/group_service.py
from app.modules.permission.repositories.group_repository import GroupRepository
from app.modules.permission.schemas.group_schema import PermissionGroupListSchema
from app.modules.permission.schemas.permission_schema import PermissionSchema
from app.modules.permission.schemas.role_schema import RoleSchema

class GroupService:
    def __init__(self, repo: GroupRepository):
        self.repo = repo

    def list_groups(self):
        groups = self.repo.get_all_groups()

        result = []
        for g in groups:
            result.append(
                PermissionGroupListSchema(
                    id=g.id,
                    name=g.name,
                    permissions=[
                        PermissionSchema(
                            id=p.permission.id,
                            name=p.permission.name,
                            is_default=p.permission.is_default
                        )
                        for p in g.permissions
                    ],
                    roles=[
                        RoleSchema(
                            id=rg.role.id,
                            name=rg.role.name
                        )
                        for rg in g.roles
                    ]
                )
            )
        return result