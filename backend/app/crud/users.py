"""CRUD methods for users."""
from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.schemas.pydantic_users import UserUpdate, UserOut
from models import User, RoleEnum


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Get a user by username - for auth."""
    if not username:
        return None
    try:
        user = session.query(User).filter(User.username == username).one_or_none()
    except NoResultFound:
        return None
    return user


def create_user(session: Session, user_in: UserUpdate) -> UserOut:
    """Create a new user."""
    # Convert role to an enum
    role = (
        RoleEnum(user_in.role)
        if user_in.role in RoleEnum.__members__
        else RoleEnum.USER
    )
    user = User(
        username=user_in.username, email=user_in.email, password_hash="temp", role=role
    )
    user.set_password(user_in.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserOut.model_validate(user)


def get_user(session: Session, user_id: str) -> Optional[UserOut]:
    """Get a user."""
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return UserOut.model_validate(user)


def get_users(session: Session) -> List[UserOut]:
    """Get all users."""
    users = session.query(User).all()
    return [UserOut(**user.as_dict()) for user in users]


def update_user(session: Session, user_id, user_in: UserUpdate) -> Optional[UserOut]:
    """Update a user."""
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in user_in.dict().items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return UserOut.from_orm(user)


def delete_user(session: Session, username: str) -> None:
    """Delete a user."""
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return None
    session.delete(user)
    session.commit()
    return None
