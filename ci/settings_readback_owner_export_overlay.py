from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "evidence" / "settings-readback" / "GCL-GHOS-OWNER-EXPORT-001.reference.json"
OVERLAY = ROOT / "deviations" / "GCL-GHOS-SETTINGS-READBACK-001.owner-export-overlay.json"
BASE = ROOT / "deviations" / "GCL-GHOS-SETTINGS-READBACK-001.json"
REFERENCE_SCHEMA = ROOT / "schemas" / "settings_readback_owner_export_reference.schema.json"
OVERLAY_SCHEMA = ROOT / "schemas" / "settings_readback_deviation_overlay.schema.json"

EXPECTED_REPOSITORIES = {
    "grandchallenge/.github",
    "grandchallenge/INTELLECT",
    "grandchallenge/gcl-standards",
    "grandchallenge/MATH-PROGRAMME",
    "grandchallenge/MATHFORGE",
    "grandchallenge/MATHSOLVE",
    "grandchallenge/MATHCERT",
    "grandchallenge/MODULUS",
    "grandchallenge/GLOSS",
    "grandchallenge/QUANTUM-TECHNOLOGIES",
    "grandchallenge/lean-action",
    "grandchallenge/upload-pages-artifact",
}
EXPECTED_OPEN = {
    "MODULUS-P1-001": ("P1", "grandchallenge/MODULUS", "https://github.com/grandchallenge/MODULUS/issues/6"),
    "MODULUS-P2-001": ("P2", "grandchallenge/MODULUS", "https://github.com/grandchallenge/MODULUS/issues/6"),
    "QUANTUM-P1-001": ("P1", "grandchallenge/QUANTUM-TECHNOLOGIES", "https://github.com/grandchallenge/QUANTUM-TECHNOLOGIES/issues/14"),
    "QUANTUM-P2-001": ("P2", "grandchallenge/QUANTUM-TECHNOLOGIES", "https://github.com/grandchallenge/QUANTUM-TECHNOLOGIES/issues/14"),
}
FALSE_BOUNDARIES = {
    "organization_wide_conformance",
    "mathematical_claim_authorized",
    "certification_claim_authorized",
    "novelty_claim_authorized",
    "deployment_claim_authorized",
    "commercial_claim_authorized",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"record must be an object: {path}")
    return value


def validate_records(reference: dict, overlay: dict, base: dict) -> None:
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

    source = reference["source"]
    exact_source = {
        "exact_head": "bbbfa03561c52ae839118e2a035c0d78c85ce20c",
        "merge_commit": "45792900aa0198ea30ff2315a897d3c71f119f9a",
        "git_blob_sha1": "c15d10b3ad5287d625642850ed5d0986e9afaefc",
        "sha256": "b60f42d46e6044358d70d0f673f08afbc4e295afba95cd2fe3e9a65d8ab57d7c",
        "recorded_at": "2026-08-03T13:15:59Z",
    }
    for field, expected in exact_source.items():
        if source.get(field) != expected:
            raise ValueError(f"owner-export source identity drift: {field}")

    repositories = reference["coverage"]["repositories"]
    if set(repositories) != EXPECTED_REPOSITORIES or len(repositories) != len(EXPECTED_REPOSITORIES):
        raise ValueError("owner-export repository coverage drift")

    if overlay["replacement_evidence"] != str(REFERENCE.relative_to(ROOT)).replace("\\", "/"):
        raise ValueError("overlay replacement-evidence path drift")
    base_ref = overlay["base_campaign_record"]
    if base_ref["admission_merge"] != "3d5e35a8635cb8864a816cf0e589a5831dc2c706":
        raise ValueError("base campaign admission identity drift")
    if base.get("campaign_id") != overlay["campaign_id"]:
        raise ValueError("base and overlay campaign identity mismatch")

    base_rows = {
        row.get("id"): row
        for row in base.get("rows", [])
        if isinstance(row, dict)
    }
    blocked = base_rows.get("ORG-READBACK-BLOCKED-001")
    if not blocked or blocked.get("disposition") != "readback_blocked":
        raise ValueError("base blocked-readback row is not preserved")

    closed = overlay["closed_rows"]
    if len(closed) != 1 or closed[0]["id"] != "ORG-READBACK-BLOCKED-001":
        raise ValueError("overlay must close exactly the blocked-readback row")
    if closed[0]["disposition"] != "closed_evidence_admitted":
        raise ValueError("blocked-readback closure disposition drift")

    open_rows = overlay["open_rows"]
    row_map = {row["id"]: row for row in open_rows}
    if set(row_map) != set(EXPECTED_OPEN) or len(row_map) != len(open_rows):
        raise ValueError("open deviation identity coverage drift")
    for row_id, (priority, scope, issue) in EXPECTED_OPEN.items():
        row = row_map[row_id]
        if (row["priority"], row["scope"], row["remediation_issue"]) != (
            priority,
            scope,
            issue,
        ):
            raise ValueError(f"open deviation binding drift: {row_id}")

    counts = Counter(row["priority"] for row in open_rows)
    expected_counts = {"P0": 0, "P1": 2, "P2": 2, "P3": 0}
    actual_counts = {priority: counts.get(priority, 0) for priority in expected_counts}
    if actual_counts != expected_counts or overlay["open_priority_counts"] != expected_counts:
        raise ValueError("open-priority counts drift")

    if overlay["organization_wide_conformance"] is not False:
        raise ValueError("organization-wide conformance remains blocked")
    for record in (reference, overlay):
        boundaries = record["claim_boundaries"]
        for field in FALSE_BOUNDARIES:
            if boundaries.get(field) is not False:
                raise ValueError(f"claim-boundary inflation: {field}")


def validate() -> None:
    validate_records(load(REFERENCE), load(OVERLAY), load(BASE))


if __name__ == "__main__":
    validate()
    print("settings-readback owner-export overlay validation passed")
