from __future__ import annotations

from harnessify.domains.catalog import list_domain_packs


def test_domain_catalog_includes_active_and_planned_packs() -> None:
    packs = list_domain_packs()

    assert any(pack.id == "support_refunds" and pack.status == "active" for pack in packs)
    assert any(pack.id == "fintech_dispute_intake" and pack.status == "planned" for pack in packs)
