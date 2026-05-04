from __future__ import annotations

import importlib.util


def integration_status() -> dict[str, str | bool]:
    installed = importlib.util.find_spec("opentelemetry") is not None
    return {
        "name": "otel",
        "installed": installed,
        "message": "OpenTelemetry is installed." if installed else "OpenTelemetry is not installed.",
    }
