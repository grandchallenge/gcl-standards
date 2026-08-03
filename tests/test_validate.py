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

    def math_adoption(self) -> dict[str, object]:
        return yaml.safe_load(
            (ROOT / "programme-adoption" / "MATH-PROGRAMME.yaml").read_text(
                encoding="utf-8"
            )
        )

    def admitted_standard_pending_programme_adoption(self) -> dict[str, object]:
        adoption = self.math_adoption()
        adoption["decision_status"] = "accepted"
        adoption["constitutional_source"]["amendment_status"] = "effective"
        adoption["constitutional_source"]["amendment_commit"] = "a" * 40
        adoption["constitutional_source"]["review_receipt"] = "receipt.json"
        adoption["standards_commit"] = "b" * 40
        return adoption

    def test_cert_profile_cannot_claim_policy_only(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "repository_profile.schema.json").read_text(
                encoding="utf-8"
            )
        )
        profile = json.loads(
            (ROOT / "fixtures" / "repository_profiles" / "MATHCERT.json").read_text(
                encoding="utf-8"
            )
        )
        broken = copy.deepcopy(profile)
        broken["claim_promotion_role"] = "unbounded"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(broken, schema)

    def test_proposed_adoption_tracks_acyclic_sequence(self) -> None:
        adoption = self.math_adoption()
        self.assertEqual(adoption["status"], "proposed")
        self.assertEqual(adoption["decision_status"], "proposed")
        self.assertEqual(
            adoption["decision_ref"],
            "decisions/ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md",
        )
        self.assertIsNone(adoption["constitutional_source"]["amendment_commit"])
        self.assertIsNone(adoption["constitutional_source"]["review_receipt"])
        self.assertIsNone(adoption["standards_commit"])
        validate_module.validate_math_programme_adoption(adoption)

    def test_accepted_adr_can_precede_programme_adoption(self) -> None:
        admitted = self.admitted_standard_pending_programme_adoption()
        self.assertEqual(admitted["status"], "proposed")
        self.assertEqual(admitted["decision_status"], "accepted")
        self.assertIsNone(admitted["activation_date"])
        validate_module.validate_math_programme_adoption(admitted)

    def test_active_adoption_requires_accepted_adr(self) -> None:
        broken = self.math_adoption()
        broken["status"] = "active"
        broken["constitutional_source"]["amendment_status"] = "effective"
        broken["constitutional_source"]["amendment_commit"] = "a" * 40
        broken["constitutional_source"]["review_receipt"] = "receipt.json"
        broken["standards_commit"] = "b" * 40
        broken["activation_date"] = "2026-08-03"
        with self.assertRaisesRegex(ValueError, "accepted ADR-0001"):
            validate_module.validate_math_programme_adoption(broken)

    def test_accepted_adr_requires_complete_exact_identity(self) -> None:
        admitted = self.admitted_standard_pending_programme_adoption()
        validate_module.validate_math_programme_adoption(admitted)
        mutations = (
            ("amendment_commit", "short"),
            ("standards_commit", "short"),
            ("review_receipt", ""),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                broken = copy.deepcopy(admitted)
                if field in {"amendment_commit", "review_receipt"}:
                    broken["constitutional_source"][field] = value
                else:
                    broken[field] = value
                with self.assertRaisesRegex(
                    ValueError, "effective amendment, review receipt"
                ):
                    validate_module.validate_math_programme_adoption(broken)

    def test_active_adoption_adds_activation_date(self) -> None:
        active = self.admitted_standard_pending_programme_adoption()
        active["status"] = "active"
        active["activation_date"] = "2026-08-03"
        validate_module.validate_math_programme_adoption(active)
        active["activation_date"] = "03-08-2026"
        with self.assertRaisesRegex(ValueError, "ISO activation date"):
            validate_module.validate_math_programme_adoption(active)

    def test_non_active_adoption_cannot_claim_activation_date(self) -> None:
        broken = self.admitted_standard_pending_programme_adoption()
        broken["activation_date"] = "2026-08-03"
        with self.assertRaisesRegex(ValueError, "cannot claim an activation date"):
            validate_module.validate_math_programme_adoption(broken)

    def test_adr_sequence_is_acyclic_and_numbered(self) -> None:
        decision = (
            ROOT / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"
        ).read_text(encoding="utf-8")
        self.assertIn("1. `GI-AMEND-0001` is ratified and effective", decision)
        for ordinal in range(2, 8):
            self.assertIn(f"{ordinal}.", decision)
        self.assertIn(
            "MATH-PROGRAMME pilot adoption follows ADR acceptance", decision
        )
        self.assertIn(
            "It is not a prerequisite for this ADR to become accepted", decision
        )
        self.assertNotIn("the mathematics pilot records its adoption commit", decision)

    def test_profile_cannot_name_standards_as_constitutional_source(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "repository_profile.schema.json").read_text(
                encoding="utf-8"
            )
        )
        profile = json.loads(
            (ROOT / "fixtures" / "repository_profiles" / "INTELLECT.json").read_text(
                encoding="utf-8"
            )
        )
        broken = copy.deepcopy(profile)
        broken["constitutional_source"]["repository"] = "grandchallenge/gcl-standards"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(broken, schema)

    def test_intellect_has_distinct_constitutional_profile(self) -> None:
        profile = json.loads(
            (ROOT / "fixtures" / "repository_profiles" / "INTELLECT.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(profile["profile"], "constitutional")
        self.assertNotIn("canonical_policy_source", profile)
        self.assertEqual(profile["operating_policy_source"]["status"], "candidate")

    def test_action_forks_have_supply_chain_only_profiles(self) -> None:
        for name in ("lean-action.json", "upload-pages-artifact.json"):
            with self.subTest(name=name):
                profile = json.loads(
                    (ROOT / "fixtures" / "repository_profiles" / name).read_text(
                        encoding="utf-8"
                    )
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
            (ROOT / "programme-adoption" / "REGRET-CONTRACT-1.0.0.yaml").read_text(
                encoding="utf-8"
            )
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
        self.assertEqual(adoption["source_lock"], validate_module.EXPECTED_REGRET_SOURCE_LOCK)
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
        self.assertTrue(all(value is False for value in adoption["claim_boundaries"].values()))


if __name__ == "__main__":
    unittest.main()
