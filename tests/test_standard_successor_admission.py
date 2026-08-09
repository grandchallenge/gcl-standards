from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "standard_successor_admission",
    ROOT / "ci" / "standard_successor_admission.py",
)
assert SPEC and SPEC.loader
successor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(successor)


class SuccessorAdmissionTests(unittest.TestCase):
    def admission(self) -> dict[str, object]:
        return json.loads(
            (ROOT / "admissions" / "GCL-GHOS-00-0.1.1.json").read_text(
                encoding="utf-8"
            )
        )

    def test_exact_successor_admission_passes(self) -> None:
        record = successor.validate_successor_admission()
        self.assertEqual(record["status"], "admitted")
        self.assertEqual(record["next_gate"]["status"], "not_started")

    def test_schema_is_closed_and_valid(self) -> None:
        schema = json.loads(
            (
                ROOT / "schemas" / "standard_successor_admission.schema.json"
            ).read_text(encoding="utf-8")
        )
        jsonschema.Draft202012Validator.check_schema(schema)
        broken = self.admission()
        broken["constitutional_claim_authorized"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(broken, schema, cls=jsonschema.Draft202012Validator)

    def test_recorded_source_blob_substitution_fails_closed(self) -> None:
        broken = copy.deepcopy(self.admission())
        broken["reviewed_source"]["artifacts"][0]["git_blob_sha1"] = "0" * 40
        with self.assertRaisesRegex(
            successor.SuccessorAdmissionError,
            "recorded source blob identities drift",
        ):
            successor.validate_successor_admission(broken)

    def test_reviewed_head_substitution_fails_closed(self) -> None:
        broken = copy.deepcopy(self.admission())
        broken["reviewed_source"]["reviewed_commit"] = "0" * 40
        with self.assertRaises(jsonschema.ValidationError):
            successor.validate_successor_admission(broken)

    def test_claim_authority_inflation_fails_closed(self) -> None:
        for key in self.admission()["claim_boundaries"]:
            with self.subTest(key=key):
                broken = copy.deepcopy(self.admission())
                broken["claim_boundaries"][key] = True
                with self.assertRaises(jsonschema.ValidationError):
                    successor.validate_successor_admission(broken)

    def test_agent_identity_and_session_must_be_distinct(self) -> None:
        broken = copy.deepcopy(self.admission())
        broken["review_staffing"]["referee"]["reviewer_id"] = broken[
            "review_staffing"
        ]["adversary"]["reviewer_id"]
        with self.assertRaisesRegex(
            successor.SuccessorAdmissionError,
            "identities must differ",
        ):
            successor.validate_successor_admission(broken)


if __name__ == "__main__":
    unittest.main()
