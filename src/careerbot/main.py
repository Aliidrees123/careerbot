from careerbot.config import load_settings
from careerbot.llm.openai_client import build_client
from careerbot.chat.orchestrator import ChatOrchestrator


import gradio as gr

# Entry point to bring everything together and launch the app

def main():

    settings = load_settings()

    client = build_client(settings.openai_api_key)

    system_message = {
        "role": "system",
        "content": [ 
            {
                "type": "input_text",
                "text": "You are careerbot, an AI designed to answer questions about my career, skills, and experience."
            }
        ]
    }

    orchestrator = ChatOrchestrator(client=client, model=settings.openai_model, system_message=system_message)

    app = gr.ChatInterface(fn=orchestrator)

    app.launch()

if __name__ == "__main__":
    main()
    