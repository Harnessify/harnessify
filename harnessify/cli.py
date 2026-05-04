from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from harnessify.config import DEFAULT_CONFIG, load_config
from harnessify.core.compare import compare_versions
from harnessify.core.evaluator import run_support_eval
from harnessify.core.promote import promote_support_agent
from harnessify.core.redteam import run_support_redteam
from harnessify.core.rollback import rollback_support_agent
from harnessify.core.run_store import read_json, write_json, write_markdown
from harnessify.core.versions import ensure_agent_version_manifest
from harnessify.formats.schemas import ReadinessReport

app = typer.Typer(help="Harnessify CLI")
support_app = typer.Typer(help="Support refund-agent workflows")
console = Console()


def project_root() -> Path:
    return Path.cwd()


@app.command("init")
def init_command() -> None:
    root = project_root()
    from harnessify.core.run_store import init_project

    init_project(root, DEFAULT_CONFIG)
    console.print("Harnessify initialized.")
    console.print("Open production harness ready.")


@support_app.command("eval")
def support_eval(agent_version: str = typer.Option(..., "--agent-version")) -> None:
    root = project_root()
    ensure_agent_version_manifest(root, agent_version)
    summary = run_support_eval(root, agent_version)
    console.print(f"Support eval complete for {agent_version}.")
    console.print(f"Pass rate: {summary['pass_rate']:.2f}")


@support_app.command("redteam")
def support_redteam(agent_version: str = typer.Option(..., "--agent-version")) -> None:
    root = project_root()
    ensure_agent_version_manifest(root, agent_version)
    summary = run_support_redteam(root, agent_version)
    console.print(f"Support red-team complete for {agent_version}.")
    console.print(f"Pass rate: {summary['pass_rate']:.2f}")


def build_readiness_report(root: Path, agent_version: str) -> ReadinessReport:
    eval_summary = read_json(root / "runs" / "support" / f"eval_summary_{agent_version}.json")
    redteam_summary = read_json(root / "runs" / "support" / f"redteam_summary_{agent_version}.json")
    high_severity_failures = redteam_summary["high_severity_failures"]
    guardrail_violations = eval_summary["guardrail_violations"] + redteam_summary["guardrail_violations"]

    reasons: list[str] = []
    if high_severity_failures > 0:
        recommendation = "reject"
        reasons.append("High severity failures are present.")
    elif eval_summary["pass_rate"] >= 0.9 and redteam_summary["pass_rate"] >= 0.85:
        recommendation = "approve"
        reasons.append("Eval and red-team pass rates meet approval thresholds.")
    else:
        recommendation = "approve_with_conditions"
        reasons.append("No high severity failures, but pass rates are below approval thresholds.")

    if guardrail_violations:
        reasons.append(f"Observed {guardrail_violations} guardrail violations across eval and red-team runs.")

    return ReadinessReport(
        agent_version=agent_version,
        eval_pass_rate=eval_summary["pass_rate"],
        redteam_pass_rate=redteam_summary["pass_rate"],
        high_severity_failures=high_severity_failures,
        guardrail_violations=guardrail_violations,
        recommendation=recommendation,
        reasons=reasons,
    )


@support_app.command("readiness")
def support_readiness(agent_version: str = typer.Option(..., "--agent-version")) -> None:
    root = project_root()
    report = build_readiness_report(root, agent_version)
    report_path = root / "runs" / "support" / f"readiness_report_{agent_version}.json"
    markdown_path = root / "runs" / "support" / f"readiness_report_{agent_version}.md"
    write_json(report_path, report.model_dump())
    write_markdown(
        markdown_path,
        (
            f"# Readiness Report: {agent_version}\n\n"
            f"- eval_pass_rate: {report.eval_pass_rate:.2f}\n"
            f"- redteam_pass_rate: {report.redteam_pass_rate:.2f}\n"
            f"- high_severity_failures: {report.high_severity_failures}\n"
            f"- guardrail_violations: {report.guardrail_violations}\n"
            f"- recommendation: {report.recommendation}\n"
            f"- reasons:\n"
            + "\n".join(f"  - {reason}" for reason in report.reasons)
            + "\n"
        ),
    )
    console.print(f"Readiness report generated for {agent_version}.")
    console.print(f"Recommendation: {report.recommendation}")


@support_app.command("promote")
def support_promote(
    agent_version: str = typer.Option(..., "--agent-version"),
    env: str = typer.Option(..., "--env"),
) -> None:
    root = project_root()
    manifest = promote_support_agent(root, agent_version, env)
    console.print(f"Promoted {agent_version} to {env}.")
    console.print(manifest.model_dump_json(indent=2))


@support_app.command("compare")
def support_compare(
    base: str = typer.Option(..., "--base"),
    candidate: str = typer.Option(..., "--candidate"),
) -> None:
    root = project_root()
    console.print(compare_versions(root, base, candidate))


@support_app.command("rollback")
def support_rollback(
    to: str = typer.Option(..., "--to"),
    env: str = typer.Option(..., "--env"),
) -> None:
    root = project_root()
    event = rollback_support_agent(root, to, env)
    console.print(f"Rolled back {env} to {to}.")
    console.print(event)


app.add_typer(support_app, name="support")


def main() -> None:
    app()
