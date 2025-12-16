from sqlalchemy import Column, Integer, String
from app.database.base import Base
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    users = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )

    # relasi ke role_groups
    groups = relationship("RoleGroup", back_populates="role")

    @property
    def group_objects(self):
        return [rg.group for rg in self.groups]

    @property
    def permission_objects(self):
        return [gp.permission for gp in self.permissions]