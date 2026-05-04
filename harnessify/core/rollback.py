from __future__ import annotations

from pathlib import Path

from harnessify.core.run_store import append_jsonl, read_json, utc_now_iso, write_json


def rollback_support_agent(root: Path, to_agent_version: str, env: str, reason: str = "manual rollback") -> dict:
    production_path = root / "versions" / f"{env}.json"
    if not production_path.exists():
        raise FileNotFoundError(f"Production manifest not found for env={env}")

    manifest = read_json(production_path)
    from_agent_version = manifest.get("agent_version")
    manifest["agent_version"] = to_agent_version
    manifest["previous_agent_version"] = from_agent_version
    manifest["promoted_at"] = utc_now_iso()
    write_json(production_path, manifest)

    event = {
        "env": env,
        "from_agent_version": from_agent_version,
        "to_agent_version": to_agent_version,
        "rolled_back_at": utc_now_iso(),
        "reason": reason,
    }
    append_jsonl(root / "versions" / "rollback_event.jsonl", event)
    return event
