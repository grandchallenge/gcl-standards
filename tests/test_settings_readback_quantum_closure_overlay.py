from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci" / "settings_readback_quantum_closure_overlay.py"
SPEC = importlib.util.spec_from_file_location("quantum_closure_overlay", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class QuantumClosureOverlayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = MODULE.load(MODULE.REFERENCE)
        self.overlay = MODULE.load(MODULE.OVERLAY)
        self.prior = MODULE.load(MODULE.PRIOR_OVERLAY)
        self.base = MODULE.load(MODULE.BASE)
        self.profile = MODULE.load(MODULE.PROFILE)

    def validate(
        self,
        reference=None,
        overlay=None,
        prior=None,
        base=None,
        profile=None,
    ) -> None:
        MODULE.validate_records(
            reference if reference is not None else self.reference,
            overlay if overlay is not None else self.overlay,
            prior if prior is not None else self.prior,
            base if base is not None else self.base,
            profile if profile is not None else self.profile,
        )

    def test_exact_records_validate(self) -> None:
        self.validate()

    def test_rejects_evidence_merge_substitution(self) -> None:
        value = copy.deepcopy(self.reference)
        value["source"]["merge_commit"] = "0" * 40
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_evidence_blob_substitution(self) -> None:
        value = copy.deepcopy(self.reference)
        value["source"]["git_blob_sha1"] = "1" * 40
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_evidence_digest_substitution(self) -> None:
        value = copy.deepcopy(self.reference)
        value["source"]["sha256"] = "2" * 64
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_source_bundle_substitution(self) -> None:
        value = copy.deepcopy(self.reference)
        value["source"]["source_bundle_sha256"] = "3" * 64
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_profile_binding_substitution(self) -> None:
        value = copy.deepcopy(self.reference)
        value["standards_profile"]["merge_commit"] = "4" * 40
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_profile_semantic_drift(self) -> None:
        value = copy.deepcopy(self.profile)
        value["claim_promotion_role"] = "none"
        with self.assertRaises(Exception):
            self.validate(profile=value)

    def test_rejects_readback_gap(self) -> None:
        value = copy.deepcopy(self.reference)
        value["verified_state"]["readback_gaps"] = ["unexpected"]
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_settings_drift(self) -> None:
        value = copy.deepcopy(self.reference)
        value["verified_state"]["repository_merge_settings"][
            "allow_rebase_merge"
        ] = True
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_ruleset_drift(self) -> None:
        value = copy.deepcopy(self.reference)
        value["verified_state"]["strict_required_status_checks_policy"] = False
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_security_drift(self) -> None:
        value = copy.deepcopy(self.reference)
        value["verified_state"]["private_vulnerability_reporting_enabled"] = False
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_required_context_omission(self) -> None:
        value = copy.deepcopy(self.reference)
        value["verified_state"]["required_contexts"].pop()
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_prior_overlay_substitution(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["prior_overlay"]["merge_commit"] = "5" * 40
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_prior_quantum_row_omission(self) -> None:
        value = copy.deepcopy(self.prior)
        value["open_rows"].pop()
        with self.assertRaises(Exception):
            self.validate(prior=value)

    def test_rejects_closed_row_omission(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["closed_rows"] = [
            row
            for row in value["closed_rows"]
            if row["id"] != "QUANTUM-P1-001"
        ]
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_duplicate_closed_row(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["closed_rows"].append(copy.deepcopy(value["closed_rows"][-1]))
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_quantum_reopening(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["open_rows"] = [
            {
                "id": "QUANTUM-P2-001",
                "priority": "P2",
                "disposition": "repair_required",
            }
        ]
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_priority_count_drift(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["open_priority_counts"]["P1"] = 1
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_false_conformance(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["organization_wide_conformance"] = True
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_claim_inflation(self) -> None:
        value = copy.deepcopy(self.reference)
        value["claim_boundaries"]["commercial_claim_authorized"] = True
        with self.assertRaises(Exception):
            self.validate(reference=value)


if __name__ == "__main__":
    unittest.main()
