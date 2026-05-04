from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4

from harnessify.config import HarnessifyConfig, write_default_config


def utc_now() -> datetime:
    return datetime.now(UTC)


def utc_now_iso() -> str:
    return utc_now().isoformat()


def timestamp_slug() -> str:
    return utc_now().strftime("%Y%m%dT%H%M%S%fZ")


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def init_project(root: Path, config: HarnessifyConfig) -> None:
    ensure_directory(root / config.project.runs_dir)
    ensure_directory(root / config.project.versions_dir)
    ensure_directory(root / config.project.agents_dir)
    ensure_directory(root / config.project.versions_dir / "agents")
    write_default_config(root)


def hash_file(path: Path) -> str:
    if not path.exists():
        return hashlib.sha256(b"").hexdigest()
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def create_run_dir(root: Path, domain: str, case_id: str) -> Path:
    return ensure_directory(root / "runs" / domain / f"{timestamp_slug()}_{case_id}")


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[Any]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any] | str]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for row in rows:
        if isinstance(row, str):
            lines.append(row)
        else:
            lines.append(json.dumps(row, sort_keys=True))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def append_jsonl(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
    return path


def write_markdown(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def relative_to_root(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def new_run_id() -> str:
    return uuid4().hex
