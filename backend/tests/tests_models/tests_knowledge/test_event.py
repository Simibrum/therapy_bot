"""Tests for the Event model."""

from models.knowledge.event import Event


class TestEvent:
    """Test the Event model."""

    def test_create_event(self, event: Event) -> None:
        """Test creating an event."""
        assert event.id is not None
