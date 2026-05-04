# Harnessify

Harnessify is an open production harness for AI agents.

Production-readiness for agents, across any model or runtime.

Status: pre-alpha

## What It Does

Harnessify sits above an existing agent runtime and helps teams:

- evaluate agent behavior before production
- red-team risky workflows
- enforce portable guardrails
- compare agent versions
- generate readiness reports
- promote safe versions
- roll back risky versions

It is designed to reduce harness lock-in by keeping readiness artifacts open and portable.

## What It Is Not

- not another agent framework
- not a chatbot product
- not a multi-agent orchestrator
- not a dashboard-first SaaS

## Current Wedge

The first wedge is intentionally narrow:

- local-first CLI
- one domain pack: support refund-agent readiness
- reference agents plus bring-your-own adapters
- open local artifacts for eval, red-team, compare, readiness, promotion, and rollback

The current product claim is simple:

Bring your existing agent. Harnessify tells you whether this version is safe to promote.

## Product Shape

Harnessify is built around three layers:

- domain packs: policies, eval cases, red-team probes, scorers, and readiness rules for one workflow
- reference agents: small runnable examples that prove the harness contract
- bring-your-own adapters: wrappers for existing runtimes such as callable Python agents, shell-executed agents, and Deep Agents

## Quickstart

```bash
pip install -e ".[dev]"
hfy init
hfy support eval --agent-version v1
hfy support redteam --agent-version v1
hfy support readiness --agent-version v1
hfy support eval --agent-version v2 --agent-impl bad_candidate_v2
hfy support redteam --agent-version v2 --agent-impl bad_candidate_v2
hfy support readiness --agent-version v2
hfy support compare --base v1 --candidate v2
```

To prove runtime portability with the same reference agent:

```bash
hfy support eval --agent-version v1 --adapter shell
hfy support redteam --agent-version v1 --adapter shell
```

## Runtime Direction

Today the repo includes:

- callable adapter path
- shell adapter path
- Deep Agents adapter module

The intent is to stay above the runtime:

- the runtime owns planning, tools, memory, and execution
- Harnessify owns readiness, comparison, and release evidence

## OSS and Cloud

The OSS CLI is the adoption wedge.

- OSS/local: CLI, domain packs, adapters, open files, reports, manifests, rollback events
- team cloud: approvals, version history, readiness history, policy-pack management, rollback registry
- enterprise: governance, multi-environment controls, and audit exports

## Read More

- [Vision](docs/vision.md)
- [Open Formats](docs/open_formats.md)
- [Adapters](docs/adapters.md)
- [Support Domain](docs/support_domain.md)
- [Domain Packs](docs/domain_packs.md)
- [Deep Agents](docs/deepagents.md)
- [Cloud](docs/cloud.md)

## License

Apache-2.0
