from __future__ import annotations

from pathlib import Path

from harnessify.config import load_config
from harnessify.core.run_store import hash_file, read_json, utc_now_iso, write_json
from harnessify.formats.schemas import ProductionManifest
from harnessify.integrations.git_repo import get_git_commit


def promote_support_agent(root: Path, agent_version: str, env: str) -> ProductionManifest:
    config = load_config(root)
    eval_summary_path = root / "runs" / "support" / f"eval_summary_{agent_version}.json"
    redteam_summary_path = root / "runs" / "support" / f"redteam_summary_{agent_version}.json"
    readiness_report_path = root / "runs" / "support" / f"readiness_report_{agent_version}.json"
    production_path = root / "versions" / f"{env}.json"

    previous_agent_version = None
    if production_path.exists():
        previous_agent_version = read_json(production_path).get("agent_version")

    manifest = ProductionManifest(
        env=env,
        agent_version=agent_version,
        promoted_at=utc_now_iso(),
        config_hash=hash_file(root / "hfy.yaml"),
        policy_hash=hash_file(root / config.support.policy_path),
        eval_summary_path=str(eval_summary_path.relative_to(root)),
        redteam_summary_path=str(redteam_summary_path.relative_to(root)),
        readiness_report_path=str(readiness_report_path.relative_to(root)),
        git_commit=get_git_commit(root),
        previous_agent_version=previous_agent_version,
    )
    write_json(production_path, manifest.model_dump())
    return manifest
