"""Fixtures for testing knowledge models."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import pytest
from config import TZ_INFO
from models.chat_reference import ChatReference
from models.knowledge.event import Event
from models.knowledge.person import Person
from models.knowledge.place import Place

if TYPE_CHECKING:
    from models.chat import Chat
    from models.graph.node import Node
    from sqlalchemy.orm import Session


@pytest.fixture()
def person(shared_session: Session, multiple_nodes: list[Node]) -> Person:
    """Return a person."""
    person = Person(node_id=multiple_nodes[0].id, user_id=multiple_nodes[0].user_id)
    shared_session.add(person)
    shared_session.commit()
    return person


@pytest.fixture()
def event(shared_session: Session, multiple_nodes: list[Node]) -> Event:
    """Return an event."""
    event = Event(
        node_id=multiple_nodes[0].id,
        user_id=multiple_nodes[0].user_id,
        date=datetime.now(TZ_INFO),
    )
    shared_session.add(event)
    shared_session.commit()
    return event


@pytest.fixture()
def place(shared_session: Session, multiple_nodes: list[Node]) -> Place:
    """Return a place."""
    place = Place(node_id=multiple_nodes[0].id, user_id=multiple_nodes[0].user_id)
    shared_session.add(place)
    shared_session.commit()
    return place


@pytest.fixture()
def nodes_with_chats(shared_session: Session, multiple_nodes: list[Node], chat_instance: Chat) -> list[Node]:
    """Return nodes with chats."""
    shared_session.add(chat_instance)
    for node in multiple_nodes:
        chat_reference = ChatReference(chat=chat_instance, node=node)
        shared_session.add(chat_reference)
        node.chats.append(chat_reference)
        shared_session.add(node)
    shared_session.commit()
    return multiple_nodes
