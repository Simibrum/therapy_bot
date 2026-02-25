"""Pydantic schemas for knowledge graph API responses."""

from __future__ import annotations

from pydantic import BaseModel

from app.schemas.pydantic_edges import EdgeOut
from app.schemas.pydantic_nodes import NodeOut


class SessionEntitiesOut(BaseModel):
    """Response schema for session entities."""

    session_id: int
    entities: list[NodeOut]


class SessionEdgesOut(BaseModel):
    """Response schema for session edges."""

    session_id: int
    edges: list[EdgeOut]


class KnowledgeGraphOut(BaseModel):
    """Full knowledge graph for a user across all sessions."""

    nodes: list[NodeOut]
    edges: list[EdgeOut]


class BatchProcessingOut(BaseModel):
    """Response schema for batch processing."""

    processed_chats: int
    nodes_created: int
    edges_created: int
