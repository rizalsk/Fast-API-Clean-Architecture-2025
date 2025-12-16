from sqlalchemy.orm import Session
from app.modules.permission.repositories.permission_group_repository import PermissionGroupRepository

class PermissionGroupService:
    def __init__(self, db: Session):
        self.repo = PermissionGroupRepository(db)

    def create(self, name: str):
        return self.repo.create(name)

    def update(self, group_id: int, name: str):
        return self.repo.update(group_id, name)

    def delete(self, group_id: int):
        return self.repo.delete(group_id)

    def list(self):
        return self.repo.get_all()
