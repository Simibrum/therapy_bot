"""Model for a general object or thing in the knowledge graph."""

from models.common import ObjectMixin
from models.knowledge.common import Common


class Object(Common, ObjectMixin):
    """Model for a general object or thing in the knowledge graph."""

    __tablename__ = "objects"
    # Object-specific fields passed through ObjectMixin
