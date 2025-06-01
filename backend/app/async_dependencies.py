"""Async dependencies for FastAPI."""
from config import SECRET_KEY
from database.db_engine import DBSessionManager
from fastapi_login import LoginManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.async_users import get_user_by_username_async

# Configure FASTAPI Login
manager = LoginManager(SECRET_KEY.encode("utf-8"), "/token", use_cookie=False)


@manager.user_loader()
async def async_query_user(username: str, async_session: AsyncSession = None):
    """Query the user asynchronously."""
    if not async_session:
        async with DBSessionManager.get_async_session() as async_session:
            user = await get_user_by_username_async(async_session, username)
    else:
        user = await get_user_by_username_async(async_session, username)
    return user
