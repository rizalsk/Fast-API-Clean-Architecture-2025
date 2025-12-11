from sqlalchemy import Column, Integer, String
from app.database.base import Base

class PermissionGroup(Base):
    __tablename__ = "permission_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
