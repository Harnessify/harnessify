from __future__ import annotations

from harnessify.formats.schemas import (
    AgentVersionManifest,
    GuardrailViolation,
    ProductionManifest,
    ReadinessReport,
    RunRecord,
    TraceEvent,
)


def test_open_format_models_validate() -> None:
    violation = GuardrailViolation(
        type="refund_amount_exceeds_order_total",
        severity="high",
        message="Refund amount exceeds the order total.",
        evidence={"refund_amount": 100, "order_total": 50},
    )
    trace = TraceEvent(
        event_id="evt-1",
        run_id="run-1",
        timestamp="2026-05-03T00:00:00Z",
        event_type="decision_computed",
        actor="demo_agent",
        payload={"decision": "approve"},
    )
    run = RunRecord(
        run_id="run-1",
        domain="support",
        case_id="damaged_item",
        agent_version="v1",
        adapter="callable_agent",
        input_path="runs/support/input.json",
        output_path="runs/support/output.json",
        score=1.0,
        passed=True,
        guardrail_violations=[violation],
        trace_path="runs/support/trace.jsonl",
        created_at="2026-05-03T00:00:00Z",
    )
    manifest = AgentVersionManifest(
        agent_version="v1",
        config_hash="abc",
        policy_hash="def",
        created_at="2026-05-03T00:00:00Z",
        metadata={"domain": "support"},
    )
    readiness = ReadinessReport(
        agent_version="v1",
        eval_pass_rate=1.0,
        redteam_pass_rate=1.0,
        high_severity_failures=0,
        guardrail_violations=0,
        recommendation="approve",
        reasons=["Thresholds met."],
    )
    production = ProductionManifest(
        env="production",
        agent_version="v1",
        promoted_at="2026-05-03T00:00:00Z",
        config_hash="abc",
        policy_hash="def",
        eval_summary_path="runs/support/eval_summary_v1.json",
        redteam_summary_path="runs/support/redteam_summary_v1.json",
        readiness_report_path="runs/support/readiness_report_v1.json",
    )

    assert trace.payload["decision"] == "approve"
    assert run.guardrail_violations[0].severity == "high"
    assert manifest.metadata["domain"] == "support"
    assert readiness.recommendation == "approve"
    assert production.env == "production"
