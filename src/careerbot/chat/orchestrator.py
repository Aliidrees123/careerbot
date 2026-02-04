from careerbot.llm.openai_client import request_response
from openai import OpenAI

# Chat loop - build messages, calls LLM, handles tool calls, and returns output
class ChatOrchestrator:

    # Build the ChatOrchestrator object
    def __init__(self, *, client: OpenAI, model: str, system_message: dict, profile_context: str):
        if not model or not model.strip():
            raise ValueError("Missing OpenAI model")
        
        self._client = client
        self._model = model
        self._system_message = system_message
        self._profile_context = profile_context

    # Call the chat function
    def __call__(self, message: str, history: list[dict]) -> str:
        return self.chat(message=message, history=history)
    
    # Build the message, call the LLM, and return the response
    def chat(self, *, message: str, history: list[dict]) -> str:

        model_request = self._build_model_request(history=history, message=message)
        model_response = request_response(client=self._client, model=self._model, input=model_request)
        return model_response.output_text

    # Format the user's input
    def _wrap_text(self, message: str) -> dict:
        return {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": message
                }
            ]
        }

    # Format the chat history from Gradio
    def _format_gradio_history(self, history: list[dict]) -> list[dict]:
        formatted_history = []

        for item in history:
            role = item["role"]
            content = item["content"]

            if isinstance(content, list):
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and "text" in block:
                        text_parts.append(block["text"])
                content_text = "\n".join(text_parts)
            else: 
                content_text = content

            if role == "assistant":
                block_type = "output_text"
            else:
                block_type = "input_text"

            formatted_history.append(
                {
                    "role": role,
                    "content": [
                        {
                            "type": block_type,
                            "text": content_text
                        }
                    ]
                }
            )
                
        return formatted_history
    
    # Formats the profile context
    def _format_profile_context(self, profile_context: str | None) -> dict:
        return {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": profile_context
                }
            ]
        }

    # Build the overall input for the LLM
    def _build_model_request(self, *, history: list[dict], message: str) -> list[dict]:

        model_request = []

        model_request.append(self._system_message)

        if self._profile_context:
            formatted_profile_context = self._format_profile_context(self._profile_context)
            model_request.append(formatted_profile_context)
        
        formatted_history = self._format_gradio_history(history)
        model_request += formatted_history

        user_message = self._wrap_text(message)
        model_request.append(user_message)

        return model_request
