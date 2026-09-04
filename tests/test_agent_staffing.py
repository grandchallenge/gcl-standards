from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from agent_staffing import (  # noqa: E402
    AgentStaffingError,
    ROLLOUT,
    validate,
    validate_review_set,
    validate_rollout,
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


def test_candidate_contract_is_well_formed() -> None:
    validate()


def test_one_system_may_staff_distinct_non_reserved_passes() -> None:
    validate_review_set([review("Adversary", "adversary-1"), review("Referee", "referee-1")])


def test_rollout_cannot_claim_early_effectiveness(monkeypatch, tmp_path: Path) -> None:
    candidate = ROLLOUT.read_text(encoding="utf-8").replace(
        '"status": "candidate_pending_superior_authority"', '"status": "effective"'
    )
    changed = tmp_path / "rollout.json"
    changed.write_text(candidate, encoding="utf-8")
    monkeypatch.setattr("agent_staffing.ROLLOUT", changed)
    with pytest.raises(AgentStaffingError, match="effective status"):
        validate_rollout()


@pytest.mark.parametrize("mutation, message", [
    (lambda rows: rows[1].update(logical_pass_id="adversary-1"), "identifiers"),
    (lambda rows: rows[1].update(mode="authoring"), "read-only"),
    (lambda rows: rows[1]["subject"].update(tree="f" * 40), "drift"),
    (lambda rows: rows[0].update(work_class="routine_bounded"), "routine-classified"),
    (lambda rows: rows[0]["authority_claims"].update(mathcert_certified=True), "schema"),
])
def test_hostile_mutations_fail_closed(mutation, message: str) -> None:
    rows = [review("Adversary", "adversary-1"), review("Referee", "referee-1")]
    mutation(rows)
    with pytest.raises((AgentStaffingError, Exception), match=message):
        validate_review_set(rows)


def test_duplicated_analysis_is_not_independence() -> None:
    rows = [review("Adversary", "adversary-1"), review("Referee", "referee-1")]
    rows[1]["criteria"] = copy.deepcopy(rows[0]["criteria"])
    rows[1]["evidence"] = copy.deepcopy(rows[0]["evidence"])
    with pytest.raises(AgentStaffingError, match="duplicated analysis"):
        validate_review_set(rows)
