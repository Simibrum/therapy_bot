from app.schemas import ChatListOut
# Generated by CodiumAI


class TestGetMessages:

    #  Returns existing messages if there are any.
    def test_existing_messages(self, therapy_session_logic_instance):
        # Add existing messages to the therapy session
        therapy_session_logic_instance.add_chat_message("user", "Hello")
        therapy_session_logic_instance.add_chat_message("therapist", "Hi, how can I help you?")
        # Call the get_messages method
        result = therapy_session_logic_instance.get_messages()
        # Assert that the result is a ChatListOut object
        assert isinstance(result, ChatListOut)
        # Assert that the result contains the existing messages
        assert len(result.messages) == 2
        assert result.messages[0].sender == "user"
        assert result.messages[0].text == "Hello"
        assert result.messages[1].sender == "therapist"
        assert result.messages[1].text == "Hi, how can I help you?"

    #  Starts a new session if there are no existing messages.
    def test_new_session(self, therapy_session_logic_instance, mocked_chat_completion, mocked_embedding_client):
        # Clear any existing messages in the therapy session
        therapy_session_logic_instance.get_therapy_session_messages().messages.clear()
        # Call the get_messages method
        result = therapy_session_logic_instance.get_messages()
        # Assert that the result is a ChatListOut object
        assert isinstance(result, ChatListOut)
        # Assert that the result contains a new session message
        assert len(result.messages) == 1
        assert result.messages[0].sender == "therapist"
        assert result.messages[0].text == "Welcome to your therapy session!"
