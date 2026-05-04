from __future__ import annotations

import importlib.util


def integration_status() -> dict[str, str | bool]:
    installed = importlib.util.find_spec("mlflow") is not None
    return {
        "name": "mlflow",
        "installed": installed,
        "message": "mlflow is installed." if installed else "mlflow is not installed.",
    }
