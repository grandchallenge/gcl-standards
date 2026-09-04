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
    for path in (REVIEW_SCHEMA, ADOPTION_SCHEMA):
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
        "activation is conditional on protected selection of `GI-STEWARD-0003`",
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
    if rollout.get("status") != "candidate_pending_superior_authority":
        raise AgentStaffingError("candidate may not claim effective status")
    authority = rollout.get("superior_authority", {})
    if authority.get("directive") != "GI-STEWARD-0003" or authority.get("effective_commit") is not None:
        raise AgentStaffingError("candidate must remain fail-closed before authority cutover")
    rows = rollout.get("repositories")
    if not isinstance(rows, list):
        raise AgentStaffingError("rollout rows must be a list")
    names = [row.get("repository") for row in rows if isinstance(row, dict)]
    if len(names) != len(set(names)) or set(names) != EXPECTED_REPOSITORIES:
        raise AgentStaffingError("rollout matrix must cover each active repository exactly once")
    if any(row.get("status") == "effective" for row in rows):
        raise AgentStaffingError("downstream adoption cannot precede authority and admission")
    obligations = rollout.get("unresolved_obligations")
    if not isinstance(obligations, list) or not obligations:
        raise AgentStaffingError("candidate rollout must expose unresolved gates")


def validate() -> None:
    validate_schemas()
    validate_standard()
    validate_rollout()


if __name__ == "__main__":
    validate()
    print("agent staffing candidate validation passed")
