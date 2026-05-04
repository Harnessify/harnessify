from __future__ import annotations

from pathlib import Path


def integration_status() -> dict[str, str | bool]:
    try:
        import git  # type: ignore
    except ImportError:
        return {
            "name": "git_repo",
            "installed": False,
            "message": "GitPython is not installed.",
        }
    return {
        "name": "git_repo",
        "installed": True,
        "message": "GitPython is installed.",
    }


def get_git_commit(root: Path) -> str | None:
    try:
        import git  # type: ignore
    except ImportError:
        return None

    try:
        repo = git.Repo(root)
    except Exception:
        return None
    return repo.head.commit.hexsha
