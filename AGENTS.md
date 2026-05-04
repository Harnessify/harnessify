# AGENTS.md

This repository builds Harnessify: an open production harness for AI agents.

## Product Intent

Harnessify is not another agent framework. It wraps existing agents and runtimes with portable production-readiness:

- evals
- red-team probes
- guardrails
- traces
- version manifests
- promotion gates
- rollback
- readiness reports
- continuous hardening

The current wedge is narrow on purpose:

- local-first CLI MVP
- support refund-agent readiness
- open local files and manifests
- reference agents plus bring-your-own adapters

## What To Optimize For

- Keep the runtime external.
- Keep formats open, local, and inspectable.
- Keep code boring, explicit, and reviewable.
- Reuse mature OSS instead of rebuilding it.
- Prefer thin adapters over deep framework abstractions.
- Preserve portability across providers, models, and runtimes.

## What Not To Build By Accident

- a generic agent framework
- a full observability platform
- a dashboard-first SaaS product
- a custom multi-agent orchestrator
- a hosted runtime control plane in the MVP
- domain logic that only works for one model vendor

## Current Architecture Shape

- `harnessify/cli.py`: local CLI entrypoint
- `harnessify/formats/`: portable Pydantic models and format helpers
- `harnessify/core/`: eval, red-team, guardrails, compare, promote, rollback
- `harnessify/adapters/`: thin runtime adapters
- `harnessify/integrations/`: optional external tool integrations
- `harnessify/domains/`: domain packs and reference agents
- `docs/`: product, domain, adapter, and cloud positioning

## Domain-Pack Rules

Each domain pack should stay concrete and operational. At minimum it should define:

- input and output schemas
- policy pack
- eval cases
- red-team probes
- scorer logic
- readiness rules
- at least one reference agent
- at least one intentionally bad candidate fixture for compare/reject demos

## Reference Agents

Reference agents exist to prove the harness contract on real workflows.

- They are fixtures, not the product center.
- They should be small and understandable.
- They should not require external APIs unless explicitly intended.
- The same domain pack should remain usable across multiple runtime implementations.

## Cloud/Product Direction

The future cloud product should sit above execution, not replace the runtime.

- OSS/local: CLI, files, packs, adapters, reports, manifests
- Team cloud: approvals, version history, policy-pack management, rollback registry
- Enterprise: governance, auditability, multi-environment controls

Keep control-plane concepts separate from data-plane execution.

## Engineering Rules

- Prefer explicit functions over deep abstraction layers.
- Avoid optional dependencies in the core path.
- Optional integrations must fail gracefully when not installed.
- Keep tests focused on contract behavior and portability.
- Do not silently change local artifact formats once established.
- If a feature makes the product feel broader than the wedge, cut it or move it to docs/TODO.

## Before Committing

- Run `pytest`.
- If CLI behavior changed, run the relevant `hfy` commands manually.
- Update docs when product positioning or workflow contracts change.
- Keep commits scoped and readable.
