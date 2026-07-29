from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate", ROOT / "ci" / "validate.py")
assert SPEC and SPEC.loader
validate_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_module)


class StandardsValidationTests(unittest.TestCase):
    def test_repository_profiles_and_adoption_validate(self) -> None:
        validate_module.validate()

    def test_cert_profile_cannot_claim_policy_only(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "repository_profile.schema.json").read_text(encoding="utf-8")
        )
        profile = json.loads(
            (
                ROOT
                / "fixtures"
                / "repository_profiles"
                / "MATHCERT.json"
            ).read_text(encoding="utf-8")
        )
        broken = copy.deepcopy(profile)
        broken["claim_promotion_role"] = "unbounded"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(broken, schema)

    def test_active_adoption_requires_exact_identity(self) -> None:
        adoption_path = ROOT / "programme-adoption" / "MATH-PROGRAMME.yaml"
        text = adoption_path.read_text(encoding="utf-8")
        self.assertIn("amendment_status: proposed", text)
        self.assertIn("amendment_commit: null", text)
        self.assertIn("standards_commit: null", text)
        self.assertIn("status: proposed", text)

    def test_profile_cannot_name_standards_as_constitutional_source(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "repository_profile.schema.json").read_text(
                encoding="utf-8"
            )
        )
        profile = json.loads(
            (
                ROOT / "fixtures" / "repository_profiles" / "INTELLECT.json"
            ).read_text(encoding="utf-8")
        )
        broken = copy.deepcopy(profile)
        broken["constitutional_source"]["repository"] = (
            "grandchallenge/gcl-standards"
        )
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(broken, schema)

    def test_intellect_has_distinct_constitutional_profile(self) -> None:
        profile = json.loads(
            (
                ROOT / "fixtures" / "repository_profiles" / "INTELLECT.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(profile["profile"], "constitutional")
        self.assertNotIn("canonical_policy_source", profile)
        self.assertEqual(
            profile["operating_policy_source"]["status"], "candidate"
        )


if __name__ == "__main__":
    unittest.main()
