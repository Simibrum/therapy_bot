"""Fixtures for testing graph models."""

import pytest

from models.graph.node import Node


@pytest.fixture()
def node(shared_session):
    """Return a node."""
    node = Node("test_label")
    shared_session.add(node)
    shared_session.commit()
    return node
