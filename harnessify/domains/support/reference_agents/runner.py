from __future__ import annotations

import json
import sys
from pathlib import Path

from harnessify.domains.support.policy import load_support_policy
from harnessify.domains.support.registry import resolve_reference_agent
from harnessify.domains.support.schemas import SupportTicket


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 6:
        raise SystemExit(
            "Usage: python -m harnessify.domains.support.reference_agents.runner "
            "<agent_impl> <input_json> <policy_yaml> <output_json> <trace_jsonl> <run_id>"
        )

    agent_impl, input_json, policy_yaml, output_json, trace_jsonl, run_id = args
    ticket = SupportTicket.model_validate(json.loads(Path(input_json).read_text(encoding="utf-8")))
    policy = load_support_policy(Path(policy_yaml))
    agent = resolve_reference_agent(agent_impl)
    decision, trace = agent(ticket=ticket, policy=policy, run_id=run_id)

    Path(output_json).write_text(json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8")
    Path(trace_jsonl).write_text(
        "\n".join(json.dumps(event, sort_keys=True) for event in trace) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
