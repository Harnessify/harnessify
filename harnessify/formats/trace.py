from __future__ import annotations

from typing import Iterable

from harnessify.formats.schemas import TraceEvent


def serialize_trace_events(events: Iterable[TraceEvent]) -> list[str]:
    return [event.model_dump_json() for event in events]
