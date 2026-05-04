from __future__ import annotations

from harnessify.adapters import openai_compatible
from harnessify.core.run_store import utc_now_iso
from harnessify.domains.support.reference_agents.deepagents_support_refund import (
    SYSTEM_PROMPT,
    build_user_message,
    parse_refund_decision_text,
)
from harnessify.domains.support.schemas import RefundDecision, SupportTicket


def run(ticket: SupportTicket, policy: dict, run_id: str) -> tuple[dict, list[dict]]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_message(ticket, policy)},
    ]
    response = openai_compatible.chat_completion(messages)
    assistant_text = openai_compatible.extract_chat_content(response)
    decision = RefundDecision.model_validate(parse_refund_decision_text(assistant_text))
    trace = [
        {
            "event_id": f"{run_id}-openai-compatible-input",
            "run_id": run_id,
            "timestamp": utc_now_iso(),
            "event_type": "openai_compatible_input_prepared",
            "actor": "openai_compatible_support_refund",
            "payload": {"messages": messages},
        },
        {
            "event_id": f"{run_id}-openai-compatible-output",
            "run_id": run_id,
            "timestamp": utc_now_iso(),
            "event_type": "openai_compatible_output_received",
            "actor": "openai_compatible_support_refund",
            "payload": {
                "assistant_text": assistant_text,
                "decision": decision.model_dump(),
            },
        },
    ]
    return decision.model_dump(), trace
