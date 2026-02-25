"""Logic to process chat text data to generate knowledge graph representations."""
from __future__ import annotations

from typing import TYPE_CHECKING

from config import logger
from llm.graph_processing import get_edges, get_nodes
from models.chat_reference import ChatReference
from models.graph.edge import Edge
from models.graph.node import Node
from sqlalchemy.exc import SQLAlchemyError

if TYPE_CHECKING:
    import spacy
    from sqlalchemy.orm import Session


def _create_or_get_node(db: Session, label: str, user_id: int, node_type: str | None = None) -> Node:
    """Find an existing node by label and user_id, or create a new one."""
    db_node = db.query(Node).filter_by(label=label, user_id=user_id).first()
    if not db_node:
        db_node = Node(label=label, user_id=user_id, node_type=node_type)
        db.add(db_node)
        db.flush()  # This will populate the id of the new node
    elif node_type and not db_node.type:
        # Update type if the existing node doesn't have one yet
        db_node.type = node_type
        db.flush()
    return db_node


def _create_chat_references(
    db: Session, doc: spacy.tokens.Doc, node_data: list[dict], chat_id: int, user_id: int
) -> tuple[list[ChatReference], list[Node]]:
    """Create nodes and chat references from extracted node data."""
    chat_references = []
    created_nodes = []

    for node in node_data:
        try:
            node_type = node.get("type")
            db_node = _create_or_get_node(db, node["label"], user_id, node_type)
            created_nodes.append(db_node)

            # Create ChatReference for each span
            for span in node["spans"]:
                chat_ref = ChatReference(
                    chat_id=chat_id,
                    node_id=db_node.id,
                    span_idx_start=span[0],
                    span_idx_end=span[-1],
                    character_idx_start=doc[span[0]].idx,
                    character_idx_end=doc[span[-1]].idx + len(doc[span[-1]]),
                )
                db.add(chat_ref)
                chat_references.append(chat_ref)

        except SQLAlchemyError:
            db.rollback()
            raise

    return chat_references, created_nodes


def _create_edges(db: Session, doc: spacy.tokens.Doc, nodes: list[Node], user_id: int) -> list[Edge]:
    """Extract and create edges between nodes."""
    if len(nodes) < 2:
        return []

    node_dicts = [{"label": node.label, "id": node.id, "type": node.type} for node in nodes]

    try:
        edge_data = get_edges(doc, node_dicts)
    except Exception:
        logger.exception("Failed to extract edges from LLM")
        return []

    if not edge_data or isinstance(edge_data, dict):
        return []

    edges = []
    # Build a lookup from node id to Node object
    node_by_id = {node.id: node for node in nodes}
    # Build a lookup from label to Node object
    node_by_label = {node.label.lower(): node for node in nodes}

    for edge_item in edge_data:
        source_ref = edge_item.get("source")
        target_ref = edge_item.get("target")
        label = edge_item.get("label", "related_to")

        # Resolve source and target - could be id (int) or label (str)
        source_node = _resolve_node_ref(source_ref, node_by_id, node_by_label)
        target_node = _resolve_node_ref(target_ref, node_by_id, node_by_label)

        if source_node and target_node and source_node.id != target_node.id:
            # Check if edge already exists
            existing_edge = (
                db.query(Edge)
                .filter_by(
                    from_node_id=source_node.id,
                    to_node_id=target_node.id,
                    user_id=user_id,
                    type=label,
                )
                .first()
            )
            if not existing_edge:
                edge = Edge(
                    user_id=user_id,
                    from_node_id=source_node.id,
                    to_node_id=target_node.id,
                    type=label,
                    description=f"{source_node.label} {label} {target_node.label}",
                )
                db.add(edge)
                edges.append(edge)

    return edges


def _resolve_node_ref(
    ref: int | str | None, node_by_id: dict[int, Node], node_by_label: dict[str, Node]
) -> Node | None:
    """Resolve a node reference which could be an id or a label string."""
    if ref is None:
        return None
    if isinstance(ref, int):
        return node_by_id.get(ref)
    if isinstance(ref, str):
        return node_by_label.get(ref.lower())
    return None


def process_text_and_create_references(
    text: str, chat_id: int, user_id: int, db: Session, nlp: spacy.language.Language
) -> list[ChatReference]:
    """Process the text and create ChatReferences, Nodes, and Edges in the database."""
    # Generate Spacy doc
    doc = nlp(text)

    # Get nodes from the doc
    node_data = get_nodes(doc)

    # Create nodes and chat references
    chat_references, created_nodes = _create_chat_references(db, doc, node_data, chat_id, user_id)

    # Create edges between nodes
    edges = _create_edges(db, doc, created_nodes, user_id)
    if edges:
        logger.debug("Created %d edges for chat %d", len(edges), chat_id)

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    return chat_references
