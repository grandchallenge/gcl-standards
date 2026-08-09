from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

import jsonschema
import yaml


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


def git_blob_sha1(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def _text(contents: Mapping[str, bytes], key: str) -> str:
    try:
        return contents[key].decode("utf-8")
    except (KeyError, UnicodeDecodeError) as exc:
        raise StatusCoherenceError(f"missing or invalid evidence content: {key}") from exc


def validate_descriptive_evidence(
    projection: dict[str, Any], evidence_contents: Mapping[str, bytes] | None
) -> None:
    if evidence_contents is None:
        raise StatusCoherenceError("exact descriptive evidence content is required")
    evidence = projection["descriptive_evidence"]
    if set(evidence_contents) != set(evidence):
        raise StatusCoherenceError("descriptive evidence content set does not match projection")
    for key, source in evidence.items():
        if git_blob_sha1(evidence_contents[key]) != source["git_blob_sha1"]:
            raise StatusCoherenceError(f"descriptive evidence Git blob drift: {key}")

    amendment = _text(evidence_contents, "amendment")
    admission = json.loads(_text(evidence_contents, "admission"))
    adoption = yaml.safe_load(_text(evidence_contents, "programme_adoption"))
    if not isinstance(admission, dict) or not isinstance(adoption, dict):
        raise StatusCoherenceError("admission and adoption evidence must be objects")

    derived = {
        "intellect_readme_amendment_status": (
            "effective" if "`GI-AMEND-0001` is effective" in _text(evidence_contents, "intellect_readme") else "proposed"
        ),
        "intellect_status_page_amendment_status": (
            "effective" if "`GI-AMEND-0001` is effective" in _text(evidence_contents, "intellect_status_page") else "proposed"
        ),
        "amendment_gcl_status_scope": (
            "candidate_at_activation"
            if "**GCL-GHOS status at activation:** Candidate; not yet admitted" in amendment
            else "current_candidate"
        ),
        "gcl_readme_standard_status": (
            "admitted" if "is the admitted GitHub Constitutional" in _text(evidence_contents, "gcl_readme") else "candidate"
        ),
        "adr_status": (
            "accepted" if "**Status:** Accepted" in _text(evidence_contents, "adr") else "proposed"
        ),
        "standard_front_matter_status": (
            "admitted" if "**Status:** Admitted documentary successor" in _text(evidence_contents, "standard") else "candidate"
        ),
        "admission_adoption_gate_status": admission.get("next_gate", {}).get("status"),
        "programme_adoption_status": adoption.get("status"),
    }
    if derived != projection["descriptive_assertions"]:
        raise StatusCoherenceError("descriptive assertions do not match exact source blobs")


def validate_projection(
    projection: dict[str, Any],
    *,
    root: Path = ROOT,
    evidence_contents: Mapping[str, bytes] | None = None,
) -> None:
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
    validate_descriptive_evidence(projection, evidence_contents)
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
