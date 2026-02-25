"""Test knowledge graph API endpoints."""
from __future__ import annotations

from models.chat_reference import ChatReference
from models.graph.edge import Edge
from models.graph.node import Node


def test_get_session_entities_unauthenticated(test_client, user_instance):
    """Test that unauthenticated users cannot access session entities."""
    response = test_client.get("/knowledge-graph/sessions/1/entities")
    assert response.status_code == 401


def test_get_session_entities_not_found(authenticated_test_client, user_instance):
    """Test 404 when session does not exist."""
    response = authenticated_test_client.get("/knowledge-graph/sessions/9999/entities")
    assert response.status_code == 404


def test_get_session_entities_empty(authenticated_test_client, therapy_session_instance):
    """Test getting entities for a session with no entities."""
    response = authenticated_test_client.get(
        f"/knowledge-graph/sessions/{therapy_session_instance.id}/entities"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == therapy_session_instance.id
    assert data["entities"] == []


def test_get_session_entities_with_data(
    authenticated_test_client, shared_session, user_instance, chat_instance, therapy_session_instance
):
    """Test getting entities when nodes and chat references exist."""
    # Create a node and chat reference
    node = Node(label="Alice", user_id=user_instance.id, node_type="person")
    shared_session.add(node)
    shared_session.flush()

    chat_ref = ChatReference(
        chat_id=chat_instance.id,
        node_id=node.id,
        span_idx_start=0,
        span_idx_end=0,
        character_idx_start=0,
        character_idx_end=5,
    )
    shared_session.add(chat_ref)
    shared_session.commit()

    response = authenticated_test_client.get(
        f"/knowledge-graph/sessions/{therapy_session_instance.id}/entities"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == therapy_session_instance.id
    assert len(data["entities"]) == 1
    assert data["entities"][0]["label"] == "Alice"
    assert data["entities"][0]["type"] == "person"


def test_get_session_edges_unauthenticated(test_client, user_instance):
    """Test that unauthenticated users cannot access session edges."""
    response = test_client.get("/knowledge-graph/sessions/1/edges")
    assert response.status_code == 401


def test_get_session_edges_not_found(authenticated_test_client, user_instance):
    """Test 404 when session does not exist."""
    response = authenticated_test_client.get("/knowledge-graph/sessions/9999/edges")
    assert response.status_code == 404


def test_get_session_edges_empty(authenticated_test_client, therapy_session_instance):
    """Test getting edges for a session with no edges."""
    response = authenticated_test_client.get(
        f"/knowledge-graph/sessions/{therapy_session_instance.id}/edges"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == therapy_session_instance.id
    assert data["edges"] == []


def test_get_session_edges_with_data(
    authenticated_test_client, shared_session, user_instance, chat_instance, therapy_session_instance
):
    """Test getting edges when nodes, edges, and chat references exist."""
    # Create nodes
    node_alice = Node(label="Alice", user_id=user_instance.id, node_type="person")
    node_bob = Node(label="Bob", user_id=user_instance.id, node_type="person")
    shared_session.add_all([node_alice, node_bob])
    shared_session.flush()

    # Create chat references for both nodes
    for node in [node_alice, node_bob]:
        chat_ref = ChatReference(
            chat_id=chat_instance.id,
            node_id=node.id,
            span_idx_start=0,
            span_idx_end=0,
            character_idx_start=0,
            character_idx_end=5,
        )
        shared_session.add(chat_ref)

    # Create an edge between them
    edge = Edge(
        user_id=user_instance.id,
        from_node_id=node_alice.id,
        to_node_id=node_bob.id,
        type="knows",
        description="Alice knows Bob",
    )
    shared_session.add(edge)
    shared_session.commit()

    response = authenticated_test_client.get(
        f"/knowledge-graph/sessions/{therapy_session_instance.id}/edges"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == therapy_session_instance.id
    assert len(data["edges"]) == 1
    assert data["edges"][0]["type"] == "knows"
    assert data["edges"][0]["from_node_id"] == node_alice.id
    assert data["edges"][0]["to_node_id"] == node_bob.id


def test_get_knowledge_graph_unauthenticated(test_client, user_instance):
    """Test that unauthenticated users cannot access the knowledge graph."""
    response = test_client.get("/knowledge-graph")
    assert response.status_code == 401


def test_get_knowledge_graph_empty(authenticated_test_client, user_instance):
    """Test getting an empty knowledge graph."""
    response = authenticated_test_client.get("/knowledge-graph")
    assert response.status_code == 200
    data = response.json()
    assert data["nodes"] == []
    assert data["edges"] == []


def test_get_knowledge_graph_with_data(authenticated_test_client, shared_session, user_instance):
    """Test getting the full knowledge graph with nodes and edges."""
    # Create nodes
    node1 = Node(label="Alice", user_id=user_instance.id, node_type="person")
    node2 = Node(label="Bob", user_id=user_instance.id, node_type="person")
    shared_session.add_all([node1, node2])
    shared_session.flush()

    # Create edge
    edge = Edge(
        user_id=user_instance.id,
        from_node_id=node1.id,
        to_node_id=node2.id,
        type="knows",
        description="Alice knows Bob",
    )
    shared_session.add(edge)
    shared_session.commit()

    response = authenticated_test_client.get("/knowledge-graph")
    assert response.status_code == 200
    data = response.json()
    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1
    labels = {n["label"] for n in data["nodes"]}
    assert labels == {"Alice", "Bob"}


def test_batch_process_unauthenticated(test_client, user_instance):
    """Test that unauthenticated users cannot trigger batch processing."""
    response = test_client.post("/knowledge-graph/process")
    assert response.status_code == 401


def test_batch_process_no_unprocessed_chats(
    authenticated_test_client, shared_session, user_instance, chat_instance, mocker
):
    """Test batch processing when all chats already have references."""
    # Create a chat reference so the chat is already processed
    node = Node(label="Test", user_id=user_instance.id)
    shared_session.add(node)
    shared_session.flush()
    chat_ref = ChatReference(
        chat_id=chat_instance.id,
        node_id=node.id,
        span_idx_start=0,
        span_idx_end=0,
        character_idx_start=0,
        character_idx_end=4,
    )
    shared_session.add(chat_ref)
    shared_session.commit()

    # Mock the NLP service
    mocker.patch("app.routes.knowledge_graph.nlp_service.get_nlp")

    response = authenticated_test_client.post("/knowledge-graph/process")
    assert response.status_code == 200
    data = response.json()
    assert data["processed_chats"] == 0


def test_batch_process_with_unprocessed_chats(
    authenticated_test_client, shared_session, user_instance, chat_instance, test_nlp, mocker
):
    """Test batch processing processes unprocessed chats."""
    # Mock the NLP service to return our test_nlp
    mocker.patch("app.routes.knowledge_graph.nlp_service.get_nlp", return_value=test_nlp)

    # Mock the LLM calls
    mocker.patch(
        "logic.process_chat_create_nodes.get_nodes",
        return_value=[{"label": "TestEntity", "spans": [[0]]}],
    )
    mocker.patch(
        "logic.process_chat_create_nodes.get_edges",
        return_value=[],
    )

    response = authenticated_test_client.post("/knowledge-graph/process")
    assert response.status_code == 200
    data = response.json()
    assert data["processed_chats"] == 1
    assert data["nodes_created"] >= 1


def test_batch_process_nlp_unavailable(authenticated_test_client, user_instance, mocker):
    """Test batch processing when NLP service is unavailable."""
    mocker.patch(
        "app.routes.knowledge_graph.nlp_service.get_nlp",
        side_effect=OSError("Model not found"),
    )

    response = authenticated_test_client.post("/knowledge-graph/process")
    assert response.status_code == 503
    assert "NLP service" in response.json()["detail"]
