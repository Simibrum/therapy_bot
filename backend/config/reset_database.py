"""Command to reset the database."""
from database import Base
from database.db_engine import DBSessionManager

from config.init_database import create_tables
from config.init_logger import logger


def reset_database() -> None:
    """Function to reset the database."""
    # Get the database engine
    db = DBSessionManager()
    confirmation = input("Are you sure you want to reset the database? (y/N) ")
    if confirmation.lower() != "y":
        print("Aborting...")
        return
    logger.info("Dropping all existing tables.")
    # Drop all tables
    Base.metadata.drop_all(bind=db.get_engine())
    # Create all tables
    create_tables()


if __name__ == "__main__":
    reset_database()
