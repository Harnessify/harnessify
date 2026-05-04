from __future__ import annotations

import importlib.util


def integration_status() -> dict[str, str | bool]:
    installed = importlib.util.find_spec("deepeval") is not None
    return {
        "name": "deepeval",
        "installed": installed,
        "message": "deepeval is installed." if installed else "deepeval is not installed.",
    }
