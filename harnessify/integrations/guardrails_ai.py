from __future__ import annotations

import importlib.util


def integration_status() -> dict[str, str | bool]:
    installed = importlib.util.find_spec("guardrails") is not None
    return {
        "name": "guardrails_ai",
        "installed": installed,
        "message": "guardrails is installed." if installed else "guardrails is not installed.",
    }
