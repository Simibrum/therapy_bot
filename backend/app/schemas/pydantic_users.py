"""File to store login and security-related classes and functions."""
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserOut(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class UserInDB(UserOut):
    hashed_password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str
