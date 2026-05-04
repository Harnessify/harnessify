from __future__ import annotations

import json
from pathlib import Path

from harnessify.core.run_store import utc_now_iso
from harnessify.domains.support.policy import load_support_policy
from harnessify.domains.support.schemas import RefundDecision, SupportTicket


def evaluate_ticket(ticket: SupportTicket, policy: dict, run_id: str) -> tuple[dict, list[dict]]:
    trace = [
        {
            "event_id": f"{run_id}-input",
            "run_id": run_id,
            "timestamp": utc_now_iso(),
            "event_type": "input_loaded",
            "actor": "demo_agent",
            "payload": ticket.model_dump(),
        },
        {
            "event_id": f"{run_id}-policy",
            "run_id": run_id,
            "timestamp": utc_now_iso(),
            "event_type": "policy_loaded",
            "actor": "demo_agent",
            "payload": policy,
        },
    ]

    decision = "escalate"
    refund_amount = min(ticket.order_total, ticket.order_total)
    needs_human_review = True
    reason = "A support specialist needs to review this request."

    if ticket.prior_refunds_90d >= 2:
        decision = "escalate"
        needs_human_review = True
        reason = "A support specialist needs to review this request because of account history."
        refund_amount = min(ticket.order_total, ticket.order_total)
    elif ticket.refund_reason == "changed_mind" and ticket.days_since_delivery > 14:
        decision = "deny"
        refund_amount = 0.0
        needs_human_review = False
        reason = "This request does not qualify for a refund after the review window."
    elif ticket.refund_reason == "damaged_item" and ticket.days_since_delivery <= 14:
        if ticket.order_total > 50:
            decision = "escalate"
            refund_amount = min(ticket.order_total, ticket.order_total)
            needs_human_review = True
            reason = "A support specialist needs to review this damaged-item refund request."
        else:
            decision = "approve"
            refund_amount = min(ticket.order_total, ticket.order_total)
            needs_human_review = False
            reason = "This damaged-item request qualifies for a refund."
    elif ticket.refund_reason == "late_delivery":
        if ticket.order_total > 50:
            decision = "escalate"
            refund_amount = min(ticket.order_total, ticket.order_total)
            needs_human_review = True
            reason = "A support specialist needs to review this late-delivery refund request."
        else:
            decision = "approve"
            refund_amount = min(ticket.order_total, ticket.order_total)
            needs_human_review = False
            reason = "This late-delivery request qualifies for a refund review outcome."
    else:
        decision = "escalate"
        refund_amount = min(ticket.order_total, ticket.order_total)
        needs_human_review = True
        reason = "A support specialist needs to review this request."

    result = RefundDecision(
        decision=decision,
        refund_amount=refund_amount,
        needs_human_review=needs_human_review,
        reason=reason,
    )
    trace.append(
        {
            "event_id": f"{run_id}-decision",
            "run_id": run_id,
            "timestamp": utc_now_iso(),
            "event_type": "decision_computed",
            "actor": "demo_agent",
            "payload": result.model_dump(),
        }
    )
    return result.model_dump(), trace


def run_from_files(input_path: Path, policy_path: Path, output_path: Path, run_id: str = "file-run") -> Path:
    ticket = SupportTicket.model_validate(json.loads(input_path.read_text(encoding="utf-8")))
    policy = load_support_policy(policy_path)
    decision, _trace = evaluate_ticket(ticket=ticket, policy=policy, run_id=run_id)
    output_path.write_text(json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8")
    return output_path
