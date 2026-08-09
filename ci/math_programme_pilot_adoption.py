from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
CI_DIR = Path(__file__).resolve().parent
if str(CI_DIR) not in sys.path:
    sys.path.insert(0, str(CI_DIR))

from git_content import git_blob_sha1_at_commit  # noqa: E402


ADOPTION_PATH = ROOT / "programme-adoption" / "MATH-PROGRAMME.yaml"
SCHEMA_PATH = ROOT / "schemas" / "math_programme_pilot_adoption.schema.json"
ADMISSION_PATH = ROOT / "admissions" / "GCL-GHOS-00-0.1.1.json"

EXPECTED_ACTIVATION_COMMIT = "8d47ed8930d33253ae476c64dfec7c748185a535"
EXPECTED_DOCUMENTARY_CLOSURE_COMMIT = "d9c659f70490c328b9b4c068224136c02edc534c"
EXPECTED_RECEIPT_ADMISSION_COMMIT = "ad4eac22321f87c42d34884eca5405ffea250f75"
EXPECTED_STANDARDS_ADMISSION_COMMIT = "5c4e73e55d362a5198b9076ead694909a5e0ebf3"
EXPECTED_REVIEWED_SOURCE_COMMIT = "3a5ed516bb9ccb43e2d67e9270e1ec2a793e01ac"
EXPECTED_CONSTITUTIONAL_PACKET = (
    "22dbfa0ea0e652161126dd4647477036b89e6c13ecbd9101cda60ce00e9f95c5"
)
EXPECTED_SUCCESSOR_PACKET = (
    "b39b2f3fab12089622ccba5072c89dd758128117b5426075658148b2b495e917"
)
EXPECTED_DECISION_BLOB = "e4d61cfcc5e8ed330b350ab34323bb36a29fcd4c"
EXPECTED_STANDARD_BLOB = "fd2651ba5036cf2455bf925dcd85364894d55726"


class PilotAdoptionError(ValueError):
    pass


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise PilotAdoptionError(f"record must be an object: {path}")
    return value


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise PilotAdoptionError(f"record must be an object: {path}")
    return value


