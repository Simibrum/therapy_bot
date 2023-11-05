"""Routes for Therapy Sessions."""
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.websockets import WebSocket

from config import logger
from app.dependencies import manager, query_user
from models import User
from logic.therapy_session_logic import TherapySessionLogic

router = APIRouter()


def verify_token(token: str) -> Union[User, None]:
    """Verify the token and return the user."""
    user = manager.get_current_user(token)
    return user


@router.post("/new_session/")
async def new_session(current_user: User = Depends(manager)):
    """Create a new therapy session."""
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Create a new therapy session using the logic module
    new_therapy_session = TherapySessionLogic(user_id=current_user.id)
    return {"session_id": new_therapy_session.therapy_session_id}


@router.websocket("/ws/session/{therapy_session_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        therapy_session_id: int
):
    """Websocket endpoint for the therapy session."""
    await websocket.accept()

    token_json = await websocket.receive_json()
    token = token_json.get("access_token")
    if token:
        logger.info("Token received")
        current_user = verify_token(token)
    else:
        logger.info("No token received")
        current_user = None
    if not current_user:
        await websocket.send_text("Invalid token")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    else:
        await websocket.send_text("Valid token")

    # while True:
    #     # Get the therapy session - TODO needs to be async
    #     therapy_session = TherapySessionLogic(pre_existing_session_id=therapy_session_id)
    #     if not therapy_session:
    #         raise HTTPException(status_code=404, detail="Therapy session not found")
    #     # Get existing or initial chat messages  - TODO needs to be async
    #     messages_to_send = therapy_session.get_messages()
    #     # Send initial therapist message
    #     await websocket.send_json(messages_to_send)
    #
    #     data = await websocket.receive_text()
    #     # Process user message and generate therapist response - TODO needs to be async
    #     chat_out = therapy_session.generate_response(data)
    #     # Send therapist response
    #     await websocket.send_json(chat_out)

