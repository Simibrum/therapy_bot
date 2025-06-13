"""Dependencies for FastAPI app."""
from __future__ import annotations

from typing import TYPE_CHECKING

from config import SECRET_KEY
from database.db_engine import DBSessionManager
from fastapi_login import LoginManager

from app.crud.users import get_user_by_username

if TYPE_CHECKING:
    from models import User
    from sqlalchemy.orm import Session

# Configure FASTAPI Login
manager = LoginManager(SECRET_KEY.encode("utf-8"), "/token", use_cookie=False)


@manager.user_loader(db_session=None)
def query_user(username: str, db_session: Session) -> User | None:
    """Query the user."""
    close = False
    if not db_session:
        close = True
        db_session = DBSessionManager.get_session()
    user = get_user_by_username(db_session, username)
    if close:
        db_session.close()
    return user
