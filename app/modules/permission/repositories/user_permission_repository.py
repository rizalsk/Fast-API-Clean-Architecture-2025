from sqlalchemy.orm import Session
from app.modules.permission.models.user_permission import UserPermission

class UserPermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def assign(self, user_id: int, permission_id: int, group_id: int = None):
        up = UserPermission(user_id=user_id, permission_id=permission_id, group_id=group_id)
        self.db.add(up)
        self.db.commit()

    def remove_all(self, user_id: int, group_id: int = None):
        query = self.db.query(UserPermission).filter(UserPermission.user_id == user_id)
        if group_id:
            query = query.filter(UserPermission.group_id == group_id)
        query.delete()
        self.db.commit()
