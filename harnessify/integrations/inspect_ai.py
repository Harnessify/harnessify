from __future__ import annotations

import importlib.util


def integration_status() -> dict[str, str | bool]:
    installed = importlib.util.find_spec("inspect_ai") is not None
    return {
        "name": "inspect_ai",
        "installed": installed,
        "message": "inspect_ai is installed." if installed else "inspect_ai is not installed.",
    }
