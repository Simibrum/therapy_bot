"""Routes for Knowledge Graph API."""
from __future__ import annotations

from typing import TYPE_CHECKING

from config import logger
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Chat, ChatReference, Edge, Node, TherapySession, User
from sqlalchemy import select
from spacy_nlp import nlp_service

from app.dependencies import manager
from app.schemas.pydantic_graph import (
    BatchProcessingOut,
    KnowledgeGraphOut,
    SessionEdgesOut,
    SessionEntitiesOut,
)

if TYPE_CHECKING:
    import spacy
    from sqlalchemy.orm import Session

router = APIRouter(prefix="/knowledge-graph", tags=["knowledge-graph"])


def _verify_session_ownership(db: Session, session_id: int, user_id: int) -> TherapySession:
    """Verify that a therapy session belongs to the user."""
    therapy_session = (
        db.query(TherapySession)
        .filter(TherapySession.id == session_id, TherapySession.user_id == user_id)
        .first()
    )
    if not therapy_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return therapy_session


@router.get("/sessions/{session_id}/entities", response_model=SessionEntitiesOut)
def get_session_entities(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(manager)
) -> SessionEntitiesOut:
    """Get extracted entities (nodes) for a therapy session."""
    _verify_session_ownership(db, session_id, current_user.id)

    chat_ids_q = select(Chat.id).where(Chat.therapy_session_id == session_id)
    entities = (
        db.query(Node)
        .join(ChatReference)
        .filter(ChatReference.chat_id.in_(chat_ids_q))
        .distinct()
        .all()
    )

    return SessionEntitiesOut(session_id=session_id, entities=entities)


@router.get("/sessions/{session_id}/edges", response_model=SessionEdgesOut)
def get_session_edges(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(manager)
) -> SessionEdgesOut:
    """Get extracted edges (relationships) for a therapy session."""
    _verify_session_ownership(db, session_id, current_user.id)

    # Get node IDs that belong to this session via chat references
    chat_ids_q = select(Chat.id).where(Chat.therapy_session_id == session_id)
    node_ids_q = (
        select(ChatReference.node_id)
        .where(ChatReference.chat_id.in_(chat_ids_q))
        .distinct()
    )

    # Get edges where both from_node and to_node are in the session's node set
    edges = (
        db.query(Edge)
        .filter(
            Edge.from_node_id.in_(node_ids_q),
            Edge.to_node_id.in_(node_ids_q),
            Edge.user_id == current_user.id,
        )
        .all()
    )

    return SessionEdgesOut(session_id=session_id, edges=edges)


@router.get("", response_model=KnowledgeGraphOut)
def get_user_knowledge_graph(
    db: Session = Depends(get_db), current_user: User = Depends(manager)
) -> KnowledgeGraphOut:
    """Get the full knowledge graph for the current user across all sessions."""
    nodes = db.query(Node).filter(Node.user_id == current_user.id).all()
    edges = db.query(Edge).filter(Edge.user_id == current_user.id).all()

    return KnowledgeGraphOut(nodes=nodes, edges=edges)


def _process_single_chat(chat: Chat, user_id: int, db: Session, nlp: spacy.language.Language) -> int:
    """Process a single chat message for entity/edge extraction. Returns 1 on success, 0 on failure."""
    from logic.process_chat_create_nodes import process_text_and_create_references

    try:
        process_text_and_create_references(
            text=chat.text, chat_id=chat.id, user_id=user_id, db=db, nlp=nlp
        )
    except Exception:
        logger.exception("Failed to process chat %d during batch processing", chat.id)
        db.rollback()
        return 0
    return 1


@router.post("/process", response_model=BatchProcessingOut)
def batch_process_chats(
    db: Session = Depends(get_db), current_user: User = Depends(manager)
) -> BatchProcessingOut:
    """Process all existing chat messages for the current user to build the knowledge graph.

    This is useful for retroactively extracting entities and relationships from
    chat history that was created before the knowledge graph feature was enabled.
    """
    try:
        nlp = nlp_service.get_nlp()
    except OSError:
        logger.error("Failed to load NLP service for batch processing")
        raise HTTPException(
            status_code=503, detail="NLP service is not available."
        ) from None

    # Count existing nodes/edges before processing
    nodes_before = db.query(Node).filter(Node.user_id == current_user.id).count()
    edges_before = db.query(Edge).filter(Edge.user_id == current_user.id).count()

    # Get all user chats that don't already have chat references
    chats_with_refs_q = select(ChatReference.chat_id).distinct()
    unprocessed_chats = (
        db.query(Chat)
        .filter(
            Chat.user_id == current_user.id,
            Chat.sender == "user",
            ~Chat.id.in_(chats_with_refs_q),
        )
        .order_by(Chat.timestamp.asc())
        .all()
    )

    processed_count = 0
    for chat in unprocessed_chats:
        processed_count += _process_single_chat(chat, current_user.id, db, nlp)

    nodes_after = db.query(Node).filter(Node.user_id == current_user.id).count()
    edges_after = db.query(Edge).filter(Edge.user_id == current_user.id).count()

    return BatchProcessingOut(
        processed_chats=processed_count,
        nodes_created=nodes_after - nodes_before,
        edges_created=edges_after - edges_before,
    )
