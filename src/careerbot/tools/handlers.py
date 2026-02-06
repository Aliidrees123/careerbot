from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

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
def handle_record_user_details(args: dict, *, out_dir: Path) -> ToolResult:

    email = (args.get("email") or "").strip()

    if not email:
        return ToolResult(
            tool_name="record_user_details",
            ok=False,
            content="",
            error="Missing required field: email"
        )
    
    record = {
        "timestamp": _utc_now_iso(),
        "email": email,
        "name": (args.get("name") or "").strip() or None,
        "company": (args.get("company") or "").strip() or None,
        "notes": (args.get("notes") or "").strip() or None
    }

    _append_jsonl(out_dir / "user_details.jsonl", record)

    return ToolResult(
        tool_name="record_user_details",
        ok=True,
        content=json.dumps({"saved": True, "email": email}, ensure_ascii=False)
    )

# Handle record_unknown_question_tool
def handle_record_unknown_question(args: dict, *, out_dir: Path) -> ToolResult:
    
    question = (args.get("question") or "").strip()

    if not question:
        return ToolResult(
            tool_name="record_unknown_question",
            ok=False,
            content="",
            error="Missing required field: question"
        )
    
    record = {
        "timestamp": _utc_now_iso(),
        "question": question
    }

    _append_jsonl(out_dir / "unknown_question.jsonl", record)

    return ToolResult(
        tool_name="record_unknown_question",
        ok=True,
        content=json.dumps({"saved": True, "question": question}, ensure_ascii=False)
    )
    

# Handle record_role_interest_tool
def handle_record_role_interest(args: dict, *, out_dir: Path) -> ToolResult:
    
    title = (args.get("title") or "").strip()
    responsibilities = (args.get("responsibilities") or "").strip()

    if not title:
        return ToolResult(
            tool_name="record_role_interest",
            ok=False,
            content="",
            error="Missing required field: title"
        )
    
    if not responsibilities:
        return ToolResult(
            tool_name="record_role_interest",
            ok=False,
            content="",
            error="Missing required field: responsibilities"
        )
    
    record = {
        "timestamp": _utc_now_iso(),
        "title": title,
        "responsibilities": responsibilities,
        "company": (args.get("company") or "").strip() or None,
        "level": (args.get("level") or "").strip() or None,
        "salary": (args.get("salary") or "").strip() or None,
        "location": (args.get("location") or "").strip() or None,
        "notes": (args.get("notes") or "").strip() or None
    }

    _append_jsonl(out_dir / "role_interest.jsonl", record)

    return ToolResult(
        tool_name="record_role_interest",
        ok=True,
        content=json.dumps({"saved": True, "title": title, "responsibilities": responsibilities}, ensure_ascii=False)
    )

# Execute the tool
def execute_tool(tool_name: str, args: dict, *, out_dir: Path) -> ToolResult:
    
    handlers = {
        "record_user_details": handle_record_user_details,
        "record_unknown_question": handle_record_unknown_question,
        "record_role_interest": handle_record_role_interest
    }

    handler = handlers.get(tool_name)
    if handler is None:
        return ToolResult(
            tool_name=tool_name,
            ok=False,
            content="",
            error=f"Unknown tool: {tool_name}"
        )
    
    try:
        return handler(args=args, out_dir=out_dir)
    except Exception as e:
        return ToolResult(
            tool_name=tool_name,
            ok=False,
            content="",
            error=f"Tool execution failed: {type(e).__name__}: {e}"
        )