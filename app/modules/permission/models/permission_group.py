from sqlalchemy import Column, Integer, String
from app.database.base import Base
from sqlalchemy.orm import relationship

class PermissionGroup(Base):
    __tablename__ = "permission_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    permissions = relationship("PermissionGroupPermission", back_populates="group")
    roles = relationship("RoleGroup", back_populates="group")
    
    user_permissions = relationship("UserPermission", back_populates="group")

    @property
    def role_objects(self):
        return [rg.role for rg in self.roles]

    @property
    def permission_objects(self):
        return [gp.permission for gp in self.permissions]