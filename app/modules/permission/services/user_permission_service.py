from sqlalchemy.orm import Session
from app.modules.permission.repositories.user_permission_repository import UserPermissionRepository
from typing import List

class UserPermissionService:
    def __init__(self, db: Session):
        self.repo = UserPermissionRepository(db)

    def assign_permissions(self, user_id: int, permission_ids: List[int], group_id=None):
        self.repo.remove_all(user_id, group_id)
        for pid in permission_ids:
            self.repo.assign(user_id, pid, group_id)
