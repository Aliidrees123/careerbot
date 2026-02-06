from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Executes tool calls based on LLM requests

@dataclass(frozen=True)
class ToolResult:
    tool_name: str
    ok: bool
    content: str
    error: str | None = None

# Append a JSON object into a JSONL file
def _append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# Get current time
def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

# Handle record_user_details_tool
