from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "evidence" / "settings-readback" / "GCL-GHOS-MODULUS-POST-REPAIR-READBACK-001.reference.json"
OVERLAY = ROOT / "deviations" / "GCL-GHOS-SETTINGS-READBACK-001.modulus-closure-overlay.json"
PRIOR_OVERLAY = ROOT / "deviations" / "GCL-GHOS-SETTINGS-READBACK-001.owner-export-overlay.json"
BASE = ROOT / "deviations" / "GCL-GHOS-SETTINGS-READBACK-001.json"
REFERENCE_SCHEMA = ROOT / "schemas" / "settings_readback_modulus_reference.schema.json"
OVERLAY_SCHEMA = ROOT / "schemas" / "settings_readback_modulus_closure_overlay.schema.json"

EXPECTED_SOURCE = {
    "repository": "grandchallenge/MODULUS",
    "pull_request": 17,
    "exact_head": "a9350368e3dfd7272f7c21d2ddbb37fd9d458b5b",
    "merge_commit": "2a6fb6f190e52d23a9c65b710d82f9d4527bbe71",
    "path": "governance/settings-readback/evidence/GCL-GHOS-MODULUS-POST-REPAIR-READBACK-001.json",
    "digest_path": "governance/settings-readback/evidence/GCL-GHOS-MODULUS-POST-REPAIR-READBACK-001.json.sha256",
    "attestation_path": "governance/settings-readback/evidence/GCL-GHOS-MODULUS-POST-REPAIR-READBACK-001.attestation.md",
    "git_blob_sha1": "b6fb29688329511b5b006ebcdd00e2addf99e296",
    "attestation_git_blob_sha1": "70eaa895b786e61a5681ee720bb97dda21b01c29",
    "sha256": "be189dda6d5ee0b0b9a2d0c9af64f6910215bc24e3e524c9344ef06cbafd9143",
    "size_bytes": 272012,
    "schema_version": "1.1.0",
    "recorded_at": "2026-08-04T00:13:03Z",
    "actor": {"login": "fyremael", "id": 17925951, "repository_admin": True},
    "protected_main": "d23c285e7f9245c1504a64d108373dccedaf05e6",
    "owner_controls_evidence_baseline": "f54dd2c0b26ea46ef6b598f6a65dfcef2c47da47",
}
EXPECTED_CONTEXTS = {
    "test-and-lint (3.10)", "test-and-lint (3.11)", "test-and-lint (3.12)",
    "benchmark-report", "policy / policy", "security / action-policy",
}
EXPECTED_SURFACES = {
    ".github/CODEOWNERS", ".github/dependabot.yml", ".github/workflows/ci.yml",
    ".github/workflows/gcl-conformance.yml", "AGENTS.md", "SUPPORT.md",
}
EXPECTED_CLOSED = {
    "ORG-READBACK-BLOCKED-001": ("P1", "grandchallenge", "closed_evidence_admitted", "https://github.com/grandchallenge/.github/issues/38"),
    "MODULUS-P1-001": ("P1", "grandchallenge/MODULUS", "closed_repair_verified", "https://github.com/grandchallenge/MODULUS/issues/6"),
    "MODULUS-P2-001": ("P2", "grandchallenge/MODULUS", "closed_repair_verified", "https://github.com/grandchallenge/MODULUS/issues/6"),
}
EXPECTED_OPEN = {
    "QUANTUM-P1-001": ("P1", "grandchallenge/QUANTUM-TECHNOLOGIES", "https://github.com/grandchallenge/QUANTUM-TECHNOLOGIES/issues/14"),
    "QUANTUM-P2-001": ("P2", "grandchallenge/QUANTUM-TECHNOLOGIES", "https://github.com/grandchallenge/QUANTUM-TECHNOLOGIES/issues/14"),
}
FALSE_BOUNDARIES = {
    "organization_wide_conformance", "mathematical_claim_authorized",
    "certification_claim_authorized", "novelty_claim_authorized",
    "deployment_claim_authorized", "commercial_claim_authorized",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"record must be an object: {path}")
    return value


