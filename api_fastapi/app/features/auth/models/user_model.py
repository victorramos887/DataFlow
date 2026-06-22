from sqlalchemy import ForeignKey, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base
from app.features.auth.models.user_roles_models import user_roles

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
   
    roles: Mapped[list["RoleModel"]] = relationship(
        "RoleModel", 
        secondary = user_roles,
        back_populates="users",
    )