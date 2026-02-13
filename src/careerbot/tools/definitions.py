# Defines tools and their JSON schemas for the LLM
record_user_details_tool = {
    "type": "function",
    "name": "record_user_details",
    "description": "Record contact details when the user provides an email address or clearly invites Ali to follow up. Use only information the user explicitly provided (do not guess missing fields).",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The user's email address"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "company": {
                "type": "string",
                "description": "The company the user works for, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that can provide context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_tool = {
    "type": "function",
    "name": "record_unknown_question",    
    "description":  "Record a question about Ali that you cannot answer from the provided profile context and conversation. Use this only after asking at most one brief clarifying question if it would help.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

record_role_interest_tool = {
    "type": "function",
    "name": "record_role_interest",
    "description": "Record hiring intent when the user indicates they are hiring for a role and provides any role details (at minimum the job title). Use only details explicitly stated by the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the job being hired for"
            },
            "responsibilities": {
                "type": "string",
                "description": "A brief overview of the key responsibilities, if the user provided it"
            },
            "company": {
                "type": "string",
                "description": "The name of the company the role is for, if the user provided it"
            },
            "level": {
                "type": "string",
                "description": "The level of experience required for the role, if the user provided it"
            },
            "salary": {
                "type": "string",
                "description": "The salary range of the role, if the user provided it"
            },
            "location": {
                "type": "string",
                "description": "The role location and number of days in office/remote, if the user provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the role that can provide context, if the user provided it" 
            }
        },
        "required": ["title"],
        "additionalProperties": False
    },
}

TOOLS = [record_role_interest_tool, record_unknown_question_tool, record_user_details_tool]
