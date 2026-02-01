# Chat loop - build messages, calls LLM, handles tool calls, and returns output

# Define the instructions for the LLM
system_message = {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are CareerBot, an AI assitant designed to speak to recruiters about my skills and experiences to bolster my job prospects"
            }
        ]
    }

# Format the user's input
def wrap_text(message):
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    
    return user_message

# Format the chat history from Gradio
def format_gradio_history(history: list):

    formatted_history = []

    for message in history:
        history_template = {
            "role": message["role"],
            "content": [
                {
                    "type": "text",
                    "text": message["content"]
                }
            ]
        }
        
        formatted_history.append(history_template)
    
    return formatted_history

# Build the overall input for the LLM
def build_model_request(system_message, history, message):

    user_message = wrap_text(message)
    formatted_history = format_gradio_history(history)

    model_request = []

    model_request.append(system_message)
    model_request += formatted_history
    model_request.append(user_message)

    return model_request
