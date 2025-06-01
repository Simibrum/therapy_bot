"""Model to define an organisation in the knowledge graph."""

from models.common import LocationMixin, OrganisationMixin
from models.knowledge.common import Common


class Organisation(Common, OrganisationMixin, LocationMixin):
    """Model to define an organisation in the knowledge graph."""

    __tablename__ = "organisations"

    # Fields from Common: id, node_id, user_id
    # Fields from OrganisationMixin: name, type, industry, founded_date, website, description
    # Fields from LocationMixin: address, city, country, location_code

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"<Organisation(id={self.id}, name='{self.name}', type='{self.type}')>"
