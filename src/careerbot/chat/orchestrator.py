from careerbot.llm.openai_client import request_response
from openai import OpenAI

# Chat loop - build messages, calls LLM, handles tool calls, and returns output
class ChatOrchestrator:

    # Build the ChatOrchestrator object
    def __init__(self, *, client: OpenAI, model: str, system_message: dict):
        if not model or not model.strip():
            raise ValueError("Missing OpenAI model")
        
        self._client = client
        self._model = model
        self._system_message = system_message

    # Call the chat function
    def __call__(self, message: str, history: list[dict]) -> str:
        return self.chat(message, history)
    
    # Build the message, call the LLM, and return the response
    def chat(self, message: str, history: list[dict]) -> str:

        model_request = self._build_model_request(history=history, message=message)
        model_response = request_response(client=self._client, model=self._model, input=model_request)
        return model_response.output_text

    # Format the user's input
    def _wrap_text(self, message: str) -> dict:
        user_message = {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": message
                }
            ]
        }
        
        return user_message

    # Format the chat history from Gradio
    def _format_gradio_history(self, history: list[dict]) -> list[dict]:
        formatted_history = []

        for item in history:
            history_template = {
                "role": item["role"],
                "content": [
                    {
                        "type": "input_text",
                        "text": item["content"]
                    }
                ]
            }
            
            formatted_history.append(history_template)
        
        return formatted_history

    # Build the overall input for the LLM
    def _build_model_request(self, *, history: list[dict], message: str) -> list[dict]:

        user_message = self._wrap_text(message)
        formatted_history = self._format_gradio_history(history)

        model_request = []

        model_request.append(self._system_message)
        model_request += formatted_history
        model_request.append(user_message)

        return model_request
