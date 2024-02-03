"""Fixtures for testing knowledge models."""
from datetime import datetime

import pytest

from models.knowledge.event import Event
from models.knowledge.person import Person
from models.knowledge.place import Place


@pytest.fixture
def person(shared_session, multiple_nodes):
    """Return a person."""
    person = Person(node_id=multiple_nodes[0].id, user_id=multiple_nodes[0].user_id)
    shared_session.add(person)
    shared_session.commit()
    return person


@pytest.fixture
def event(shared_session, multiple_nodes):
    """Return an event."""
    event = Event(
        node_id=multiple_nodes[0].id,
        user_id=multiple_nodes[0].user_id,
        date=datetime.now(),
    )
    shared_session.add(event)
    shared_session.commit()
    return event


@pytest.fixture
def place(shared_session, multiple_nodes):
    """Return a place."""
    place = Place(node_id=multiple_nodes[0].id, user_id=multiple_nodes[0].user_id)
    shared_session.add(place)
    shared_session.commit()
    return place
