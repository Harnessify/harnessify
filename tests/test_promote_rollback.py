from __future__ import annotations

import json

from harnessify.cli import build_readiness_report
from harnessify.core.evaluator import run_support_eval
from harnessify.core.promote import promote_support_agent
from harnessify.core.redteam import run_support_redteam
from harnessify.core.rollback import rollback_support_agent
from harnessify.core.run_store import write_json


def test_promote_and_rollback_write_expected_manifests(initialized_project) -> None:
    run_support_eval(initialized_project, "v1")
    run_support_redteam(initialized_project, "v1")
    report = build_readiness_report(initialized_project, "v1")
    write_json(
        initialized_project / "runs" / "support" / "readiness_report_v1.json",
        report.model_dump(),
    )

    manifest = promote_support_agent(initialized_project, "v1", "production")
    assert manifest.agent_version == "v1"
    assert (initialized_project / "versions" / "production.json").exists()

    event = rollback_support_agent(initialized_project, "v1", "production")
    assert event["to_agent_version"] == "v1"
    rollback_lines = (
        initialized_project / "versions" / "rollback_event.jsonl"
    ).read_text(encoding="utf-8").strip().splitlines()
    assert len(rollback_lines) == 1
    payload = json.loads(rollback_lines[0])
    assert payload["env"] == "production"
