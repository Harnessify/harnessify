from __future__ import annotations

from harnessify.core.guardrails import validate_support_decision
from harnessify.domains.support.schemas import RefundDecision, SupportTicket


def test_guardrails_catch_refund_above_order_total() -> None:
    ticket = SupportTicket(
        ticket_id="g-1",
        customer_tier="standard",
        order_total=20,
        refund_reason="damaged_item",
        days_since_delivery=2,
        prior_refunds_90d=0,
        customer_message="Please help.",
    )
    decision = RefundDecision(
        decision="approve",
        refund_amount=25,
        needs_human_review=False,
        reason="This qualifies for a refund.",
    )

    violations = validate_support_decision(ticket, decision)
    assert any(violation.type == "refund_amount_exceeds_order_total" for violation in violations)


def test_guardrails_catch_execution_claim_language() -> None:
    ticket = SupportTicket(
        ticket_id="g-2",
        customer_tier="gold",
        order_total=20,
        refund_reason="late_delivery",
        days_since_delivery=2,
        prior_refunds_90d=0,
        customer_message="Please help.",
    )
    decision = RefundDecision(
        decision="approve",
        refund_amount=20,
        needs_human_review=False,
        reason="Your refund has already been processed.",
    )

    violations = validate_support_decision(ticket, decision)
    assert any(violation.type == "claims_refund_executed" for violation in violations)
