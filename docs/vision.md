# Harnessify Vision

Harnessify is an open production harness for AI agents.

The core market problem is not just model lock-in. Model providers are becoming easier to swap, but agent harnesses and runtimes are still sticky. Teams often get pulled into one provider or framework's assumptions around traces, evals, memory, deployment, guardrails, and release operations.

Harnessify creates a portable production-readiness layer around any agent runtime. It does not replace the runtime. It wraps the runtime with open evals, red-team probes, guardrails, traces, manifests, promotion gates, rollback, readiness reporting, and continuous hardening workflows.

Over time, the product should split cleanly into:

- local and CI execution in the customer's environment
- a lightweight control plane for version history, approvals, policy packs, and rollback evidence

## Positioning

- Provider-neutral
- Runtime-neutral
- Model-neutral
- Domain-aware
- OSS-friendly
- Local-first for the MVP

## Production Lifecycle

build -> eval -> redteam -> guard -> promote -> monitor -> compare -> rollback -> harden

## Milestone 1 Wedge

The first wedge is intentionally narrow: support refund-agent readiness and rollback through a local CLI. This keeps the product focused on a painful release decision instead of drifting into a broad platform before the value is proven.

## What It Proves

- A runtime can stay external.
- Production-readiness can be portable.
- Files and manifests can stay open and local.
- Promotion and rollback can be reasoned about without a hosted control plane.

The cloud product, if added later, should govern release state and evidence, not become another runtime.
