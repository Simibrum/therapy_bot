"""Route for login."""
from datetime import timedelta

from database.db_engine import get_async_db
from fastapi import APIRouter, Depends
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.ext.asyncio import AsyncSession

from app.async_dependencies import async_query_user, manager
from app.schemas.pydantic_users import UserLogin, UserLoginOut

router = APIRouter()

# TODO - implement a version with short-lived access tokens and longer-lived refresh tokens
# Refresh tokens need login and are invalidated on logout; access tokens need a refresh token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
async def login(
    user_login: UserLogin,
    async_session: AsyncSession = Depends(get_async_db),
):
    """Authenticate a user and return a cookie."""
    username = user_login.username
    password = user_login.password
    if not username or not password:
        raise InvalidCredentialsException
    user = await async_query_user(username, async_session)
    if not user or not (user.is_active and user.check_password(password)):
        raise InvalidCredentialsException
    access_token = manager.create_access_token(data={"sub": username}, expires=timedelta(hours=1))
    return UserLoginOut(
        access_token=access_token,
        token_type="bearer",
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        is_active=user.is_active,
    )  # nosec: B106
