from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from agent_staffing import (  # noqa: E402
    AgentStaffingError,
    validate,
    validate_documentary_coverage,
    validate_review_set,
)


def review(role: str, pass_id: str) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "work_class": "substantive",
        "effects": ["public_contract"],
        "reviewer_system_id": "codex-system-1",
        "logical_pass_id": pass_id,
        "role": role,
        "mode": "non_authoring_read_only",
        "subject": {
            "repository": "grandchallenge/example",
            "commit": "a" * 40,
            "tree": "b" * 40,
            "base_commit": "c" * 40,
            "dependency_closure_sha256": "d" * 64,
            "material_evidence_sha256": "e" * 64,
        },
        "criteria": [f"{role} criteria"],
        "finding": "approved",
        "evidence": [f"{role} evidence"],
        "unresolved_obligations": [],
        "reserved_authority_ref": None,
        "authority_claims": {"human_authorized": False, "mathcert_certified": False},
    }


class AgentStaffingTests(unittest.TestCase):
    def test_candidate_contract_is_well_formed(self) -> None:
        validate()

    def test_documentary_coverage_is_complete(self) -> None:
        validate_documentary_coverage()

    def test_one_system_may_staff_distinct_non_reserved_passes(self) -> None:
        validate_review_set([review("Adversary", "adversary-1"), review("Referee", "referee-1")])

    def test_hostile_mutations_fail_closed(self) -> None:
        mutations = (
            lambda rows: rows[1].update(logical_pass_id="adversary-1"),
            lambda rows: rows[1].update(mode="authoring"),
            lambda rows: rows[1]["subject"].update(tree="f" * 40),
            lambda rows: rows[0].update(work_class="routine_bounded"),
            lambda rows: rows[0]["authority_claims"].update(mathcert_certified=True),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                rows = [review("Adversary", "adversary-1"), review("Referee", "referee-1")]
                mutation(rows)
                with self.assertRaises(Exception):
                    validate_review_set(rows)

    def test_duplicated_analysis_is_not_independence(self) -> None:
        rows = [review("Adversary", "adversary-1"), review("Referee", "referee-1")]
        rows[1]["criteria"] = copy.deepcopy(rows[0]["criteria"])
        rows[1]["evidence"] = copy.deepcopy(rows[0]["evidence"])
        with self.assertRaisesRegex(AgentStaffingError, "duplicated analysis"):
            validate_review_set(rows)
