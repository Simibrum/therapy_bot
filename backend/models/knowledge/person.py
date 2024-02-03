"""Model to define a person in the knowledge graph."""


from models.chats_mixin import HasChatReferences
from models.common import PersonNameMixin, LifeDatesMixin
from models.knowledge.common import Common


class Person(Common, PersonNameMixin, LifeDatesMixin, HasChatReferences):
    """Model to define a person in the knowledge graph."""

    __tablename__ = "persons"

    # first_name, last_name, and middle_name are inherited from PersonNameMixin
    # date_of_birth and date_of_death are inherited from LifeDatesMixin
