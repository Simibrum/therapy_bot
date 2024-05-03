"""Package to store different forms of knowledge relating to a person.

Initially there are three main "things":
* people
* places
* events

This package will contain the models for these different forms of knowledge.

There is a common base class for all knowledge models, which is the `Common` class.
"""

from models.knowledge.event import Event
from models.knowledge.person import Person
from models.knowledge.place import Place

__all__ = [
    "Person",
    "Place",
    "Event",
]
