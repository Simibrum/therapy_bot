"""Async CRUD functions for users."""
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_user_by_username_async(db_session: AsyncSession, username: str):
    """Get a user by username asynchronously."""
    result = await db_session.execute(select(User).filter(User.username == username))
    return result.scalars().first()
