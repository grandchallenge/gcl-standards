from __future__ import annotations

import hashlib
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "standard_admission.schema.json"
ADMISSION_PATH = ROOT / "admissions" / "GCL-GHOS-00-0.1.0.json"
EXPECTED_REVIEWED_COMMIT = "fa90ffc2bd23a6b0c8e184c7da2dd6ef1174a4ee"
EXPECTED_ACTIVATION_COMMIT = "8d47ed8930d33253ae476c64dfec7c748185a535"
EXPECTED_DOCUMENTARY_CLOSURE_COMMIT = (
    "d9c659f70490c328b9b4c068224136c02edc534c"
)
EXPECTED_RECEIPT_ADMISSION_COMMIT = (
    "ad4eac22321f87c42d34884eca5405ffea250f75"
)
EXPECTED_PACKET = "22dbfa0ea0e652161126dd4647477036b89e6c13ecbd9101cda60ce00e9f95c5"
EXPECTED_RECEIPT_PATH = "governance/reviews/GI-AMEND-0001-22dbfa0ea0e6.json"


class StandardAdmissionError(ValueError):
    pass


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise StandardAdmissionError(f"record must be an object: {path}")
    return value


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def validate_standard_admission(
    admission: dict[str, object] | None = None,
    *,
    root: Path = ROOT,
) -> dict[str, object]:
    schema = load_json(root / "schemas" / "standard_admission.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    record = admission or load_json(
        root / "admissions" / "GCL-GHOS-00-0.1.0.json"
    )
    jsonschema.validate(
        record,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    authority = record["constitutional_authority"]
    if authority["activation_commit"] != EXPECTED_ACTIVATION_COMMIT:
        raise StandardAdmissionError("constitutional activation commit drift")
    if (
        authority["documentary_closure_commit"]
        != EXPECTED_DOCUMENTARY_CLOSURE_COMMIT
    ):
        raise StandardAdmissionError("constitutional documentary closure drift")
    receipt = authority["review_receipt"]
    if receipt["path"] != EXPECTED_RECEIPT_PATH:
        raise StandardAdmissionError("review receipt path drift")
    if receipt["packet_sha256"] != EXPECTED_PACKET:
        raise StandardAdmissionError("review packet digest drift")
    if receipt["admission_commit"] != EXPECTED_RECEIPT_ADMISSION_COMMIT:
        raise StandardAdmissionError("review receipt admission commit drift")
    if not receipt["path"].endswith(f"-{receipt['packet_sha256'][:12]}.json"):
        raise StandardAdmissionError("review receipt filename is not content-addressed")

    decision = record["decision"]
    standard = record["standard"]
    if decision["reviewed_commit"] != EXPECTED_REVIEWED_COMMIT:
        raise StandardAdmissionError("ADR reviewed commit drift")
    if standard["reviewed_commit"] != EXPECTED_REVIEWED_COMMIT:
        raise StandardAdmissionError("standard reviewed commit drift")

    decision_path = root / decision["path"]
    standard_path = root / standard["path"]
    if git_blob_sha1(decision_path) != decision["git_blob_sha1"]:
        raise StandardAdmissionError("ADR source blob drift")
    if git_blob_sha1(standard_path) != standard["git_blob_sha1"]:
        raise StandardAdmissionError("standard source blob drift")

    decision_text = decision_path.read_text(encoding="utf-8")
    standard_text = standard_path.read_text(encoding="utf-8")
    if "**Status:** Proposed for successor exact-packet review" not in decision_text:
        raise StandardAdmissionError("reviewed ADR source status drift")
    if "**Status:** Candidate" not in standard_text:
        raise StandardAdmissionError("reviewed standard source status drift")
    if "Candidate status does not create binding authority." not in standard_text:
        raise StandardAdmissionError("standard candidate boundary missing")

    staffing = record["review_staffing"]
    adversary = staffing["adversary"]
    referee = staffing["referee"]
    if adversary["reviewer_id"] == referee["reviewer_id"]:
        raise StandardAdmissionError("Adversary and Referee identities must differ")
    if adversary["session_id"] == referee["session_id"]:
        raise StandardAdmissionError("Adversary and Referee sessions must differ")

    boundaries = record["claim_boundaries"]
    if any(value is not False for value in boundaries.values()):
        raise StandardAdmissionError("standards admission claim-boundary inflation")
    if record["next_gate"] != {
        "operation": "MATH-PROGRAMME pilot adoption",
        "status": "not_started",
        "programme": "grandchallenge/MATH-PROGRAMME",
    }:
        raise StandardAdmissionError("next-gate identity drift")

    return record
