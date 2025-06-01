"""Route for login."""
from datetime import timedelta

from database.db_engine import get_db
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session

from app.dependencies import manager, query_user
from app.schemas.pydantic_users import UserLogin, UserLoginOut

router = APIRouter()

# TODO - implement a version with short-lived access tokens and longer-lived refresh tokens
# Refresh tokens need login and are invalidated on logout; access tokens need a refresh token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
def login_json(
    user_login: UserLogin,
    session: Session = Depends(get_db),
):
    """Login endpoint that accepts JSON data."""
    return authenticate_user(user_login.username, user_login.password, session)


@router.post("/token")
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    """OAuth2 compatible token endpoint for Swagger UI."""
    return authenticate_user(form_data.username, form_data.password, session)


def authenticate_user(username: str, password: str, session: Session):
    """Common authentication logic."""
    if not username or not password:
        raise InvalidCredentialsException
    user = query_user(username, session)
    if not user or not (user.is_active and user.check_password(password)):
        raise InvalidCredentialsException
    access_token = manager.create_access_token(data={"sub": username}, expires=timedelta(hours=1))
    return UserLoginOut(
        access_token=access_token,
        token_type="bearer",  # nosec B106
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        is_active=user.is_active,
    )
