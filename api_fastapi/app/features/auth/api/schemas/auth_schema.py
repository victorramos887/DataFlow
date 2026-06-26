from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List

class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    roles: List | None = []

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    roles: List | None = []
    model_config = ConfigDict(from_attributes=True)
    
class UserSummaryResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRequestRole(BaseModel):
    id: int
    roles: List[int]