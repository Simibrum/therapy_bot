class TestPlace:
    def test_create_place(self, place):
        """Test creating a place."""
        assert place.id is not None
