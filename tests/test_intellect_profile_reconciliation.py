from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci" / "intellect_profile_reconciliation.py"
SPEC = importlib.util.spec_from_file_location(
    "intellect_profile_reconciliation", MODULE_PATH
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class IntellectProfileReconciliationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = MODULE.load(MODULE.PROFILE)
        self.reconciliation = MODULE.load(MODULE.RECONCILIATION)
        self.base_campaign = MODULE.load(MODULE.BASE_CAMPAIGN)
        self.owner_overlay = MODULE.load(MODULE.OWNER_OVERLAY)
        self.owner_reference = MODULE.load(MODULE.OWNER_REFERENCE)

    def validate(
        self,
        profile=None,
        reconciliation=None,
        base_campaign=None,
        owner_overlay=None,
        owner_reference=None,
    ) -> None:
        MODULE.validate_records(
            profile if profile is not None else self.profile,
            reconciliation if reconciliation is not None else self.reconciliation,
            base_campaign if base_campaign is not None else self.base_campaign,
            owner_overlay if owner_overlay is not None else self.owner_overlay,
            owner_reference if owner_reference is not None else self.owner_reference,
        )

    def test_exact_records_validate(self) -> None:
        self.validate()

    def test_rejects_stale_constitution_version(self) -> None:
        value = copy.deepcopy(self.profile)
        value["constitutional_source"]["effective_version"] = "1.0.0"
        with self.assertRaises(Exception):
            self.validate(profile=value)

    def test_rejects_candidate_standard_status(self) -> None:
        value = copy.deepcopy(self.profile)
        value["operating_policy_source"]["status"] = "candidate"
        with self.assertRaises(Exception):
            self.validate(profile=value)

    def test_rejects_malformed_authority_commit(self) -> None:
        value = copy.deepcopy(self.profile)
        value["constitutional_source"]["activation_commit"] = "short"
        with self.assertRaises(Exception):
            self.validate(profile=value)

    def test_rejects_ambiguous_claim_role_mapping(self) -> None:
        value = copy.deepcopy(self.profile)
        value["github_projection"]["projection_semantics"][
            "live_claim_promotion_role"
        ] = "policy_only"
        with self.assertRaises(Exception):
            self.validate(profile=value)

    def test_rejects_provider_property_substitution(self) -> None:
        value = copy.deepcopy(self.profile)
        value["github_projection"]["custom_properties"][
            "constitutional_profile"
        ] = "Provider"
        with self.assertRaises(Exception):
            self.validate(profile=value)

    def test_rejects_provider_ruleset_substitution(self) -> None:
        value = copy.deepcopy(self.profile)
        value["github_projection"]["default_branch_ruleset"] = (
            "Provider profile - main"
        )
        with self.assertRaises(Exception):
            self.validate(profile=value)

    def test_rejects_false_intellect_conformance(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["repair_row"]["disposition"] = "conformant"
        with self.assertRaises(Exception):
            self.validate(reconciliation=value)

    def test_rejects_priority_downgrade(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["repair_row"]["priority"] = "P1"
        with self.assertRaises(Exception):
            self.validate(reconciliation=value)

    def test_rejects_missing_carried_deviation(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["carried_open_rows"].pop()
        with self.assertRaises(Exception):
            self.validate(reconciliation=value)

    def test_rejects_live_mutation_in_phase_a(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["phase_boundaries"]["phase_a_live_mutation_authorized"] = True
        with self.assertRaises(Exception):
            self.validate(reconciliation=value)

    def test_rejects_profile_conformance_claim(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["phase_boundaries"]["profile_conformance_authorized"] = True
        with self.assertRaises(Exception):
            self.validate(reconciliation=value)

    def test_rejects_claim_inflation(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["claim_boundaries"]["certification_claim_authorized"] = True
        with self.assertRaises(Exception):
            self.validate(reconciliation=value)

    def test_rejects_owner_evidence_substitution(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["base_records"]["owner_export_reference"]["source_sha256"] = (
            "0" * 64
        )
        with self.assertRaises(Exception):
            self.validate(reconciliation=value)

    def test_rejects_base_false_conformance_rewrite(self) -> None:
        value = copy.deepcopy(self.base_campaign)
        for row in value["rows"]:
            if row.get("id") == "OBS-INTELLECT-001":
                row["disposition"] = "repair_required"
        with self.assertRaises(Exception):
            self.validate(base_campaign=value)


if __name__ == "__main__":
    unittest.main()
