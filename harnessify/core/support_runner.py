from __future__ import annotations

import sys
from pathlib import Path

from harnessify.adapters.callable_agent import run_callable_agent
from harnessify.adapters.shell_agent import run_shell_agent
from harnessify.config import load_config
from harnessify.domains.support.policy import load_support_policy
from harnessify.domains.support.registry import (
    resolve_deepagents_reference_agent,
    resolve_reference_agent,
)
from harnessify.domains.support.schemas import SupportTicket


def run_support_agent(
    root: Path,
    agent_impl: str,
    adapter: str,
    ticket: SupportTicket,
    run_id: str,
    run_dir: Path,
) -> dict:
    config = load_config(root)
    policy_path = root / config.support.policy_path
    policy = load_support_policy(policy_path)

    if adapter == "callable":
        agent = resolve_reference_agent(agent_impl)
        result = run_callable_agent(agent, ticket=ticket, policy=policy, run_id=run_id)
        result["adapter"] = "callable"
        result["runtime"] = agent_impl
        result["provider"] = "local"
        return result

    if adapter == "shell":
        output_path = run_dir / "output.json"
        trace_path = run_dir / "trace.tmp.jsonl"
        command = [
            sys.executable,
            "-m",
            "harnessify.domains.support.reference_agents.runner",
            agent_impl,
            str(run_dir / "input.json"),
            str(policy_path),
            str(output_path),
            str(trace_path),
            run_id,
        ]
        result = run_shell_agent(command, output_path=output_path, trace_path=trace_path)
        trace_path.unlink(missing_ok=True)
        result["created_at"] = result["trace"][-1]["timestamp"] if result["trace"] else ""
        result["adapter"] = "shell"
        result["runtime"] = f"shell::{agent_impl}"
        result["provider"] = "local"
        return result

    if adapter == "deepagents":
        deepagents_agent = resolve_deepagents_reference_agent(agent_impl)
        result = run_callable_agent(deepagents_agent, ticket=ticket, policy=policy, run_id=run_id)
        result["adapter"] = "deepagents"
        result["runtime"] = agent_impl
        result["provider"] = "deepagents"
        return result

    raise ValueError(f"Unknown adapter '{adapter}'. Available: callable, shell, deepagents")