def validate_records(reference: dict, overlay: dict, prior_overlay: dict, base: dict) -> None:
    reference_schema = load(REFERENCE_SCHEMA)
    overlay_schema = load(OVERLAY_SCHEMA)
    jsonschema.Draft202012Validator.check_schema(reference_schema)
    jsonschema.Draft202012Validator.check_schema(overlay_schema)
    jsonschema.validate(reference, reference_schema, cls=jsonschema.Draft202012Validator, format_checker=jsonschema.FormatChecker())
    jsonschema.validate(overlay, overlay_schema, cls=jsonschema.Draft202012Validator, format_checker=jsonschema.FormatChecker())

    if reference["source"] != EXPECTED_SOURCE:
        raise ValueError("MODULUS readback source identity drift")
    verified = reference["verified_state"]
    if set(verified["required_contexts"]) != EXPECTED_CONTEXTS:
        raise ValueError("required-context coverage drift")
    if set(verified["governed_surfaces"]) != EXPECTED_SURFACES:
        raise ValueError("governed-surface coverage drift")
    if verified["validation_findings"] != []:
        raise ValueError("admitted MODULUS readback contains findings")
    for field in (
        "repository_merge_settings_conformant", "ruleset_list_detail_complete",
        "vulnerability_alerts_enabled", "dependabot_security_updates_enabled",
        "private_vulnerability_reporting_enabled", "codeql_default_setup_configured",
    ):
        if verified.get(field) is not True:
            raise ValueError(f"verified MODULUS state drift: {field}")
    if verified["protected_main_ruleset_id"] != 20266757 or verified["immutable_release_tag_ruleset_id"] != 20334249:
        raise ValueError("MODULUS ruleset identity drift")

    if base.get("campaign_id") != overlay["campaign_id"]:
        raise ValueError("base campaign identity mismatch")
    if prior_overlay.get("operation_id") != "GCL-GHOS-SETTINGS-READBACK-OWNER-OVERLAY-001":
        raise ValueError("prior overlay identity drift")
    if prior_overlay.get("open_priority_counts") != {"P0": 0, "P1": 2, "P2": 2, "P3": 0}:
        raise ValueError("prior overlay priority state drift")
    if overlay["prior_overlay"] != {
        "repository": "grandchallenge/gcl-standards",
        "path": "deviations/GCL-GHOS-SETTINGS-READBACK-001.owner-export-overlay.json",
        "merge_commit": "692ff6a1b8ec4113c8917470cb0e4c094ff7d334",
        "git_blob_sha1": "fe0e377a287883c10ce82042a73404acae6a9b2c",
    }:
        raise ValueError("prior overlay binding drift")
    if overlay["replacement_evidence"] != str(REFERENCE.relative_to(ROOT)).replace("\\", "/"):
        raise ValueError("replacement-evidence path drift")

    closed_rows = overlay["closed_rows"]
    closed = {row["id"]: row for row in closed_rows}
    if set(closed) != set(EXPECTED_CLOSED) or len(closed) != len(closed_rows):
        raise ValueError("closed deviation identity coverage drift")
    for row_id, expected in EXPECTED_CLOSED.items():
        row = closed[row_id]
        actual = (row["priority"], row["scope"], row["disposition"], row["remediation_issue"])
        if actual != expected:
            raise ValueError(f"closed deviation binding drift: {row_id}")

    open_rows = overlay["open_rows"]
    open_map = {row["id"]: row for row in open_rows}
    if set(open_map) != set(EXPECTED_OPEN) or len(open_map) != len(open_rows):
        raise ValueError("open deviation identity coverage drift")
    for row_id, expected in EXPECTED_OPEN.items():
        row = open_map[row_id]
        actual = (row["priority"], row["scope"], row["remediation_issue"])
        if actual != expected or row["disposition"] != "repair_required":
            raise ValueError(f"open deviation binding drift: {row_id}")

    counts = Counter(row["priority"] for row in open_rows)
    expected_counts = {"P0": 0, "P1": 1, "P2": 1, "P3": 0}
    actual_counts = {priority: counts.get(priority, 0) for priority in expected_counts}
    if actual_counts != expected_counts or overlay["open_priority_counts"] != expected_counts:
        raise ValueError("open-priority counts drift")
    if overlay["organization_wide_conformance"] is not False:
        raise ValueError("organization-wide conformance remains blocked")
    for record in (reference, overlay):
        for field in FALSE_BOUNDARIES:
            if record["claim_boundaries"].get(field) is not False:
                raise ValueError(f"claim-boundary inflation: {field}")


def validate() -> None:
    validate_records(load(REFERENCE), load(OVERLAY), load(PRIOR_OVERLAY), load(BASE))


if __name__ == "__main__":
    validate()
    print("MODULUS settings-readback closure overlay validation passed")
