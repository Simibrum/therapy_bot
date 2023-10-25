"""Functions to handle chat completion."""
from config import openai_api_key
from llm.common import api_request


def get_chat_completion(
    user_input: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.3,
    api_key: str = openai_api_key,
) -> str:
    """Get a chat completion from the OpenAI API."""
    messages = [
        {"speaker": "user", "text": user_input},
        {"speaker": "therapist", "text": "Hello, how are you?"},
        {"speaker": "user", "text": "I'm doing well, how about you?"},
        {"speaker": "therapist", "text": "I'm doing well, thanks for asking."},
        {"speaker": "user", "text": "That's good to hear."},
        {"speaker": "therapist", "text": "Yes, it is."},
        {"speaker": "user", "text": "I'm going to go now, bye."},
        {"speaker": "therapist", "text": "Okay, bye."},
    ]
    messages.append({"speaker": "user", "text": user_input})
    response = api_request(
        messages=messages,
        model=model,
        temperature=temperature,
        api_key=api_key
    )
    return response["choices"][0]["text"]
