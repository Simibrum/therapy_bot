"""File to store login and security-related classes and functions."""
from typing import Optional
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    age: Optional[int] = None


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


class UserLoginOut(BaseModel):
    """Model to return useful user details on login."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    id: int
    username: str
    first_name: Optional[str] = None
    is_active: bool
