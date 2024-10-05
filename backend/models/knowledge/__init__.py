"""Package to store different forms of knowledge relating to a person.

Initially there are three main "things":
* people
* places
* events

This package will contain the models for these different forms of knowledge.

There is a common base class for all knowledge models, which is the `Common` class.

en_core_web_trf in spacy has the following entity types
('CARDINAL', 'DATE', 'EVENT', 'FAC', 'GPE', 'LANGUAGE', 'LAW', 'LOC', 'MONEY', 'NORP', 'ORDINAL',
'ORG', 'PERCENT', 'PERSON', 'PRODUCT', 'QUANTITY', 'TIME', 'WORK_OF_ART')

CARDINAL: Numerals that do not fall under another type
DATE: Absolute or relative dates or periods
EVENT: Named hurricanes, battles, wars, sports events, etc.
FAC: Buildings, airports, highways, bridges, etc.
GPE: Countries, cities, states
LANGUAGE: Any named language
LAW: Named documents made into laws.
LOC: Non-GPE locations, mountain ranges, bodies of water
MONEY: Monetary values, including unit
NORP: Nationalities or religious or political groups
ORDINAL: "first", "second", etc.
ORG: Companies, agencies, institutions, etc.
PERCENT: Percentage, including "%"
PERSON: People, including fictional
PRODUCT: Objects, vehicles, foods, etc. (not services)
QUANTITY: Measurements, as of weight or distance
TIME: Times smaller than a day
WORK_OF_ART: Titles of books, songs, etc.
"""

from models.knowledge.event import Event
from models.knowledge.object import Object
from models.knowledge.organisation import Organisation
from models.knowledge.person import Person
from models.knowledge.place import Place

# Generate VALID_TYPES
VALID_TYPES = [None] + [cls.__name__.lower() for cls in [Person, Place, Event, Object, Organisation]]

__all__ = [
    "Person",
    "Place",
    "Event",
    "Object",
    "Organisation",
    "VALID_TYPES",
]
