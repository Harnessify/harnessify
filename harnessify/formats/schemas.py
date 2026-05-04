from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Severity = Literal["low", "medium", "high"]
Recommendation = Literal["approve", "reject", "approve_with_conditions"]


class AgentVersionManifest(BaseModel):
    agent_version: str
    runtime: str | None = None
    provider: str | None = None
    model: str | None = None
    config_hash: str
    policy_hash: str
    prompt_hash: str | None = None
    created_at: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class GuardrailViolation(BaseModel):
    type: str
    severity: Severity
    message: str
    evidence: dict[str, Any] = Field(default_factory=dict)


class RunRecord(BaseModel):
    run_id: str
    domain: str
    case_id: str
    agent_version: str
    adapter: str
    provider: str | None = None
    runtime: str | None = None
    input_path: str
    output_path: str
    score: float
    passed: bool
    guardrail_violations: list[GuardrailViolation] = Field(default_factory=list)
    trace_path: str
    created_at: str


class TraceEvent(BaseModel):
    event_id: str
    run_id: str
    timestamp: str
    event_type: str
    actor: str
    payload: dict[str, Any] = Field(default_factory=dict)


class ReadinessReport(BaseModel):
    agent_version: str
    eval_pass_rate: float
    redteam_pass_rate: float
    high_severity_failures: int
    guardrail_violations: int
    recommendation: Recommendation
    reasons: list[str] = Field(default_factory=list)


class ProductionManifest(BaseModel):
    env: str
    agent_version: str
    promoted_at: str
    config_hash: str
    policy_hash: str
    eval_summary_path: str
    redteam_summary_path: str
    readiness_report_path: str
    git_commit: str | None = None
    previous_agent_version: str | None = None
