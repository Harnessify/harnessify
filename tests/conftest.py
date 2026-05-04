from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from harnessify.config import DEFAULT_CONFIG
from harnessify.core.run_store import init_project


@pytest.fixture
def project_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    source_domains = repo_root / "harnessify" / "domains"
    target_domains = tmp_path / "harnessify" / "domains"
    target_domains.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_domains, target_domains)
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def initialized_project(project_root: Path) -> Path:
    init_project(project_root, DEFAULT_CONFIG)
    return project_root
