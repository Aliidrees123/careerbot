# Wraps OpenAI calls - allows for easy LLM switching without changing logic

from openai import OpenAI

# Initialise OpenAI client
def build_client(api_key: str) -> OpenAI:
    
    # Ensure API key is provided
    if not api_key or not api_key.strip():
        raise ValueError("Missing OpenAI API key")
    
    # Return initialised client
    return OpenAI(api_key = api_key)

# Send 
def request_response(*, client: OpenAI, model: str, input: list[dict]) -> dict:

    # Ensure model is provided
    if not model or not model.strip():
        raise ValueError("Missing OpenAI model")
    
    # Ensure input is provided
    if not input or not isinstance(input, list):
        raise ValueError("Input must be a non-empty list of messages")
    
    # Send request and return response
    response = client.responses.create(
        model=model,
        input=input
    )
    return response