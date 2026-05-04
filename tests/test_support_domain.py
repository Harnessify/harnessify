from __future__ import annotations

import json
from pathlib import Path

from harnessify.core.evaluator import load_eval_cases
from harnessify.domains.support.demo_agent import run_from_files
from harnessify.domains.support.policy import load_support_policy
from harnessify.domains.support.schemas import RefundDecision, SupportTicket


def test_support_eval_cases_load(initialized_project: Path) -> None:
    cases = load_eval_cases(initialized_project)

    assert len(cases) == 4
    assert {case.id for case in cases} == {
        "damaged_item",
        "late_delivery",
        "suspicious_refund",
        "prompt_injection_refund",
    }


def test_demo_agent_outputs_valid_schema(initialized_project: Path) -> None:
    ticket = SupportTicket(
        ticket_id="demo-1",
        customer_tier="standard",
        order_total=25,
        refund_reason="damaged_item",
        days_since_delivery=3,
        prior_refunds_90d=0,
        customer_message="My item was damaged.",
    )
    input_path = initialized_project / "ticket.json"
    output_path = initialized_project / "refund_decision.json"
    input_path.write_text(json.dumps(ticket.model_dump()), encoding="utf-8")

    run_from_files(
        input_path=input_path,
        policy_path=initialized_project / "harnessify" / "domains" / "support" / "policies" / "refund_policy.yaml",
        output_path=output_path,
    )

    decision = RefundDecision.model_validate(json.loads(output_path.read_text(encoding="utf-8")))
    assert decision.decision == "approve"
    assert decision.refund_amount == 25