def validate_records(
    adoption: dict[str, object],
    admission: dict[str, object],
    schema: dict[str, object],
) -> None:
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(adoption, schema, cls=jsonschema.Draft202012Validator)

    constitutional = adoption["constitutional_source"]
    receipt = constitutional["review_receipt"]
    standard_admission = adoption["standard_admission"]
    claims = adoption["claim_boundaries"]

    if constitutional["amendment_commit"] != EXPECTED_ACTIVATION_COMMIT:
        raise PilotAdoptionError("constitutional activation commit drift")
    if receipt["commit_sha"] != constitutional["amendment_commit"]:
        raise PilotAdoptionError("receipt integration commit must match activation commit")
    if constitutional["documentary_closure_commit"] != EXPECTED_DOCUMENTARY_CLOSURE_COMMIT:
        raise PilotAdoptionError("documentary closure commit drift")
    if receipt["admission_commit"] != EXPECTED_RECEIPT_ADMISSION_COMMIT:
        raise PilotAdoptionError("receipt admission commit drift")
    if receipt["packet_sha256"] != EXPECTED_CONSTITUTIONAL_PACKET:
        raise PilotAdoptionError("constitutional packet drift")
    if not receipt["path"].endswith(
        f"-{EXPECTED_CONSTITUTIONAL_PACKET[:12]}.json"
    ):
        raise PilotAdoptionError("receipt path does not match packet prefix")

    if adoption["standards_commit"] != EXPECTED_STANDARDS_ADMISSION_COMMIT:
        raise PilotAdoptionError("standards admission merge drift")
    if standard_admission["commit_sha"] != adoption["standards_commit"]:
        raise PilotAdoptionError("standard admission commit mismatch")
    if standard_admission["reviewed_source_commit"] != EXPECTED_REVIEWED_SOURCE_COMMIT:
        raise PilotAdoptionError("reviewed standards source drift")
    if standard_admission["decision_git_blob_sha1"] != EXPECTED_DECISION_BLOB:
        raise PilotAdoptionError("ADR blob identity drift")
    if standard_admission["standard_git_blob_sha1"] != EXPECTED_STANDARD_BLOB:
        raise PilotAdoptionError("standard blob identity drift")
    if standard_admission["packet_sha256"] != EXPECTED_SUCCESSOR_PACKET:
        raise PilotAdoptionError("successor review packet drift")

    if admission["operation_id"] != standard_admission["operation_id"]:
        raise PilotAdoptionError("standard admission operation mismatch")
    if admission["status"] != "admitted":
        raise PilotAdoptionError("standard admission is not admitted")
    if admission["review_packet"]["packet_sha256"] != EXPECTED_SUCCESSOR_PACKET:
        raise PilotAdoptionError("admission packet identity drift")
    if (
        admission["reviewed_source"]["reviewed_commit"]
        != EXPECTED_REVIEWED_SOURCE_COMMIT
    ):
        raise PilotAdoptionError("admitted ADR source drift")
    admitted_artifacts = {
        row["path"]: row["git_blob_sha1"]
        for row in admission["reviewed_source"]["artifacts"]
    }
    decision_path = "decisions/ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"
    standard_path = "standards/GCL-GHOS-00.md"
    if admitted_artifacts[decision_path] != EXPECTED_DECISION_BLOB:
        raise PilotAdoptionError("admitted ADR blob drift")
    if admitted_artifacts[standard_path] != EXPECTED_STANDARD_BLOB:
        raise PilotAdoptionError("admitted standard blob drift")

    if (
        git_blob_sha1_at_commit(
            root=ROOT,
            commit=admission["reviewed_source"]["reviewed_commit"],
            relative_path=decision_path,
        )
        != EXPECTED_DECISION_BLOB
    ):
        raise PilotAdoptionError("admitted ADR Git identity drift")
    if (
        git_blob_sha1_at_commit(
            root=ROOT,
            commit=admission["reviewed_source"]["reviewed_commit"],
            relative_path=standard_path,
        )
        != EXPECTED_STANDARD_BLOB
    ):
        raise PilotAdoptionError("admitted standard Git identity drift")

    if adoption["admission_gate_status"] != "complete":
        raise PilotAdoptionError("selected admission adoption gate is not complete")
    if admission["next_gate"]["status"] != "not_started":
        raise PilotAdoptionError("immutable admission gate was rewritten")
    if adoption["predecessor_adoption"] != {
        "standard_version": "0.1.0",
        "standards_commit": "31211b286a9c4a2874da5559118ef2f026f7de52",
        "admission_path": "admissions/GCL-GHOS-00-0.1.0.json",
        "admission_operation_id": "GI-AMEND-0001-STANDARDS-ADMISSION-001",
        "status": "active",
        "activation_date": "2026-08-03",
    }:
        raise PilotAdoptionError("0.1.0 adoption lineage drift")

    false_boundaries = {
        key: value
        for key, value in claims.items()
        if key != "programme_pilot_adoption_complete"
    }
    if claims["programme_pilot_adoption_complete"] is not True:
        raise PilotAdoptionError("programme pilot adoption is not complete")
    if any(value is not False for value in false_boundaries.values()):
        raise PilotAdoptionError("pilot adoption inflates a prohibited claim boundary")
    if not adoption["unresolved_deviations"]:
        raise PilotAdoptionError("pilot adoption must retain unresolved deviations")


def validate() -> None:
    validate_records(
        load_yaml(ADOPTION_PATH),
        load_json(ADMISSION_PATH),
        load_json(SCHEMA_PATH),
    )


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"MATH-PROGRAMME pilot adoption validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print("MATH-PROGRAMME GCL-GHOS pilot adoption validation passed")
