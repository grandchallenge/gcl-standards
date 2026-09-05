from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
REVIEW_SCHEMA = ROOT / "schemas" / "multi_role_review.schema.json"
ADOPTION_SCHEMA = ROOT / "schemas" / "repository_staffing_adoption.schema.json"
STANDARD = ROOT / "standards" / "GCL-AGENT-STAFFING-001.md"
ROLLOUT = ROOT / "status" / "GCL-AGENT-STAFFING-001-rollout.json"
DOCUMENTARY_COVERAGE = ROOT / "status" / "GCL-AGENT-STAFFING-001-documentary-coverage.json"
DOCUMENTARY_COVERAGE_SCHEMA = ROOT / "schemas" / "staffing_documentary_coverage.schema.json"
EXPECTED_REPOSITORIES = {
    "grandchallenge/INTELLECT", "grandchallenge/gcl-standards",
    "grandchallenge/.github", "grandchallenge/MATH-PROGRAMME",
    "grandchallenge/MATHFORGE", "grandchallenge/MATHSOLVE",
    "grandchallenge/MATHCERT", "grandchallenge/AETHER",
    "grandchallenge/TROVE-CURATA", "grandchallenge/BUTTERFLY",
    "grandchallenge/GLOSS", "grandchallenge/MODULUS",
    "grandchallenge/QUANTUM-TECHNOLOGIES", "grandchallenge/GCT-EXECUTIVE",
    "grandchallenge/lean-action", "grandchallenge/upload-pages-artifact",
}


class AgentStaffingError(ValueError):
    """Raised when functional role separation is not evidenced."""


def _load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schemas() -> None:
    for path in (REVIEW_SCHEMA, ADOPTION_SCHEMA, DOCUMENTARY_COVERAGE_SCHEMA):
        jsonschema.Draft202012Validator.check_schema(_load(path))


def validate_review_set(reviews: Sequence[Mapping[str, object]]) -> None:
    schema = _load(REVIEW_SCHEMA)
    pass_ids: set[str] = set()
    analyses: set[tuple[str, ...]] = set()
    subjects: set[tuple[str, ...]] = set()
    reserved_effects = {
        "human_authority", "math_certification", "destructive_disposal",
        "safety_critical", "credential_expansion", "public_commitment",
        "irreversible_resource", "production_semantic", "corpus_admission",
    }
    substantive_effects = {"public_contract", "authority_boundary", "material_result"}

    for review in reviews:
        jsonschema.validate(review, schema, format_checker=jsonschema.FormatChecker())
        pass_id = str(review["logical_pass_id"])
        if pass_id in pass_ids:
            raise AgentStaffingError("logical audit pass identifiers must be unique")
        pass_ids.add(pass_id)
        if review["role"] in {"Adversary", "Referee"} and review["mode"] != "non_authoring_read_only":
            raise AgentStaffingError("Adversary and Referee passes must be read-only")
        effects = set(review["effects"])
        if effects & reserved_effects and review["work_class"] != "reserved":
            raise AgentStaffingError("reserved effects cannot be classification-downgraded")
        if effects & substantive_effects and review["work_class"] == "routine_bounded":
            raise AgentStaffingError("substantive effects cannot be routine-classified")
        if review["work_class"] == "reserved" and review["reserved_authority_ref"] is None:
            raise AgentStaffingError("reserved work requires exact human authority")
        if review["work_class"] != "reserved" and review["reserved_authority_ref"] is not None:
            raise AgentStaffingError("non-reserved work cannot claim reserved authority")
        if review["finding"] == "approved" and review["unresolved_obligations"]:
            raise AgentStaffingError("approved review cannot retain obligations")
        if any(review["authority_claims"].values()):
            raise AgentStaffingError("a review cannot manufacture authority or certification")
        analysis = tuple(sorted(review["criteria"]) + sorted(review["evidence"]) + [str(review["finding"])])
        if analysis in analyses:
            raise AgentStaffingError("duplicated analysis is not a distinct logical pass")
        analyses.add(analysis)
        subject = review["subject"]
        subjects.add(tuple(str(subject[key]) for key in (
            "commit", "tree", "base_commit", "dependency_closure_sha256", "material_evidence_sha256"
        )))

    if len(subjects) > 1:
        raise AgentStaffingError("subject or material-evidence drift invalidates the review set")


def validate_standard() -> None:
    text = STANDARD.read_text(encoding="utf-8")
    required = (
        "`GI-STEWARD-0003` is effective",
        "A single Codex system MAY staff multiple non-reserved roles",
        "MUST NOT claim that a different system, invocation, task, model,",
        "Automation MAY prepare, faithfully record, and mechanically execute",
        "It MUST NOT manufacture or infer it.",
        "`non_authoring_read_only`",
        "certify a mathematical claim for which it supplied the sole construction",
        "green CI or numerical evidence supplies mathematical certification",
    )
    for boundary in required:
        if boundary not in text:
            raise AgentStaffingError(f"missing canonical staffing boundary: {boundary}")


def validate_rollout() -> None:
    rollout = _load(ROLLOUT)
    if not isinstance(rollout, dict):
        raise AgentStaffingError("rollout matrix must be an object")
    if rollout.get("status") != "effective":
        raise AgentStaffingError("rollout matrix must record effective completion")
    authority = rollout.get("superior_authority", {})
    if authority != {
        "repository": "grandchallenge/INTELLECT",
        "directive": "GI-STEWARD-0003",
        "candidate_commit": "d05bcf9d128333d49641de93df951355d8c2c041",
        "effective_commit": "7e01dc6b1be46171f0cba5e140ca881f6ab2f50f",
    }:
        raise AgentStaffingError("candidate must bind the protected authority cutover")
    rows = rollout.get("repositories")
    if not isinstance(rows, list):
        raise AgentStaffingError("rollout rows must be a list")
    names = [row.get("repository") for row in rows if isinstance(row, dict)]
    if len(names) != len(set(names)) or set(names) != EXPECTED_REPOSITORIES:
        raise AgentStaffingError("rollout matrix must cover each active repository exactly once")
    effective = {row.get("repository") for row in rows if row.get("status") == "effective"}
    if effective != EXPECTED_REPOSITORIES:
        raise AgentStaffingError("all active repositories must have effective adoption")
    for row in rows:
        commit = row.get("adoption_commit")
        if not isinstance(commit, str) or len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
            raise AgentStaffingError("effective adoption requires an exact commit")
    obligations = rollout.get("unresolved_obligations")
    if obligations != []:
        raise AgentStaffingError("completed rollout cannot retain obligations")


def validate_documentary_coverage() -> None:
    coverage = _load(DOCUMENTARY_COVERAGE)
    jsonschema.validate(
        coverage,
        _load(DOCUMENTARY_COVERAGE_SCHEMA),
        format_checker=jsonschema.FormatChecker(),
    )
    rows = coverage["repositories"]
    names = [row["repository"] for row in rows]
    if len(names) != len(set(names)) or set(names) != EXPECTED_REPOSITORIES:
        raise AgentStaffingError("documentary coverage must include every repository exactly once")
    if any(row["operative_conflicting_language_count"] != 0 for row in rows):
        raise AgentStaffingError("operative documentary conflicts remain")
    if any(row["status"] != "covered" for row in rows):
        raise AgentStaffingError("every repository must have covered documentary status")
    if coverage["unresolved_obligations"] != []:
        raise AgentStaffingError("documentary coverage cannot be complete with obligations")


def validate() -> None:
    validate_schemas()
    validate_standard()
    validate_rollout()
    validate_documentary_coverage()


if __name__ == "__main__":
    validate()
    print("agent staffing candidate validation passed")
