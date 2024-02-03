"""Model to define a place in the knowledge graph."""


from sqlalchemy import Numeric
from sqlalchemy.orm import mapped_column, Mapped

from models.chats_mixin import HasChatReferences
from models.common import LocationMixin
from models.knowledge.common import Common


class Place(Common, LocationMixin, HasChatReferences):
    __tablename__ = "places"

    # Place-specific fields
    latitude: Mapped[float] = mapped_column(
        Numeric(9, 6), nullable=True
    )  # Up to 6 decimal places of precision
    longitude: Mapped[float] = mapped_column(
        Numeric(9, 6), nullable=True
    )  # Up to 6 decimal places of precision
    elevation: Mapped[float] = mapped_column(
        Numeric(9, 6), nullable=True
    )  # Up to 6 decimal places of precision

    # Address, City, and Country are inherited from LocationMixin
