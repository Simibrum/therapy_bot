# Generated by CodiumAI

from app.crud.users import get_user_by_username


class TestGetUserByUsername:
    """Test the get_user_by_username function."""

    #  Retrieve an existing user by their username
    def test_retrieve_existing_user(self, shared_session, user_instance):
        session = shared_session

        # Retrieve the user by their username
        retrieved_user = get_user_by_username(session, user_instance.username)

        # Assert that the retrieved user is not None and has the correct username
        assert retrieved_user is not None
        assert retrieved_user.username == user_instance.username

        session.close()

    #  Return None when no user exists with the given username
    def test_return_none_for_nonexistent_user(self, shared_session):
        session = shared_session

        # Retrieve a non-existent user by their username
        username = "nonexistent_user"
        retrieved_user = get_user_by_username(session, username)

        # Assert that the retrieved user is None
        assert retrieved_user is None

        session.close()

    #  Test with an empty string as the username
    def test_empty_string_username(self, shared_session):
        session = shared_session

        # Retrieve a user with an empty string as the username
        username = ""
        retrieved_user = get_user_by_username(session, username)

        # Assert that the retrieved user is None
        assert retrieved_user is None

        session.close()

    #  Test with a username that contains special characters
    def test_special_characters_username(self, shared_session):
        session = shared_session

        # Retrieve a user with a username that contains special characters
        username = "user@123"
        retrieved_user = get_user_by_username(session, username)

        # Assert that the retrieved user is None
        assert retrieved_user is None

        session.close()

    #  Test with a username that is longer than the maximum allowed length
    def test_long_username(self, shared_session):
        session = shared_session

        # Retrieve a user with a username that is longer than the maximum allowed length
        username = "a" * 256
        retrieved_user = get_user_by_username(session, username)

        # Assert that the retrieved user is None
        assert retrieved_user is None

        session.close()

    #  Test with a username that is not a string
    def test_non_string_username(self, shared_session):
        session = shared_session

        # Retrieve a user with a non-string username
        username = 12345
        retrieved_user = get_user_by_username(session, username)

        # Assert that the retrieved user is None
        assert retrieved_user is None

        session.close()
