from __future__ import annotations

from typing import Any, Callable

from harnessify.core.run_store import utc_now_iso


def run_callable_agent(func: Callable[..., tuple[dict[str, Any], list[dict[str, Any]]]], **kwargs: Any) -> dict[str, Any]:
    decision, trace = func(**kwargs)
    return {
        "decision": decision,
        "trace": trace,
        "created_at": utc_now_iso(),
    }
