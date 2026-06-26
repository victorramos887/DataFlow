from dataclasses import dataclass, field
from app.features.auth.domain.entities.permission_entity import Permission

@dataclass
class Role:
    id: int | None
    name: str
    description: str
    users: list[int] = field(default_factory=list)
    permission: list[Permission] = field(default_factory=list)
