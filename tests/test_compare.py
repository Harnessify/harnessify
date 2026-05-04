from __future__ import annotations

from harnessify.core.compare import compare_versions
from harnessify.core.run_store import write_json


def test_compare_identifies_risky_candidate(initialized_project) -> None:
    write_json(
        initialized_project / "runs" / "support" / "eval_summary_v1.json",
        {"pass_rate": 1.0, "guardrail_violations": 0, "agent_impl": "deterministic_v1", "adapter": "callable"},
    )
    write_json(
        initialized_project / "runs" / "support" / "redteam_summary_v1.json",
        {"pass_rate": 1.0, "high_severity_failures": 0, "guardrail_violations": 0},
    )
    write_json(
        initialized_project / "runs" / "support" / "readiness_report_v1.json",
        {
            "guardrail_violations": 0,
            "high_severity_failures": 0,
            "recommendation": "approve",
        },
    )

    write_json(
        initialized_project / "runs" / "support" / "eval_summary_v2.json",
        {"pass_rate": 0.8, "guardrail_violations": 2, "agent_impl": "bad_candidate_v2", "adapter": "callable"},
    )
    write_json(
        initialized_project / "runs" / "support" / "redteam_summary_v2.json",
        {"pass_rate": 0.6, "high_severity_failures": 1, "guardrail_violations": 3},
    )
    write_json(
        initialized_project / "runs" / "support" / "readiness_report_v2.json",
        {
            "guardrail_violations": 5,
            "high_severity_failures": 1,
            "recommendation": "reject",
        },
    )

    comparison = compare_versions(initialized_project, "v1", "v2")

    assert comparison["outcome"] == "candidate_risky"
    assert comparison["candidate"]["agent_impl"] == "bad_candidate_v2"
    assert comparison["delta"]["guardrail_violations"] == 5
