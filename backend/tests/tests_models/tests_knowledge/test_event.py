"""Tests for the Event model."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from models.chat_reference import ChatReference

if TYPE_CHECKING:
    from models.graph.node import Node
    from models.knowledge.event import Event


class TestEvent:
    """Test the Event model."""

    def test_create_event(self, event: Event) -> None:
        """Test creating an event."""
        assert event.id is not None

    def test_event_date(self, event: Event) -> None:
        """Test the event date."""
        assert event.date is not None
        assert isinstance(event.date, datetime)

    def test_event_relationships(self, event: Event, nodes_with_chats: list[Node]) -> None:
        """Test the event relationships."""
        assert nodes_with_chats is not None
        # Check whether the event node has a chat
        assert event.node.chats is not None
        assert len(event.node.chats) > 0
        assert isinstance(event.node.chats[0], ChatReference)
        assert event.node.chats[0].id is not None
        assert event.node.chats[0].chat is not None
        assert event.node.chats[0].chat.text == "Hello, how are you?"
