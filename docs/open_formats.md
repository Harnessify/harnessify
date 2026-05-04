# Open Formats

Harnessify stores Milestone 1 artifacts in local JSON, JSONL, Markdown, and YAML files so the outputs stay inspectable and portable.

## Core Models

- `TraceEvent`: one trace event with `event_id`, `run_id`, `timestamp`, `event_type`, `actor`, and `payload`
- `RunRecord`: one run summary that points to the input, output, trace, score, and guardrail artifacts
- `AgentVersionManifest`: portable metadata for an agent version
- `GuardrailViolation`: one local guardrail failure with severity and evidence
- `ReadinessReport`: approval-oriented summary across eval and red-team runs
- `ProductionManifest`: current promoted version plus hashes and report pointers

## Local Artifact Layout

```text
runs/
  support/
    <timestamp>_<case_id>/
      input.json
      output.json
      score.json
      trace.jsonl
      guardrail_violations.json
      verdict.md
    eval_summary_v1.json
    redteam_summary_v1.json
    readiness_report_v1.md
    readiness_report_v1.json

versions/
  agents/
    v1.json
  production.json
  rollback_event.jsonl
```

## Design Rules

- Keep formats local-first and readable.
- Prefer stable JSON/YAML over opaque binary storage.
- Treat paths and manifests as portability primitives, not internal implementation details.
- Keep room for OpenTelemetry, MLflow, and external eval adapters later without changing the local contract.
