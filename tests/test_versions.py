from __future__ import annotations

from harnessify.core.versions import ensure_agent_version_manifest


def test_agent_version_manifest_written(initialized_project) -> None:
    manifest = ensure_agent_version_manifest(initialized_project, "v1")

    assert manifest.agent_version == "v1"
    assert manifest.config_hash
    assert manifest.policy_hash
    assert (initialized_project / "versions" / "agents" / "v1.json").exists()
