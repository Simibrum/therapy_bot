"""Tests for the therapists models."""
import pytest
from sqlalchemy.orm import sessionmaker
from models import Therapist, User


def test_therapist(db_setup, user_instance, therapist_instance):
    """Test the therapist model."""
    # db_setup fixture is automatically injected by pytest
    test_engine = db_setup
    # Create a new SQLAlchemy session
    Session = sessionmaker(bind=test_engine)
    session = Session()

    # Query the database to retrieve the therapist
    retrieved_therapist = session.query(Therapist).filter_by(id=therapist_instance.id).one()

    # Assert that the retrieved therapist's attributes match the original therapist's attributes
    assert retrieved_therapist.first_name == "Test"
    assert retrieved_therapist.last_name == "Therapist"
    assert retrieved_therapist.user_id == user_instance.id
    assert retrieved_therapist.residence == "Test City"
    assert retrieved_therapist.description == "Test Description"

    # Clean up by closing the session
    session.close()

# Usage
# Save this test in a file named test_your_module.py
# Run the test using the command: pytest test_your_module.py
