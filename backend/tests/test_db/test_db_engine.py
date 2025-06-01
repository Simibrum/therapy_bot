"""Testing the database engine."""


import pytest
import pytest_asyncio
from database.db_engine import DBSessionManager
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Create a base class for declarative models
Base = declarative_base()


# Define a simple model for testing
class TestModel(Base):
    __tablename__ = "test_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)


# Test configurations
class SyncTestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {"echo": True}


class AsyncTestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {"echo": True}


# Fixture for sync tests
@pytest.fixture(scope="function")
def sync_db_session_manager():
    manager = DBSessionManager()
    engine = manager.get_sync_engine(SyncTestConfig())
    Base.metadata.create_all(engine)
    yield manager
    Base.metadata.drop_all(engine)


# Fixture for async tests
@pytest_asyncio.fixture(scope="function")
async def async_db_session_manager():
    manager = DBSessionManager()
    engine = manager.get_async_engine(AsyncTestConfig())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield manager
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Synchronous tests
def test_sync_session(sync_db_session_manager):
    session = sync_db_session_manager.get_sync_session(SyncTestConfig())
    assert isinstance(session, Session)

    # Test inserting and querying data
    test_model = TestModel(name="Test Name")
    session.add(test_model)
    session.commit()

    result = session.query(TestModel).filter_by(name="Test Name").first()
    assert result is not None
    assert result.name == "Test Name"


def test_sync_engine(sync_db_session_manager):
    engine = sync_db_session_manager.get_sync_engine(SyncTestConfig())
    assert engine.url.database == ":memory:"


# Asynchronous tests
@pytest.mark.asyncio()
async def test_async_session(async_db_session_manager):
    async_session = await async_db_session_manager.get_async_session(AsyncTestConfig())
    assert isinstance(async_session, AsyncSession)

    # Test inserting and querying data asynchronously
    async with async_session as session:
        test_model = TestModel(name="Async Test")
        session.add(test_model)
        await session.commit()

        result = await session.execute(select(TestModel).filter_by(name="Async Test"))
        fetched_model = result.scalar_one_or_none()
        assert fetched_model is not None
        assert fetched_model.name == "Async Test"


@pytest.mark.asyncio()
async def test_async_engine(async_db_session_manager):
    engine = async_db_session_manager.get_async_engine(AsyncTestConfig())
    assert isinstance(engine, create_async_engine(url="sqlite+aiosqlite:///:memory:").__class__)
    assert engine.url.database == ":memory:"


# Test backward compatibility wrappers
def test_backward_compatibility(sync_db_session_manager):
    engine = sync_db_session_manager.get_engine(SyncTestConfig())
    assert engine.url.database == ":memory:"

    session = sync_db_session_manager.get_session(SyncTestConfig())
    assert isinstance(session, Session)

    session_factory = sync_db_session_manager.get_session_factory(SyncTestConfig())
    assert callable(session_factory)


if __name__ == "__main__":
    pytest.main()
