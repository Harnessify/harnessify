from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from harnessify.cli import app
from harnessify.config import load_config


def test_init_command_writes_default_config(project_root: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    assert "Harnessify initialized." in result.stdout
    assert (project_root / "hfy.yaml").exists()
    assert (project_root / "runs").exists()
    assert (project_root / "versions").exists()
    assert (project_root / "agents").exists()


def test_load_config_reads_defaults_after_init(initialized_project: Path) -> None:
    config = load_config(initialized_project)

    assert config.project.runs_dir == "runs"
    assert config.support.policy_path.endswith("refund_policy.yaml")
