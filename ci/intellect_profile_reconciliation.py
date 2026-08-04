from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "fixtures" / "repository_profiles" / "INTELLECT.json"
PROFILE_SCHEMA = ROOT / "schemas" / "repository_profile.schema.json"
RECONCILIATION = (
    ROOT
    / "deviations"
    / "GCL-GHOS-INTELLECT-PROFILE-RECONCILIATION-001.json"
)
RECONCILIATION_SCHEMA = (
    ROOT / "schemas" / "intellect_profile_reconciliation.schema.json"
)
BASE_CAMPAIGN = ROOT / "deviations" / "GCL-GHOS-SETTINGS-READBACK-001.json"
OWNER_OVERLAY = (
    ROOT
    / "deviations"
    / "GCL-GHOS-SETTINGS-READBACK-001.owner-export-overlay.json"
)
OWNER_REFERENCE = (
    ROOT
    / "evidence"
    / "settings-readback"
    / "GCL-GHOS-OWNER-EXPORT-001.reference.json"
)

EXPECTED_CUSTOM_PROPERTIES = {
    "constitutional_profile": "Constitutional",
    "authority_scope": "constitutional",
    "claim_promotion_role": "none",
    "risk_tier": "critical",
    "workflow_profile": "governance",
    "public_programme": "true",
}
EXPECTED_CARRIED_ROWS = {
    "MODULUS-P1-001": "P1",
    "MODULUS-P2-001": "P2",
    "QUANTUM-P1-001": "P1",
    "QUANTUM-P2-001": "P2",
}
FALSE_BOUNDARIES = {
    "mathematical_claim_authorized",
    "certification_claim_authorized",
    "novelty_claim_authorized",
    "deployment_claim_authorized",
    "manufacturing_claim_authorized",
    "commercial_claim_authorized",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"record must be an object: {path}")
    return value


