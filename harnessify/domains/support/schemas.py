from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


CustomerTier = Literal["standard", "gold", "enterprise"]
RefundReason = Literal["damaged_item", "late_delivery", "changed_mind", "unknown"]
DecisionType = Literal["approve", "deny", "escalate"]
ProbeSeverity = Literal["low", "medium", "high"]


class SupportTicket(BaseModel):
    ticket_id: str
    customer_tier: CustomerTier
    order_total: float
    refund_reason: RefundReason
    days_since_delivery: int
    prior_refunds_90d: int
    customer_message: str


class RefundDecision(BaseModel):
    decision: DecisionType
    refund_amount: float
    needs_human_review: bool
    reason: str


class ExpectedBehavior(BaseModel):
    decision: DecisionType
    needs_human_review: bool
    refund_amount: float | None = None
    refund_amount_max: float | None = None
    reason_must_contain: list[str] = Field(default_factory=list)
    reason_must_not_contain: list[str] = Field(default_factory=list)


class EvalCase(BaseModel):
    id: str
    ticket: SupportTicket
    expected_behavior: ExpectedBehavior
    should_pass: bool = True


class RedteamProbe(BaseModel):
    id: str
    category: str
    severity: ProbeSeverity
    ticket: SupportTicket
    expected_behavior: ExpectedBehavior
    should_pass: bool = True
