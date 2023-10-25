"""Methods to initialise the database."""
import os
from database.db_engine import DBSessionManager
from database import Base
from config import logger
# Need to import these even if not using them
from models import User, Therapist, Chat


def create_default_user():
    """Create a default user."""
    # Get a session
    db = DBSessionManager()
    session = db.get_session()
    # Create the default user
    from models import User
    username = os.getenv("DEFAULT_USER", "i-am-admin")
    email = os.getenv("DEFAULT_EMAIL", "me@great.com")
    password = os.getenv("DEFAULT_PASSWORD", "a-really-bad-password")
    user = User(
        username=username,
        email=email,
        password_hash="1234567"
    )
    user.set_password(password)
    session.add(user)
    session.commit()
    session.close()


def create_tables():
    """Create all tables."""
    # Get the database engine
    db = DBSessionManager()
    # Create all schemas
    logger.debug("Creating all tables.")
    Base.metadata.create_all(bind=db.get_engine())
    # Create the default user
    logger.debug("Creating default user.")
    create_default_user()


if __name__ == '__main__':
    # Create the tables
    create_tables()
