"""Methods to initialise the database."""
import os

from config import logger
from database import Base
from database.db_engine import DBSessionManager
# Need to import these even if not using them
from models import Therapist, User


def create_default_user():
    """Create a default user."""
    # Get a session
    db = DBSessionManager()
    session = db.get_session()
    # Create the default user
    username = os.getenv("DEFAULT_USER", "i-am-admin")
    email = os.getenv("DEFAULT_EMAIL", "me@great.com")
    password = os.getenv("DEFAULT_PASSWORD", "a-really-bad-password")
    user = User(username=username, email=email, password_hash="1234567")
    user.set_password(password)
    first_name = "Brian"
    user.first_name = first_name
    session.add(user)
    session.commit()
    session.close()


def create_default_therapist():
    """Create a default therapist."""
    # Get a session
    db = DBSessionManager()
    session = db.get_session()
    # Get the default user
    user = session.query(User).filter(User.username == "i-am-admin").first()
    # Create the default therapist
    description = (
        "Annie Hall is a compassionate therapist in Bristol, known for her integrative approach to mental health. "
        "She combines traditional counseling with modern techniques, providing tailored support for individuals "
        "seeking clarity and growth. Her warmth and expertise create a safe space for healing and personal development."
    )
    therapist = Therapist(
        first_name="Annie",
        last_name="Hall",
        user_id=user.id,
        residence="Bristol",
        description=description,
    )
    session.add(therapist)
    session.commit()


def create_tables():
    """Create all tables."""
    # Get the database engine
    db = DBSessionManager()
    # Create all schemas
    logger.info("Creating all tables.")
    Base.metadata.create_all(bind=db.get_engine())
    # Create the default user
    logger.info("Creating default user.")
    create_default_user()
    # Create the default therapist
    logger.info("Creating default therapist.")
    create_default_therapist()


if __name__ == "__main__":
    # Create the tables
    create_tables()
