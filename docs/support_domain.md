# Support Domain

Milestone 1 ships one domain pack: support refund-agent readiness.

## Domain Goal

Prove that Harnessify can wrap a domain-specific agent workflow, evaluate it locally, red-team it, enforce guardrails, produce a readiness report, compare versions, and drive promotion or rollback decisions.

## Input Schema

The support ticket model captures:

- customer tier
- order total
- refund reason
- days since delivery
- prior refunds in the last 90 days
- raw customer message

## Output Schema

The refund decision model returns:

- `approve`, `deny`, or `escalate`
- refund amount
- whether human review is required
- a customer-facing reason

## Policy Focus

The policy pack enforces:

- auto approval for eligible damaged items
- no refund above order total
- human review for larger refunds
- escalation for suspicious refund history
- denial for late changed-mind requests
- resistance to policy override attempts
- no fake execution claims
- no verbatim policy leakage

## Milestone 1 Agent

The built-in support agent is deterministic and local. It does not call an LLM, external APIs, payment systems, or helpdesk platforms. That keeps the milestone small, reproducible, and easy to review.
