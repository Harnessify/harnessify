from __future__ import annotations

import json
import re

from typer.testing import CliRunner

from harnessify.cli import app
from harnessify.core.run_store import read_json
from harnessify.domains.support.demo_agent import evaluate_ticket
from harnessify.domains.support.schemas import SupportTicket


class FakeDeepSupportAgent:
    def invoke(self, payload):
        content = payload["messages"][-1]["content"]
        match = re.search(r"Ticket:\n(\{.*\})\n\nReturn only JSON\.", content, flags=re.DOTALL)
        if not match:
            raise ValueError("Could not extract ticket JSON from prompt.")
        ticket = SupportTicket.model_validate(json.loads(match.group(1)))
        decision, _trace = evaluate_ticket(ticket=ticket, policy={"rules": []}, run_id="fake-deep")
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": json.dumps(decision),
                }
            ]
        }


def test_deepagents_support_example_generates_readiness(monkeypatch, initialized_project) -> None:
    from harnessify.domains.support.reference_agents import deepagents_support_refund

    monkeypatch.setattr(deepagents_support_refund, "build_agent", lambda: FakeDeepSupportAgent())
    runner = CliRunner()

    assert runner.invoke(
        app,
        [
            "support",
            "eval",
            "--agent-version",
            "deep-v1",
            "--agent-impl",
            "deepagents_support_refund",
            "--adapter",
            "deepagents",
        ],
    ).exit_code == 0
    assert runner.invoke(
        app,
        [
            "support",
            "redteam",
            "--agent-version",
            "deep-v1",
            "--agent-impl",
            "deepagents_support_refund",
            "--adapter",
            "deepagents",
        ],
    ).exit_code == 0
    assert runner.invoke(app, ["support", "readiness", "--agent-version", "deep-v1"]).exit_code == 0

    summary = read_json(initialized_project / "runs" / "support" / "eval_summary_deep-v1.json")
    report = read_json(initialized_project / "runs" / "support" / "readiness_report_deep-v1.json")

    assert summary["adapter"] == "deepagents"
    assert summary["agent_impl"] == "deepagents_support_refund"
    assert summary["pass_rate"] == 1.0
    assert report["agent_version"] == "deep-v1"
    assert report["recommendation"] == "approve"
