from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class DomainPack(BaseModel):
    id: str
    title: str
    industry: str
    workflow: str
    primary_risk: str
    buyer: str
    status: Literal["active", "planned"]


DOMAIN_PACKS: list[DomainPack] = [
    DomainPack(
        id="support_refunds",
        title="Support Refund Readiness",
        industry="customer support",
        workflow="refund decisions and escalation",
        primary_risk="monetary leakage and policy override",
        buyer="support operations / applied AI",
        status="active",
    ),
    DomainPack(
        id="support_account_recovery",
        title="Support Account Recovery",
        industry="customer support",
        workflow="identity and account recovery handling",
        primary_risk="identity spoofing and privilege escalation",
        buyer="trust and safety / support platform",
        status="planned",
    ),
    DomainPack(
        id="fintech_dispute_intake",
        title="Fintech Dispute Intake",
        industry="fintech",
        workflow="dispute and chargeback intake",
        primary_risk="compliance errors and bad evidence capture",
        buyer="risk operations",
        status="planned",
    ),
    DomainPack(
        id="healthcare_triage",
        title="Healthcare Triage Escalation",
        industry="healthcare",
        workflow="triage and escalation recommendations",
        primary_risk="unsafe advice and missed escalation",
        buyer="clinical operations",
        status="planned",
    ),
    DomainPack(
        id="it_access_requests",
        title="IT Access Request Readiness",
        industry="enterprise IT",
        workflow="internal access request handling",
        primary_risk="approval spoofing and privilege escalation",
        buyer="IT and security engineering",
        status="planned",
    ),
]


def list_domain_packs() -> list[DomainPack]:
    return DOMAIN_PACKS
