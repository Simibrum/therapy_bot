"""Fixtures for models tests."""
from __future__ import annotations

import pytest

from models.graph.node import Node


@pytest.fixture()
def multiple_nodes(shared_session, user_instance) -> list[Node]:
    """Return multiple nodes."""
    nodes = []
    for i in range(10):
        node = Node(label=f"test_label_{i}", user_id=user_instance.id)
        shared_session.add(node)
        nodes.append(node)
    shared_session.commit()
    return nodes
