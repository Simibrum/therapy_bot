"""Test edge extraction in process_chat_create_nodes."""
from __future__ import annotations

import pytest
from logic.process_chat_create_nodes import (
    _create_edges,
    _create_or_get_node,
    _resolve_node_ref,
    process_text_and_create_references,
)
from models.graph.edge import Edge
from models.graph.node import Node


def test_create_or_get_node_new(shared_session, user_instance):
    """Test creating a new node when none exists."""
    node = _create_or_get_node(shared_session, "Alice", user_instance.id, "person")
    assert node.label == "Alice"
    assert node.type == "person"
    assert node.user_id == user_instance.id
    assert node.id is not None


def test_create_or_get_node_existing(shared_session, user_instance):
    """Test that an existing node is returned instead of creating a duplicate."""
    node1 = _create_or_get_node(shared_session, "Bob", user_instance.id, "person")
    shared_session.flush()
    node2 = _create_or_get_node(shared_session, "Bob", user_instance.id, "person")
    assert node1.id == node2.id


def test_create_or_get_node_updates_type(shared_session, user_instance):
    """Test that an existing node's type is updated if it was previously None."""
    node = _create_or_get_node(shared_session, "Carol", user_instance.id, None)
    shared_session.flush()
    assert node.type is None

    updated_node = _create_or_get_node(shared_session, "Carol", user_instance.id, "person")
    assert updated_node.id == node.id
    assert updated_node.type == "person"


def test_resolve_node_ref_by_id():
    """Test resolving a node reference by integer id."""
    mock_node = Node(label="Test", user_id=1)
    mock_node.id = 42
    node_by_id = {42: mock_node}
    node_by_label = {"test": mock_node}

    result = _resolve_node_ref(42, node_by_id, node_by_label)
    assert result is mock_node


def test_resolve_node_ref_by_label():
    """Test resolving a node reference by string label."""
    mock_node = Node(label="Test", user_id=1)
    mock_node.id = 42
    node_by_id = {42: mock_node}
    node_by_label = {"test": mock_node}

    result = _resolve_node_ref("Test", node_by_id, node_by_label)
    assert result is mock_node


def test_resolve_node_ref_case_insensitive():
    """Test that label resolution is case-insensitive."""
    mock_node = Node(label="Alice", user_id=1)
    mock_node.id = 1
    node_by_id = {1: mock_node}
    node_by_label = {"alice": mock_node}

    result = _resolve_node_ref("ALICE", node_by_id, node_by_label)
    assert result is mock_node


def test_resolve_node_ref_none():
    """Test that None input returns None."""
    result = _resolve_node_ref(None, {}, {})
    assert result is None


def test_resolve_node_ref_unknown():
    """Test that an unknown reference returns None."""
    result = _resolve_node_ref("Unknown", {}, {})
    assert result is None


def test_create_edges_basic(test_nlp, shared_session, user_instance, mocker):
    """Test basic edge creation between two nodes."""
    text = "Alice loves Bob."
    doc = test_nlp(text)

    # Create nodes in the DB
    node_alice = _create_or_get_node(shared_session, "Alice", user_instance.id, "person")
    node_bob = _create_or_get_node(shared_session, "Bob", user_instance.id, "person")
    shared_session.flush()

    # Mock get_edges to return a relationship
    mocker.patch(
        "logic.process_chat_create_nodes.get_edges",
        return_value=[
            {"source": node_alice.id, "target": node_bob.id, "label": "loves"},
        ],
    )

    edges = _create_edges(shared_session, doc, [node_alice, node_bob], user_instance.id)

    assert len(edges) == 1
    assert edges[0].from_node_id == node_alice.id
    assert edges[0].to_node_id == node_bob.id
    assert edges[0].type == "loves"
    assert edges[0].description == "Alice loves Bob"


def test_create_edges_with_label_refs(test_nlp, shared_session, user_instance, mocker):
    """Test edge creation when LLM returns string labels instead of IDs."""
    text = "Alice met Bob in London."
    doc = test_nlp(text)

    node_alice = _create_or_get_node(shared_session, "Alice", user_instance.id, "person")
    node_bob = _create_or_get_node(shared_session, "Bob", user_instance.id, "person")
    shared_session.flush()

    mocker.patch(
        "logic.process_chat_create_nodes.get_edges",
        return_value=[
            {"source": "Alice", "target": "Bob", "label": "met"},
        ],
    )

    edges = _create_edges(shared_session, doc, [node_alice, node_bob], user_instance.id)

    assert len(edges) == 1
    assert edges[0].from_node_id == node_alice.id
    assert edges[0].to_node_id == node_bob.id


def test_create_edges_skips_self_reference(test_nlp, shared_session, user_instance, mocker):
    """Test that edges from a node to itself are skipped."""
    text = "Alice knows Alice."
    doc = test_nlp(text)

    node_alice = _create_or_get_node(shared_session, "Alice", user_instance.id, "person")
    shared_session.flush()

    mocker.patch(
        "logic.process_chat_create_nodes.get_edges",
        return_value=[
            {"source": node_alice.id, "target": node_alice.id, "label": "knows"},
        ],
    )

    edges = _create_edges(shared_session, doc, [node_alice], user_instance.id)
    # Single node means less than 2, so should return early
    assert len(edges) == 0


