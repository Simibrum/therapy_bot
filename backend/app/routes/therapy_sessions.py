"""Routes for Therapy Sessions."""
from typing import Union

from config import logger
from database import get_async_db
from fastapi import APIRouter, Depends, HTTPException, status
from logic.therapy_session_logic import TherapySessionLogic
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from app.async_dependencies import manager
from app.schemas.pydantic_therapy_sessions import TherapySessionListOut

router = APIRouter()


async def verify_token(token: str) -> Union[User, None]:
    """Verify the token and return the user."""
    user = await manager.get_current_user(token)
    return user


@router.get("/sessions")
async def get_sessions(
    session: AsyncSession = Depends(get_async_db), current_user: User = Depends(manager)
) -> TherapySessionListOut:
    """Get all therapy sessions for the current user."""
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Add the user to the session
    session.add(current_user)
    # Get all therapy sessions for the current user
    await session.refresh(current_user, ["therapy_sessions"])
    # Get all therapy sessions for the current user
    return TherapySessionListOut(sessions=current_user.therapy_sessions)


@router.post("/sessions/new")
async def new_session(current_user: User = Depends(manager)):
    """Create a new therapy session."""
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Create a new therapy session using the logic module
    new_therapy_session = TherapySessionLogic(user_id=current_user.id)
    return {"session_id": new_therapy_session.therapy_session_id}


@router.websocket("/ws/session/{therapy_session_id}")
async def websocket_endpoint(websocket: WebSocket, therapy_session_id: int):
    """Websocket endpoint for the therapy session."""
    await websocket.accept()
    try:
        logger.info("Waiting for token")
        token_json = await websocket.receive_json()
        token = token_json.get("access_token")
        if token:
            logger.info("Token received - validating user")
            current_user = verify_token(token)
        else:
            logger.info("No token received")
            current_user = None
        if not current_user:
            logger.info("Token invalid - closing websocket")
            await websocket.send_text("Invalid token")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        else:
            logger.info("Token valid - sending confirmation")
            await websocket.send_text("Valid token")

        logger.info("Getting initial messages")
        # Get the therapy session - TODO needs to be async
        therapy_session = TherapySessionLogic(pre_existing_session_id=therapy_session_id)
        if not therapy_session:
            await websocket.send_text("No therapy session found")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        # Get existing or initial chat messages  - TODO needs to be async
        messages_to_send = therapy_session.get_messages()
        # Send initial therapist message
        await websocket.send_json(messages_to_send.model_dump(mode="json"))

        while True:
            logger.info("Entering Chat While Loop - Waiting for message")
            data = await websocket.receive_json()
            user_text = data.get("message")
            # Process user message and generate therapist response - TODO needs to be async
            messages_to_send = therapy_session.generate_response(user_text)
            # Send therapist response
            await websocket.send_json(messages_to_send.model_dump(mode="json"))
    except WebSocketDisconnect:
        pass
    finally:
        if (
            websocket.application_state == WebSocketState.CONNECTED
            and websocket.client_state == WebSocketState.CONNECTED
        ):
            await websocket.close()
