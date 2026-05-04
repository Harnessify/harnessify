# Harnessify

Harnessify is an open production harness for AI agents.

Production-readiness for agents, across any model or runtime.

Status: pre-alpha

Harnessify helps teams:

- Avoid harness lock-in
- Evaluate any agent runtime
- Red-team workflows
- Enforce portable guardrails
- Capture open traces
- Compare versions
- Promote safe versions
- Roll back risky versions
- Continuously harden agents

## Why It Exists

Model providers are getting easier to swap. Agent harnesses and runtimes are not.

Harnessify creates an open production-readiness layer around existing agents so teams can add evals, red-team probes, guardrails, traces, manifests, promotion gates, rollback, and readiness reports without locking into one runtime.

## What It Is

- Provider-neutral
- Runtime-neutral
- Model-neutral
- Domain-aware
- OSS-friendly
- Local-first for the MVP

## What It Is Not

- Not another agent framework
- Not a chatbot
- Not a multi-agent orchestrator
- Not a SaaS dashboard

## Milestone 1

The first milestone is a local CLI MVP for support refund-agent readiness. It demonstrates a narrow wedge:

- Evaluate a support refund agent
- Run red-team probes against it
- Enforce local guardrails
- Generate a readiness report
- Compare versions
- Promote a safe version
- Roll back a risky version
- Store traces, manifests, and reports in open local files

## Quickstart

```bash
pip install -e ".[dev]"
hfy init
hfy support eval --agent-version v1
hfy support redteam --agent-version v1
hfy support readiness --agent-version v1
hfy support promote --agent-version v1 --env production
hfy support rollback --to v1 --env production
```

## Repository Layout

The MVP centers on:

- Open local formats
- Thin adapters around existing runtimes
- A deterministic support refund-agent domain pack
- Graceful optional integration hooks for OSS tools

See [docs/vision.md](docs/vision.md), [docs/open_formats.md](docs/open_formats.md), [docs/adapters.md](docs/adapters.md), and [docs/support_domain.md](docs/support_domain.md).

## License

Apache-2.0
