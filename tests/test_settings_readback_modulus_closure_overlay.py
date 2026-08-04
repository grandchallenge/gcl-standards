from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci" / "settings_readback_modulus_closure_overlay.py"
SPEC = importlib.util.spec_from_file_location("modulus_closure_overlay", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ModulusClosureOverlayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = MODULE.load(MODULE.REFERENCE)
        self.overlay = MODULE.load(MODULE.OVERLAY)
        self.prior = MODULE.load(MODULE.PRIOR_OVERLAY)
        self.base = MODULE.load(MODULE.BASE)

    def validate(self, reference=None, overlay=None, prior=None, base=None) -> None:
        MODULE.validate_records(
            reference if reference is not None else self.reference,
            overlay if overlay is not None else self.overlay,
            prior if prior is not None else self.prior,
            base if base is not None else self.base,
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

    def test_rejects_unresolved_readback_finding(self) -> None:
        value = copy.deepcopy(self.reference)
        value["verified_state"]["validation_findings"] = ["unexpected"]
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_modulus_row_omission(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["closed_rows"] = [
            row for row in value["closed_rows"] if row["id"] != "MODULUS-P1-001"
        ]
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_modulus_reopening(self) -> None:
        value = copy.deepcopy(self.overlay)
        for row in value["closed_rows"]:
            if row["id"] == "MODULUS-P2-001":
                row["disposition"] = "repair_required"
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_quantum_closure(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["open_rows"][0]["disposition"] = "closed_repair_verified"
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_quantum_row_omission(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["open_rows"].pop()
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_priority_count_drift(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["open_priority_counts"]["P1"] = 0
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_prior_overlay_substitution(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["prior_overlay"]["merge_commit"] = "3" * 40
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
