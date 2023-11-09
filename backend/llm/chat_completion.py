"""Functions to handle chat completion."""
from llm.common import api_request


def get_chat_completion(
    next_message_prompt: str,
    system_prompt: str,
    history: str = None,
    briefing_messages: list[str] = None,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.3,
) -> str:
    """Get a chat completion from the OpenAI API."""
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    if history:
        messages.append({"role": "user", "content": history})
    if briefing_messages:
        messages.extend([{"role": "user", "content": message} for message in briefing_messages])

    messages.append({"role": "user", "content": next_message_prompt})

    response = api_request(
        messages=messages,
        model=model,
        temperature=temperature
    )
    return response
