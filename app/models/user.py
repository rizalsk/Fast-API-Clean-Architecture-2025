from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    email = Column(String(100), unique=True)
    name = Column(String(100))
    avatar = Column(String(255), nullable=True)
    password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # remove if you don't need permission
    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users"
    )

    user_permissions = relationship("UserPermission", back_populates="user")
    