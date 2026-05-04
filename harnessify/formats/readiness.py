from __future__ import annotations

from harnessify.formats.schemas import ReadinessReport


def readiness_payload(report: ReadinessReport) -> dict:
    return report.model_dump()
