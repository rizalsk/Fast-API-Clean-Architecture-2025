from sqlalchemy.orm import Session
from app.modules.permission.models.permission_group import PermissionGroup

class PermissionGroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str):
        group = PermissionGroup(name=name)
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def get_all(self):
        return self.db.query(PermissionGroup).all()

    def get(self, group_id: int):
        return self.db.query(PermissionGroup).filter(PermissionGroup.id == group_id).first()

    def update(self, group_id: int, name: str):
        group = self.get(group_id)
        if group:
            group.name = name
            self.db.commit()
            self.db.refresh(group)
        return group

    def delete(self, group_id: int):
        group = self.get(group_id)
        if group:
            self.db.delete(group)
            self.db.commit()
        return group
