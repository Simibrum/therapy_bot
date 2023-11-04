"""Define an engine to create logic for use within the application.

See https://stackoverflow.com/questions/59793920/
how-to-make-sqlalchemy-engine-available-throughout-the-flask-application
for replacement of db.session
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_config
from config.init_logger import logger

# See `config.create_tables` for table creation


class DBSessionManager:
    _engine = None
    _Session = None

    @classmethod
    def get_session(cls, config=None):
        """Get a session from the sessionmaker."""
        if config is None:
            config = get_config()
        if cls._Session is None:
            logger.info(f"Getting session")
            cls._Session = cls.get_session_factory(config)
        return cls._Session()

    @classmethod
    def get_session_factory(cls, config=None):
        """Get a session factory."""
        if config is None:
            config = get_config()
        if cls._Session is None:
            logger.debug(f"Initializing database - getting session factory")
            engine_instance = cls.get_engine(config)
            cls._Session = sessionmaker(bind=engine_instance)
        return cls._Session

    @classmethod
    def get_engine(cls, config=None):
        """Get an engine instance."""
        if config is None:
            config = get_config()
        if cls._engine is None:
            cls._engine = create_engine(
                config.SQLALCHEMY_DATABASE_URI,
                **config.SQLALCHEMY_ENGINE_OPTIONS,
            )
            logger.info(f"Initializing database - created engine instance - {cls._engine.url}")
        return cls._engine


def get_db():
    """Get a database session from the pool."""
    try:
        session_manager = DBSessionManager()
        db = session_manager.get_session()
        logger.debug("Got database session for %s", db.bind.url)
        yield db
    finally:
        logger.debug("Closing database session for %s", db.bind.url)
        db.close()
