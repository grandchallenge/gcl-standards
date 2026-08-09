from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "intellect_profile_reconciliation",
    ROOT / "ci/intellect_profile_reconciliation.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class IntellectProfileReconciliationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = MODULE.load(MODULE.PROFILE)
        self.reconciliation = MODULE.load(MODULE.RECONCILIATION)
        self.base = MODULE.load(MODULE.BASE_CAMPAIGN)
        self.overlay = MODULE.load(MODULE.OWNER_OVERLAY)
        self.owner = MODULE.load(MODULE.OWNER_REFERENCE)
        self.evidence = MODULE.load(MODULE.EVIDENCE)
        self.evidence_bytes = MODULE.canonical_git_bytes(
            MODULE.EVIDENCE, root=MODULE.ROOT
        )
        self.digest = MODULE.EVIDENCE_DIGEST.read_text(encoding="utf-8")
        self.reference = MODULE.load(MODULE.EVIDENCE_REFERENCE)

    def validate(self, **changes) -> None:
        MODULE.validate_records(
            changes.get("profile", self.profile),
            changes.get("reconciliation", self.reconciliation),
            changes.get("base_campaign", self.base),
            changes.get("owner_overlay", self.overlay),
            changes.get("owner_reference", self.owner),
            changes.get("evidence", self.evidence),
            changes.get("evidence_bytes", self.evidence_bytes),
            changes.get("digest_text", self.digest),
            changes.get("reference", self.reference),
        )

    def assert_rejected(self, key: str, value) -> None:
        with self.assertRaises(Exception):
            self.validate(**{key: value})

    def test_exact_records_validate(self) -> None:
        self.validate()

    def test_rejects_stale_constitution(self) -> None:
        value = copy.deepcopy(self.profile)
        value["constitutional_source"]["effective_version"] = "1.0.0"
        self.assert_rejected("profile", value)

    def test_rejects_provider_projection(self) -> None:
        value = copy.deepcopy(self.profile)
        value["github_projection"]["custom_properties"]["constitutional_profile"] = "Provider"
        self.assert_rejected("profile", value)

    def test_rejects_false_closure_or_stale_p0(self) -> None:
        for path, replacement in (
            ("status", "phase_a_repair_required"),
            ("open_priority_counts", {"P0": 1, "P1": 2, "P2": 2, "P3": 0}),
        ):
            value = copy.deepcopy(self.reconciliation)
            value[path] = replacement
            self.assert_rejected("reconciliation", value)

    def test_rejects_reconciliation_claim_inflation(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["phase_boundaries"]["profile_conformance_authorized"] = True
        self.assert_rejected("reconciliation", value)

    def test_rejects_property_readback_substitution(self) -> None:
        value = copy.deepcopy(self.evidence)
        value["property_values_after"]["constitutional_profile"] = "Provider"
        self.assert_rejected("evidence", value)

    def test_rejects_protected_main_movement(self) -> None:
        value = copy.deepcopy(self.evidence)
        value["main_sha_after"] = "0" * 40
        self.assert_rejected("evidence", value)

    def test_rejects_ruleset_bypass(self) -> None:
        value = copy.deepcopy(self.evidence)
        value["ruleset_after"]["bypass_actors"] = [{"actor_id": 1}]
        self.assert_rejected("evidence", value)

    def test_rejects_semantic_or_companion_digest_substitution(self) -> None:
        value = copy.deepcopy(self.evidence)
        value["evidence_sha256"] = "0" * 64
        self.assert_rejected("evidence", value)
        self.assert_rejected("digest_text", "0" * 64 + "  wrong.json\n")

    def test_rejects_final_file_digest_substitution(self) -> None:
        value = copy.deepcopy(self.reference)
        value["retained_evidence"]["json_sha256"] = "0" * 64
        self.assert_rejected("reference", value)

    def test_rejects_workflow_or_artifact_substitution(self) -> None:
        for field, replacement in (
            ("workflow_run", 1),
            ("artifact_zip_sha256", "0" * 64),
        ):
            value = copy.deepcopy(self.reference)
            value["source"][field] = replacement
            self.assert_rejected("reference", value)

    def test_rejects_evidence_claim_inflation(self) -> None:
        value = copy.deepcopy(self.evidence)
        value["claim_boundaries"]["profile_conformance_authorized"] = True
        self.assert_rejected("evidence", value)


if __name__ == "__main__":
    unittest.main()
