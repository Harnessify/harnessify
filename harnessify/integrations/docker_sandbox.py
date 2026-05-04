from __future__ import annotations

import importlib.util


def integration_status() -> dict[str, str | bool]:
    installed = importlib.util.find_spec("docker") is not None
    return {
        "name": "docker_sandbox",
        "installed": installed,
        "message": "docker SDK is installed." if installed else "docker SDK is not installed.",
    }
