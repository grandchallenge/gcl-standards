from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = (
    ROOT
    / "evidence"
    / "settings-readback"
    / "GCL-GHOS-QUANTUM-POST-REPAIR-READBACK-001.reference.json"
)
OVERLAY = (
    ROOT
    / "deviations"
    / "GCL-GHOS-SETTINGS-READBACK-001.quantum-closure-overlay.json"
)
PRIOR_OVERLAY = (
    ROOT
    / "deviations"
    / "GCL-GHOS-SETTINGS-READBACK-001.modulus-closure-overlay.json"
)
BASE = ROOT / "deviations" / "GCL-GHOS-SETTINGS-READBACK-001.json"
PROFILE = ROOT / "fixtures" / "repository_profiles" / "QUANTUM-TECHNOLOGIES.json"
REFERENCE_SCHEMA = (
    ROOT / "schemas" / "settings_readback_quantum_reference.schema.json"
)
OVERLAY_SCHEMA = (
    ROOT / "schemas" / "settings_readback_quantum_closure_overlay.schema.json"
)

EXPECTED_SOURCE = {
    "repository": "grandchallenge/QUANTUM-TECHNOLOGIES",
    "pull_request": 26,
    "exact_head": "b659f44e8223d172e07ede7ef6fc9ca36b15f9c1",
    "merge_commit": "008745514436b95abd30abaa9dcad3597522dc1f",
    "path": (
        "governance/settings-readback/evidence/"
        "GCL-GHOS-QUANTUM-POST-REPAIR-READBACK-001.receipt.json"
    ),
    "digest_path": (
        "governance/settings-readback/evidence/"
        "GCL-GHOS-QUANTUM-POST-REPAIR-READBACK-001.receipt.json.sha256"
    ),
    "attestation_path": (
        "governance/settings-readback/evidence/"
        "GCL-GHOS-QUANTUM-POST-REPAIR-READBACK-001.attestation.md"
    ),
    "source_bundle_path": (
        "governance/settings-readback/evidence/source/"
        "GCL-GHOS-QUANTUM-POST-REPAIR-READBACK-001.source-bundle.json"
    ),
    "git_blob_sha1": "c80b813a0c7978554b0538a6aa109854a44dee9e",
    "digest_git_blob_sha1": "d62888783ca3348ab6a77daea8f3f3b867ac889f",
    "attestation_git_blob_sha1": "208a975c6486a7570f27a01ce236342799a22b61",
    "source_bundle_git_blob_sha1": "d8f5a1def415218850e156d057039353772db54a",
    "sha256": "83109c5c7f7461480bc5f0119c96295716a194a71dce3fdebe3552d8602efe37",
    "source_bundle_sha256": (
        "3d17fbc44356c614a0b96c9f0aa3973fc4653f7fa85ebd8bc576cf4f7cf48080"
    ),
    "size_bytes": 9029,
    "schema_version": "1.0.0",
    "recorded_at": "2026-08-04T07:20:26.7913380Z",
    "actor": {"login": "fyremael", "id": 17925951, "repository_admin": True},
    "protected_main": "a8f2441cd75e717ff30f05d32c0f5e90a7dd7394",
    "owner_controls_evidence_baseline": (
        "a8f2441cd75e717ff30f05d32c0f5e90a7dd7394"
    ),
}
EXPECTED_PROFILE_BINDING = {
    "repository": "grandchallenge/gcl-standards",
    "path": "fixtures/repository_profiles/QUANTUM-TECHNOLOGIES.json",
    "git_blob_sha1": "c7467171e9cc28271fee20d5c85691c5b2015267",
    "exact_head": "ad4493a386ec1f0cab2b9fbc2da98953f39b23db",
    "merge_commit": "5ec22de5d18e02ba91b47f74f23c7acde6bc3ddc",
}
EXPECTED_PROFILE = {
    "repository": "grandchallenge/QUANTUM-TECHNOLOGIES",
    "profile": "programme",
    "claim_promotion_role": "work_package_only",
    "risk_tier": "high",
    "required_workflow_profile": "programme-research",
    "release_policy": "immutable_admitted",
}
EXPECTED_CONTEXTS = {"policy", "security / action-policy", "validate"}
EXPECTED_WORKFLOWS = {
    ".github/workflows/gcl-conformance.yml",
    ".github/workflows/qtr-validation.yml",
}
EXPECTED_SURFACES = {".github/CODEOWNERS", ".github/dependabot.yml", "SECURITY.md"}
EXPECTED_SETTINGS = {
    "allow_auto_merge": True,
    "allow_merge_commit": True,
    "allow_rebase_merge": False,
    "allow_squash_merge": True,
    "allow_update_branch": False,
    "delete_branch_on_merge": True,
}
EXPECTED_CLOSED = {
    "ORG-READBACK-BLOCKED-001": (
        "P1",
        "grandchallenge",
        "closed_evidence_admitted",
        "https://github.com/grandchallenge/.github/issues/38",
    ),
    "MODULUS-P1-001": (
        "P1",
        "grandchallenge/MODULUS",
        "closed_repair_verified",
        "https://github.com/grandchallenge/MODULUS/issues/6",
    ),
    "MODULUS-P2-001": (
        "P2",
        "grandchallenge/MODULUS",
        "closed_repair_verified",
        "https://github.com/grandchallenge/MODULUS/issues/6",
    ),
    "QUANTUM-P1-001": (
        "P1",
        "grandchallenge/QUANTUM-TECHNOLOGIES",
        "closed_repair_verified",
        "https://github.com/grandchallenge/QUANTUM-TECHNOLOGIES/issues/14",
    ),
    "QUANTUM-P2-001": (
        "P2",
        "grandchallenge/QUANTUM-TECHNOLOGIES",
        "closed_repair_verified",
        "https://github.com/grandchallenge/QUANTUM-TECHNOLOGIES/issues/14",
    ),
}
FALSE_BOUNDARIES = {
    "organization_wide_conformance",
    "mathematical_claim_authorized",
    "certification_claim_authorized",
    "novelty_claim_authorized",
    "priority_claim_authorized",
    "quantum_advantage_claim_authorized",
    "hardware_validation_claim_authorized",
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


def validate_records(
    reference: dict,
    overlay: dict,
    prior_overlay: dict,
    base: dict,
    profile: dict,
) -> None:
    reference_schema = load(REFERENCE_SCHEMA)
    overlay_schema = load(OVERLAY_SCHEMA)
    jsonschema.Draft202012Validator.check_schema(reference_schema)
    jsonschema.Draft202012Validator.check_schema(overlay_schema)
    jsonschema.validate(
        reference,
        reference_schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )
    jsonschema.validate(
        overlay,
        overlay_schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    if reference["source"] != EXPECTED_SOURCE:
        raise ValueError("QUANTUM readback source identity drift")
    if reference["standards_profile"] != EXPECTED_PROFILE_BINDING:
        raise ValueError("QUANTUM standards-profile binding drift")
    for field, expected in EXPECTED_PROFILE.items():
        if profile.get(field) != expected:
            raise ValueError(f"QUANTUM profile drift: {field}")

    verified = reference["verified_state"]
    if set(verified["required_contexts"]) != EXPECTED_CONTEXTS:
        raise ValueError("required-context coverage drift")
    if set(verified["required_workflows"]) != EXPECTED_WORKFLOWS:
        raise ValueError("required-workflow coverage drift")
    if set(verified["governed_surfaces"]) != EXPECTED_SURFACES:
        raise ValueError("governed-surface coverage drift")
    if verified["repository_merge_settings"] != EXPECTED_SETTINGS:
        raise ValueError("repository merge-setting drift")
    if verified["validation_findings"] != [] or verified["readback_gaps"] != []:
        raise ValueError("admitted QUANTUM readback is not gap-free")
    for field in (
        "repository_merge_settings_conformant",
        "ruleset_list_detail_complete",
        "vulnerability_alerts_enabled",
        "dependabot_security_updates_enabled",
        "private_vulnerability_reporting_enabled",
        "codeql_default_setup_configured",
        "dismiss_stale_reviews_on_push",
        "required_review_thread_resolution",
        "strict_required_status_checks_policy",
    ):
        if verified.get(field) is not True:
            raise ValueError(f"verified QUANTUM state drift: {field}")
    if verified["dependabot_security_updates_paused"] is not False:
        raise ValueError("Dependabot security updates are paused")
    if verified["protected_main_ruleset_id"] != 20106953:
        raise ValueError("protected-main ruleset identity drift")
    if verified["immutable_release_tag_ruleset_id"] != 20355165:
        raise ValueError("immutable-tag ruleset identity drift")
    if verified["allowed_merge_methods"] != ["merge", "squash"]:
        raise ValueError("allowed merge-method drift")
    if verified["codeql_languages"] != ["actions", "python"]:
        raise ValueError("CodeQL language coverage drift")
    if (
        verified["codeql_query_suite"] != "extended"
        or verified["codeql_threat_model"] != "remote"
        or verified["codeql_runner_type"] != "standard"
    ):
        raise ValueError("CodeQL configuration drift")

    if base.get("campaign_id") != overlay["campaign_id"]:
        raise ValueError("base campaign identity mismatch")
    if (
        prior_overlay.get("operation_id")
        != "GCL-GHOS-SETTINGS-READBACK-MODULUS-CLOSURE-OVERLAY-001"
    ):
        raise ValueError("prior overlay identity drift")
    if prior_overlay.get("open_priority_counts") != {
        "P0": 0,
        "P1": 1,
        "P2": 1,
        "P3": 0,
    }:
        raise ValueError("prior overlay priority state drift")
    prior_open = {
        row.get("id"): row
        for row in prior_overlay.get("open_rows", [])
        if isinstance(row, dict)
    }
    if set(prior_open) != {"QUANTUM-P1-001", "QUANTUM-P2-001"}:
        raise ValueError("prior QUANTUM row coverage drift")
    if any(row.get("disposition") != "repair_required" for row in prior_open.values()):
        raise ValueError("prior QUANTUM disposition drift")

    if overlay["prior_overlay"] != {
        "repository": "grandchallenge/gcl-standards",
        "path": (
            "deviations/"
            "GCL-GHOS-SETTINGS-READBACK-001.modulus-closure-overlay.json"
        ),
        "merge_commit": "4884001459e1346aebd21e44c49a8ab2c695d09b",
        "git_blob_sha1": "7bb7d335e4c5f7da35f6db1335f6431aaef5d1f2",
    }:
        raise ValueError("prior overlay binding drift")
    expected_reference = str(REFERENCE.relative_to(ROOT)).replace("\\", "/")
    if overlay["replacement_evidence"] != expected_reference:
        raise ValueError("replacement-evidence path drift")

    closed_rows = overlay["closed_rows"]
    closed = {row["id"]: row for row in closed_rows}
    if set(closed) != set(EXPECTED_CLOSED) or len(closed) != len(closed_rows):
        raise ValueError("closed deviation identity coverage drift")
    for row_id, expected in EXPECTED_CLOSED.items():
        row = closed[row_id]
        actual = (
            row["priority"],
            row["scope"],
            row["disposition"],
            row["remediation_issue"],
        )
        if actual != expected:
            raise ValueError(f"closed deviation binding drift: {row_id}")

    if overlay["open_rows"] != []:
        raise ValueError("QUANTUM closure overlay must not retain open rows")
    expected_counts = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    counts = Counter(row["priority"] for row in overlay["open_rows"])
    actual_counts = {
        priority: counts.get(priority, 0) for priority in expected_counts
    }
    if actual_counts != expected_counts:
        raise ValueError("calculated open-priority counts drift")
    if overlay["open_priority_counts"] != expected_counts:
        raise ValueError("declared open-priority counts drift")
    if overlay["status"] != "closed":
        raise ValueError("campaign documentary status must be closed")
    if overlay["organization_wide_conformance"] is not False:
        raise ValueError("organization-wide conformance remains unauthorized")

    for record in (reference, overlay):
        if set(record["claim_boundaries"]) != FALSE_BOUNDARIES:
            raise ValueError("claim-boundary field coverage drift")
        for field in FALSE_BOUNDARIES:
            if record["claim_boundaries"].get(field) is not False:
                raise ValueError(f"claim-boundary inflation: {field}")


def validate() -> None:
    validate_records(
        load(REFERENCE),
        load(OVERLAY),
        load(PRIOR_OVERLAY),
        load(BASE),
        load(PROFILE),
    )


if __name__ == "__main__":
    validate()
    print("QUANTUM settings-readback closure overlay validation passed")
