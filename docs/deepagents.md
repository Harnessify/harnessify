# Deep Agents

Harnessify should integrate with Deep Agents as a production-readiness layer above the runtime, not as a competing harness.

## Positioning

Deep Agents is the runtime. Harnessify is the readiness layer.

That means:

- Deep Agents owns planning, tool use, subagents, filesystem usage, and runtime behavior
- Harnessify owns evals, red-team probes, guardrails, readiness reports, compare, promotion evidence, and rollback state

## Why This Fit Is Good

Deep Agents already exposes an `invoke(...)` style runtime surface and is built on top of LangGraph. That makes the adapter path thin and keeps Harnessify from coupling to runtime internals.

## Integration Strategy

### 1. Thin Runtime Adapter

Use a `DeepAgentAdapter` that wraps an object with `.invoke(...)`.

Harnessify should:

- map Harnessify inputs into the runtime's invoke payload
- map runtime outputs back into Harnessify's open formats
- keep the integration black-box at the input and output boundary

### 2. Trace Strategy

Deep Agents supports native LangSmith tracing when the relevant environment variables are set.

Harnessify should not require LangSmith to function. The better model is:

- if LangSmith traces exist, optionally attach trace metadata to Harnessify artifacts
- if LangSmith is not configured, Harnessify still produces its own local readiness artifacts

### 3. Guardrail Composition

Harnessify guardrails should compose with runtime-native controls instead of replacing them.

Examples:

- runtime permissions stay in Deep Agents
- domain policy checks stay in Harnessify
- readiness decisions stay in Harnessify

### 4. What To Avoid

- do not intercept subagent internals
- do not depend on LangSmith as a mandatory storage layer
- do not mutate Deep Agents configuration automatically in the core path

## Example Shape

```python
from deepagents import create_deep_agent

from harnessify.adapters.deepagents import create_deep_agent_adapter

agent = create_deep_agent(
    model="openai:gpt-5.4",
    tools=[],
    system_prompt="You are a support agent.",
)

harness_agent = create_deep_agent_adapter(agent)

result = harness_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Should this refund request be approved?",
            }
        ]
    }
)
```

## Recommended Milestone

The first Deep Agents milestone should be modest:

- one support refund example agent
- one adapter path
- one readiness report flow
- no auto-remediation
- no deep coupling to LangGraph internals

## Current Repo Path

The repo now includes:

- a thin adapter in `harnessify/adapters/deepagents.py`
- a support refund reference implementation in `harnessify/domains/support/reference_agents/deepagents_support_refund.py`
- a runnable example under `examples/deepagents/support_refund/`
- a deployment guide in `docs/deploy_deepagents_support_refund.md`

The intended flow is:

```bash
hfy support eval --agent-version deep-v1 --agent-impl deepagents_support_refund --adapter deepagents
hfy support redteam --agent-version deep-v1 --agent-impl deepagents_support_refund --adapter deepagents
hfy support readiness --agent-version deep-v1
```

For cloud deployment details, see `docs/deploy_deepagents_support_refund.md`.
