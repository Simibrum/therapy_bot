"""Fixtures for async tests."""

from typing import AsyncGenerator

import pytest_asyncio
from config import TestConfig
from database import Base
from logic.knowledge_graph_processor import KnowledgeGraphProcessor
from models import Chat, Therapist, TherapySession, User
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


@pytest_asyncio.fixture(scope="function")
async def async_db_setup():
    """Set up the async database for testing."""
    print("Setting up async test class & generating DB file")
    TestConfig.generate_temp_file()
    async_db_url = f"sqlite+aiosqlite:///{TestConfig.SQLALCHEMY_DATABASE_URI.split(':///')[-1]}"
    # async_db_url = "sqlite+aiosqlite:///:memory:"
    print(f"Setting up async tests in DB {async_db_url}")
    async_engine = create_async_engine(async_db_url)
    async_session_factory = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_engine.dispose()
    TestConfig.remove_temp_file()


@pytest_asyncio.fixture(scope="function")
async def async_shared_session(async_db_setup) -> AsyncGenerator[AsyncSession, None]:
    """Create a shared async session."""
    async_session_factory = sessionmaker(bind=async_db_setup, class_=AsyncSession, expire_on_commit=False)
    async with async_session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def async_user_instance(async_shared_session: AsyncSession) -> User:
    """Create a user instance asynchronously."""
    user = User(
        username="testuser",
        password_hash="hashedpassword",  # noqa: S106 -  Temporary hash - password is set below
        email="test@example.com",
    )
    user.set_password("hashedpassword")
    user.first_name = "Test"
    user.last_name = "User"
    user.address = "Test Address"
    user.city = "Test City"
    user.country = "Test Country"
    async_shared_session.add(user)
    await async_shared_session.commit()
    return user


@pytest_asyncio.fixture(scope="function")
async def async_therapist_instance(async_shared_session: AsyncSession, async_user_instance: User) -> Therapist:
    """Create a therapist instance asynchronously."""
    therapist = Therapist(
        first_name="Test",
        last_name="Therapist",
        user_id=async_user_instance.id,
        residence="Test City",
        description="Test Description",
    )
    async_shared_session.add(therapist)
    await async_shared_session.commit()
    return therapist


@pytest_asyncio.fixture(scope="function")
async def async_therapy_session_instance(
    async_shared_session: AsyncSession, async_user_instance: User, async_therapist_instance: Therapist
) -> TherapySession:
    """Create a therapy session instance asynchronously."""
    therapy_session = TherapySession(user_id=async_user_instance.id, therapist_id=async_therapist_instance.id)
    async_shared_session.add(therapy_session)
    await async_shared_session.commit()
    return therapy_session


@pytest_asyncio.fixture(scope="function")
async def async_chat_instance(
    async_shared_session: AsyncSession,
    async_user_instance: User,
    async_therapist_instance: Therapist,
    async_therapy_session_instance: TherapySession,
) -> Chat:
    """Create a chat instance asynchronously."""
    chat = Chat(
        user_id=async_user_instance.id,
        therapist_id=async_therapist_instance.id,
        therapy_session_id=async_therapy_session_instance.id,
        sender="user",
    )
    async_shared_session.add(chat)
    await async_shared_session.commit()
    return chat


@pytest_asyncio.fixture(scope="function")
async def async_knowledge_graph_processor(async_shared_session, test_nlp):
    """Create an async KnowledgeGraphProcessor instance."""
    return KnowledgeGraphProcessor(async_shared_session, test_nlp)
