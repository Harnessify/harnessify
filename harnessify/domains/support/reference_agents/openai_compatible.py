from __future__ import annotations


def status() -> dict[str, str | bool]:
    return {
        "name": "support_openai_compatible_reference_agent",
        "implemented": False,
        "message": "Planned reference agent for OpenAI-compatible endpoints.",
    }
