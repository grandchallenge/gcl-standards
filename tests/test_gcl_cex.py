from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from gcl_cex import GCLCEXError, validate, validate_completion_receipt  # noqa: E402


def review(role: str, pass_id: str, *, criteria: str, evidence: str) -> dict[str, object]:
    return {
        "record_ref": f"https://github.com/grandchallenge/example/issues/1#issuecomment-{pass_id}",
        "reviewer_system_id": "codex-system-1",
        "logical_pass_id": pass_id,
        "role": role,
        "mode": "non_authoring_read_only",
        "reviewed_repository": "grandchallenge/example",
        "reviewed_candidate_head": "a" * 40,
        "criteria": [criteria],
        "finding": "approved",
        "evidence": [evidence],
        "unresolved_obligations": [],
        "authority_claims": {"human_authorized": False, "mathcert_certified": False},
    }


def receipt() -> dict[str, object]:
    return {
        "schema_version": "0.1.0",
        "record_type": "GCL_COMPLETION_RECEIPT",
        "campaign": "EXAMPLE-001",
        "operation": "EXAMPLE-WP01",
        "candidate_head": "a" * 40,
        "merge_sha": "b" * 40,
        "protected_readback_sha": "b" * 40,
        "staffing_authority": {
            "repository": "grandchallenge/INTELLECT",
            "directive": "GI-STEWARD-0003",
            "separation_model": "role_scoped_logical_passes",
        },
        "adversary_record": review(
            "Adversary", "adversary-pass-1", criteria="challenge overreach", evidence="exact-head theorem and firewall"
        ),
        "referee_record": review(
            "Referee", "referee-pass-1", criteria="assess coherence", evidence="exact-head contract and checks"
        ),
        "required_checks": [
            {"phase": "candidate", "name": "preflight", "result": "success", "head": "a" * 40},
            {"phase": "protected_readback", "name": "post-merge", "result": "success", "head": "b" * 40},
        ],
        "disposition": {
            "type": "CLOSED",
            "frontier": "EXAMPLE_FRONTIER",
            "established": ["EXAMPLE_RESULT"],
            "next_frontier": "EXAMPLE_NEXT",
        },
        "preserved_false": ["STRONGER_CLAIM_FALSE"],
    }


class GCLCEXTests(unittest.TestCase):
    def test_standard_contract_is_well_formed(self) -> None:
        validate()

    def test_one_system_may_supply_distinct_logical_review_passes(self) -> None:
        validate_completion_receipt(receipt())

    def test_reused_logical_pass_is_rejected(self) -> None:
        row = receipt()
        row["referee_record"]["logical_pass_id"] = row["adversary_record"]["logical_pass_id"]
        with self.assertRaisesRegex(GCLCEXError, "distinct logical_pass_id"):
            validate_completion_receipt(row)

    def test_same_durable_review_record_is_rejected(self) -> None:
        row = receipt()
        row["referee_record"]["record_ref"] = row["adversary_record"]["record_ref"]
        with self.assertRaisesRegex(GCLCEXError, "distinct durable review records"):
            validate_completion_receipt(row)

    def test_duplicated_analysis_is_rejected(self) -> None:
        row = receipt()
        row["referee_record"]["criteria"] = copy.deepcopy(row["adversary_record"]["criteria"])
        row["referee_record"]["evidence"] = copy.deepcopy(row["adversary_record"]["evidence"])
        with self.assertRaisesRegex(GCLCEXError, "duplicated analysis"):
            validate_completion_receipt(row)

    def test_stale_reviewed_head_is_rejected(self) -> None:
        row = receipt()
        row["referee_record"]["reviewed_candidate_head"] = "c" * 40
        with self.assertRaisesRegex(GCLCEXError, "exact candidate head"):
            validate_completion_receipt(row)

    def test_stale_candidate_check_is_rejected(self) -> None:
        row = receipt()
        row["required_checks"][0]["head"] = "c" * 40
        with self.assertRaisesRegex(GCLCEXError, "candidate check is stale"):
            validate_completion_receipt(row)

    def test_read_only_review_mode_is_enforced(self) -> None:
        row = receipt()
        row["adversary_record"]["mode"] = "authoring"
        with self.assertRaises(Exception):
            validate_completion_receipt(row)

    def test_green_review_cannot_manufacture_authority(self) -> None:
        row = receipt()
        row["adversary_record"]["authority_claims"]["human_authorized"] = True
        with self.assertRaises(Exception):
            validate_completion_receipt(row)


if __name__ == "__main__":
    unittest.main()
