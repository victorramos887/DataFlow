from dataclasses import dataclass, field
from app.features.auth.entities.permission_entity import Permission

@dataclass
class Role:
    id: int | None
    name: str
    description: str
    permission: list[Permission] = field(default_factory=list)
