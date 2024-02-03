class TestEvent:
    def test_create_event(self, event):
        """Test creating an event."""
        assert event.id is not None
