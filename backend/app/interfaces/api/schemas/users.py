from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str


class UserUpdate(BaseModel):
    nombre: str | None = None
    rol: str | None = None
    activo: bool | None = None


class UserResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True
