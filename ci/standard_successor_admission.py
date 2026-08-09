from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
CI_DIR = Path(__file__).resolve().parent
if str(CI_DIR) not in sys.path:
    sys.path.insert(0, str(CI_DIR))

from git_content import git_blob_sha1, git_blob_sha1_at_commit  # noqa: E402


REVIEWED_SOURCE_COMMIT = "3a5ed516bb9ccb43e2d67e9270e1ec2a793e01ac"
EXPECTED_RECEIPT_SHA256 = (
    "b78cf6ee86053c79996c89c72aceb77686b746637f98beafd5f75d0d8af3abe2"
)
REVIEWED_SOURCE_PATHS = (
    ".github/workflows/ci.yml",
    "README.md",
    "ci/ghos_documentary_successor.py",
    "ci/git_content.py",
    "ci/intellect_profile_reconciliation.py",
    "ci/math_programme_pilot_adoption.py",
    "ci/standard_admission.py",
    "ci/status_coherence.py",
    "ci/validate.py",
    "decisions/ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md",
    "schemas/coherence_receipt.schema.json",
    "schemas/current_admission_selection.schema.json",
    "schemas/current_programme_adoption_selection.schema.json",
    "schemas/current_status_projection.schema.json",
    "schemas/standard_successor_lineage.schema.json",
    "standards/GCL-GHOS-00.md",
    "standards/history/GCL-GHOS-00-0.1.0.md",
    "tests/test_ghos_documentary_successor.py",
    "tests/test_git_content.py",
    "tests/test_intellect_profile_reconciliation.py",
    "tests/test_standard_admission.py",
    "tests/test_status_coherence.py",
    "tests/test_validate.py",
)
EXPECTED_RECORDED_ARTIFACTS = {
    "README.md": "d7e68ecd929691beb268417fdfcc7de660e84468",
    "ci/status_coherence.py": "b3c299bd8d75feec38e1d9a88fee1638ad38d264",
    "decisions/ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md": (
        "e4d61cfcc5e8ed330b350ab34323bb36a29fcd4c"
    ),
    "schemas/current_status_projection.schema.json": (
        "6f29f42cf9c298bd25d73956bdefc0e5cca484e6"
    ),
    "standards/GCL-GHOS-00.md": "fd2651ba5036cf2455bf925dcd85364894d55726",
    "standards/history/GCL-GHOS-00-0.1.0.md": (
        "b93c57f1fb27bf2a017a4b90719290342424f6d5"
    ),
}


class SuccessorAdmissionError(ValueError):
    pass


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SuccessorAdmissionError(f"record must be an object: {path}")
    return value


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate_successor_admission(
    admission: dict[str, object] | None = None,
    *,
    root: Path = ROOT,
) -> dict[str, object]:
    schema = load_json(root / "schemas" / "standard_successor_admission.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    record = admission or load_json(
        root / "admissions" / "GCL-GHOS-00-0.1.1.json"
    )
    jsonschema.validate(
        record,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    packet = record["review_packet"]
    receipt_path = root / packet["receipt_path"]
    if lf_sha256(receipt_path) != EXPECTED_RECEIPT_SHA256:
        raise SuccessorAdmissionError("exact Clerk receipt bytes drift")
    receipt = load_json(receipt_path)
    if receipt["status"] != "complete":
        raise SuccessorAdmissionError("review receipt is not complete")
    if receipt["campaign_id"] != packet["campaign_id"]:
        raise SuccessorAdmissionError("review campaign identity mismatch")
    if receipt["packet_sha256"] != packet["packet_sha256"]:
        raise SuccessorAdmissionError("review packet digest mismatch")
    if receipt["human_steward"] != "fyremael":
        raise SuccessorAdmissionError("Human Steward identity mismatch")

    subjects = {
        (row["repository"], row["pull_request"]): row["head_sha"]
        for row in receipt["subjects"]
    }
    if subjects != {
        ("grandchallenge/INTELLECT", 52): (
            "e12716e743fb306e41a80ace0bcfc64f71adf086"
        ),
        ("grandchallenge/gcl-standards", 36): REVIEWED_SOURCE_COMMIT,
    }:
        raise SuccessorAdmissionError("review receipt subject identity drift")

    signoffs = {row["office"]: row for row in receipt["signoffs"]}
    if set(signoffs) != {"adversary", "referee", "human_steward"}:
        raise SuccessorAdmissionError("review receipt staffing is incomplete")
    if signoffs["human_steward"]["attestation_record"] != packet[
        "steward_authorization_url"
    ]:
        raise SuccessorAdmissionError("Steward authorization record mismatch")

    source = record["reviewed_source"]
    if source["reviewed_commit"] != REVIEWED_SOURCE_COMMIT:
        raise SuccessorAdmissionError("reviewed source head drift")
    recorded_artifacts = {
        row["path"]: row["git_blob_sha1"] for row in source["artifacts"]
    }
    if recorded_artifacts != EXPECTED_RECORDED_ARTIFACTS:
        raise SuccessorAdmissionError("recorded source blob identities drift")

    for relative_path in REVIEWED_SOURCE_PATHS:
        reviewed_blob = git_blob_sha1_at_commit(
            root=root,
            commit=REVIEWED_SOURCE_COMMIT,
            relative_path=relative_path,
        )
        current_blob = git_blob_sha1(root / relative_path, root=root)
        if current_blob != reviewed_blob:
            raise SuccessorAdmissionError(
                f"reviewed source blob changed during integration: {relative_path}"
            )

    staffing = record["review_staffing"]
    if staffing["adversary"]["reviewer_id"] == staffing["referee"]["reviewer_id"]:
        raise SuccessorAdmissionError("Adversary and Referee identities must differ")
    if staffing["adversary"]["session_id"] == staffing["referee"]["session_id"]:
        raise SuccessorAdmissionError("Adversary and Referee sessions must differ")
    if any(value is not False for value in record["claim_boundaries"].values()):
        raise SuccessorAdmissionError("successor admission claim boundary inflation")

    return record


if __name__ == "__main__":
    validate_successor_admission()
    print("GCL-GHOS 0.1.1 successor admission validation passed")
