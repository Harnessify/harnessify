from __future__ import annotations

import json

from typer.testing import CliRunner

from harnessify.adapters import openai_compatible
from harnessify.cli import app
from harnessify.core.run_store import read_json


def test_openai_compatible_support_eval_path(monkeypatch, initialized_project) -> None:
    def fake_chat_completion(messages):
        content = messages[-1]["content"]
        if "changed_mind" in content and "20" in content:
            decision = {
                "decision": "deny",
                "refund_amount": 0,
                "needs_human_review": False,
                "reason": "This request does not qualify for a refund after the review window.",
            }
        elif "prior_refunds_90d" in content and "3" in content:
            decision = {
                "decision": "escalate",
                "refund_amount": 35,
                "needs_human_review": True,
                "reason": "A support specialist needs to review this request because of account history.",
            }
        elif "late_delivery" in content:
            decision = {
                "decision": "approve",
                "refund_amount": 40,
                "needs_human_review": False,
                "reason": "This late-delivery request qualifies for a refund review outcome.",
            }
        elif "70" in content:
            decision = {
                "decision": "escalate",
                "refund_amount": 70,
                "needs_human_review": True,
                "reason": "A support specialist needs to review this damaged-item refund request.",
            }
        else:
            decision = {
                "decision": "approve",
                "refund_amount": 25,
                "needs_human_review": False,
                "reason": "This damaged-item request qualifies for a refund.",
            }
        return {"choices": [{"message": {"content": json.dumps(decision)}}]}

    monkeypatch.setattr(openai_compatible, "chat_completion", fake_chat_completion)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "support",
            "eval",
            "--agent-version",
            "local-v1",
            "--agent-impl",
            "openai_compatible_support_refund",
            "--adapter",
            "openai-compatible",
        ],
    )

    assert result.exit_code == 0
    summary = read_json(initialized_project / "runs" / "support" / "eval_summary_local-v1.json")
    assert summary["adapter"] == "openai-compatible"
    assert summary["agent_impl"] == "openai_compatible_support_refund"