def test_create_edges_skips_duplicates(test_nlp, shared_session, user_instance, mocker):
    """Test that duplicate edges are not created."""
    text = "Alice loves Bob."
    doc = test_nlp(text)

    node_alice = _create_or_get_node(shared_session, "Alice", user_instance.id, "person")
    node_bob = _create_or_get_node(shared_session, "Bob", user_instance.id, "person")
    shared_session.flush()

    # Create an existing edge
    existing_edge = Edge(
        user_id=user_instance.id,
        from_node_id=node_alice.id,
        to_node_id=node_bob.id,
        type="loves",
        description="Alice loves Bob",
    )
    shared_session.add(existing_edge)
    shared_session.flush()

    mocker.patch(
        "logic.process_chat_create_nodes.get_edges",
        return_value=[
            {"source": node_alice.id, "target": node_bob.id, "label": "loves"},
        ],
    )

    edges = _create_edges(shared_session, doc, [node_alice, node_bob], user_instance.id)
    assert len(edges) == 0  # No new edges created


def test_create_edges_fewer_than_two_nodes(test_nlp, shared_session, user_instance):
    """Test that edge extraction is skipped when fewer than 2 nodes exist."""
    text = "Alice is here."
    doc = test_nlp(text)

    node_alice = _create_or_get_node(shared_session, "Alice", user_instance.id, "person")
    shared_session.flush()

    edges = _create_edges(shared_session, doc, [node_alice], user_instance.id)
    assert len(edges) == 0


def test_create_edges_handles_llm_error(test_nlp, shared_session, user_instance, mocker):
    """Test that edge creation handles LLM errors gracefully."""
    text = "Alice loves Bob."
    doc = test_nlp(text)

    node_alice = _create_or_get_node(shared_session, "Alice", user_instance.id, "person")
    node_bob = _create_or_get_node(shared_session, "Bob", user_instance.id, "person")
    shared_session.flush()

    mocker.patch(
        "logic.process_chat_create_nodes.get_edges",
        side_effect=Exception("LLM API Error"),
    )

    edges = _create_edges(shared_session, doc, [node_alice, node_bob], user_instance.id)
    assert len(edges) == 0


def test_create_edges_handles_empty_response(test_nlp, shared_session, user_instance, mocker):
    """Test that empty edge data is handled."""
    text = "Alice and Bob are here."
    doc = test_nlp(text)

    node_alice = _create_or_get_node(shared_session, "Alice", user_instance.id, "person")
    node_bob = _create_or_get_node(shared_session, "Bob", user_instance.id, "person")
    shared_session.flush()

    mocker.patch(
        "logic.process_chat_create_nodes.get_edges",
        return_value=[],
    )

    edges = _create_edges(shared_session, doc, [node_alice, node_bob], user_instance.id)
    assert len(edges) == 0


def test_process_text_creates_edges(test_nlp, user_instance, chat_instance, shared_session, mocker):
    """Test that the full flow creates both nodes and edges."""
    mocker.patch(
        "logic.process_chat_create_nodes.get_nodes",
        return_value=[
            {"label": "Alice", "type": "person", "spans": [[0]]},
            {"label": "London", "type": "place", "spans": [[3]]},
        ],
    )
    mocker.patch(
        "logic.process_chat_create_nodes.get_edges",
        return_value=[
            {"source": "Alice", "target": "London", "label": "visited"},
        ],
    )

    text = "Alice went to London for vacation."
    process_text_and_create_references(
        text=text, chat_id=chat_instance.id, user_id=user_instance.id, db=shared_session, nlp=test_nlp
    )

    # Check nodes were created
    nodes = shared_session.query(Node).all()
    assert len(nodes) == 2

    # Check edges were created
    edges = shared_session.query(Edge).all()
    assert len(edges) == 1
    assert edges[0].type == "visited"


def test_process_text_no_edges_with_single_node(test_nlp, user_instance, chat_instance, shared_session, mocker):
    """Test that edge extraction is skipped when only one node is found."""
    mocker.patch(
        "logic.process_chat_create_nodes.get_nodes",
        return_value=[{"label": "Alice", "spans": [[0]]}],
    )
    mock_get_edges = mocker.patch("logic.process_chat_create_nodes.get_edges")

    text = "Alice is happy."
    process_text_and_create_references(
        text=text, chat_id=chat_instance.id, user_id=user_instance.id, db=shared_session, nlp=test_nlp
    )

    # get_edges should not be called when there's only one node
    mock_get_edges.assert_not_called()


def test_process_text_node_types_are_saved(test_nlp, user_instance, chat_instance, shared_session, mocker):
    """Test that node types from LLM response are saved."""
    mocker.patch(
        "logic.process_chat_create_nodes.get_nodes",
        return_value=[
            {"label": "Alice", "type": "person", "spans": [[0]]},
            {"label": "London", "type": "place", "spans": [[3]]},
        ],
    )
    mocker.patch(
        "logic.process_chat_create_nodes.get_edges",
        return_value=[],
    )

    text = "Alice went to London for vacation."
    process_text_and_create_references(
        text=text, chat_id=chat_instance.id, user_id=user_instance.id, db=shared_session, nlp=test_nlp
    )

    nodes = shared_session.query(Node).all()
    node_types = {n.label: n.type for n in nodes}
    assert node_types["Alice"] == "person"
    assert node_types["London"] == "place"
