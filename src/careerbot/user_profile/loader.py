from dataclasses import dataclass
from pathlib import Path
import json

# Reads extrernal data and returns raw strings

@dataclass
class ProfileData:
    data: dict


def _read_json(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Profile store not found: {p}")

    with p.open("r", encoding="utf8") as f:
        return json.load(f)

def load_profile(profile_store_path: str) -> ProfileData:
    data = _read_json(profile_store_path)
    if not isinstance(data, dict):
        raise ValueError(f"profile_store.json must contain a JSON object at the top level")

    return ProfileData(data=data)