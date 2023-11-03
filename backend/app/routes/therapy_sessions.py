"""Routes for Therapy Sessions."""
from fastapi import APIRouter, Depends, HTTPException
from starlette.websockets import WebSocket

from app.dependencies import manager
from app.main import app
from database import get_db
from sqlalchemy.orm import Session
from models import User, Therapist, TherapySession

router = APIRouter()


@router.post("/new_session/")
async def new_session(therapist_id: int, db: Session = Depends(get_db), current_user: User = Depends(manager)):

    therapist = db.query(Therapist).filter(Therapist.id == therapist_id).first()
    if not current_user or not therapist:
        raise HTTPException(status_code=404, detail="User or Therapist not found")

    new_therapy_session = TherapySession(user_id=current_user.id, therapist_id=therapist_id)
    db.add(new_therapy_session)
    db.commit()

    return {"session_id": new_therapy_session.id}


@app.websocket("/ws/session/{therapy_session_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        therapy_session_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(manager)):
    await websocket.accept()
    # Get the therapy session
    therapy_session = db.query(TherapySession).filter(TherapySession.id == therapy_session_id).first()
    if not therapy_session:
        raise HTTPException(status_code=404, detail="Therapy session not found")
    # Send initial therapist message
    await websocket.send_json({"therapist": "Hello! How can I help you today?"})
    while True:
        data = await websocket.receive_text()
        # Process user message and generate therapist response
        response = process_user_message(data)
        await websocket.send_json({"therapist": response})
