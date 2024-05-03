"""Define a users table."""
from __future__ import annotations

from datetime import timedelta
from enum import Enum as PyEnum

import bcrypt
from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.common import LifeDatesMixin, LocationMixin, PersonNameMixin
from utils.text_crypto import generate_encryption_key

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class RoleEnum(PyEnum):
    """Set up the roles."""

    ADMIN = "admin"
    USER = "user"


class User(Base, LocationMixin, PersonNameMixin, LifeDatesMixin):
    """Define a users table."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    # Set a role for the user
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False, default=RoleEnum.USER)

    # User details - via the mixins

    # User state
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Encryption key for encrypting the chat and therapist data
    encryption_key: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    therapist = relationship("Therapist", back_populates="user")
    chats = relationship("Chat", back_populates="user")
    therapy_sessions = relationship("TherapySession", back_populates="user")

    def __init__(
        self, username: str, password_hash: str, email: str | None = None, role: RoleEnum = RoleEnum.USER
    ) -> None:
        """Initialise a user."""
        self.username = username
        self.password_hash = password_hash
        if email:
            self.email = email
        self.role = role
        self.initialise_encryption_key()

    def check_password(self, password: str) -> bool:
        """Check the password hash against the password."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def set_password(self, password: str) -> None:
        """Generate a hash of the password using bcrypt and save it to the password_hash field."""
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def create_access_token(self, expires_delta: timedelta | None = None) -> str:
        """Create an access token for the user."""
        from app.dependencies import manager

        data = {"sub": self.username}
        if not expires_delta:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return manager.create_access_token(data=data, expires=expires_delta)

    def initialise_encryption_key(self) -> None:
        """Generate an encryption key for the user."""
        self.encryption_key = generate_encryption_key()

    @property
    def is_admin(self) -> bool:
        """Check if the user is an admin."""
        return self.role == RoleEnum.ADMIN

    # Properties for Flask-Login that need to be implemented
    @property
    def is_authenticated(self) -> bool:
        """Return True if the user is authenticated."""
        return True

    @property
    def is_anonymous(self) -> bool:
        """Return anonymous user status."""
        return False

    def get_id(self) -> str:
        """Return the user ID as a string."""
        return str(self.id)

    def as_dict(self) -> dict:
        """Return the user as a dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
        }
