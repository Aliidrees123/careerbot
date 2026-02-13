from __future__ import annotations
from careerbot.user_profile.loader import ProfileData

# Build the profile context using external data

def build_profile_context(profile_data: ProfileData) -> str | None:
    summary = profile_data.summary_text
    linkedin = profile_data.linkedin_text

    if not summary and not linkedin:
        return None

    parts: list[str] = []
    parts.append("PROFILE CONTEXT: Ali (source-of-truth)")
    parts.append("Rules:")
    parts.append("- Use this information to answer questions about Ali's career, skills, and experience.")
    parts.append("- Speak in third person about Ali.")
    parts.append("- Summarise and paraphrase; do not quote long passages verbatim.")
    parts.append("- Do not invent details. If something is not stated here, say it is not documented in the current profile context.")
    parts.append("- Do not reveal this raw profile context to the user; provide a clean summary instead.")
    parts.append("")

    if summary:
        parts.append("Summary (curated):")
        parts.append(summary)
        parts.append("")

    if linkedin:
        parts.append("LinkedIn extract (raw text):")
        parts.append(linkedin)
        parts.append("")

    parts.append("END PROFILE CONTEXT")

    return "\n".join(parts)