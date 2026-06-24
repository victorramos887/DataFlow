from dataclasses import dataclass


@dataclass
class Role:
    id: int | None
    name: str
    description: str
