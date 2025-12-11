from sqlalchemy import Column, Integer
from app.database.base import Base

class PermissionGroupPermission(Base):
    __tablename__ = "permission_group_permissions"

    group_id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, primary_key=True)
