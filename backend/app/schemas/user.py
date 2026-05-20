from pydantic import BaseModel, EmailStr, Field

from app.models.enums import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=100)
    role: UserRole = UserRole.STUDENT


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: UserRole
    is_active: bool

    model_config = {
        "from_attributes": True,
    }
