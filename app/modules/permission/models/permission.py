from sqlalchemy import Column, Integer, String, Boolean
from app.database.base import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    is_default = Column(Boolean, default=False)
