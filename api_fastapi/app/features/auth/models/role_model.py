from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.features.auth.models.role_permissions_model import role_permissions
from app.features.auth.models.user_roles_models import user_roles
from app.core.base import Base

class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    
    users: Mapped[list["UserModel"]] = relationship(
        "UserModel", 
        secondary = user_roles,
        back_populates="role"
    )
    
    permission: Mapped[list["PermissionModel"]] = relationship(
        "PermissionModel",
        secondary = role_permissions,
        back_populates="roles",
    )