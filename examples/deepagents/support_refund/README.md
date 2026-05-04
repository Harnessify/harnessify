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

## Run Locally Through Harnessify

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

## Run As A Deep Agents Project

This directory is also a Deep Agents project:

- `deepagents.toml` configures the deployable agent
- `AGENTS.md` defines the support refund instructions
- `langgraph.json` exposes `agent.py:agent` for LangGraph/LangSmith style deployment
- `.env.example` lists required runtime credentials

Create a local `.env` from the example and fill in credentials:

```bash
cd examples/deepagents/support_refund
cp .env.example .env
```

Run the Deep Agents dev server:

```bash
uvx deepagents-cli dev --config deepagents.toml --port 2024
```

Deploy to LangSmith Deployment with the Deep Agents CLI:

```bash
uvx deepagents-cli deploy --config deepagents.toml
```

You need a valid `LANGSMITH_API_KEY` and model-provider credentials before deployment will work.

## Notes

- Harnessify stays at the input/output boundary.
- Deep Agents remains the runtime.
- LangSmith tracing is optional and not required for Harnessify readiness artifacts.
