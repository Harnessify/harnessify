from __future__ import annotations


def pyflue_status() -> dict[str, str]:
    return {
        "available": "false",
        "message": "PyFlue adapter will wrap external runtimes later without owning the runtime.",
    }
