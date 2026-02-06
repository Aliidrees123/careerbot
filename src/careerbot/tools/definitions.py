# Defines tools and their JSON schemas for the LLM
record_user_details_tool = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
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
    "name": "record_unknown_question",
    "description": "Use this tool to record any question that couldn't be answered because you did not know the answer",
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
    "name": "record_role_interest",
    "description": "Use this tool when a user indicates they are actively hiring for a role and provides details about it",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the job being hired for"
            },
            "company": {
                "type": "string",
                "description": "The name of the company the role is for, if the user provided it"
            },
            "level": {
                "type": "string",
                "description": "The level of experience required for the role, if the user provided it"
            },
            "responsibilities": {
                "type": "string",
                "description": "A brief overview of the key responsibilities, if the user provided it"
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
        "required": ["title", "responsibilities"],
        "additionalProperties": False
    }
}

TOOLS = [record_role_interest_tool, record_unknown_question_tool, record_user_details_tool]
