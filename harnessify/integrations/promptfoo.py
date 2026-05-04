from __future__ import annotations


def integration_status() -> dict[str, str | bool]:
    # TODO: Bridge the promptfoo CLI for red-team and eval orchestration without making it mandatory.
    return {
        "name": "promptfoo",
        "installed": False,
        "message": "promptfoo is not installed; using the internal red-team runner for Milestone 1.",
    }
