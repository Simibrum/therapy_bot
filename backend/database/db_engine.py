"""Define an engine to create logic for use within the application.

See https://stackoverflow.com/questions/59793920/
how-to-make-sqlalchemy-engine-available-throughout-the-flask-application
for replacement of db.session
"""
from contextlib import asynccontextmanager

from config import get_config
from config.init_logger import logger
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker


class DBSessionManager:
    """Class to manage both synchronous and asynchronous database sessions."""

    _sync_engine = None
    _async_engine = None
    _SyncSession = None
    _AsyncSession = None

    @classmethod
    def get_sync_session(cls, config=None) -> Session:
        """Get a synchronous session."""
        if config is None:
            config = get_config()
        if cls._SyncSession is None:
            logger.info("Getting synchronous session")
            cls._SyncSession = cls.get_sync_session_factory(config)
        return cls._SyncSession()

    @classmethod
    def get_sync_session_factory(cls, config=None) -> sessionmaker:
        """Get a synchronous session factory."""
        if config is None:
            config = get_config()
        if cls._SyncSession is None:
            logger.debug("Initializing synchronous database - getting session factory")
            engine_instance = cls.get_sync_engine(config)
            cls._SyncSession = sessionmaker(bind=engine_instance)
        return cls._SyncSession

    @classmethod
    def get_engine(cls, config=None) -> Engine:
        """Provide wrapper for a synchronous engine instance to support existing code."""
        return cls.get_sync_engine(config)

    @classmethod
    def get_session(cls, config=None) -> Session:
        """Provide wrapper for a synchronous session to support existing code."""
        return cls.get_sync_session(config)

    @classmethod
    def get_session_factory(cls, config=None) -> sessionmaker:
        """Provide wrapper for a synchronous session factory to support existing code."""
        return cls.get_sync_session_factory(config)

    @classmethod
    def get_sync_engine(cls, config=None) -> Engine:
        """Get a synchronous engine instance."""
        if config is None:
            config = get_config()
        if cls._sync_engine is None:
            cls._sync_engine = create_engine(
                config.SQLALCHEMY_DATABASE_URI,
                **config.SQLALCHEMY_ENGINE_OPTIONS,
            )
            logger.info(f"Initializing synchronous database - created engine instance - {cls._sync_engine.url}")
        return cls._sync_engine

    @classmethod
    @asynccontextmanager
    async def get_async_session(cls, config=None) -> AsyncSession:
        """Get an asynchronous session."""
        if config is None:
            config = get_config()
        if cls._AsyncSession is None:
            logger.info("Getting asynchronous session")
            cls._AsyncSession = cls.get_async_session_factory(config)
        async with cls._AsyncSession() as session:
            try:
                yield session
            finally:
                await session.close()

    @classmethod
    def get_async_session_factory(cls, config=None) -> async_sessionmaker:
        """Get an asynchronous session factory."""
        if config is None:
            config = get_config()
        if cls._AsyncSession is None:
            logger.debug("Initializing asynchronous database - getting session factory")
            engine_instance = cls.get_async_engine(config)
            cls._AsyncSession = async_sessionmaker(bind=engine_instance, expire_on_commit=False)
        return cls._AsyncSession

    @classmethod
    def get_async_engine(cls, config=None) -> AsyncEngine:
        """Get an asynchronous engine instance."""
        if config is None:
            config = get_config()
        if cls._async_engine is None:
            # Convert synchronous URL to asynchronous URL
            async_db_uri = config.SQLALCHEMY_DATABASE_URI.replace("postgresql://", "postgresql+asyncpg://")
            cls._async_engine = create_async_engine(
                async_db_uri,
                **config.SQLALCHEMY_ENGINE_OPTIONS,
            )
            logger.info(f"Initializing asynchronous database - created engine instance - {cls._async_engine.url}")
        return cls._async_engine

    @classmethod
    def reset(cls):
        """Reset all engine and session instances."""
        if cls._sync_engine:
            cls._sync_engine.dispose()
            cls._sync_engine = None
        if cls._async_engine:
            cls._async_engine.dispose()
            cls._async_engine = None
        cls._SyncSession = None
        cls._AsyncSession = None
        logger.info("Reset all database engines and sessions")


# Synchronous database session generator
def get_db() -> Session:
    """Get a synchronous database session from the pool."""
    try:
        session_manager = DBSessionManager()
        db = session_manager.get_sync_session()
        logger.debug("Got synchronous database session for %s", db.bind.url)
        yield db
    finally:
        logger.debug("Closing synchronous database session for %s", db.bind.url)
        db.close()


# Asynchronous database session generator
async def get_async_db() -> AsyncSession:
    """Get an asynchronous database session from the pool."""
    async with DBSessionManager.get_async_session() as db:
        try:
            logger.debug("Got asynchronous database session for %s", db.bind.url)
            yield db
        finally:
            logger.debug("Asynchronous database session closed")
