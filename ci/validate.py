from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
PROFILE_SCHEMA_PATH = ROOT / "schemas" / "repository_profile.schema.json"
REGRET_SCHEMA_PATH = ROOT / "schemas" / "regret_contract.schema.json"
REGRET_TEMPLATE_PATH = ROOT / "templates" / "regret_contract.yaml"
REGRET_ADOPTION_PATH = ROOT / "programme-adoption" / "REGRET-CONTRACT-1.0.0.yaml"
EXPECTED_PROFILES = {
    ".github.json",
    "GLOSS.json",
    "INTELLECT.json",
    "MATH-PROGRAMME.json",
    "MATHCERT.json",
    "MATHFORGE.json",
    "MATHSOLVE.json",
    "gcl-standards.json",
    "lean-action.json",
    "upload-pages-artifact.json",
}
EXPECTED_REGRET_SOURCE_LOCK = {
    "repository": "fyremael/MODULUS",
    "pull_request": 1,
    "head_sha": "641ba766fe8eec613a01cd4726841b1d4e93ad78",
    "artifacts": {
        "standard": {
            "path": "docs/standards/REGRET_CONTRACT_STANDARD.md",
            "git_blob_sha1": "8e8b998cb84051b728c4a8c623e754fc20b0a6e6",
        },
        "schema": {
            "path": "schemas/regret_contract.schema.json",
            "git_blob_sha1": "7bf9ba77df36d1646f123c174b0116c1552bb4cd",
        },
        "template": {
            "path": "templates/regret_contract.yaml",
            "git_blob_sha1": "6d0f041248d520715061bf1af8b1d97e27da0a43",
        },
        "rollout": {
            "path": "docs/standards/ONLINE_CONTROL_ROLLOUT.md",
            "git_blob_sha1": "f42e90a9feba0661fbf313417a798954917a85e9",
        },
    },
}
EXPECTED_REGRET_PROGRAMMES = {
    "MODULUS",
    "KIBO/KOOP",
    "AETHER",
    "SPINDLE/SPLICE",
    "Tricorder",
    "adaptive-beta",
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_math_programme_adoption(adoption: object) -> None:
    if not isinstance(adoption, dict):
        raise ValueError("MATH-PROGRAMME adoption record must be an object")
    if adoption.get("status") not in {"proposed", "active", "superseded"}:
        raise ValueError("invalid adoption status")
    if adoption.get("decision_status") not in {"proposed", "accepted", "superseded"}:
        raise ValueError("invalid ADR decision status")
    if adoption.get("decision_ref") != (
        "decisions/ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"
    ):
        raise ValueError("MATH-PROGRAMME adoption must bind ADR-0001")
    if adoption["status"] == "active":
        constitutional = adoption["constitutional_source"]
        if adoption["decision_status"] != "accepted":
            raise ValueError("active adoption requires accepted ADR-0001")
        if (
            constitutional["amendment_status"] != "effective"
            or not constitutional["amendment_commit"]
            or not constitutional["review_receipt"]
            or not adoption["standards_commit"]
            or not adoption["activation_date"]
        ):
            raise ValueError(
                "active adoption requires an effective amendment, review receipt, "
                "accepted decision, exact commits, and activation date"
            )
    if adoption["status"] == "proposed" and adoption["decision_status"] == "accepted":
        raise ValueError("accepted ADR requires a separate standards-admission state")


def validate_regret_contract() -> None:
    schema = load_json(REGRET_SCHEMA_PATH)
    jsonschema.Draft202012Validator.check_schema(schema)
    if not isinstance(schema, dict):
        raise ValueError("regret contract schema must be an object")
    if schema.get("$id") != "https://grandchallenge.ai/schemas/regret-contract-1.0.0.json":
        raise ValueError("regret contract schema identity drift")

    template = load_yaml(REGRET_TEMPLATE_PATH)
    if not isinstance(template, dict):
        raise ValueError("regret contract template must be an object")
    jsonschema.validate(
        template,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )
    loss = template["loss"]
    if loss["lower_bound"] > loss["upper_bound"]:
        raise ValueError("regret contract loss bounds are inverted")

    adoption = load_yaml(REGRET_ADOPTION_PATH)
    if not isinstance(adoption, dict):
        raise ValueError("regret contract adoption ledger must be an object")
    if adoption.get("standard_id") != "GCL-RC-00":
        raise ValueError("regret contract standard identity drift")
    if adoption.get("standard_version") != "1.0.0":
        raise ValueError("regret contract version drift")
    if adoption.get("status") != "candidate_migrated":
        raise ValueError("regret contract may not claim activation before admission")
    if adoption.get("standards_commit") is not None:
        raise ValueError("candidate migration cannot pre-pin its future merge commit")
    if adoption.get("decision_ref") != "decisions/ADR-0002_REGRET_CONTRACT_STANDARD.md":
        raise ValueError("regret contract decision reference drift")
    if adoption.get("source_lock") != EXPECTED_REGRET_SOURCE_LOCK:
        raise ValueError("regret contract source lock drift")

    reference = adoption.get("reference_implementation", {})
    if reference != {
        "repository": "fyremael/MODULUS",
        "pull_request": 1,
        "commit_sha": "641ba766fe8eec613a01cd4726841b1d4e93ad78",
        "package": "modulus.online",
        "status": "candidate_unmerged",
    }:
        raise ValueError("regret contract reference implementation drift")

    programme_rows = adoption.get("programmes", [])
    if not isinstance(programme_rows, list):
        raise ValueError("regret contract programme adoption rows must be a list")
    programme_map = {
        row.get("programme"): row
        for row in programme_rows
        if isinstance(row, dict) and isinstance(row.get("programme"), str)
    }
    if set(programme_map) != EXPECTED_REGRET_PROGRAMMES:
        raise ValueError("regret contract programme adoption coverage drift")
    if len(programme_map) != len(programme_rows):
        raise ValueError("duplicate or malformed regret contract programme row")
    for programme, row in programme_map.items():
        if row.get("status") not in {"reference_implementation_candidate", "planned"}:
            raise ValueError(f"invalid regret contract adoption status: {programme}")
        obligations = row.get("unresolved_obligations")
        if not isinstance(obligations, list) or not obligations or not all(
            isinstance(item, str) and item.strip() for item in obligations
        ):
            raise ValueError(f"missing regret contract obligations: {programme}")

    boundaries = adoption.get("claim_boundaries", {})
    for field in (
        "standard_activation_complete",
        "any_programme_conformant",
        "convergence_claim_authorized",
        "safety_claim_authorized",
        "novelty_claim_authorized",
    ):
        if boundaries.get(field) is not False:
            raise ValueError(f"regret contract claim-boundary inflation: {field}")

    standard = (ROOT / "standards" / "GCL-RC-00.md").read_text(encoding="utf-8")
    for required in (
        "**Status:** Candidate migrated for Council admission",
        "641ba766fe8eec613a01cd4726841b1d4e93ad78",
        "Canonical custody in this repository does not by itself activate the standard.",
        "Programme adoption is explicit, versioned, and commit-addressed.",
        "Conformance does not prove global neural-network convergence",
    ):
        if required not in standard:
            raise ValueError(f"missing Regret Contract boundary: {required}")

    decision = (
        ROOT / "decisions" / "ADR-0002_REGRET_CONTRACT_STANDARD.md"
    ).read_text(encoding="utf-8")
    for required in (
        "**Status:** Proposed for exact-head Council review",
        "Registry custody and green CI do not activate the standard.",
        "protected MODULUS revision",
    ):
        if required not in decision:
            raise ValueError(f"missing Regret Contract decision boundary: {required}")


def validate() -> None:
    schema = load_json(PROFILE_SCHEMA_PATH)
    jsonschema.Draft202012Validator.check_schema(schema)

    profile_dir = ROOT / "fixtures" / "repository_profiles"
    profiles = sorted(profile_dir.glob("*.json"))
    names = {path.name for path in profiles}
    if names != EXPECTED_PROFILES:
        raise ValueError(
            f"repository profile discovery mismatch: expected={sorted(EXPECTED_PROFILES)} "
            f"actual={sorted(names)}"
        )

    repositories: set[str] = set()
    profiles_by_repository: dict[str, dict[str, object]] = {}
    for path in profiles:
        profile = load_json(path)
        if not isinstance(profile, dict):
            raise ValueError(f"repository profile must be an object: {path}")
        jsonschema.validate(profile, schema, format_checker=jsonschema.FormatChecker())
        repository = profile["repository"]
        if repository in repositories:
            raise ValueError(f"duplicate repository profile: {repository}")
        repositories.add(repository)
        profiles_by_repository[repository] = profile

    template = load_json(ROOT / "templates" / "repository_profile.json")
    jsonschema.validate(template, schema, format_checker=jsonschema.FormatChecker())

    intellect = profiles_by_repository["grandchallenge/INTELLECT"]
    if intellect["profile"] != "constitutional":
        raise ValueError("INTELLECT must use the constitutional profile")
    standards = profiles_by_repository["grandchallenge/gcl-standards"]
    if "Subordinate" not in standards["authority_scope"]:
        raise ValueError("gcl-standards must declare subordinate authority")

    adoption = load_yaml(ROOT / "programme-adoption" / "MATH-PROGRAMME.yaml")
    validate_math_programme_adoption(adoption)

    standard = (ROOT / "standards" / "GCL-GHOS-00.md").read_text(encoding="utf-8")
    required_boundaries = [
        "subordinate operating standard, not a constitution",
        "AETHER owns production append order",
        "Automation may request review",
        "It may not approve, merge, certify, or promote a claim.",
        "may not ratify a constitutional amendment",
        "one digest-addressed exact-revision",
        "every non-Steward office may be staffed",
        "additional-human approval counts",
        "Human Steward reserved authorization",
        "Candidate status does not create binding authority.",
        "MATH-PROGRAMME pilot adoption follows that standards admission",
    ]
    for boundary in required_boundaries:
        if boundary not in standard:
            raise ValueError(f"missing constitutional boundary: {boundary}")

    decision = (
        ROOT / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"
    ).read_text(encoding="utf-8")
    required_sequence = [
        "**Status:** Proposed for successor exact-packet review",
        "`GI-AMEND-0001` is ratified and effective at an exact INTELLECT commit",
        "the constitutional review receipt for the successor exact packet",
        "MATH-PROGRAMME pilot adoption follows ADR acceptance and GCL-GHOS admission",
        "It is not a prerequisite for this ADR to become accepted",
    ]
    for boundary in required_sequence:
        if boundary not in decision:
            raise ValueError(f"missing acyclic ADR boundary: {boundary}")
    forbidden_sequence = [
        "the mathematics pilot records its adoption commit",
        "This ADR becomes accepted only after:\n\n1. `GI-AMEND-0001` is ratified and effective;\n2.",
    ]
    for stale in forbidden_sequence:
        if stale in decision:
            raise ValueError(f"circular ADR sequence remains: {stale}")

    validate_regret_contract()


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print("gcl-standards validation passed")
