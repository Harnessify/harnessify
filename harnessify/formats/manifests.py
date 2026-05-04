from __future__ import annotations

from harnessify.formats.schemas import AgentVersionManifest, ProductionManifest


def manifest_payload(manifest: AgentVersionManifest) -> dict:
    return manifest.model_dump()


def production_manifest_payload(manifest: ProductionManifest) -> dict:
    return manifest.model_dump()
