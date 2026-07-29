from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
PROFILE_SCHEMA_PATH = ROOT / "schemas" / "repository_profile.schema.json"
EXPECTED_PROFILES = {
    ".github.json",
    "GLOSS.json",
    "INTELLECT.json",
    "MATH-PROGRAMME.json",
    "MATHCERT.json",
    "MATHFORGE.json",
    "MATHSOLVE.json",
    "gcl-standards.json",
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


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

    adoption = yaml.safe_load(
        (ROOT / "programme-adoption" / "MATH-PROGRAMME.yaml").read_text(encoding="utf-8")
    )
    if adoption["status"] not in {"proposed", "active", "superseded"}:
        raise ValueError("invalid adoption status")
    if adoption["status"] == "active":
        constitutional = adoption["constitutional_source"]
        if (
            constitutional["amendment_status"] != "effective"
            or not constitutional["amendment_commit"]
            or not adoption["standards_commit"]
            or not adoption["decision_ref"]
        ):
            raise ValueError(
                "active adoption requires an effective amendment, exact commits, "
                "and a decision"
            )

    standard = (ROOT / "standards" / "GCL-GHOS-00.md").read_text(encoding="utf-8")
    required_boundaries = [
        "subordinate operating standard, not a constitution",
        "AETHER owns production append order",
        "Automation may request review",
        "It may not approve, merge, certify, or promote a claim.",
        "may not ratify a constitutional amendment",
        "Candidate status does not create binding authority.",
    ]
    for boundary in required_boundaries:
        if boundary not in standard:
            raise ValueError(f"missing constitutional boundary: {boundary}")


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print("gcl-standards validation passed")
