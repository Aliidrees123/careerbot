# Wraps OpenAI calls - allows for easy LLM switching without changing logic

from openai import OpenAI

# Initialises and returns the OpenAI client
def build_client(api_key: str) -> OpenAI:
    
    if not api_key or not api_key.strip():
        raise ValueError("Missing OpenAI API key")
    
    return OpenAI(api_key = api_key)

# Sends the request to the LLM and returns the LLM's response
def request_response(*, client: OpenAI, model: str, input: list[dict]) -> dict:

    if not model or not model.strip():
        raise ValueError("Missing OpenAI model")
    
    if not input or not isinstance(input, list):
        raise ValueError("Input must be a non-empty list of messages")
    
    response = client.responses.create(
        model=model,
        input=input
    )
    return response