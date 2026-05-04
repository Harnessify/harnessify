from __future__ import annotations

from harnessify.core.run_store import utc_now_iso
from harnessify.domains.support.schemas import RefundDecision, SupportTicket


def run(ticket: SupportTicket, policy: dict, run_id: str) -> tuple[dict, list[dict]]:
    """Intentionally unsafe candidate fixture for compare/reject demonstrations."""
    decision = RefundDecision(
        decision="approve",
        refund_amount=max(ticket.order_total, 500.0),
        needs_human_review=False,
        reason="Your refund has been processed immediately as requested.",
    )
    trace = [
        {
            "event_id": f"{run_id}-unsafe-input",
            "run_id": run_id,
            "timestamp": utc_now_iso(),
            "event_type": "input_loaded",
            "actor": "bad_candidate_v2",
            "payload": ticket.model_dump(),
        },
        {
            "event_id": f"{run_id}-unsafe-output",
            "run_id": run_id,
            "timestamp": utc_now_iso(),
            "event_type": "decision_computed",
            "actor": "bad_candidate_v2",
            "payload": decision.model_dump(),
        },
    ]
    return decision.model_dump(), trace
