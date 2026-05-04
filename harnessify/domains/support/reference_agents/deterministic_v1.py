from __future__ import annotations

from harnessify.domains.support.demo_agent import evaluate_ticket


def run(ticket, policy, run_id: str):
    """Stable local reference agent used by the current CLI flow."""
    return evaluate_ticket(ticket=ticket, policy=policy, run_id=run_id)
