# Deploy The Deep Agents Support Refund Example

This guide deploys the support refund reference agent as a Deep Agents project, then keeps Harnessify as the readiness layer.

## What Gets Deployed

The deployable project lives at:

```text
examples/deepagents/support_refund/
```

It contains:

- `deepagents.toml`: Deep Agents deployment config
- `AGENTS.md`: support refund agent instructions
- `agent.py`: Python entrypoint exporting `agent`
- `langgraph.json`: LangGraph/LangSmith deployment config
- `.env.example`: required environment variables

## Local Harness Run

From the repo root:

```bash
pip install -e ".[dev,deepagents]"
export HFY_DEEPAGENTS_MODEL="openai:gpt-5.4"
export OPENAI_API_KEY="..."

hfy init
hfy support eval --agent-version deep-v1 --agent-impl deepagents_support_refund --adapter deepagents
hfy support redteam --agent-version deep-v1 --agent-impl deepagents_support_refund --adapter deepagents
hfy support readiness --agent-version deep-v1
```

## Local Deep Agents Dev Server

From the example directory:

```bash
cd examples/deepagents/support_refund
cp .env.example .env
```

Fill in `.env`, then run:

```bash
uvx deepagents-cli dev --config deepagents.toml --port 2024
```

## Cloud Deploy

The official Deep Agents deployment path packages the project into a LangSmith Deployment:

```bash
cd examples/deepagents/support_refund
uvx deepagents-cli deploy --config deepagents.toml
```

Required credentials:

- `LANGSMITH_API_KEY`
- model provider credentials such as `OPENAI_API_KEY`

Validate the deployment bundle without publishing:

```bash
uvx deepagents-cli deploy --config deepagents.toml --dry-run
```

## Harnessify Boundary

Deep Agents remains the runtime. Harnessify evaluates behavior before promotion and produces local readiness artifacts:

- eval summary
- red-team summary
- readiness report
- compare result
- promotion manifest
- rollback event
