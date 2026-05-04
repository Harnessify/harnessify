# Domain Packs

Harnessify becomes valuable when it stops being abstract. Domain packs are how the product gets specific.

Each domain pack defines the production-readiness contract for one workflow:

- input and output schemas
- policy pack
- eval cases
- red-team probes
- guardrail expectations
- scoring logic
- readiness recommendation rules
- reference agents

## Why Domain Packs Matter

Generic eval tooling is easy to ignore. Domain packs make the release decision concrete:

- what can go wrong
- what policy must be enforced
- what behavior counts as safe enough to ship
- what should block promotion or trigger rollback

## Good Early Domain Packs

### Support Refunds

- Risk: monetary leakage, prompt injection, policy override
- Buyer: support operations, CX engineering, applied AI lead
- Harness output: refund readiness report and rollback evidence

### Support Account Recovery

- Risk: identity spoofing, privilege escalation, unsafe resets
- Buyer: support platform, trust and safety, security operations
- Harness output: escalation correctness and auditability

### Fintech Dispute Intake

- Risk: compliance mistakes, unsupported claims, incomplete evidence capture
- Buyer: risk, operations, dispute operations
- Harness output: case-quality gating and explanation trails

### Insurance Claims Intake

- Risk: over-promising outcomes, bad extraction, policy leakage
- Buyer: operations, claims automation, compliance
- Harness output: readiness scoring before production rollout

### Healthcare Triage Escalation

- Risk: unsafe advice, missing escalation, false reassurance
- Buyer: clinical operations, care navigation, digital health product teams
- Harness output: escalation safety and policy compliance

### IT Access Requests

- Risk: approval spoofing, privilege escalation, policy bypass
- Buyer: internal IT, security engineering, enterprise automation teams
- Harness output: release gate for action-taking internal agents

## What A Pack Should Ship

At minimum:

- one deterministic reference agent
- one candidate-bad fixture for compare/reject demonstrations
- one bring-your-own adapter path
- local eval and red-team assets

Over time:

- multiple reference agents in different runtimes
- richer policy packs
- versioned readiness rubrics
- optional cloud-managed pack distribution
