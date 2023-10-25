"""Define a users table."""
import bcrypt
from typing import Optional
from sqlalchemy import Enum, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import timedelta
from database import Base
from utils.text_crypto import generate_encryption_key

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class RoleEnum(PyEnum):
    """Set up the roles."""
    ADMIN = 'admin'
    USER = 'user'


class User(Base):
    """Define a users table."""
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # Set a role for the user
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False, default=RoleEnum.USER)

    # User details
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    date_of_birth: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    # Encryption key for encrypting the chat and therapist data
    encryption_key: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    therapist = relationship("Therapist", back_populates="user")
    chats = relationship("Chat", back_populates="user")

    def __init__(self, username, password_hash, email=None, role=RoleEnum.USER):
        self.username = username
        self.password_hash = password_hash
        if email:
            self.email = email
        self.role = role
        self.initialise_encryption_key()

    def check_password(self, password):
        """Check the password hash against the password."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def set_password(self, password):
        """
        Generate a hash of the password using bcrypt and save it to the password_hash field.
        """
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def create_access_token(self, expires_delta: Optional[timedelta] = None):
        from app.dependencies import manager
        data = {"sub": self.username}
        if not expires_delta:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = manager.create_access_token(data=data, expires=expires_delta)
        return access_token

    def initialise_encryption_key(self):
        """Generate an encryption key for the user."""
        self.encryption_key = generate_encryption_key()

    @property
    def is_admin(self):
        return self.role == RoleEnum.ADMIN

    # Properties for Flask-Login that need to be implemented
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def as_dict(self):
        """Return the user as a dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value
        }
