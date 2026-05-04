from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_support_policy(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
