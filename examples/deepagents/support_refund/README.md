# Deep Agents Support Refund Example

This example shows how to run Harnessify against a real Deep Agents runtime for the support refund domain.

## Prerequisites

Install Harnessify plus Deep Agents and one provider package. Example:

```bash
pip install -e ".[dev]"
pip install deepagents langchain-openai
```

Set a model for the example agent:

```bash
export HFY_DEEPAGENTS_MODEL="openai:gpt-5.4"
export OPENAI_API_KEY="..."
```

## Run The Harness

From the repo root:

```bash
hfy init
hfy support eval --agent-version deep-v1 --agent-impl deepagents_support_refund --adapter deepagents
hfy support redteam --agent-version deep-v1 --agent-impl deepagents_support_refund --adapter deepagents
hfy support readiness --agent-version deep-v1
```

You can then compare the Deep Agents runtime against the deterministic baseline:

```bash
hfy support eval --agent-version v1
hfy support redteam --agent-version v1
hfy support readiness --agent-version v1
hfy support compare --base v1 --candidate deep-v1
```

## Notes

- Harnessify stays at the input/output boundary.
- Deep Agents remains the runtime.
- LangSmith tracing is optional and not required for Harnessify readiness artifacts.
