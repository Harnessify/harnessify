from __future__ import annotations

import json
import tomllib
from pathlib import Path


def test_deepagents_support_refund_deploy_files_are_present() -> None:
    root = Path(__file__).resolve().parents[1]
    example_dir = root / "examples" / "deepagents" / "support_refund"

    assert (example_dir / "AGENTS.md").exists()
    assert (example_dir / "agent.py").exists()
    assert (example_dir / "deepagents.toml").exists()
    assert (example_dir / "langgraph.json").exists()
    assert (example_dir / ".env.example").exists()


def test_deepagents_support_refund_deploy_config_points_to_agent() -> None:
    root = Path(__file__).resolve().parents[1]
    example_dir = root / "examples" / "deepagents" / "support_refund"
    deepagents_config = tomllib.loads((example_dir / "deepagents.toml").read_text(encoding="utf-8"))
    langgraph_config = json.loads((example_dir / "langgraph.json").read_text(encoding="utf-8"))

    assert deepagents_config["agent"]["name"] == "harnessify-support-refund"
    assert deepagents_config["sandbox"]["provider"] == "none"
    assert langgraph_config["graphs"]["agent"] == "./agent.py:agent"
    assert "../../.." in langgraph_config["dependencies"]
