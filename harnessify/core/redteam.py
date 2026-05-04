from __future__ import annotations

from pathlib import Path

from harnessify.adapters.callable_agent import run_callable_agent
from harnessify.config import load_config
from harnessify.core.run_store import (
    create_run_dir,
    new_run_id,
    read_json,
    relative_to_root,
    write_json,
    write_jsonl,
    write_markdown,
)
from harnessify.domains.support.demo_agent import evaluate_ticket
from harnessify.domains.support.policy import load_support_policy
from harnessify.domains.support.schemas import RedteamProbe, RefundDecision, SupportTicket
from harnessify.domains.support.scorer import score_expected_behavior
from harnessify.formats.schemas import RunRecord, TraceEvent
from harnessify.formats.trace import serialize_trace_events
import yaml


def load_redteam_probes(root: Path) -> list[RedteamProbe]:
    config = load_config(root)
    data = yaml.safe_load((root / config.support.redteam_path).read_text(encoding="utf-8")) or {}
    probes = data.get("probes", [])
    return [RedteamProbe.model_validate(probe) for probe in probes]


def run_support_redteam(root: Path, agent_version: str) -> dict:
    config = load_config(root)
    policy = load_support_policy(root / config.support.policy_path)
    probes = load_redteam_probes(root)

    results = []
    for probe in probes:
        run_dir = create_run_dir(root, "support", probe.id)
        run_id = new_run_id()
        ticket = SupportTicket.model_validate(probe.ticket.model_dump())
        write_json(run_dir / "input.json", ticket.model_dump())

        agent_result = run_callable_agent(evaluate_ticket, ticket=ticket, policy=policy, run_id=run_id)
        decision = RefundDecision.model_validate(agent_result["decision"])
        write_json(run_dir / "output.json", decision.model_dump())

        score_result = score_expected_behavior(
            ticket=ticket,
            decision=decision,
            expected_behavior=probe.expected_behavior,
            should_pass=probe.should_pass,
        )
        score_payload = {
            "passed": score_result["passed"],
            "score": score_result["score"],
            "reason": score_result["reason"],
            "guardrail_violations": [violation.model_dump() for violation in score_result["guardrail_violations"]],
        }
        write_json(run_dir / "score.json", score_payload)
        write_json(
            run_dir / "guardrail_violations.json",
            [violation.model_dump() for violation in score_result["guardrail_violations"]],
        )

        trace_events = [
            TraceEvent.model_validate(event)
            for event in agent_result["trace"] + score_result["trace_events"]
        ]
        write_jsonl(run_dir / "trace.jsonl", serialize_trace_events(trace_events))
        verdict = "PASS" if score_result["passed"] else "FAIL"
        write_markdown(
            run_dir / "verdict.md",
            (
                f"# {verdict}\n\n- Probe: {probe.id}\n- Category: {probe.category}\n"
                f"- Severity: {probe.severity}\n- Score: {score_result['score']}\n- Reason: {score_result['reason']}\n"
            ),
        )

        run_record = RunRecord(
            run_id=run_id,
            domain="support",
            case_id=probe.id,
            agent_version=agent_version,
            adapter="callable_agent",
            runtime="deterministic_rules",
            provider="local",
            input_path=relative_to_root(run_dir / "input.json", root),
            output_path=relative_to_root(run_dir / "output.json", root),
            score=score_result["score"],
            passed=score_result["passed"],
            guardrail_violations=score_result["guardrail_violations"],
            trace_path=relative_to_root(run_dir / "trace.jsonl", root),
            created_at=agent_result["created_at"],
        )
        results.append(
            {
                "probe_id": probe.id,
                "category": probe.category,
                "severity": probe.severity,
                "run_dir": relative_to_root(run_dir, root),
                "score": score_result["score"],
                "passed": score_result["passed"],
                "reason": score_result["reason"],
                "guardrail_violations": score_payload["guardrail_violations"],
                "run_record": run_record.model_dump(),
            }
        )

    total = len(results)
    passed = sum(1 for result in results if result["passed"])
    high_severity_failures = sum(
        1 for result in results if not result["passed"] and result["severity"] == "high"
    )
    guardrail_violations = sum(len(result["guardrail_violations"]) for result in results)
    summary = {
        "agent_version": agent_version,
        "kind": "redteam",
        "total_cases": total,
        "passed_cases": passed,
        "pass_rate": passed / total if total else 0.0,
        "high_severity_failures": high_severity_failures,
        "guardrail_violations": guardrail_violations,
        "results": results,
    }
    write_json(root / "runs" / "support" / f"redteam_summary_{agent_version}.json", summary)
    return summary
