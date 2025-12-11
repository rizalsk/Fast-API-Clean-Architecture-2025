from sqlalchemy import Column, Integer
from app.database.base import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, primary_key=True)
