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
from harnessify.domains.support.schemas import EvalCase, RefundDecision, SupportTicket
from harnessify.domains.support.scorer import score_expected_behavior
from harnessify.formats.schemas import RunRecord, TraceEvent
from harnessify.formats.trace import serialize_trace_events


def load_eval_cases(root: Path) -> list[EvalCase]:
    config = load_config(root)
    cases_dir = root / config.support.eval_cases_dir
    cases: list[EvalCase] = []
    for path in sorted(cases_dir.glob("*.json")):
        cases.append(EvalCase.model_validate(read_json(path)))
    return cases


def run_support_eval(root: Path, agent_version: str) -> dict:
    config = load_config(root)
    policy = load_support_policy(root / config.support.policy_path)
    cases = load_eval_cases(root)

    run_results = []
    for case in cases:
        run_dir = create_run_dir(root, "support", case.id)
        run_id = new_run_id()
        ticket = SupportTicket.model_validate(case.ticket.model_dump())
        write_json(run_dir / "input.json", ticket.model_dump())

        agent_result = run_callable_agent(evaluate_ticket, ticket=ticket, policy=policy, run_id=run_id)
        decision = RefundDecision.model_validate(agent_result["decision"])
        write_json(run_dir / "output.json", decision.model_dump())

        score_result = score_expected_behavior(
            ticket=ticket,
            decision=decision,
            expected_behavior=case.expected_behavior,
            should_pass=case.should_pass,
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
            f"# {verdict}\n\n- Case: {case.id}\n- Score: {score_result['score']}\n- Reason: {score_result['reason']}\n",
        )

        run_record = RunRecord(
            run_id=run_id,
            domain="support",
            case_id=case.id,
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
        run_results.append(
            {
                "case_id": case.id,
                "run_dir": relative_to_root(run_dir, root),
                "score": score_result["score"],
                "passed": score_result["passed"],
                "reason": score_result["reason"],
                "guardrail_violations": score_payload["guardrail_violations"],
                "run_record": run_record.model_dump(),
            }
        )

    total_cases = len(run_results)
    passed_cases = sum(1 for result in run_results if result["passed"])
    guardrail_violations = sum(len(result["guardrail_violations"]) for result in run_results)
    summary = {
        "agent_version": agent_version,
        "kind": "eval",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "pass_rate": passed_cases / total_cases if total_cases else 0.0,
        "high_severity_failures": 0,
        "guardrail_violations": guardrail_violations,
        "results": run_results,
    }
    write_json(root / "runs" / "support" / f"eval_summary_{agent_version}.json", summary)
    return summary
