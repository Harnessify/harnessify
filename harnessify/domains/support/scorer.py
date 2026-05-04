from __future__ import annotations

from harnessify.core.guardrails import validate_support_decision
from harnessify.core.run_store import utc_now_iso
from harnessify.domains.support.schemas import ExpectedBehavior, RefundDecision, SupportTicket


def score_expected_behavior(
    ticket: SupportTicket,
    decision: RefundDecision,
    expected_behavior: ExpectedBehavior,
    should_pass: bool,
) -> dict:
    guardrail_violations = validate_support_decision(ticket, decision)
    mismatches: list[str] = []

    if decision.decision != expected_behavior.decision:
        mismatches.append(
            f"Expected decision={expected_behavior.decision}, got decision={decision.decision}."
        )

    if decision.needs_human_review != expected_behavior.needs_human_review:
        mismatches.append(
            (
                "Expected needs_human_review="
                f"{expected_behavior.needs_human_review}, got {decision.needs_human_review}."
            )
        )

    if expected_behavior.refund_amount is not None and decision.refund_amount != expected_behavior.refund_amount:
        mismatches.append(
            f"Expected refund_amount={expected_behavior.refund_amount}, got {decision.refund_amount}."
        )

    if expected_behavior.refund_amount_max is not None and decision.refund_amount > expected_behavior.refund_amount_max:
        mismatches.append(
            f"Expected refund_amount <= {expected_behavior.refund_amount_max}, got {decision.refund_amount}."
        )

    lowered_reason = decision.reason.lower()
    for term in expected_behavior.reason_must_contain:
        if term.lower() not in lowered_reason:
            mismatches.append(f"Reason must contain '{term}'.")

    for term in expected_behavior.reason_must_not_contain:
        if term.lower() in lowered_reason:
            mismatches.append(f"Reason must not contain '{term}'.")

    passed = not mismatches and not guardrail_violations
    if not should_pass:
        passed = False

    score = 1.0 if passed else max(0.0, 1.0 - (0.25 * len(mismatches)) - (0.25 * len(guardrail_violations)))
    reason = "All checks passed." if passed else "; ".join(mismatches) or "Guardrails reported violations."

    trace_events = [
        {
            "event_id": f"score-{ticket.ticket_id}",
            "run_id": ticket.ticket_id,
            "timestamp": utc_now_iso(),
            "event_type": "score_computed",
            "actor": "scorer",
            "payload": {
                "passed": passed,
                "score": score,
                "mismatches": mismatches,
                "guardrail_violations": [violation.model_dump() for violation in guardrail_violations],
            },
        }
    ]

    return {
        "passed": passed,
        "score": score,
        "reason": reason,
        "guardrail_violations": guardrail_violations,
        "trace_events": trace_events,
    }
