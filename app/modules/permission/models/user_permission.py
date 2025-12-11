from sqlalchemy import Column, Integer
from app.database.base import Base

class UserPermission(Base):
    __tablename__ = "user_permissions"

    user_id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=True)
