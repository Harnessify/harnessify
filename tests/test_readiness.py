from __future__ import annotations

from pathlib import Path

from harnessify.cli import build_readiness_report
from harnessify.core.evaluator import run_support_eval
from harnessify.core.redteam import run_support_redteam
from harnessify.core.run_store import read_json, write_json


def test_eval_and_redteam_summaries_and_readiness(initialized_project: Path) -> None:
    eval_summary = run_support_eval(initialized_project, "v1")
    redteam_summary = run_support_redteam(initialized_project, "v1")

    assert eval_summary["pass_rate"] == 1.0
    assert redteam_summary["pass_rate"] == 1.0

    report = build_readiness_report(initialized_project, "v1")
    write_json(
        initialized_project / "runs" / "support" / "readiness_report_v1.json",
        report.model_dump(),
    )

    assert report.recommendation == "approve"
    assert report.high_severity_failures == 0
    assert read_json(initialized_project / "runs" / "support" / "eval_summary_v1.json")["passed_cases"] == 4
