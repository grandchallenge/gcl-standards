from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

import jsonschema
import yaml


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
        self.assertIn("review_receipt: null", text)
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

    def test_action_forks_have_supply_chain_only_profiles(self) -> None:
        for name in ("lean-action.json", "upload-pages-artifact.json"):
            with self.subTest(name=name):
                profile = json.loads(
                    (
                        ROOT / "fixtures" / "repository_profiles" / name
                    ).read_text(encoding="utf-8")
                )
                self.assertEqual(profile["profile"], "provider")
                self.assertEqual(profile["claim_promotion_role"], "none")
                self.assertEqual(profile["risk_tier"], "critical")
                self.assertEqual(
                    profile["required_workflow_profile"],
                    "provider-action-supply-chain",
                )
                self.assertIn(
                    "no constitutional, programme, or mathematical claim authority",
                    profile["authority_scope"],
                )

    def regret_schema(self) -> dict[str, object]:
        return json.loads(
            (ROOT / "schemas" / "regret_contract.schema.json").read_text(
                encoding="utf-8"
            )
        )

    def regret_template(self) -> dict[str, object]:
        return yaml.safe_load(
            (ROOT / "templates" / "regret_contract.yaml").read_text(
                encoding="utf-8"
            )
        )

    def regret_adoption(self) -> dict[str, object]:
        return yaml.safe_load(
            (
                ROOT
                / "programme-adoption"
                / "REGRET-CONTRACT-1.0.0.yaml"
            ).read_text(encoding="utf-8")
        )

    def test_regret_contract_template_validates(self) -> None:
        jsonschema.validate(
            self.regret_template(),
            self.regret_schema(),
            cls=jsonschema.Draft202012Validator,
        )

    def test_tracking_requires_switch_comparator(self) -> None:
        broken = copy.deepcopy(self.regret_template())
        broken["guarantee"] = "tracking"
        broken["comparator"] = "fixed"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(
                broken,
                self.regret_schema(),
                cls=jsonschema.Draft202012Validator,
            )

    def test_delayed_feedback_requires_delay_field(self) -> None:
        broken = copy.deepcopy(self.regret_template())
        broken["feedback"] = "delayed_bandit"
        del broken["delayed_feedback_max_steps"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(
                broken,
                self.regret_schema(),
                cls=jsonschema.Draft202012Validator,
            )

    def test_regret_source_lock_is_exact(self) -> None:
        adoption = self.regret_adoption()
        self.assertEqual(
            adoption["source_lock"], validate_module.EXPECTED_REGRET_SOURCE_LOCK
        )
        self.assertEqual(
            adoption["reference_implementation"]["commit_sha"],
            "641ba766fe8eec613a01cd4726841b1d4e93ad78",
        )

    def test_regret_adoption_coverage_and_obligations(self) -> None:
        adoption = self.regret_adoption()
        rows = adoption["programmes"]
        self.assertEqual(
            {row["programme"] for row in rows},
            validate_module.EXPECTED_REGRET_PROGRAMMES,
        )
        self.assertTrue(all(row["unresolved_obligations"] for row in rows))

    def test_regret_candidate_cannot_claim_activation(self) -> None:
        adoption = self.regret_adoption()
        self.assertEqual(adoption["status"], "candidate_migrated")
        self.assertIsNone(adoption["standards_commit"])
        self.assertTrue(
            all(value is False for value in adoption["claim_boundaries"].values())
        )


if __name__ == "__main__":
    unittest.main()
