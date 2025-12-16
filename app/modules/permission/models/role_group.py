from sqlalchemy import Column, Integer, ForeignKey
from app.database.base import Base
from sqlalchemy.orm import relationship

class RoleGroup(Base):
    __tablename__ = "role_groups"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("permission_groups.id"), primary_key=True)

    role = relationship("Role", back_populates="groups")
    group = relationship("PermissionGroup", back_populates="roles")