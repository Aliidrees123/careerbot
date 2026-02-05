# Loads .env variables and centralises settings

import os
from dotenv import load_dotenv
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    summary_txt_path: Path
    linkedin_pdf_path: Path
    debug: bool

def _parse_bool_env(name:str) -> bool:
    value = os.getenv(name, "")
    return value.strip().lower() == "true"
    
def load_settings() -> Settings:
    load_dotenv(override=True)

    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "data"

    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    openai_model = os.getenv("OPENAI_MODEL", "gpt-5-mini").strip()

    summary_txt_path = data_dir / "summary.txt"
    linkedin_pdf_path = data_dir / "linkedin.pdf"

    debug = _parse_bool_env("CAREERBOT_DEBUG")

    if not openai_api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")
    
    if not summary_txt_path.exists():
        raise RuntimeError(f"Missing summary.txt at {summary_txt_path}")
    
    if not linkedin_pdf_path.exists():
        raise RuntimeError(f"Missing linkedin.pdf at {linkedin_pdf_path}")

    return Settings(
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        summary_txt_path=summary_txt_path,
        linkedin_pdf_path=linkedin_pdf_path
    )


