from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci" / "settings_readback_owner_export_overlay.py"
SPEC = importlib.util.spec_from_file_location("settings_overlay", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OwnerExportOverlayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = MODULE.load(MODULE.REFERENCE)
        self.overlay = MODULE.load(MODULE.OVERLAY)
        self.base = MODULE.load(MODULE.BASE)

    def validate(self, reference=None, overlay=None, base=None) -> None:
        MODULE.validate_records(
            reference if reference is not None else self.reference,
            overlay if overlay is not None else self.overlay,
            base if base is not None else self.base,
        )

    def test_exact_records_validate(self) -> None:
        self.validate()

    def test_rejects_evidence_merge_substitution(self) -> None:
        value = copy.deepcopy(self.reference)
        value["source"]["merge_commit"] = "0" * 40
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_blob_substitution(self) -> None:
        value = copy.deepcopy(self.reference)
        value["source"]["git_blob_sha1"] = "1" * 40
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_digest_substitution(self) -> None:
        value = copy.deepcopy(self.reference)
        value["source"]["sha256"] = "2" * 64
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_repository_omission(self) -> None:
        value = copy.deepcopy(self.reference)
        value["coverage"]["repositories"].pop()
        value["coverage"]["repository_count"] = 11
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_reopening_blocked_row(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["closed_rows"][0]["disposition"] = "readback_blocked"
        with self.assertRaises(Exception):
            self.validate(overlay=value)

    def test_rejects_open_row_omission(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["open_rows"].pop()
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
        value["claim_boundaries"]["certification_claim_authorized"] = True
        with self.assertRaises(Exception):
            self.validate(reference=value)

    def test_rejects_base_campaign_substitution(self) -> None:
        value = copy.deepcopy(self.overlay)
        value["base_campaign_record"]["admission_merge"] = "3" * 40
        with self.assertRaises(Exception):
            self.validate(overlay=value)


if __name__ == "__main__":
    unittest.main()
