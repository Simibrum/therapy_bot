class TestPerson:
    def test_create_person(self, person):
        """Test creating a person."""
        assert person.id is not None
