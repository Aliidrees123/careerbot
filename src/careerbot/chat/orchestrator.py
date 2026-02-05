from careerbot.llm.openai_client import request_response
from openai import OpenAI
from typing import Any

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
    
    # Ensure history is a String, not List
    def _normalise_history_content_to_text(self, content) -> str:
        if isinstance(content, str):
            return content
        
        if isinstance(content, list):
            parts: list[str] = []
            for block in content:
                if isinstance(block, dict):
                    text = block.get("text")
                    if isinstance(text, str):
                        parts.append(text)
            return "\n".join(parts)
        
        return str(content)

    # Ensure correct role is used for history
    def _history_block_type_for_role(self, role: str) -> str:
        return "output_text" if role == "assistant" else "input_text"

    # Format the chat history from Gradio
    def _format_gradio_history(self, history: list[dict]) -> list[dict]:
        formatted_history = []

        for item in history:
            role = item.get("role", "user")
            content = item.get("content", "")

            content_text = self._normalise_history_content_to_text(content)
            block_type = self._history_block_type_for_role(role)

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
