from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "standard_admission", ROOT / "ci" / "standard_admission.py"
)
assert SPEC and SPEC.loader
standard_admission = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(standard_admission)


class GCLGHOSAdmissionTests(unittest.TestCase):
    def admission(self) -> dict[str, object]:
        return json.loads(
            (ROOT / "admissions" / "GCL-GHOS-00-0.1.0.json").read_text(
                encoding="utf-8"
            )
        )

    def test_canonical_admission_is_exact(self) -> None:
        record = standard_admission.validate_standard_admission()
        self.assertEqual(record["status"], "admitted")
        self.assertEqual(record["decision"]["status"], "accepted")
        self.assertEqual(record["standard"]["status"], "admitted")
        self.assertEqual(
            record["decision"]["reviewed_commit"],
            "fa90ffc2bd23a6b0c8e184c7da2dd6ef1174a4ee",
        )
        self.assertEqual(
            record["standard"]["reviewed_commit"],
            "fa90ffc2bd23a6b0c8e184c7da2dd6ef1174a4ee",
        )

    def test_schema_is_closed(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "standard_admission.schema.json").read_text(
                encoding="utf-8"
            )
        )
        broken = self.admission()
        broken["unexpected"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(
                broken,
                schema,
                cls=jsonschema.Draft202012Validator,
                format_checker=jsonschema.FormatChecker(),
            )

    def test_reviewed_commit_drift_fails_closed(self) -> None:
        for artifact in ("decision", "standard"):
            with self.subTest(artifact=artifact):
                broken = copy.deepcopy(self.admission())
                broken[artifact]["reviewed_commit"] = "0" * 40
                with self.assertRaisesRegex(
                    standard_admission.StandardAdmissionError,
                    "reviewed commit drift",
                ):
                    standard_admission.validate_standard_admission(broken)

    def test_source_blob_drift_fails_closed(self) -> None:
        for artifact in ("decision", "standard"):
            with self.subTest(artifact=artifact):
                broken = copy.deepcopy(self.admission())
                broken[artifact]["git_blob_sha1"] = "0" * 40
                with self.assertRaisesRegex(
                    standard_admission.StandardAdmissionError,
                    "source blob drift",
                ):
                    standard_admission.validate_standard_admission(broken)

    def test_agent_identity_and_session_collapse_fail_closed(self) -> None:
        for field, message in (
            ("reviewer_id", "identities must differ"),
            ("session_id", "sessions must differ"),
        ):
            with self.subTest(field=field):
                broken = copy.deepcopy(self.admission())
                broken["review_staffing"]["referee"][field] = (
                    broken["review_staffing"]["adversary"][field]
                )
                with self.assertRaisesRegex(
                    standard_admission.StandardAdmissionError,
                    message,
                ):
                    standard_admission.validate_standard_admission(broken)

    def test_receipt_substitution_fails_closed(self) -> None:
        broken = copy.deepcopy(self.admission())
        broken["constitutional_authority"]["review_receipt"]["packet_sha256"] = (
            "0" * 64
        )
        with self.assertRaisesRegex(
            standard_admission.StandardAdmissionError,
            "review packet digest drift",
        ):
            standard_admission.validate_standard_admission(broken)

    def test_claim_inflation_fails_closed(self) -> None:
        broken = copy.deepcopy(self.admission())
        broken["claim_boundaries"]["organization_wide_conformance_authorized"] = True
        with self.assertRaises(jsonschema.ValidationError):
            standard_admission.validate_standard_admission(broken)

    def test_programme_adoption_remains_separate_and_proposed(self) -> None:
        adoption = yaml.safe_load(
            (ROOT / "programme-adoption" / "MATH-PROGRAMME.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(adoption["status"], "proposed")
        self.assertEqual(adoption["decision_status"], "proposed")
        self.assertIsNone(adoption["standards_commit"])
        self.assertIsNone(adoption["activation_date"])
        self.assertFalse(
            self.admission()["claim_boundaries"]["programme_adoption_complete"]
        )

    def test_source_headers_remain_historical_reviewed_state(self) -> None:
        decision = (
            ROOT / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"
        ).read_text(encoding="utf-8")
        standard = (ROOT / "standards" / "GCL-GHOS-00.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("**Status:** Proposed for successor exact-packet review", decision)
        self.assertIn("**Status:** Candidate", standard)
        self.assertEqual(self.admission()["effective_condition"], "protected_merge_of_this_exact_record")


if __name__ == "__main__":
    unittest.main()
