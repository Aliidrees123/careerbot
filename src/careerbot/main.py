from careerbot.config import load_settings
from careerbot.llm.openai_client import build_client
from careerbot.chat.orchestrator import ChatOrchestrator
from careerbot.user_profile.loader import load_profile
from careerbot.user_profile.prompt import build_profile_context
from careerbot.tools.definitions import TOOLS


import gradio as gr

# Entry point to bring everything together and launch the app

def main():

    settings = load_settings()

    client = build_client(settings.openai_api_key)

    profile_data = load_profile(settings.summary_txt_path, settings.linkedin_pdf_path)

    profile_context = build_profile_context(profile_data=profile_data)

    system_message = {
        "role": "system",
        "content": [ 
            {
                "type": "input_text",
                "text": "You are careerbot, an AI designed to answer questions about my career, skills, and experience."
            }
        ]
    }

    orchestrator = ChatOrchestrator(client=client, model=settings.openai_model, system_message=system_message, profile_context=profile_context, tools=TOOLS, tool_results_dir=settings.tool_results_dir)

    app = gr.ChatInterface(fn=orchestrator)

    app.launch()

if __name__ == "__main__":
    main()
    