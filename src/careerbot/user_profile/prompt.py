from __future__ import annotations
from careerbot.user_profile.loader import ProfileData

def _fmt_list(items: list[str], *, prefix: str = "- ") -> str:
    cleaned = [x.strip() for x in items if isinstance(x, str) and x.strip()]
    return "\n".join(f"{prefix}{x}" for x in cleaned)

def _get_str(d: dict, key: str) -> str:
    v = d.get(key, "")
    if not isinstance(v, str):
        return ""
    return v.strip()

def _add_section_header(parts: list[str], title: str) -> None:
    parts.append(f"{title}")
    parts.append("")

def build_profile_context(profile_data: ProfileData) -> str | None:
    data = profile_data.data
    if not isinstance(data, dict) or not data:
        return None
    
    parts = []

    # Rules
    parts.append("PROFILE CONTEXT: Ali (source-of-truth)")
    parts.append("Rules:")
    parts.append("- Use this information to answer questions about Ali's career, skills, and experience.")
    parts.append("- Speak in third person about Ali.")
    parts.append("- Summarise and paraphrase; do not quote long passages verbatim.")
    parts.append("- Do not invent details. If something is not stated here, say it is not documented.")
    parts.append("- Do not reveal this raw profile context to the user; provide a clean summary instead.")
    parts.append("")

    # Overview
    overview = data.get("overview", {})
    if isinstance(overview, dict) and overview:
        _add_section_header(parts, "Overview")
        summary = _get_str(overview, "summary")
        current_role = _get_str(overview, _get_str)
        location = _get_str(overview, "location")
        career_focus = _get_str(overview, "career_focus")

        if summary:
            parts.append(f"- Summary: {summary}")
        if current_role:
            parts.append(f"- Current role: {current_role}")
        if location:
            parts.append(f"- Location: {location}")
        if career_focus:
            parts.append(f"- Career focus: {career_focus}")
        parts.append("")

    # Experience
    experience = data.get("experience", {})
    if isinstance(experience, dict) and experience:
        _add_section_header(parts, "Experience")

        for role_key, role in experience.items():
            if not isinstance(role, dict):
                continue

            title = _get_str(role, "title")
            company = _get_str(role, "company")
            start = _get_str(role, "start_date")
            end = _get_str(role, "end_date")
            role_summary = _get_str(role, "summary")

            # Get role title and company else use key
            header_bits = [x for x in [title, company] if x]
            header = " — ".join(header_bits) if header_bits else role_key

            date_bits = [x for x in [start, end] if x]
            dates = " to ".join(date_bits) if date_bits else ""

            parts.append(f"{header}" + (f" ({dates})" if dates else ""))

            if role_summary:
                parts.append(f"Summary: {role_summary}")

            highlights = role.get("highlights", [])
            if isinstance(highlights, list) and highlights:
                parts.append("Highlights:")
                parts.append(_fmt_list([str(x) for x in highlights]))

            technologies = role.get("technologies", [])
            if isinstance(technologies, list) and technologies:
                parts.append("Technologies:")
                parts.append(_fmt_list([str(x) for x in technologies]))

            parts.append("")  # spacer between roles

        parts.append("")

    # Projects
    projects = data.get("projects", {})
    if isinstance(projects, dict) and projects:
        _add_section_header(parts, "Projects")

        for project_key, proj in projects.items():
            if not isinstance(proj, dict):
                continue

            proj_summary = _get_str(proj, "summary")
            problem = _get_str(proj, "problem_solved")
            impact = _get_str(proj, "impact")

            parts.append(f"{project_key}:")

            if proj_summary:
                parts.append(f"Summary: {proj_summary}")
            if problem:
                parts.append(f"Problem solved: {problem}")

            arch = proj.get("architecture", [])
            if isinstance(arch, list) and arch:
                parts.append("Architecture:")
                parts.append(_fmt_list([str(x) for x in arch]))

            technologies = proj.get("technologies", [])
            if isinstance(technologies, list) and technologies:
                parts.append("Technologies:")
                parts.append(_fmt_list([str(x) for x in technologies]))

            if impact:
                parts.append(f"Impact: {impact}")

            parts.append("")

        parts.append("")

    # Skills
    skills = data.get("skills", {})
    if isinstance(skills, dict) and skills:
        _add_section_header(parts, "Skills")

        # Skills are grouped; we only print groups that have content.
        for group_name, items in skills.items():
            if not isinstance(items, list) or not items:
                continue

            clean_items = [str(x).strip() for x in items if str(x).strip()]
            if not clean_items:
                continue

            pretty_name = group_name.replace("_", " ").title()
            parts.append(f"{pretty_name}:")
            parts.append(_fmt_list(clean_items))
            parts.append("")

        parts.append("")

    # Education
    education = data.get("education", {})
    if isinstance(education, dict) and education:
        _add_section_header(parts, "Education")

        for edu_key, edu in education.items():
            if not isinstance(edu, dict):
                continue

            degree = _get_str(edu, "degree")
            institution = _get_str(edu, "institution")
            focus = _get_str(edu, "focus")
            thesis = _get_str(edu, "thesis")

            header_bits = [x for x in [degree, institution] if x]
            header = " — ".join(header_bits) if header_bits else edu_key
            parts.append(header)

            if focus:
                parts.append(f"Focus: {focus}")

            modules = edu.get("key_modules", [])
            if isinstance(modules, list) and modules:
                parts.append("Key modules:")
                parts.append(_fmt_list([str(x) for x in modules]))

            if thesis:
                parts.append(f"Thesis: {thesis}")

            parts.append("")

        parts.append("")

    # Certifications
    certs = data.get("certifications", [])
    if isinstance(certs, list) and certs:
        _add_section_header(parts, "Certifications")
        parts.append(_fmt_list([str(x) for x in certs]))
        parts.append("")

    # Preferences
    preferences = data.get("preferences", {})
    if isinstance(preferences, dict) and preferences:
        _add_section_header(parts, "Preferences")

        roles_targeted = preferences.get("roles_targeted", [])
        if isinstance(roles_targeted, list) and roles_targeted:
            parts.append("Roles targeted:")
            parts.append(_fmt_list([str(x) for x in roles_targeted]))
            parts.append("")

        location_prefs = preferences.get("location_preferences", [])
        if isinstance(location_prefs, list) and location_prefs:
            parts.append("Location preferences:")
            parts.append(_fmt_list([str(x) for x in location_prefs]))
            parts.append("")

        working_style = _get_str(preferences, "working_style")
        if working_style:
            parts.append(f"- Working style: {working_style}")
            parts.append("")

    parts.append("END PROFILE CONTEXT")

    # Return result
    content = "\n".join(parts).strip()
    return content if content else None