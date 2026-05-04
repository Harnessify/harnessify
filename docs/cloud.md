# Cloud Offering

Harnessify Cloud should not be another agent runtime and should not start as another tracing dashboard.

The product line should separate the execution plane from the release-control plane.

## Product Layers

### OSS / Local

The open-source CLI is the adoption wedge.

- local-first execution
- open JSON, JSONL, Markdown, and YAML artifacts
- domain packs
- reference agents
- bring-your-own runtime adapters
- readiness reports
- promotion manifests
- rollback events

### Team Cloud

The first cloud layer should help teams coordinate release decisions around agents they already run elsewhere.

- shared version registry
- readiness history
- compare history
- promotion approvals
- rollback registry
- policy-pack management
- evidence bundle indexing

### Enterprise

The enterprise layer adds governance, not a new runtime.

- SSO and RBAC
- multi-environment controls
- audit exports
- signed evidence bundles
- policy governance and approval workflows
- connector management for internal systems

## Architecture

### Data Plane

Customer-controlled execution:

- agents run in the customer's chosen runtime
- evals and probes can run locally, in CI, or in the customer's VPC
- raw traces and artifacts can remain local if needed

### Control Plane

Harnessify-managed release state:

- promoted version history
- readiness decisions
- policy-pack versions
- approval events
- rollback events
- artifact metadata and evidence pointers

## What The Cloud Should Own

- version provenance
- release approvals
- policy-pack lifecycle
- compare and regression history
- rollback history
- evidence indexing

## What The Cloud Should Not Own First

- full agent execution
- agent orchestration
- custom memory systems
- custom tracing storage for every event
- generic observability UI trying to replace existing tools

## Best Initial Commercial Story

Bring your existing agent. Harnessify tells you whether this version is safe to promote, why, and what to roll back to if it fails.
