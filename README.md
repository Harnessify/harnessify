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

## Product Shape

Harnessify is built around three layers:

- Domain packs: policies, eval cases, red-team probes, scorers, and readiness rules for a concrete workflow
- Reference agents: runnable examples for each domain that prove the harness contract end to end
- Bring-your-own agents: adapters for existing runtimes such as callable Python agents, shell-wrapped agents, and OpenAI-compatible endpoints

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

## Domain Pack Examples

The first domain pack is support refund-agent readiness. Adjacent domain packs that fit the same product shape:

- Support account recovery
- Fintech dispute intake
- Insurance claims intake
- Healthcare triage escalation
- IT helpdesk access requests
- Procurement vendor onboarding

Each domain pack should include:

- A policy pack
- Eval cases
- Red-team probes
- A scorer
- A readiness rubric
- One or more reference agents

## Reference Agents

Harnessify needs actual agents for real use-cases, but they are not the product center.

- Reference agents exist to prove the harness contract on realistic workflows
- Customer agents are expected to stay in the customer's chosen runtime
- The same domain pack should work across multiple agent implementations over time

For Milestone 1, the support pack includes a deterministic local reference agent and room for future OpenAI-compatible and LangGraph reference agents.

## OSS and Cloud

The open-source CLI proves the workflow locally. The eventual cloud product should sit above execution, not replace the runtime.

- OSS/local: CLI, open files, domain packs, adapters, readiness reports, promotion manifests, rollback events
- Team cloud: shared version registry, readiness history, approval workflows, policy-pack management, rollback registry
- Enterprise: governance, RBAC/SSO, audit exports, multi-environment controls, signed evidence bundles

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

See [docs/vision.md](docs/vision.md), [docs/open_formats.md](docs/open_formats.md), [docs/adapters.md](docs/adapters.md), [docs/support_domain.md](docs/support_domain.md), [docs/domain_packs.md](docs/domain_packs.md), and [docs/cloud.md](docs/cloud.md).

## License

Apache-2.0
