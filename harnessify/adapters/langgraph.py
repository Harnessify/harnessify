from __future__ import annotations


def langgraph_status() -> dict[str, str]:
    return {
        "available": "false",
        "message": "LangGraph adapter will remain a thin compatibility layer in a later milestone.",
    }
