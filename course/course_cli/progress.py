"""Tracks student progress in a JSON file at the course root."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRESS_FILE = ".course-progress.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(root: Path) -> dict[str, Any]:
    path = root / PROGRESS_FILE
    if not path.exists():
        return {"exercises": {}, "peeks": [], "started_at": _now()}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {"exercises": {}, "peeks": [], "started_at": _now()}


def save(root: Path, data: dict[str, Any]) -> None:
    path = root / PROGRESS_FILE
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def mark(
    root: Path,
    target: str,
    status: str,
    **extra: Any,
) -> dict[str, Any]:
    data = load(root)
    ex = data["exercises"].setdefault(target, {})
    ex["status"] = status
    ex["updated_at"] = _now()
    ex.update(extra)
    save(root, data)
    return data


def record_peek(
    root: Path,
    target: str,
    reason: str = "",
) -> dict[str, Any]:
    data = load(root)
    data.setdefault("peeks", []).append(
        {"target": target, "reason": reason, "at": _now()}
    )
    ex = data["exercises"].setdefault(target, {})
    ex["peeks"] = ex.get("peeks", 0) + 1
    ex["last_peek_at"] = _now()
    save(root, data)
    return data
