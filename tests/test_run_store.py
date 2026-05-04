from __future__ import annotations

from pathlib import Path

from harnessify.core.run_store import create_run_dir, read_json, write_json, write_jsonl


def test_run_store_writes_open_files(initialized_project: Path) -> None:
    run_dir = create_run_dir(initialized_project, "support", "case-1")
    payload = {"hello": "world"}

    write_json(run_dir / "payload.json", payload)
    write_jsonl(run_dir / "trace.jsonl", [{"event": "one"}, {"event": "two"}])

    assert read_json(run_dir / "payload.json") == payload
    assert (run_dir / "trace.jsonl").read_text(encoding="utf-8").count("\n") == 2
