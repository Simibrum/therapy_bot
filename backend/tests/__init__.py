
import openai


def custom_create(model, messages, api_key: str, temperature: float = 0.7, max_tokens: int = 10,  ):
    """Custom create function to tailor model for cheaper/quicker testing."""
    # Change model to cheaper and quicker model
    return openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        api_key=api_key
    )
