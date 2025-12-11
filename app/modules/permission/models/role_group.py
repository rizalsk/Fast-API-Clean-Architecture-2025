from sqlalchemy import Column, Integer
from app.database.base import Base

class RoleGroup(Base):
    __tablename__ = "role_groups"

    role_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, primary_key=True)
