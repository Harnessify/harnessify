from __future__ import annotations

import importlib.util
from collections.abc import Callable
from typing import Any


InputMapper = Callable[[dict[str, Any]], dict[str, Any]]
OutputMapper = Callable[[Any], dict[str, Any]]


def deepagents_status() -> dict[str, str | bool]:
    installed = importlib.util.find_spec("deepagents") is not None
    return {
        "name": "deepagents",
        "installed": installed,
        "message": (
            "deepagents is installed."
            if installed
            else "deepagents is not installed. Install it to run Deep Agents through Harnessify."
        ),
    }


def default_input_mapper(payload: dict[str, Any]) -> dict[str, Any]:
    if "messages" in payload:
        return payload
    if "input" in payload and isinstance(payload["input"], dict):
        return payload["input"]
    raise ValueError("DeepAgentAdapter expected a payload with 'messages' or 'input'.")


def default_output_mapper(result: Any) -> dict[str, Any]:
    if isinstance(result, dict):
        return result
    raise ValueError("DeepAgentAdapter expected the agent to return a dict.")


class DeepAgentAdapter:
    """Thin wrapper around a Deep Agents-style runtime object with `.invoke(...)`."""

    def __init__(
        self,
        agent: Any,
        *,
        input_mapper: InputMapper | None = None,
        output_mapper: OutputMapper | None = None,
    ) -> None:
        if not hasattr(agent, "invoke"):
            raise TypeError("DeepAgentAdapter requires an object with an invoke method.")
        self.agent = agent
        self.input_mapper = input_mapper or default_input_mapper
        self.output_mapper = output_mapper or default_output_mapper

    def invoke(self, payload: dict[str, Any]) -> dict[str, Any]:
        deepagents_input = self.input_mapper(payload)
        result = self.agent.invoke(deepagents_input)
        return self.output_mapper(result)


def create_deep_agent_adapter(
    agent: Any,
    *,
    input_mapper: InputMapper | None = None,
    output_mapper: OutputMapper | None = None,
) -> DeepAgentAdapter:
    return DeepAgentAdapter(
        agent,
        input_mapper=input_mapper,
        output_mapper=output_mapper,
    )
