from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "GCL-CC-00.md"
STATUS = ROOT / "status" / "GCL-CC-00-current.json"
ADMISSION = ROOT / "admissions" / "GCL-CC-00-0.1.0.json"
SCHEMA = ROOT / "schemas" / "gcl_cc_admission.schema.json"

REQUIRED_STANDARD = (
    "Operational or presentational drift SHALL be a blocking defect.",
    "A subsequent substantive operation SHALL NOT begin while such drift remains unresolved.",
    "LEASED -> LAUNCHED -> RETURNED -> CAPTURED -> ADJUDICATING",
    "Campaign state SHALL explicitly record when a candidate is `NOT_SUBMITTED`.",
    "A remediation SHALL either:",
    "A new remediation SHALL NOT be layered over an unresolved remediation",
    "Documentation that merely states CORE CLARITY principles is not conformance.",
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> None:
    text = STANDARD.read_text(encoding="utf-8")
    for fragment in REQUIRED_STANDARD:
        if fragment not in text:
            raise ValueError(f"missing GCL-CC-00 normative boundary: {fragment}")

    schema = load(SCHEMA)
    admission = load(ADMISSION)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        admission,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    status = load(STATUS)
    if status.get("identifier") != "GCL-CC-00" or status.get("version") != "0.1.0":
        raise ValueError("GCL-CC-00 status identity drift")
    if status.get("status") != "admitted":
        raise ValueError("GCL-CC-00 status must be admitted")
    if status.get("admission", {}).get("record") != "admissions/GCL-CC-00-0.1.0.json":
        raise ValueError("GCL-CC-00 status admission pointer drift")
    if status.get("programme_adoption", {}).get("status") != "not_yet_adopted":
        raise ValueError("GCL-CC-00 programme adoption cannot precede downstream protected adoption")
    if any(status.get("claim_boundaries", {}).values()):
        raise ValueError("GCL-CC-00 status widens prohibited authority")


if __name__ == "__main__":
    validate()
    print("GCL-CC-00 admission and status validated")
