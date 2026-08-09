from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
CI_DIR = Path(__file__).resolve().parent
if str(CI_DIR) not in sys.path:
    sys.path.insert(0, str(CI_DIR))

from git_content import canonical_git_bytes  # noqa: E402
PROFILE = ROOT / "fixtures/repository_profiles/INTELLECT.json"
PROFILE_SCHEMA = ROOT / "schemas/repository_profile.schema.json"
RECONCILIATION = ROOT / "deviations/GCL-GHOS-INTELLECT-PROFILE-RECONCILIATION-001.json"
RECONCILIATION_SCHEMA = ROOT / "schemas/intellect_profile_reconciliation.schema.json"
EVIDENCE = ROOT / "evidence/settings-readback/GCL-GHOS-INTELLECT-PROFILE-RECONCILIATION-001.json"
EVIDENCE_DIGEST = ROOT / "evidence/settings-readback/GCL-GHOS-INTELLECT-PROFILE-RECONCILIATION-001.json.sha256"
EVIDENCE_REFERENCE = ROOT / "evidence/settings-readback/GCL-GHOS-INTELLECT-PROFILE-RECONCILIATION-001.reference.json"
EVIDENCE_REFERENCE_SCHEMA = ROOT / "schemas/intellect_profile_phase_b_evidence_reference.schema.json"
BASE_CAMPAIGN = ROOT / "deviations/GCL-GHOS-SETTINGS-READBACK-001.json"
OWNER_OVERLAY = ROOT / "deviations/GCL-GHOS-SETTINGS-READBACK-001.owner-export-overlay.json"
OWNER_REFERENCE = ROOT / "evidence/settings-readback/GCL-GHOS-OWNER-EXPORT-001.reference.json"

EXPECTED_PROPERTIES = {
    "authority_scope": "constitutional",
    "claim_promotion_role": "none",
    "constitutional_profile": "Constitutional",
    "public_programme": "true",
    "risk_tier": "critical",
    "workflow_profile": "governance",
}
EXPECTED_BEFORE = {
    "authority_scope": "provider",
    "claim_promotion_role": "none",
    "constitutional_profile": "Provider",
    "public_programme": "true",
    "risk_tier": "high",
    "workflow_profile": "provider",
}
EXPECTED_CHECKS = [
    "test (3.11.14)",
    "test (3.12.13)",
    "policy / policy",
    "security / action-policy",
]
EXPECTED_OPEN_ROWS = {
    "MODULUS-P1-001",
    "MODULUS-P2-001",
    "QUANTUM-P1-001",
    "QUANTUM-P2-001",
}
FALSE_EVIDENCE_BOUNDARIES = {
    "profile_conformance_authorized",
    "organization_wide_conformance",
    "mathematical_claim_authorized",
    "certification_claim_authorized",
    "novelty_claim_authorized",
    "priority_claim_authorized",
    "deployment_claim_authorized",
    "manufacturing_claim_authorized",
    "product_claim_authorized",
    "commercial_claim_authorized",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"record must be an object: {path}")
    return value


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def rule(ruleset: dict, kind: str) -> dict:
    for row in ruleset.get("rules", []):
        if row.get("type") == kind:
            return row
    raise ValueError(f"INTELLECT ruleset lacks {kind}")


