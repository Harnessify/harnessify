from __future__ import annotations

from pathlib import Path

from harnessify.config import load_config
from harnessify.core.run_store import hash_file, relative_to_root, utc_now_iso, write_json
from harnessify.formats.schemas import AgentVersionManifest


def agent_manifest_path(root: Path, agent_version: str) -> Path:
    return root / "versions" / "agents" / f"{agent_version}.json"


def ensure_agent_version_manifest(root: Path, agent_version: str) -> AgentVersionManifest:
    path = agent_manifest_path(root, agent_version)
    if path.exists():
        return AgentVersionManifest.model_validate_json(path.read_text(encoding="utf-8"))

    config = load_config(root)
    policy_path = root / config.support.policy_path
    config_hash = hash_file(root / "hfy.yaml")
    policy_hash = hash_file(policy_path)
    manifest = AgentVersionManifest(
        agent_version=agent_version,
        runtime="deterministic_rules",
        provider="local",
        model=None,
        config_hash=config_hash,
        policy_hash=policy_hash,
        prompt_hash=None,
        created_at=utc_now_iso(),
        metadata={
            "domain": "support",
            "policy_path": relative_to_root(policy_path, root),
            "adapter": "callable_agent",
        },
    )
    write_json(path, manifest.model_dump())
    return manifest
