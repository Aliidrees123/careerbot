from careerbot.llm.openai_client import request_response
from careerbot.tools.handlers import execute_tool
from openai import OpenAI
from pathlib import Path
import json

# Chat loop - build messages, calls LLM, handles tool calls, and returns output
class ChatOrchestrator:

    # Build the ChatOrchestrator object
    def __init__(self, *, client: OpenAI, model: str, system_message: dict, profile_context: str, tools: list, tool_results_dir: Path):
        if not model or not model.strip():
            raise ValueError("Missing OpenAI model")
        
        self._client = client
        self._model = model
        self._system_message = system_message
        self._profile_context = profile_context
        self._tools = tools
        self._tool_results_dir = tool_results_dir

    # Call the chat function
    def __call__(self, message: str, history: list[dict]) -> str:
        return self.chat(message=message, history=history)
    
    # Build the message, call the LLM & any tools, and return the response
    def chat(self, *, message: str, history: list[dict]) -> str:

        # Maximum tool calls
        max_iterations = 3
        # New message + history
        input_items = self._build_model_request(history=history, message=message)
        # Fallback in case of no response
        last_text = ""
        # Track response.output ids that are already appended
        seen_output_ids = set() 

        # Loop to allow for tool calls until max_iterations
        for _ in range(max_iterations):

            # The response from the OpenAI client
            response = request_response(
                client=self._client,
                model=self._model,
                input=input_items,
                tools=self._tools
            )

            if getattr(response, "output_text", ""):
                last_text = response.output_text

            # List of tools that were called
            tool_calls = [
            item for item in response.output
            if item.type == "function_call"
            ]

            # If no tools called then return response
            if not tool_calls:
                return response.output_text

            # Appends the response.output to input_items if we haven't seen the id before
            for item in response.output:
                item_id = getattr(item, "id", None)
                if not item_id:
                    input_items.append(item)
                    continue
                if item_id in seen_output_ids:
                    continue
                seen_output_ids.add(item_id)
                input_items.append(item)

            # Execute each tool call and append tool outputs
            for call in tool_calls:
                # Parse tool args
                try:
                    args = json.loads(call.arguments) if call.arguments else {}
                except Exception as e:
                    # If error, feed this back as tool output
                    input_items.append(
                        {
                            "type": "function_call_output",
                            "call_id": call.call_id,
                            "output": json.dumps(
                                {"ok": False, "error": f"Invalid tool arguments JSON: {e}", "raw": call.arguments},
                                ensure_ascii=False,
                            ),
                        }
                    )
                    continue

                result = execute_tool(
                    call.name,
                    args,
                    out_dir=self._tool_results_dir
                )

                if result.ok:
                    out_str = result.content if isinstance(result.content, str) else json.dumps(result.content, ensure_ascii=False)
                else:
                    out_str = result.error if isinstance(result.error, str) else json.dumps({"error": result.error}, ensure_ascii=False)

                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": out_str
                    }
                )
                
        return last_text or "I couldn't complete that action right now."

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
