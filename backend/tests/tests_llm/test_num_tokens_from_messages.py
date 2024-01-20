# Generated by CodiumAI

import pytest

from backend.llm.common import num_tokens_from_messages


class TestNumTokensFromMessages:

    #  Returns the correct number of tokens for a single message with no name and no additional keys.
    def test_single_message_no_name_no_additional_keys(self):
        # I have test_client and user_instance
        messages = [{"content": "Hello"}]
        expected_tokens = 7  # 4 tokens for message structure + 1 token for "Hello" + 2 tokens for assistant reply
        assert num_tokens_from_messages(messages) == expected_tokens

    #  Returns the correct number of tokens for a single message with a name and no additional keys.
    def test_single_message_with_name_no_additional_keys(self):
        # I have test_client and user_instance
        messages = [{"name": "User", "content": "Hello"}]
        expected_tokens = 7
        assert num_tokens_from_messages(messages) == expected_tokens

    #  Returns the correct number of tokens for a single message with additional keys.
    def test_single_message_with_additional_keys(self):
        # I have test_client and user_instance
        messages = [{"content": "Hello", "key1": "value1", "key2": "value2"}]
        expected_tokens = 11
        assert num_tokens_from_messages(messages) == expected_tokens

    #  Raises a KeyError if an invalid model is provided.
    def test_invalid_model_raises_key_error(self):
        # I have test_client and user_instance
        messages = [{"content": "Hello"}]
        invalid_model = "invalid_model"
        with pytest.raises(NotImplementedError):
            num_tokens_from_messages(messages, model=invalid_model)

    #  Returns the correct number of tokens for a single message with the maximum length of content.
    def test_single_message_max_content_length(self):
        # I have test_client and user_instance
        max_content = "a " * 4096  # maximum length of content is 4096 characters
        messages = [{"content": max_content}]
        expected_tokens = 4103
        assert num_tokens_from_messages(messages) == expected_tokens

    #  Returns the correct number of tokens for a single message with the maximum length of name.
    def test_single_message_max_name_length(self):
        # I have test_client and user_instance
        max_name = "a " * 4096  # maximum length of name is 4096 characters
        messages = [{"name": max_name, "content": "Hello"}]
        expected_tokens = 4103
        assert num_tokens_from_messages(messages) == expected_tokens