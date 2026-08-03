from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "math_programme_pilot_adoption",
    ROOT / "ci" / "math_programme_pilot_adoption.py",
)
assert SPEC and SPEC.loader
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


class MathProgrammePilotAdoptionTests(unittest.TestCase):
    def records(self) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        return (
            pilot.load_yaml(pilot.ADOPTION_PATH),
            pilot.load_json(pilot.ADMISSION_PATH),
            pilot.load_json(pilot.SCHEMA_PATH),
        )

    def test_active_pilot_adoption_validates(self) -> None:
        adoption, admission, schema = self.records()
        pilot.validate_records(adoption, admission, schema)
        self.assertEqual(adoption["status"], "active")
        self.assertEqual(adoption["decision_status"], "accepted")
        self.assertTrue(adoption["claim_boundaries"]["programme_pilot_adoption_complete"])

    def test_activation_commit_substitution_fails_closed(self) -> None:
        adoption, admission, schema = self.records()
        mutated = copy.deepcopy(adoption)
        mutated["constitutional_source"]["amendment_commit"] = "a" * 40
        mutated["constitutional_source"]["review_receipt"]["commit_sha"] = "a" * 40
        with self.assertRaisesRegex(pilot.PilotAdoptionError, "activation commit drift"):
            pilot.validate_records(mutated, admission, schema)

    def test_receipt_admission_substitution_fails_closed(self) -> None:
        adoption, admission, schema = self.records()
        mutated = copy.deepcopy(adoption)
        mutated["constitutional_source"]["review_receipt"]["admission_commit"] = "b" * 40
        with self.assertRaisesRegex(pilot.PilotAdoptionError, "receipt admission commit drift"):
            pilot.validate_records(mutated, admission, schema)

    def test_standard_admission_substitution_fails_closed(self) -> None:
        adoption, admission, schema = self.records()
        mutated = copy.deepcopy(adoption)
        mutated["standards_commit"] = "c" * 40
        mutated["standard_admission"]["commit_sha"] = "c" * 40
        with self.assertRaisesRegex(pilot.PilotAdoptionError, "standards admission merge drift"):
            pilot.validate_records(mutated, admission, schema)

    def test_reviewed_blob_substitution_fails_closed(self) -> None:
        adoption, admission, schema = self.records()
        mutated = copy.deepcopy(adoption)
        mutated["standard_admission"]["standard_git_blob_sha1"] = "d" * 40
        with self.assertRaisesRegex(pilot.PilotAdoptionError, "standard blob identity drift"):
            pilot.validate_records(mutated, admission, schema)

    def test_claim_inflation_fails_schema(self) -> None:
        adoption, admission, schema = self.records()
        mutated = copy.deepcopy(adoption)
        mutated["claim_boundaries"]["organization_wide_conformance_authorized"] = True
        with self.assertRaises(Exception):
            pilot.validate_records(mutated, admission, schema)

    def test_pilot_retains_unresolved_deviations(self) -> None:
        adoption, admission, schema = self.records()
        mutated = copy.deepcopy(adoption)
        mutated["unresolved_deviations"] = []
        with self.assertRaises(Exception):
            pilot.validate_records(mutated, admission, schema)


if __name__ == "__main__":
    unittest.main()
