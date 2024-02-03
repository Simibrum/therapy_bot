from llm.common import client


def custom_chat_completion(
    model, messages, temperature: float = 0.7, max_tokens: int = 10
):
    """Custom create function to tailor model for cheaper/quicker testing."""
    # Change model to cheaper and quicker model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content
