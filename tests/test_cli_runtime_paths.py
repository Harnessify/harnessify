from __future__ import annotations

from typer.testing import CliRunner

from harnessify.cli import app
from harnessify.core.run_store import read_json


def test_shell_adapter_produces_eval_summary(initialized_project) -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["support", "eval", "--agent-version", "v1", "--agent-impl", "deterministic_v1", "--adapter", "shell"],
    )

    assert result.exit_code == 0
    summary = read_json(initialized_project / "runs" / "support" / "eval_summary_v1.json")
    assert summary["adapter"] == "shell"
    assert summary["agent_impl"] == "deterministic_v1"
    assert summary["pass_rate"] == 1.0


def test_bad_candidate_compare_demo_reports_risky(initialized_project) -> None:
    runner = CliRunner()

    assert runner.invoke(app, ["support", "eval", "--agent-version", "v1"]).exit_code == 0
    assert runner.invoke(app, ["support", "redteam", "--agent-version", "v1"]).exit_code == 0
    assert runner.invoke(app, ["support", "readiness", "--agent-version", "v1"]).exit_code == 0

    assert runner.invoke(
        app,
        ["support", "eval", "--agent-version", "v2", "--agent-impl", "bad_candidate_v2"],
    ).exit_code == 0
    assert runner.invoke(
        app,
        ["support", "redteam", "--agent-version", "v2", "--agent-impl", "bad_candidate_v2"],
    ).exit_code == 0
    assert runner.invoke(app, ["support", "readiness", "--agent-version", "v2"]).exit_code == 0

    compare_result = runner.invoke(app, ["support", "compare", "--base", "v1", "--candidate", "v2"])
    assert compare_result.exit_code == 0
    assert "candidate_risky" in compare_result.stdout
    assert "bad_candidate_v2" in compare_result.stdout
