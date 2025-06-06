"""Model to define a person in the knowledge graph."""

from models.common import LifeDatesMixin, PersonNameMixin
from models.knowledge.common import Common


class Person(Common, PersonNameMixin, LifeDatesMixin):
    """Model to define a person in the knowledge graph."""

    __tablename__ = "persons"

    # first_name, last_name, and middle_name are inherited from PersonNameMixin
    # date_of_birth and date_of_death are inherited from LifeDatesMixin
