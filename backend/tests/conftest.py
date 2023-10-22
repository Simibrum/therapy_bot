"""Configuration for testing."""
import os
import pytest
from sqlalchemy.orm import sessionmaker
from models import User, Therapist, Chat

from config import TestConfig
from database import Base
from database.db_engine import DBSessionManager


@pytest.fixture(scope='session', autouse=True)
def setup_testing_environment():
    print("Setting up testing environment")
    existing_env = os.environ.get('CONFIG_ENV')
    os.environ['CONFIG_ENV'] = 'testing'
    yield  # This will return control to the test function
    if existing_env:
        os.environ['CONFIG_ENV'] = existing_env  # Revert env var in teardown
    print("Tearing down testing environment")


@pytest.fixture(scope='function')
def db_setup():
    print("Setting up test class & generating DB file")
    TestConfig.generate_temp_file()
    print(f"Setting up tests in DB {TestConfig.SQLALCHEMY_DATABASE_URI}")
    test_engine = DBSessionManager.get_engine()
    TestSession = DBSessionManager.get_session_factory()
    assert "tmp" in TestSession.kw.get("bind").url.database
    Base.metadata.create_all(bind=test_engine)

    yield test_engine  # This will return control to the test function, and pass the test_engine to it

    print("Tearing down tests")
    assert "tmp" in test_engine.url.database
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
    TestConfig.remove_temp_file()


# Session fixture to use in tests
@pytest.fixture
def shared_session(db_setup):
    """Create a shared session."""
    test_engine = db_setup
    Session = sessionmaker(bind=test_engine)
    session = Session()

    yield session

    # Teardown code
    session.close()


# User fixture to use in tests
@pytest.fixture
def user_instance(shared_session):
    """Create a user instance."""
    user = User(
        username="testuser",
        password_hash="hashedpassword", # Temporary hash - password is set below
        email="test@example.com"
    )
    user.set_password("hashedpassword")
    shared_session.add(user)
    shared_session.commit()
    return user


# Therapist fixture to use in tests
@pytest.fixture
def therapist_instance(shared_session, user_instance):
    """Create a therapist instance."""
    therapist = Therapist(
        first_name="Test",
        last_name="Therapist",
        user_id=user_instance.id,
        residence="Test City",
        description="Test Description"
    )
    shared_session.add(therapist)
    shared_session.commit()
    return therapist


@pytest.fixture
def chat_instance(shared_session, user_instance, therapist_instance):
    """Create a chat instance."""
    chat = Chat(
        user=user_instance,
        therapist=therapist_instance,
        sender="user"
    )
    chat.text = "Hello, how are you?"
    shared_session.add(chat)
    shared_session.commit()
    return chat

