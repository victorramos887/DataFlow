from pydantic import BaseModel, Field, ConfigDict

class PermissionRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1024)