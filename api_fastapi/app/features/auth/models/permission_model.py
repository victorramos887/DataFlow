from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.features.auth.models.role_permissions_model import role_permissions
from app.core.base import Base


class PermissionModel(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    
    roles: Mapped[list["RoleModel"]] = relationship(
        "RoleModel",
        secondary = role_permissions,
        back_populates="permission",
    )