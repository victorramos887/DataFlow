from pydantic import BaseModel, Field, ConfigDict

from typing import List

from app.features.auth.api.schemas.auth_permission_schema import PermissionSummaryResponse
from app.features.auth.api.schemas.auth_schema import UserSummaryResponse
class RolesRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1024)
    
class RolesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None
    users: list | None = []
    permission: list | None = []
    
class RolesPermission(BaseModel):
    id: int
    permission: List[int]
    
class RolesResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    permissions: list[PermissionSummaryResponse] = Field(default_factory=list)
    users: list[UserSummaryResponse] = Field(default_factory=list)
    
class RoleResponsePermissionSummary(BaseModel):
    id: int
    name: str
    description: str | None = None
