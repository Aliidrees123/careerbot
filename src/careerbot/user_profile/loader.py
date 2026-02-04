from dataclasses import dataclass
from pypdf import PdfReader

# Reads extrernal data and returns raw strings

@dataclass
class ProfileData:
    summary_text: str | None
    linkedin_text: str | None

def _read_summary_text(file_path: str) -> str | None:
    with open (file_path, "r", encoding="utf-8") as f:
        summary_text = f.read().strip()

    if not summary_text:
        return None

    return summary_text

def _read_linkedin_data(file_path: str) -> str | None:
    reader = PdfReader(file_path)
    linkedin_summary = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin_summary += text

    linkedin_summary = linkedin_summary.strip()
    if linkedin_summary == "":
        return None
        
    return linkedin_summary

def load_profile(summary_file_path: str, linkedin_file_path: str) -> ProfileData:
    summary_text = _read_summary_text(summary_file_path)
    linkedin_text = _read_linkedin_data(linkedin_file_path)

    return ProfileData(summary_text=summary_text, linkedin_text=linkedin_text)