def validate_records(
    profile: dict,
    reconciliation: dict,
    base_campaign: dict,
    owner_overlay: dict,
    owner_reference: dict,
    evidence: dict,
    evidence_bytes: bytes,
    digest_text: str,
    reference: dict,
) -> None:
    schemas = [load(PROFILE_SCHEMA), load(RECONCILIATION_SCHEMA), load(EVIDENCE_REFERENCE_SCHEMA)]
    for schema in schemas:
        jsonschema.Draft202012Validator.check_schema(schema)
    for value, schema in ((profile, schemas[0]), (reconciliation, schemas[1]), (reference, schemas[2])):
        jsonschema.validate(value, schema, cls=jsonschema.Draft202012Validator,
                            format_checker=jsonschema.FormatChecker())

    if profile.get("repository") != "grandchallenge/INTELLECT" or profile.get("profile") != "constitutional":
        raise ValueError("INTELLECT profile identity drift")
    if profile.get("claim_promotion_role") != "policy_only" or profile.get("risk_tier") != "critical":
        raise ValueError("INTELLECT canonical authority drift")
    if profile.get("github_projection", {}).get("custom_properties") != EXPECTED_PROPERTIES:
        raise ValueError("INTELLECT canonical projection drift")
    if profile.get("github_projection", {}).get("default_branch_ruleset") != "Constitutional profile - main":
        raise ValueError("INTELLECT canonical ruleset drift")

    base_rows = {row.get("id"): row for row in base_campaign.get("rows", []) if isinstance(row, dict)}
    if base_rows.get("OBS-INTELLECT-001", {}).get("disposition") != "conformant":
        raise ValueError("base false-conformance identity drift")
    owner_rows = {row.get("id") for row in owner_overlay.get("open_rows", []) if isinstance(row, dict)}
    if owner_rows != EXPECTED_OPEN_ROWS:
        raise ValueError("carried owner-overlay row drift")
    source = owner_reference.get("source", {})
    owner_binding = reconciliation["base_records"]["owner_export_reference"]
    if owner_binding["source_sha256"] != source.get("sha256") or owner_binding["source_git_blob_sha1"] != source.get("git_blob_sha1"):
        raise ValueError("owner-export evidence binding drift")

    if evidence.get("operation_id") != "GCL-GHOS-INTELLECT-PROFILE-RECONCILIATION-001" or evidence.get("phase") != "B" or evidence.get("mode") != "apply" or evidence.get("verified") is not True:
        raise ValueError("Phase B execution identity drift")
    if evidence.get("repository") != "grandchallenge/INTELLECT" or evidence.get("organization") != "grandchallenge":
        raise ValueError("Phase B repository identity drift")
    actor = evidence.get("actor", {})
    names = [row.get("full_name") for row in actor.get("repositories", [])]
    if actor.get("authentication") != "github_app_installation" or actor.get("repository_count") != 2 or names != ["grandchallenge/INTELLECT", "grandchallenge/MATH-PROGRAMME"]:
        raise ValueError("Phase B installation scope drift")
    if evidence.get("main_sha_before") != evidence.get("main_sha_after") or evidence.get("main_sha_after") != "0096eb21ca62c5ef7f6e458f358edcb1cd963a20":
        raise ValueError("protected INTELLECT main drift")
    if evidence.get("property_values_before") != EXPECTED_BEFORE or evidence.get("property_values_after") != EXPECTED_PROPERTIES:
        raise ValueError("INTELLECT property readback drift")

    extensions = {"constitutional_profile": "Constitutional", "authority_scope": "constitutional"}
    for name, required in extensions.items():
        before = evidence["property_schemas_before"][name]
        after = evidence["property_schemas_after"][name]
        allowed = list(before["allowed_values"])
        if required not in allowed:
            allowed.append(required)
        if after["allowed_values"] != allowed:
            raise ValueError(f"property vocabulary drift: {name}")
        for field in ("property_name", "source_type", "value_type", "required", "description", "values_editable_by", "require_explicit_values"):
            if before.get(field) != after.get(field):
                raise ValueError(f"property non-vocabulary drift: {name}.{field}")

    before_ruleset = evidence.get("ruleset_before", {})
    after_ruleset = evidence.get("ruleset_after", {})
    if before_ruleset != after_ruleset:
        raise ValueError("ruleset changed during final execution")
    if after_ruleset.get("id") != 19964077 or after_ruleset.get("name") != "Constitutional profile - main" or after_ruleset.get("enforcement") != "active":
        raise ValueError("ruleset identity drift")
    if after_ruleset.get("conditions") != {"ref_name": {"exclude": [], "include": ["~DEFAULT_BRANCH"]}}:
        raise ValueError("ruleset branch condition drift")
    if after_ruleset.get("bypass_actors") != [] or after_ruleset.get("current_user_can_bypass") != "never":
        raise ValueError("ruleset bypass drift")
    status = rule(after_ruleset, "required_status_checks")["parameters"]
    if status.get("strict_required_status_checks_policy") is not True or [row.get("context") for row in status.get("required_status_checks", [])] != EXPECTED_CHECKS:
        raise ValueError("required status-check drift")
    pr = rule(after_ruleset, "pull_request")["parameters"]
    expected_pr = {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": True,
        "require_last_push_approval": False,
        "require_code_owner_review": False,
        "required_review_thread_resolution": True,
        "allowed_merge_methods": ["merge", "squash"],
    }
    for field, expected in expected_pr.items():
        if pr.get(field) != expected:
            raise ValueError(f"pull-request protection drift: {field}")
    types = {row.get("type") for row in after_ruleset.get("rules", [])}
    if not {"deletion", "non_fast_forward"}.issubset(types):
        raise ValueError("destructive-change protection drift")

    expected_mutations = [
        {"operation": "extend_property_schemas", "properties": [
            {"property_name": "constitutional_profile", "required_value": "Constitutional"},
            {"property_name": "authority_scope", "required_value": "constitutional"},
        ]},
        {"operation": "apply_repository_property_values", "repository": "grandchallenge/INTELLECT"},
        {"operation": "rename_ruleset", "ruleset_id": 19964077, "target_name": "Constitutional profile - main"},
    ]
    if evidence.get("mutations") != expected_mutations:
        raise ValueError("Phase B mutation-set drift")
    for field in FALSE_EVIDENCE_BOUNDARIES:
        if evidence.get("claim_boundaries", {}).get(field) is not False:
            raise ValueError(f"evidence claim inflation: {field}")

    semantic = evidence.get("evidence_sha256")
    payload = copy.deepcopy(evidence)
    payload.pop("evidence_sha256", None)
    if semantic != canonical_sha256(payload):
        raise ValueError("semantic evidence digest mismatch")
    if digest_text != f"{semantic}  intellect-profile-admin-evidence.json\n":
        raise ValueError("digest companion mismatch")
    final_sha = hashlib.sha256(evidence_bytes).hexdigest()
    retained = reference["retained_evidence"]
    if retained["json_sha256"] != final_sha or retained["json_size_bytes"] != len(evidence_bytes) or retained["semantic_sha256"] != semantic or retained["companion_value"] != semantic:
        raise ValueError("retained evidence binding drift")
    source_ref = reference["source"]
    if (source_ref["workflow_run"], source_ref["job_id"], source_ref["artifact_id"], source_ref["head_sha"], source_ref["artifact_zip_sha256"]) != (
        30882443280, 91906476034, 8881792628,
        "e5713330aa983501ec7a5c0c89caf0b827f9a6e6",
        "21116b3d91e962a6e2bf017ffb2ed9ebfd406b11a0f99f22fe146c865829d6f7",
    ):
        raise ValueError("source workflow binding drift")
    for field in FALSE_EVIDENCE_BOUNDARIES:
        if reference.get("claim_boundaries", {}).get(field) is not False:
            raise ValueError(f"reference claim inflation: {field}")
    phase = reconciliation["phase_b_evidence"]
    if phase["workflow_run"] != source_ref["workflow_run"] or phase["job_id"] != source_ref["job_id"] or phase["artifact_id"] != source_ref["artifact_id"] or phase["source_head"] != source_ref["head_sha"] or phase["semantic_sha256"] != semantic or phase["json_sha256"] != final_sha or phase["artifact_zip_sha256"] != source_ref["artifact_zip_sha256"]:
        raise ValueError("reconciliation evidence cross-binding drift")


def validate() -> None:
    validate_records(
        load(PROFILE), load(RECONCILIATION), load(BASE_CAMPAIGN),
        load(OWNER_OVERLAY), load(OWNER_REFERENCE), load(EVIDENCE),
        canonical_git_bytes(EVIDENCE, root=ROOT),
        EVIDENCE_DIGEST.read_text(encoding="utf-8"),
        load(EVIDENCE_REFERENCE),
    )


if __name__ == "__main__":
    validate()
    print("INTELLECT profile reconciliation and Phase B evidence validation passed")
