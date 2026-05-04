from __future__ import annotations

import subprocess
from pathlib import Path


from harnessify.core.run_store import read_json, read_jsonl


def shell_agent_status() -> dict[str, str]:
    return {
        "available": "true",
        "message": "Shell adapter can execute a local agent command and recover output from open files.",
    }


def run_shell_agent(command: list[str], output_path: Path, trace_path: Path) -> dict:
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return {
        "decision": read_json(output_path),
        "trace": read_jsonl(trace_path),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
