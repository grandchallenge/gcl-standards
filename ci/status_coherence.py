from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


class StatusCoherenceError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise StatusCoherenceError(f"record must be an object: {path}")
    return value


def projection_schema(*, root: Path = ROOT) -> dict[str, Any]:
    schema_dir = root / "schemas"
    schema = copy.deepcopy(load_json(schema_dir / "current_status_projection.schema.json"))
    schema["properties"]["lineage"] = load_json(
        schema_dir / "standard_successor_lineage.schema.json"
    )
    schema["properties"]["selected_admission"] = load_json(
        schema_dir / "current_admission_selection.schema.json"
    )
    schema["properties"]["selected_programme_adoption"] = load_json(
        schema_dir / "current_programme_adoption_selection.schema.json"
    )
    return schema


def validate_projection(projection: dict[str, Any], *, root: Path = ROOT) -> None:
    constitutional = projection.get("constitutional", {})
    assertions = projection.get("descriptive_assertions", {})
    admission = projection.get("selected_admission", {})
    adoption = projection.get("selected_programme_adoption", {})
    lineage = projection.get("lineage", {})

    if constitutional.get("amendment_status") == "effective" and (
        assertions.get("intellect_readme_amendment_status") == "proposed"
        or assertions.get("intellect_status_page_amendment_status") == "proposed"
    ):
        raise StatusCoherenceError(
            "effective amendment cannot have a proposed current status projection"
        )
    if admission.get("status") == "admitted" and (
        admission.get("front_matter_status") == "candidate"
        or assertions.get("standard_front_matter_status") == "candidate"
    ):
        raise StatusCoherenceError(
            "admitted selected standard cannot have candidate current front matter"
        )
    if adoption.get("status") == "active" and (
        admission.get("next_gate", {}).get("status") == "not_started"
        or assertions.get("admission_adoption_gate_status") == "not_started"
    ):
        raise StatusCoherenceError(
            "active programme adoption cannot have a not_started admission gate"
        )
    if admission.get("version") == lineage.get("predecessor_version"):
        raise StatusCoherenceError(
            "historical admission cannot be selected as current without successor lineage"
        )

    schema = projection_schema(root=root)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        projection,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    if adoption["admission_commit_sha"] != admission["commit_sha"]:
        raise StatusCoherenceError("programme adoption does not bind selected admission")
    if any(value is not False for value in projection["claim_boundaries"].values()):
        raise StatusCoherenceError("current-status projection widens prohibited authority")


def validate_schemas(*, root: Path = ROOT) -> None:
    for name in (
        "standard_successor_lineage.schema.json",
        "current_admission_selection.schema.json",
        "current_programme_adoption_selection.schema.json",
        "current_status_projection.schema.json",
        "coherence_receipt.schema.json",
    ):
        jsonschema.Draft202012Validator.check_schema(load_json(root / "schemas" / name))


if __name__ == "__main__":
    validate_schemas()
    print("status coherence schemas validated")
