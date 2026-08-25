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

from git_content import git_blob_sha1  # noqa: E402


HISTORICAL_STANDARD_010 = ROOT / "standards" / "history" / "GCL-GHOS-00-0.1.0.md"
HISTORICAL_STANDARD_011 = ROOT / "standards" / "history" / "GCL-GHOS-00-0.1.1.md"
CURRENT_STANDARD = ROOT / "standards" / "GCL-GHOS-00.md"
ADR = ROOT / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"
README = ROOT / "README.md"
ADMISSION_020 = ROOT / "admissions" / "GCL-GHOS-00-0.2.0.json"
ADMISSION_SCHEMA = ROOT / "schemas" / "standard_normative_successor_admission.schema.json"
EXPECTED_HISTORICAL_010_BLOB = "b93c57f1fb27bf2a017a4b90719290342424f6d5"
EXPECTED_HISTORICAL_011_BLOB = "fd2651ba5036cf2455bf925dcd85364894d55726"
EXPECTED_REVIEWED_020_BLOB = "fdb8c9575725281f73649f160cab6b7b01cd09e0"
EXPECTED_011_NORMATIVE_SHA256 = (
    "c9912acb0aacc186f93655e9e1b7938235954bb9466dcddf923cd601ed7bc2a3"
)


class DocumentarySuccessorError(ValueError):
    pass


def normative_body(text: str) -> bytes:
    normalized = text.replace("\r\n", "\n")
    marker = "## Purpose\n"
    if marker not in normalized:
        raise DocumentarySuccessorError("GCL-GHOS normative body marker is missing")
    return (marker + normalized.split(marker, 1)[1]).encode("utf-8")


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise DocumentarySuccessorError(f"record must be an object: {path}")
    return value


def validate(*, root: Path = ROOT) -> None:
    historical_010 = root / "standards" / "history" / "GCL-GHOS-00-0.1.0.md"
    historical_011 = root / "standards" / "history" / "GCL-GHOS-00-0.1.1.md"
    current = root / "standards" / "GCL-GHOS-00.md"
    adr = root / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"
    readme = root / "README.md"
    admission_path = root / "admissions" / "GCL-GHOS-00-0.2.0.json"
    schema_path = root / "schemas" / "standard_normative_successor_admission.schema.json"

    if git_blob_sha1(historical_010, root=root) != EXPECTED_HISTORICAL_010_BLOB:
        raise DocumentarySuccessorError("historical 0.1.0 Git blob identity drift")
    if git_blob_sha1(historical_011, root=root) != EXPECTED_HISTORICAL_011_BLOB:
        raise DocumentarySuccessorError("historical 0.1.1 Git blob identity drift")

    body_010 = normative_body(historical_010.read_text(encoding="utf-8"))
    text_011 = historical_011.read_text(encoding="utf-8")
    body_011 = normative_body(text_011)
    if body_010 != body_011:
        raise DocumentarySuccessorError("admitted 0.1.1 normative body differs from 0.1.0")
    if hashlib.sha256(body_011).hexdigest() != EXPECTED_011_NORMATIVE_SHA256:
        raise DocumentarySuccessorError("admitted 0.1.1 normative body digest drift")
    if "### Bounded execution continuity" in text_011:
        raise DocumentarySuccessorError("historical 0.1.1 was silently rewritten")

    current_text = current.read_text(encoding="utf-8")
    current_body = normative_body(current_text)
    if current_body == body_011:
        raise DocumentarySuccessorError("0.2.0 successor does not contain a normative change")

    for required in (
        "**Version:** 0.2.0",
        "**Predecessor admission:** `admissions/GCL-GHOS-00-0.1.1.json`",
        "**Historical predecessor:** `standards/history/GCL-GHOS-00-0.1.1.md`",
        "**Admission authority:** exact protected `gcl-standards` admission record",
        "**Adoption authority:** exact programme-owned adoption record",
        "### Bounded execution continuity",
        "A recoverable platform, connector,",
        "tooling failure does not by\nitself constitute an authority boundary.",
        "Fail-closed behavior applies to authority, admission, certification, promotion,",
        "It SHALL NOT be\ninterpreted as requiring premature abandonment of authorized evidence gathering,",
        "Evidence from a\nsuperseded artifact, revision, run, job, or other identity SHALL NOT be reused as\ncurrent evidence.",
        "Programme-owned policy MAY define concrete recovery ladders",
        "Programme adoption of `0.2.0`\nis a later, separate, exact, programme-owned decision.",
    ):
        if required not in current_text:
            raise DocumentarySuccessorError(
                f"missing 0.2.0 bounded-execution-continuity field: {required}"
            )

    if git_blob_sha1(current, root=root) != EXPECTED_REVIEWED_020_BLOB:
        raise DocumentarySuccessorError("reviewed 0.2.0 standard source blob drift")

    admission = _load_json(admission_path)
    schema = _load_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        admission,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    staffing = admission["review_staffing"]
    if not isinstance(staffing, dict):
        raise DocumentarySuccessorError("review staffing must be an object")
    adversary = staffing.get("adversary")
    referee = staffing.get("referee")
    if not isinstance(adversary, dict) or not isinstance(referee, dict):
        raise DocumentarySuccessorError("adversary and referee records are required")
    if adversary.get("reviewer_id") == referee.get("reviewer_id"):
        raise DocumentarySuccessorError("Adversary and Referee identities must be distinct")
    if adversary.get("session_id") == referee.get("session_id"):
        raise DocumentarySuccessorError("Adversary and Referee sessions must be distinct")

    boundaries = admission["claim_boundaries"]
    if not isinstance(boundaries, dict) or any(value is not False for value in boundaries.values()):
        raise DocumentarySuccessorError("0.2.0 admission widens a prohibited claim boundary")

    adr_text = adr.read_text(encoding="utf-8")
    if "**Status:** Accepted" not in adr_text:
        raise DocumentarySuccessorError("ADR-0001 current status is not accepted")
    if "Human Steward approval is **pending**" in adr_text:
        raise DocumentarySuccessorError("ADR-0001 retains stale pending approval text")

    readme_text = readme.read_text(encoding="utf-8")
    for required in (
        "Version `0.1.1` remains the version selected by the existing",
        "Version `0.2.0` is the reviewed normative successor adding bounded execution",
        "[`admissions/GCL-GHOS-00-0.2.0.json`](admissions/GCL-GHOS-00-0.2.0.json)",
        "which becomes effective only through protected merge of that exact record.",
        "The\nreviewed standard source remains byte-identical to PR #52 head",
        "MATH-PROGRAMME adoption of\n`0.2.0` remains a separate later gate",
    ):
        if required not in readme_text:
            raise DocumentarySuccessorError(
                f"README 0.2.0 admission projection is incomplete: {required}"
            )
    for forbidden in (
        "0.2.0 adoption is active",
        "MATH-PROGRAMME actively adopts `0.2.0`",
        "organization-wide conformance is authorized",
    ):
        if forbidden in readme_text:
            raise DocumentarySuccessorError(
                f"README prematurely promotes 0.2.0: {forbidden}"
            )


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"GCL-GHOS successor admission validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print("GCL-GHOS 0.2.0 reviewed-source admission validation passed")
