from __future__ import annotations

import importlib.util

import pytest

from harnessify.adapters.deepagents import DeepAgentAdapter, create_deep_agent_adapter, deepagents_status


class FakeDeepAgent:
    def __init__(self) -> None:
        self.last_payload = None

    def invoke(self, payload):
        self.last_payload = payload
        return {"messages": [{"role": "assistant", "content": "ok"}]}


def test_deepagents_adapter_wraps_invoke_shape() -> None:
    agent = FakeDeepAgent()
    adapter = create_deep_agent_adapter(agent)

    result = adapter.invoke({"messages": [{"role": "user", "content": "hello"}]})

    assert agent.last_payload == {"messages": [{"role": "user", "content": "hello"}]}
    assert result["messages"][0]["content"] == "ok"


def test_deepagents_adapter_requires_invoke_method() -> None:
    with pytest.raises(TypeError):
        DeepAgentAdapter(object())


def test_deepagents_status_reports_missing_dependency(monkeypatch) -> None:
    monkeypatch.setattr(importlib.util, "find_spec", lambda _name: None)

    status = deepagents_status()
    assert status["installed"] is False
