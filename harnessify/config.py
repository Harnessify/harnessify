from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ProjectPaths(BaseModel):
    runs_dir: str = "runs"
    versions_dir: str = "versions"
    agents_dir: str = "agents"


class SupportConfig(BaseModel):
    policy_path: str = "harnessify/domains/support/policies/refund_policy.yaml"
    eval_cases_dir: str = "harnessify/domains/support/eval_cases"
    redteam_path: str = "harnessify/domains/support/redteam.yaml"


class HarnessifyConfig(BaseModel):
    project: ProjectPaths = Field(default_factory=ProjectPaths)
    support: SupportConfig = Field(default_factory=SupportConfig)


DEFAULT_CONFIG = HarnessifyConfig()


def default_config_data() -> dict[str, Any]:
    return DEFAULT_CONFIG.model_dump()


def config_path(root: Path) -> Path:
    return root / "hfy.yaml"


def write_default_config(root: Path) -> Path:
    path = config_path(root)
    if not path.exists():
        path.write_text(yaml.safe_dump(default_config_data(), sort_keys=False), encoding="utf-8")
    return path


def load_config(root: Path) -> HarnessifyConfig:
    path = config_path(root)
    if not path.exists():
        return DEFAULT_CONFIG
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return HarnessifyConfig.model_validate(data)
