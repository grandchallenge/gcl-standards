from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("settings_readback", ROOT / "ci" / "settings_readback.py")
assert SPEC and SPEC.loader
settings_readback = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(settings_readback)

class SettingsReadbackTests(unittest.TestCase):
    def normalized(self):
        return json.loads(settings_readback.NORMALIZED.read_text(encoding="utf-8"))
    def ledger(self):
        return json.loads(settings_readback.LEDGER.read_text(encoding="utf-8"))
    def test_canonical_evidence_validates(self):
        normalized, ledger = settings_readback.validate_settings_readback()
        self.assertEqual(normalized["repository_count"], 12)
        self.assertFalse(ledger["organization_wide_conformance"])
        self.assertEqual(ledger["open_priority_counts"], {"P0": 0, "P1": 3, "P2": 2, "P3": 0})
    def test_repository_omission_fails_closed(self):
        normalized = self.normalized(); ledger = self.ledger()
        normalized["repositories"].pop()
        with self.assertRaises((jsonschema.ValidationError, settings_readback.SettingsReadbackError)):
            settings_readback.validate_settings_readback(normalized, ledger)
    def test_duplicate_disposition_id_fails_closed(self):
        normalized = self.normalized(); ledger = self.ledger()
        ledger["rows"].append(copy.deepcopy(ledger["rows"][0]))
        with self.assertRaisesRegex(settings_readback.SettingsReadbackError, "duplicate deviation row id"):
            settings_readback.validate_settings_readback(normalized, ledger)
    def test_false_conformance_with_open_p1_fails_closed(self):
        normalized = self.normalized(); ledger = self.ledger()
        ledger["organization_wide_conformance"] = True
        with self.assertRaises((jsonschema.ValidationError, settings_readback.SettingsReadbackError)):
            settings_readback.validate_settings_readback(normalized, ledger)
    def test_blocked_readback_cannot_be_relabelled_conformant_without_evidence(self):
        normalized = self.normalized(); ledger = self.ledger()
        row = next(row for row in ledger["rows"] if row["id"] == "ORG-READBACK-BLOCKED-001")
        row["disposition"] = "conformant"
        row["remediation_issue"] = None
        with self.assertRaisesRegex(settings_readback.SettingsReadbackError, "missing required deviation scope|open deviation|blocked readback|conformance"):
            # Remove required repository deviation scope as an additional unsupported-inference mutation.
            ledger["rows"] = [r for r in ledger["rows"] if r["scope"] != "grandchallenge/MODULUS"]
            settings_readback.validate_settings_readback(normalized, ledger)
    def test_open_deviation_requires_remediation_issue(self):
        normalized = self.normalized(); ledger = self.ledger()
        row = next(row for row in ledger["rows"] if row["disposition"] == "repair_required")
        row["remediation_issue"] = None
        with self.assertRaisesRegex(settings_readback.SettingsReadbackError, "lacks remediation issue"):
            settings_readback.validate_settings_readback(normalized, ledger)

if __name__ == "__main__":
    unittest.main()
