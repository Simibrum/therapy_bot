"""Tests for the Organisation model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from models.chat_reference import ChatReference

if TYPE_CHECKING:
    from models.graph.node import Node
    from models.knowledge.organisation import Organisation
    from sqlalchemy.orm import Session


class TestOrganisation:
    """Test the Organisation model."""

    def test_create_organisation(self, organisation: Organisation) -> None:
        """Test creating an organisation."""
        assert organisation.id is not None

    def test_organisation_name(self, organisation: Organisation) -> None:
        """Test the organisation name."""
        assert organisation.name is not None
        assert isinstance(organisation.name, str)

    def test_organisation_relationships(
        self, organisation: Organisation, nodes_with_chats: list[Node], shared_session: Session
    ) -> None:
        """Test the organisation relationships."""
        assert nodes_with_chats is not None
        assert shared_session is not None
        # Check whether the organisation node has a chat
        assert organisation.node.chats is not None
        assert len(organisation.node.chats) > 0
        assert isinstance(organisation.node.chats[0], ChatReference)
        assert organisation.node.chats[0].id is not None
        assert organisation.node.chats[0].chat is not None
        assert organisation.node.chats[0].chat.text == "Hello, how are you?"
