from __future__ import annotations

from collections.abc import Callable

from harnessify.domains.support.reference_agents import (
    bad_candidate_v2,
    deepagents_support_refund,
    deterministic_v1,
)


SupportAgentCallable = Callable[..., tuple[dict, list[dict]]]


REFERENCE_AGENT_IMPLS: dict[str, SupportAgentCallable] = {
    "deterministic_v1": deterministic_v1.run,
    "bad_candidate_v2": bad_candidate_v2.run,
}

DEEPAGENTS_AGENT_IMPLS: dict[str, SupportAgentCallable] = {
    "deepagents_support_refund": deepagents_support_refund.run,
}


def resolve_reference_agent(agent_impl: str) -> SupportAgentCallable:
    try:
        return REFERENCE_AGENT_IMPLS[agent_impl]
    except KeyError as exc:
        available = ", ".join(sorted(REFERENCE_AGENT_IMPLS))
        raise ValueError(f"Unknown support agent implementation '{agent_impl}'. Available: {available}") from exc


def list_reference_agents() -> list[str]:
    return sorted(REFERENCE_AGENT_IMPLS)


def resolve_deepagents_reference_agent(agent_impl: str) -> SupportAgentCallable:
    try:
        return DEEPAGENTS_AGENT_IMPLS[agent_impl]
    except KeyError as exc:
        available = ", ".join(sorted(DEEPAGENTS_AGENT_IMPLS))
        raise ValueError(
            f"Unknown Deep Agents support implementation '{agent_impl}'. Available: {available}"
        ) from exc


def list_deepagents_reference_agents() -> list[str]:
    return sorted(DEEPAGENTS_AGENT_IMPLS)
