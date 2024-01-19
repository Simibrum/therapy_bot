"""Code for backend API."""

from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import manager
from app.routes.login import router as login_router
from app.routes.therapy_sessions import router as therapy_sessions_router
from app.schemas.pydantic_users import UserOut
from config import FRONTEND_URL
from models import User

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://192.168.32.3:3000",
    "http://192.168.32.2:3000",
    "http://172.29.0.3:3000",
    "http://172.29.0.2:3000",
    FRONTEND_URL
    # Add any other origins you might have
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex='https?://.*',  # TODO REMEMBER TO CHANGE THIS IN PRODUCTION
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor()

# Add the login router
app.include_router(login_router)
# Add the therapy sessions router
app.include_router(therapy_sessions_router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(manager)):
    """Return details of the current user."""
    if current_user.is_active:
        return UserOut.model_validate(current_user)
    else:
        # Return 403 Forbidden if the user is not active
        raise HTTPException(status_code=403, detail="User not found")
