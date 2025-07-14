# file: backend/app/schemas/user.py
from pydantic import BaseModel
from typing import List
from .role import Role 

class UserBase(BaseModel):
    username: str
    full_name: str | None = None

class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class User(UserBase):
    id: int
    is_active: bool
    roles: List[Role] = []
    class Config:
        from_attributes = True