"""Test creating chat references."""

import pytest
from logic.process_chat_create_nodes import (
    process_text_and_create_references,  # Replace 'your_module' with the actual module name
)
from models.chat_reference import ChatReference
from models.graph.node import Node


def test_process_text_and_create_references_basic(test_nlp, user_instance, chat_instance, shared_session, mocker):
    # Mock the get_nodes function
    mock_get_nodes = mocker.patch(
        "logic.process_chat_create_nodes.get_nodes",
        return_value=[{"label": "Alice", "spans": [[0]]}, {"label": "London", "spans": [[3]]}],
    )

    text = "Alice went to London for vacation."
    result = process_text_and_create_references(
        text=text, chat_id=chat_instance.id, user_id=user_instance.id, db=shared_session, nlp=test_nlp
    )

    # Check that get_nodes was called with the correct doc
    mock_get_nodes.assert_called_once()
    assert mock_get_nodes.call_args[0][0].text == text

    # Check that the correct number of ChatReferences were created
    assert len(result) == 2

    # Check that the Nodes were created correctly
    nodes = shared_session.query(Node).all()
    assert len(nodes) == 2
    assert {node.label for node in nodes} == {"Alice", "London"}

    # Check that the ChatReferences were created correctly
    for chat_ref in result:
        assert chat_ref.chat_id == chat_instance.id
        assert chat_ref.node_id in [node.id for node in nodes]
        assert chat_ref.span_idx_start is not None
        assert chat_ref.span_idx_end is not None
        assert chat_ref.character_idx_start is not None
        assert chat_ref.character_idx_end is not None


def test_process_text_and_create_references_existing_node(
    test_nlp, user_instance, chat_instance, shared_session, mocker
):
    # Create an existing node
    existing_node = Node(label="Alice", user_id=user_instance.id)
    shared_session.add(existing_node)
    shared_session.commit()

    mocker.patch(
        "logic.process_chat_create_nodes.get_nodes",
        return_value=[{"label": "Alice", "spans": [[0]]}, {"label": "London", "spans": [[3]]}],
    )

    text = "Alice went to London again."
    result = process_text_and_create_references(
        text=text, chat_id=chat_instance.id, user_id=user_instance.id, db=shared_session, nlp=test_nlp
    )

    # Check that only one new Node was created
    nodes = shared_session.query(Node).all()
    assert len(nodes) == 2
    assert {node.label for node in nodes} == {"Alice", "London"}

    # Check that the existing node was reused
    alice_refs = [ref for ref in result if ref.node.label == "Alice"]
    assert len(alice_refs) == 1
    assert alice_refs[0].node_id == existing_node.id


def test_process_text_and_create_references_empty_text(test_nlp, user_instance, chat_instance, shared_session, mocker):
    mocker.patch("logic.process_chat_create_nodes.get_nodes", return_value=[])

    text = ""
    result = process_text_and_create_references(
        text=text, chat_id=chat_instance.id, user_id=user_instance.id, db=shared_session, nlp=test_nlp
    )

    assert len(result) == 0
    assert shared_session.query(Node).count() == 0
    assert shared_session.query(ChatReference).count() == 0


def test_process_text_and_create_references_multi_span(test_nlp, user_instance, chat_instance, shared_session, mocker):
    mocker.patch(
        "logic.process_chat_create_nodes.get_nodes",
        return_value=[{"label": "New York", "spans": [[0, 1]]}, {"label": "popular destination", "spans": [[3, 4]]}],
    )

    text = "New York is a popular destination for tourists."
    result = process_text_and_create_references(
        text=text, chat_id=chat_instance.id, user_id=user_instance.id, db=shared_session, nlp=test_nlp
    )

    assert len(result) == 2
    for chat_ref in result:
        if chat_ref.node.label == "New York":
            assert chat_ref.span_idx_start == 0
            assert chat_ref.span_idx_end == 1
        elif chat_ref.node.label == "popular destination":
            assert chat_ref.span_idx_start == 3
            assert chat_ref.span_idx_end == 4


def test_process_text_and_create_references_error_handling(
    test_nlp, user_instance, chat_instance, shared_session, mocker
):
    """Test that the function correctly handles errors and rolls back the session."""
    mocker.patch("logic.process_chat_create_nodes.get_nodes", return_value=[{"label": "Alice", "spans": [[0]]}])

    # Simulate a database error
    mocker.patch.object(shared_session, "commit", side_effect=Exception("Database error"))

    text = "Alice went to London."
    with pytest.raises(Exception, match="Database error"):
        process_text_and_create_references(
            text=text, chat_id=chat_instance.id, user_id=user_instance.id, db=shared_session, nlp=test_nlp
        )

    # Manually roll back the session to undo any uncommitted changes
    shared_session.rollback()

    # Check that no nodes or chat references were created due to the rollback
    assert shared_session.query(Node).count() == 0
    assert shared_session.query(ChatReference).count() == 0
