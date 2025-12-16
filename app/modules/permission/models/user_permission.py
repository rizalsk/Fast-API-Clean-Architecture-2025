from app.database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    UniqueConstraint,
    ForeignKey
)

class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("permission_groups.id"), nullable=True)

    user = relationship("User", back_populates="user_permissions")
    permission = relationship("Permission", back_populates="user_permissions")
    group = relationship("PermissionGroup", back_populates="user_permissions")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "permission_id",
            "group_id",
            name="uq_user_permission_group"
        ),
    )