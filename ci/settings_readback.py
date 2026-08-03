from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
NORMALIZED = ROOT / "evidence" / "settings-readback" / "GCL-GHOS-SETTINGS-READBACK-001.normalized.json"
LEDGER = ROOT / "deviations" / "GCL-GHOS-SETTINGS-READBACK-001.json"
SCHEMA = ROOT / "schemas" / "settings_readback.schema.json"
EXPECTED_REPOSITORIES = {
    "grandchallenge/.github", "grandchallenge/INTELLECT", "grandchallenge/gcl-standards",
    "grandchallenge/MATH-PROGRAMME", "grandchallenge/MATHFORGE", "grandchallenge/MATHSOLVE",
    "grandchallenge/MATHCERT", "grandchallenge/MODULUS", "grandchallenge/GLOSS",
    "grandchallenge/QUANTUM-TECHNOLOGIES", "grandchallenge/lean-action",
    "grandchallenge/upload-pages-artifact",
}
ORGANIZATION_BLOCKED_STATUS_FIELDS = {
    "actions_permissions_status",
    "actions_workflow_permissions_status",
    "rulesets_status",
}


class SettingsReadbackError(ValueError):
    pass


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SettingsReadbackError(f"{path} must contain an object")
    return value


def validate_settings_readback(normalized=None, ledger=None) -> tuple[dict[str, object], dict[str, object]]:
    normalized = load(NORMALIZED) if normalized is None else normalized
    ledger = load(LEDGER) if ledger is None else ledger
    schema = load(SCHEMA)
    checker = jsonschema.FormatChecker()
    jsonschema.validate(normalized, schema, cls=jsonschema.Draft202012Validator, format_checker=checker)
    jsonschema.validate(ledger, schema, cls=jsonschema.Draft202012Validator, format_checker=checker)

    repos = [row["repository"] for row in normalized["repositories"]]
    if set(repos) != EXPECTED_REPOSITORIES or len(repos) != len(set(repos)):
        raise SettingsReadbackError("repository inventory drift or duplication")

    ids = [row["id"] for row in ledger["rows"]]
    if len(ids) != len(set(ids)):
        raise SettingsReadbackError("duplicate deviation row id")

    organization_readback = normalized["organization_readback"]
    organization_blocked = any(
        organization_readback[field] != 200
        for field in ORGANIZATION_BLOCKED_STATUS_FIELDS
    )
    organization_rows = [
        row for row in ledger["rows"]
        if row["id"] == "ORG-READBACK-BLOCKED-001"
    ]
    if organization_blocked:
        if len(organization_rows) != 1:
            raise SettingsReadbackError("blocked organization readback requires one exact deviation row")
        organization_row = organization_rows[0]
        if organization_row["disposition"] != "readback_blocked":
            raise SettingsReadbackError("blocked organization readback cannot be relabelled conformant")
        if organization_row["remediation_issue"] != organization_readback["blocked_evidence_issue"]:
            raise SettingsReadbackError("blocked organization readback remediation issue drift")

    open_p0_p1 = [
        row for row in ledger["rows"]
        if row["priority"] in {"P0", "P1"}
        and row["disposition"] != "conformant"
    ]
    if ledger["organization_wide_conformance"] and open_p0_p1:
        raise SettingsReadbackError("organization-wide conformance cannot coexist with open P0/P1 rows")

    blocked = [row for row in ledger["rows"] if row["disposition"] == "readback_blocked"]
    if blocked and normalized["claim_boundaries"]["organization_wide_conformance"]:
        raise SettingsReadbackError("blocked readback cannot support conformance")

    by_scope = {row["scope"] for row in ledger["rows"]}
    for scope in ("grandchallenge/MODULUS", "grandchallenge/QUANTUM-TECHNOLOGIES"):
        if scope not in by_scope:
            raise SettingsReadbackError(f"missing required deviation scope {scope}")

    for row in ledger["rows"]:
        if row["disposition"] in {"repair_required", "readback_blocked"} and not row["remediation_issue"]:
            raise SettingsReadbackError("open deviation lacks remediation issue")

    return normalized, ledger


if __name__ == "__main__":
    validate_settings_readback()
    print("settings readback validation passed")
