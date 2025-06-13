"""Fixtures that use synchronous database operations."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import pytest
from config import TZ_INFO, TestConfig
from database import Base, DBSessionManager
from logic.therapy_session_logic import TherapySessionLogic
from models import Chat, Therapist, TherapySession, User
from sqlalchemy.orm import Session, sessionmaker

if TYPE_CHECKING:
    from sqlalchemy import Engine


@pytest.fixture()
def sync_db_setup() -> Engine:
    """Set up the database for testing.

    This is a synchronous fixture that sets up the database for testing.
    """
    print("Setting up test class & generating DB file")
    TestConfig.generate_temp_file()
    print(f"Setting up tests in DB {TestConfig.SQLALCHEMY_DATABASE_URI}")

    # Reset the DBSessionManager to ensure the test engine is used
    DBSessionManager.reset()

    test_engine = DBSessionManager.get_sync_engine(config=TestConfig)
    test_session = DBSessionManager.get_session_factory()
    print(test_session.kw.get("bind").url.database)
    assert "tmp" in test_session.kw.get("bind").url.database
    Base.metadata.create_all(bind=test_engine)

    yield test_engine  # This will return control to the test function, and pass the test_engine to it

    print("Tearing down tests")
    assert "tmp" in test_engine.url.database
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
    TestConfig.remove_temp_file()


@pytest.fixture()
def db_session_manager(sync_db_setup: Engine) -> DBSessionManager:
    """Create a session manager."""
    assert sync_db_setup  # Ensure the db_setup fixture is called to initialize the database
    return DBSessionManager()


@pytest.fixture()
def shared_session(sync_db_setup: Engine) -> Session:
    """Create a shared session based on a synchronous DB."""
    test_engine = sync_db_setup
    session_factory = sessionmaker(bind=test_engine)
    session = session_factory()

    yield session

    # Teardown code
    session.close()


@pytest.fixture()
def user_instance(shared_session: Session) -> User:
    """Create a user instance for use in synchronous sessions."""
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
    # Define a test date of birth as a datetime object
    user.date_of_birth = datetime(1980, 1, 1, tzinfo=TZ_INFO)

    shared_session.add(user)
    shared_session.commit()
    return user


@pytest.fixture()
def therapist_instance(shared_session: Session, user_instance: User) -> Therapist:
    """Create a therapist instance for use in synchronous sessions."""
    therapist = Therapist(
        first_name="Test",
        last_name="Therapist",
        user_id=user_instance.id,
        residence="Test City",
        description="Test Description",
    )
    shared_session.add(therapist)
    shared_session.commit()
    return therapist


@pytest.fixture()
def therapy_session_instance(
    shared_session: Session, user_instance: User, therapist_instance: Therapist
) -> TherapySession:
    """Create a therapy session instance."""
    therapy_session = TherapySession(user=user_instance, therapist=therapist_instance)
    shared_session.add(therapy_session)
    shared_session.commit()
    return therapy_session


@pytest.fixture()
def therapy_session_logic_instance(therapy_session_instance: TherapySession) -> TherapySessionLogic:
    """Create a therapy session logic instance."""
    return TherapySessionLogic(pre_existing_session_id=therapy_session_instance.id)


@pytest.fixture()
def chat_instance(
    shared_session: Session,
    user_instance: User,
    therapist_instance: Therapist,
    therapy_session_instance: TherapySession,
) -> Chat:
    """Create a chat instance."""
    chat = Chat(
        user=user_instance,
        therapist=therapist_instance,
        sender="user",
        therapy_session=therapy_session_instance,
    )
    chat.text = "Hello, how are you?"
    shared_session.add(chat)
    shared_session.commit()
    return chat
