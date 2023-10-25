"""Dependencies for FastAPI app."""
from fastapi_login import LoginManager
from sqlalchemy.orm import Session
from database.db_engine import DBSessionManager

from config import SECRET_KEY
from app.crud.users import get_user_by_username

# Configure FASTAPI Login
manager = LoginManager(SECRET_KEY.encode("utf-8"), '/token', use_cookie=True, cookie_name='access_token')


@manager.user_loader(db_session=None)
def query_user(username: str, db_session: Session):
    """Query the user."""
    close = False
    if not db_session:
        close = True
        db_session = DBSessionManager.get_session()
    user = get_user_by_username(db_session, username)
    if close:
        db_session.close()
    return user
