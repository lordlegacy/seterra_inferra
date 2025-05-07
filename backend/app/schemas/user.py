from pydantic import BaseModel
from typing import Optional
from backend.app.models.user import UserRole  # Enum with "user", "support", "admin"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[UserRole] = UserRole.user  # <- Add this

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole

    class Config:
        orm_mode = True


class RoleUpdate(BaseModel):
    role: UserRole
