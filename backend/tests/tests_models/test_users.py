"""Tests for the users models."""
from sqlalchemy.orm import sessionmaker
from models import User, RoleEnum


def test_user(db_setup, user_instance):
    test_engine = db_setup
    Session = sessionmaker(bind=test_engine)
    session = Session()

    # Retrieve the user from the database
    retrieved_user = session.query(User).filter_by(id=user_instance.id).one()

    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.check_password("hashedpassword")
    assert not retrieved_user.check_password("wrongpassword")
    assert retrieved_user.role == RoleEnum.USER
    assert not retrieved_user.is_admin
    assert retrieved_user.encryption_key

    session.close()
