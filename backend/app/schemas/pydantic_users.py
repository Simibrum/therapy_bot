"""File to store login and security-related classes and functions."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str | None = None
    is_active: bool | None = None
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    age: int | None = None


class UserInDB(UserOut):
    hashed_password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
    role: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginOut(BaseModel):
    """Model to return useful user details on login."""

    access_token: str
    refresh_token: str | None = None
    token_type: str
    id: int
    username: str
    first_name: str | None = None
    is_active: bool
