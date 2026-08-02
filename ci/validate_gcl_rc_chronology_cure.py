from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "gcl_rc_chronology_cure.schema.json"
RECORD_PATH = ROOT / "implementation" / "GCL-RC-CHRONOLOGY-CURE-001.json"
DOCUMENT_PATH = ROOT / "implementation" / "GCL-RC-CHRONOLOGY-CURE-001.md"

EXPECTED_COMMENTS = {
    5160929262: ("jimsteeg", "2026-08-02T23:47:40Z"),
    5160945680: ("fyremael", "2026-08-02T23:52:26Z"),
}


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def validate_record(record: dict[str, object]) -> None:
    schema = load_json(SCHEMA_PATH)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(record, schema, cls=jsonschema.Draft202012Validator)

    subject = record["subject"]
    assert isinstance(subject, dict)
    if subject["pre_merge_steward_authorization_present"] is not False:
        raise ValueError("chronology cure may not invent pre-merge Steward authorization")

    comments = record["post_merge_comments"]
    assert isinstance(comments, list)
    observed: dict[int, tuple[str, str]] = {}
    for comment in comments:
        assert isinstance(comment, dict)
        observed[int(comment["comment_id"])] = (
            str(comment["author"]),
            str(comment["created_at"]),
        )
    if observed != EXPECTED_COMMENTS:
        raise ValueError("post-merge comment identity drift")

    ratification = record["retrospective_ratification"]
    assert isinstance(ratification, dict)
    state = record["state"]
    if state == "ratification_pending":
        if any(ratification[key] is not None for key in ("comment_id", "author", "recorded_at")):
            raise ValueError("pending cure may not bind partial ratification")
    else:
        if ratification["author"] != "fyremael":
            raise ValueError("completed retrospective ratification must be Human Steward-authored")
        if not isinstance(ratification["comment_id"], int):
            raise ValueError("completed retrospective ratification requires comment ID")
        if ratification["comment_id"] in EXPECTED_COMMENTS:
            raise ValueError("prospective post-merge comment cannot serve as retrospective cure")
        if not isinstance(ratification["recorded_at"], str):
            raise ValueError("completed retrospective ratification requires timestamp")

    boundaries = record["preserved_boundaries"]
    assert isinstance(boundaries, dict)
    if boundaries != {
        "standard_status": "candidate",
        "any_programme_conformant": False,
        "mathematical_claim_authorized": False,
        "deployment_claim_authorized": False,
        "revert_required": False,
    }:
        raise ValueError("chronology cure boundary drift")

    document = DOCUMENT_PATH.read_text(encoding="utf-8")
    for required in (
        "but no Human Steward disposition was recorded before merge",
        "Neither may be represented as pre-merge authorization",
        "No content revert is required",
        "`GCL-RC-00` remains a candidate",
    ):
        if required not in document:
            raise ValueError(f"missing chronology-cure boundary: {required}")


def validate() -> None:
    validate_record(load_json(RECORD_PATH))


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"chronology cure validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print("chronology cure validation passed")
