from sqlalchemy import Column, Integer
from app.database.base import Base

class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, primary_key=True)
