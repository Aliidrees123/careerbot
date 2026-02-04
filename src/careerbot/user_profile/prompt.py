from __future__ import annotations
from careerbot.user_profile.loader import ProfileData

# Build the profile context using external data

def build_profile_context(profile_data: ProfileData) -> str | None:
    summary = profile_data.summary_text
    linkedin = profile_data.linkedin_text

    if not summary and not linkedin:
        return None

    parts: list[str] = [
        "This is background information on the individual whose career, skills, and experience you will be talking about."
    ]
    if summary:
        parts.append(f"You can find a custom written summary of their experience here: {summary}.")
    if linkedin:
        parts.append(f"You can find information from the individual's LinkedIn here: {linkedin}.")

    return "\n".join(parts)