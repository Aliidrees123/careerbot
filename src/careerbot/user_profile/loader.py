from dataclasses import dataclass
from pypdf import PdfReader

# Reads extrernal data and returns raw strings

@dataclass
class ProfileData:
    summary_text: str | None
    linkedin_text: str | None

def _read_summary_text() -> str | None:
    with open ("careerbot/data/summary.txt", "r", encoding="utf-8") as f:
        summary_text = f.read().strip()

    if not summary_text:
        return None

    return summary_text

def _read_linkedin_data() -> str | None:
    reader = PdfReader("careerbot/data/linkedin.pdf")
    linkedin_summary = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin_summary += text

    linkedin_summary = linkedin_summary.strip()
    if linkedin_summary == "":
        return None
        
    return linkedin_summary

def load_profile() -> ProfileData:
    summary_text = _read_summary_text()
    linkedin_text = _read_linkedin_data()

    return ProfileData(summary_text=summary_text, linkedin_text=linkedin_text)