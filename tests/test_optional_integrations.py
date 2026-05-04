from __future__ import annotations

import importlib.util

from harnessify.integrations import deepeval, docker_sandbox, git_repo, guardrails_ai, inspect_ai, mlflow, otel, promptfoo


def test_optional_integrations_fail_gracefully_when_missing(monkeypatch) -> None:
    monkeypatch.setattr(importlib.util, "find_spec", lambda _name: None)

    assert deepeval.integration_status()["installed"] is False
    assert inspect_ai.integration_status()["installed"] is False
    assert guardrails_ai.integration_status()["installed"] is False
    assert mlflow.integration_status()["installed"] is False
    assert otel.integration_status()["installed"] is False
    assert docker_sandbox.integration_status()["installed"] is False
    assert promptfoo.integration_status()["installed"] is False


def test_git_repo_integration_returns_status_dict() -> None:
    status = git_repo.integration_status()
    assert "installed" in status
    assert "message" in status
