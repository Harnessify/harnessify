from __future__ import annotations

from pathlib import Path

from harnessify.core.run_store import read_json


def compare_versions(root: Path, base: str, candidate: str) -> dict:
    base_eval = read_json(root / "runs" / "support" / f"eval_summary_{base}.json")
    candidate_eval = read_json(root / "runs" / "support" / f"eval_summary_{candidate}.json")
    base_redteam = read_json(root / "runs" / "support" / f"redteam_summary_{base}.json")
    candidate_redteam = read_json(root / "runs" / "support" / f"redteam_summary_{candidate}.json")
    base_readiness = read_json(root / "runs" / "support" / f"readiness_report_{base}.json")
    candidate_readiness = read_json(root / "runs" / "support" / f"readiness_report_{candidate}.json")

    outcome = "inconclusive"
    if candidate_readiness["high_severity_failures"] > 0:
        outcome = "candidate_risky"
    elif candidate_readiness["recommendation"] == "reject":
        outcome = "candidate_risky"
    else:
        candidate_better_or_equal = (
            candidate_eval["pass_rate"] >= base_eval["pass_rate"]
            and candidate_redteam["pass_rate"] >= base_redteam["pass_rate"]
            and candidate_readiness["guardrail_violations"] <= base_readiness["guardrail_violations"]
            and candidate_readiness["high_severity_failures"] <= base_readiness["high_severity_failures"]
        )
        candidate_worse = (
            candidate_eval["pass_rate"] < base_eval["pass_rate"]
            or candidate_redteam["pass_rate"] < base_redteam["pass_rate"]
            or candidate_readiness["guardrail_violations"] > base_readiness["guardrail_violations"]
            or candidate_readiness["high_severity_failures"] > base_readiness["high_severity_failures"]
        )

        if candidate_better_or_equal and candidate_readiness["recommendation"] in {"approve", "approve_with_conditions"}:
            outcome = "candidate_improved"
        elif candidate_worse:
            outcome = "candidate_regressed"

    return {
        "outcome": outcome,
        "base": {
            "agent_version": base,
            "agent_impl": base_eval.get("agent_impl"),
            "adapter": base_eval.get("adapter"),
            "eval_pass_rate": base_eval["pass_rate"],
            "redteam_pass_rate": base_redteam["pass_rate"],
            "high_severity_failures": base_readiness["high_severity_failures"],
            "guardrail_violations": base_readiness["guardrail_violations"],
            "recommendation": base_readiness["recommendation"],
        },
        "candidate": {
            "agent_version": candidate,
            "agent_impl": candidate_eval.get("agent_impl"),
            "adapter": candidate_eval.get("adapter"),
            "eval_pass_rate": candidate_eval["pass_rate"],
            "redteam_pass_rate": candidate_redteam["pass_rate"],
            "high_severity_failures": candidate_readiness["high_severity_failures"],
            "guardrail_violations": candidate_readiness["guardrail_violations"],
            "recommendation": candidate_readiness["recommendation"],
        },
        "delta": {
            "eval_pass_rate": candidate_eval["pass_rate"] - base_eval["pass_rate"],
            "redteam_pass_rate": candidate_redteam["pass_rate"] - base_redteam["pass_rate"],
            "high_severity_failures": candidate_readiness["high_severity_failures"] - base_readiness["high_severity_failures"],
            "guardrail_violations": candidate_readiness["guardrail_violations"] - base_readiness["guardrail_violations"],
        },
    }