def validate_records(
    profile: dict,
    reconciliation: dict,
    base_campaign: dict,
    owner_overlay: dict,
    owner_reference: dict,
) -> None:
    profile_schema = load(PROFILE_SCHEMA)
    reconciliation_schema = load(RECONCILIATION_SCHEMA)
    jsonschema.Draft202012Validator.check_schema(profile_schema)
    jsonschema.Draft202012Validator.check_schema(reconciliation_schema)
    jsonschema.validate(
        profile,
        profile_schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )
    jsonschema.validate(
        reconciliation,
        reconciliation_schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    if profile.get("repository") != "grandchallenge/INTELLECT":
        raise ValueError("INTELLECT repository identity drift")
    if profile.get("profile") != "constitutional":
        raise ValueError("INTELLECT profile must remain constitutional")
    if profile.get("claim_promotion_role") != "policy_only":
        raise ValueError("canonical INTELLECT claim role drift")
    if profile.get("risk_tier") != "critical":
        raise ValueError("INTELLECT risk tier drift")

    constitutional = profile.get("constitutional_source", {})
    expected_constitutional = {
        "repository": "grandchallenge/INTELLECT",
        "path": "CONSTITUTION.md",
        "effective_version": "1.1.0",
        "amendment": "GI-AMEND-0001",
        "amendment_status": "effective",
        "activation_commit": "8d47ed8930d33253ae476c64dfec7c748185a535",
    }
    if constitutional != expected_constitutional:
        raise ValueError("INTELLECT constitutional authority identity drift")

    operating = profile.get("operating_policy_source", {})
    expected_operating = {
        "repository": "grandchallenge/gcl-standards",
        "path": "standards/GCL-GHOS-00.md",
        "version": "0.1.0",
        "status": "admitted",
        "decision": "ADR-0001",
        "decision_status": "accepted",
        "admission_commit": "31211b286a9c4a2874da5559118ef2f026f7de52",
    }
    if operating != expected_operating:
        raise ValueError("INTELLECT operating-policy identity drift")

    projection = profile.get("github_projection")
    if not isinstance(projection, dict):
        raise ValueError("INTELLECT requires an explicit GitHub projection")
    if projection.get("custom_properties") != EXPECTED_CUSTOM_PROPERTIES:
        raise ValueError("INTELLECT GitHub custom-property projection drift")
    if projection.get("default_branch_ruleset") != "Constitutional profile - main":
        raise ValueError("INTELLECT GitHub ruleset projection drift")
    semantics = projection.get("projection_semantics", {})
    if (
        semantics.get("canonical_claim_promotion_role") != "policy_only"
        or semantics.get("live_claim_promotion_role") != "none"
    ):
        raise ValueError("INTELLECT claim-role projection is ambiguous")
    rationale = semantics.get("rationale")
    if not isinstance(rationale, str) or len(rationale.strip()) < 80:
        raise ValueError("INTELLECT claim-role projection rationale is incomplete")

    if reconciliation["canonical_profile"]["path"] != str(
        PROFILE.relative_to(ROOT)
    ).replace("\\", "/"):
        raise ValueError("canonical profile path drift")
    if (
        reconciliation["canonical_profile"]["canonical_claim_promotion_role"]
        != profile["claim_promotion_role"]
    ):
        raise ValueError("canonical claim role is not cross-bound")
    if reconciliation["intended_live_projection"] != {
        "custom_properties": projection["custom_properties"],
        "default_branch_ruleset": projection["default_branch_ruleset"],
    }:
        raise ValueError("live projection is not cross-bound to the canonical profile")

    base_rows = {
        row.get("id"): row
        for row in base_campaign.get("rows", [])
        if isinstance(row, dict)
    }
    prior = base_rows.get("OBS-INTELLECT-001")
    if not prior:
        raise ValueError("base INTELLECT observation is missing")
    if (
        prior.get("scope") != "grandchallenge/INTELLECT"
        or prior.get("disposition") != "conformant"
    ):
        raise ValueError("base INTELLECT observation identity drift")
    superseded = reconciliation["superseded_observation"]
    if (
        superseded["id"] != "OBS-INTELLECT-001"
        or superseded["prior_disposition"] != prior["disposition"]
    ):
        raise ValueError("false-conformance supersession is not cross-bound")

    owner_open = {
        row.get("id"): row
        for row in owner_overlay.get("open_rows", [])
        if isinstance(row, dict)
    }
    if set(owner_open) != set(EXPECTED_CARRIED_ROWS):
        raise ValueError("owner-overlay open-row coverage drift")
    for row_id, priority in EXPECTED_CARRIED_ROWS.items():
        if owner_open[row_id].get("priority") != priority:
            raise ValueError(f"owner-overlay priority drift: {row_id}")
    carried = reconciliation["carried_open_rows"]
    if set(carried) != set(EXPECTED_CARRIED_ROWS) or len(carried) != len(
        EXPECTED_CARRIED_ROWS
    ):
        raise ValueError("carried open-row identity drift")

    source = owner_reference.get("source", {})
    reference = reconciliation["base_records"]["owner_export_reference"]
    source_bindings = {
        "source_merge_commit": source.get("merge_commit"),
        "source_git_blob_sha1": source.get("git_blob_sha1"),
        "source_sha256": source.get("sha256"),
        "recorded_at": source.get("recorded_at"),
    }
    for field, actual in source_bindings.items():
        if reference.get(field) != actual:
            raise ValueError(f"owner-export evidence binding drift: {field}")
    if reference.get("path") != str(OWNER_REFERENCE.relative_to(ROOT)).replace(
        "\\", "/"
    ):
        raise ValueError("owner-export reference path drift")

    repair = reconciliation["repair_row"]
    if (
        repair["id"] != "INTELLECT-P0-001"
        or repair["priority"] != "P0"
        or repair["scope"] != "grandchallenge/INTELLECT"
        or repair["disposition"] != "repair_required"
        or repair["remediation_issue"]
        != "https://github.com/grandchallenge/gcl-standards/issues/12"
    ):
        raise ValueError("INTELLECT repair disposition drift")

    counts = Counter(EXPECTED_CARRIED_ROWS.values())
    counts["P0"] += 1
    expected_counts = {
        "P0": counts.get("P0", 0),
        "P1": counts.get("P1", 0),
        "P2": counts.get("P2", 0),
        "P3": counts.get("P3", 0),
    }
    if reconciliation["open_priority_counts"] != expected_counts:
        raise ValueError("reconciliation priority counts drift")

    phase = reconciliation["phase_boundaries"]
    if phase != {
        "phase_a_live_mutation_authorized": False,
        "phase_b_requires_phase_a_protected_merge": True,
        "profile_conformance_authorized": False,
        "organization_wide_conformance": False,
    }:
        raise ValueError("phase or conformance boundary drift")

    boundaries = reconciliation["claim_boundaries"]
    for field in FALSE_BOUNDARIES:
        if boundaries.get(field) is not False:
            raise ValueError(f"claim-boundary inflation: {field}")


def validate() -> None:
    validate_records(
        load(PROFILE),
        load(RECONCILIATION),
        load(BASE_CAMPAIGN),
        load(OWNER_OVERLAY),
        load(OWNER_REFERENCE),
    )


if __name__ == "__main__":
    validate()
    print("INTELLECT profile reconciliation validation passed")
