from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
RECEIPT_SCHEMA = ROOT / "schemas" / "gcl_completion_receipt.schema.json"
STANDARD = ROOT / "standards" / "GCL-CEX-01.md"
STATUS = ROOT / "status" / "GCL-CEX-01-current.json"


class GCLCEXError(ValueError):
    """Raised when a GCL-CEX campaign receipt is not admissible."""


def _load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _analysis_key(review: Mapping[str, object]) -> tuple[tuple[str, ...], tuple[str, ...], str]:
    criteria = tuple(sorted(str(item) for item in review["criteria"]))
    evidence = tuple(sorted(str(item) for item in review["evidence"]))
    return criteria, evidence, str(review["finding"])


def validate_completion_receipt(receipt: Mapping[str, object]) -> None:
    schema = _load(RECEIPT_SCHEMA)
    jsonschema.validate(
        receipt,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    candidate_head = str(receipt["candidate_head"])
    merge_sha = str(receipt["merge_sha"])
    readback_sha = str(receipt["protected_readback_sha"])
    if merge_sha != readback_sha:
        raise GCLCEXError("protected readback must equal the admitted protected merge")

    adversary = receipt["adversary_record"]
    referee = receipt["referee_record"]
    if not isinstance(adversary, Mapping) or not isinstance(referee, Mapping):
        raise GCLCEXError("review records must be structured objects")

    if adversary["logical_pass_id"] == referee["logical_pass_id"]:
        raise GCLCEXError("Adversary and Referee require distinct logical_pass_id values")
    if adversary["record_ref"] == referee["record_ref"]:
        raise GCLCEXError("Adversary and Referee require distinct durable review records")

    for label, review in (("Adversary", adversary), ("Referee", referee)):
        if review["reviewed_candidate_head"] != candidate_head:
            raise GCLCEXError(f"{label} review does not bind the exact candidate head")
        if review["mode"] != "non_authoring_read_only":
            raise GCLCEXError(f"{label} review must be non_authoring_read_only")
        if review["finding"] != "approved":
            raise GCLCEXError(f"{label} review must approve before completion")
        if review["unresolved_obligations"]:
            raise GCLCEXError(f"{label} approval cannot retain unresolved obligations")
        if any(bool(value) for value in review["authority_claims"].values()):
            raise GCLCEXError(f"{label} review cannot manufacture authority or certification")

    if adversary["reviewed_repository"] != referee["reviewed_repository"]:
        raise GCLCEXError("review repository drift invalidates the review pair")
    if _analysis_key(adversary) == _analysis_key(referee):
        raise GCLCEXError("duplicated analysis is not a distinct logical review pass")

    checks = receipt["required_checks"]
    if not isinstance(checks, list) or not checks:
        raise GCLCEXError("completion receipt requires exact check evidence")
    candidate_seen = False
    protected_seen = False
    for check in checks:
        if not isinstance(check, Mapping):
            raise GCLCEXError("check evidence must be structured")
        phase = check.get("phase")
        head = check.get("head")
        result = check.get("result")
        if result != "success":
            raise GCLCEXError("completion receipt cannot admit a non-success check")
        if phase == "candidate":
            candidate_seen = True
            if head != candidate_head:
                raise GCLCEXError("candidate check is stale")
        elif phase == "protected_readback":
            protected_seen = True
            if head != readback_sha:
                raise GCLCEXError("protected-readback check is stale")
        else:
            raise GCLCEXError("check phase must be candidate or protected_readback")
    if not candidate_seen or not protected_seen:
        raise GCLCEXError("receipt requires both candidate and protected-readback checks")


def validate_standard() -> None:
    schema = _load(RECEIPT_SCHEMA)
    jsonschema.Draft202012Validator.check_schema(schema)

    text = STANDARD.read_text(encoding="utf-8")
    required = (
        "GCL-CEX-01",
        "completion receipt",
        "exact-head",
        "protected readback",
        "MATHCERT retains sole certification authority",
    )
    for token in required:
        if token not in text:
            raise GCLCEXError(f"missing GCL-CEX-01 boundary: {token}")

    status = _load(STATUS)
    if not isinstance(status, dict):
        raise GCLCEXError("GCL-CEX-01 status must be an object")
    if status.get("identifier") != "GCL-CEX-01":
        raise GCLCEXError("GCL-CEX-01 status identity drift")
    if status.get("status") not in {"candidate", "admitted"}:
        raise GCLCEXError("invalid GCL-CEX-01 status")


def validate() -> None:
    validate_standard()


if __name__ == "__main__":
    validate()
    print("GCL-CEX-01 validation passed")
