from dataclasses import dataclass, field
from typing import List

from app.features.auth.domain.entities.roles_entity import Role
@dataclass
class User:
    id: int | None
    name: str
    email: str
    password_hash: str
    roles: List[Role] = field(default_factory=list)
    is_active: bool = True