from sqlalchemy import Column, Integer, ForeignKey
from app.database.base import Base

class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = {"extend_existing": True}

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)