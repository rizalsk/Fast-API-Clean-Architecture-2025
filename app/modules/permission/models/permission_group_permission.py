from sqlalchemy import Column, Integer, ForeignKey
from app.database.base import Base
from sqlalchemy.orm import relationship

class PermissionGroupPermission(Base):
    __tablename__ = "permission_group_permissions"

    group_id = Column(Integer, ForeignKey("permission_groups.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)

    group = relationship("PermissionGroup", back_populates="permissions")
    permission = relationship("Permission")