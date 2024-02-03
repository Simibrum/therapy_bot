"""Fixtures for testing graph models."""

import pytest

from models.graph.node import Node


@pytest.fixture
def node(shared_session):
    """Return a node."""
    node = Node("test_label")
    shared_session.add(node)
    shared_session.commit()
    return node


@pytest.fixture
def multiple_nodes(shared_session, user_instance):
    """Return multiple nodes."""
    nodes = []
    for i in range(10):
        node = Node(label="test_label_{i}", user_id=user_instance.id)
        shared_session.add(node)
        nodes.append(node)
    shared_session.commit()
    return nodes
