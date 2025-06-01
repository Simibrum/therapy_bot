"""Fixtures for models tests."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from models.graph.node import Node

if TYPE_CHECKING:
    from models.user import User
    from sqlalchemy.orm import Session


@pytest.fixture()
def multiple_nodes(shared_session: Session, user_instance: User) -> list[Node]:
    """Return multiple nodes."""
    nodes = []
    for i in range(10):
        node = Node(label=f"test_label_{i}", user_id=user_instance.id, node_type="object")
        shared_session.add(node)
        nodes.append(node)
    shared_session.commit()
    return nodes
