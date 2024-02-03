"""Fixtures for models tests."""

import pytest

from models.graph.node import Node


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
