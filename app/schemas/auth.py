"""Pydantic schemas for user registration, login, and JWT tokens."""

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: UserRole

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
