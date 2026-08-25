from __future__ import annotations

import hashlib
import sys
from pathlib import Path


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
EXPECTED_HISTORICAL_010_BLOB = "b93c57f1fb27bf2a017a4b90719290342424f6d5"
EXPECTED_HISTORICAL_011_BLOB = "fd2651ba5036cf2455bf925dcd85364894d55726"
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


def validate(*, root: Path = ROOT) -> None:
    historical_010 = root / "standards" / "history" / "GCL-GHOS-00-0.1.0.md"
    historical_011 = root / "standards" / "history" / "GCL-GHOS-00-0.1.1.md"
    current = root / "standards" / "GCL-GHOS-00.md"
    adr = root / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"
    readme = root / "README.md"

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
        raise DocumentarySuccessorError("0.2.0 candidate does not contain a normative change")

    for required in (
        "**Version:** 0.2.0",
        "**Status:** Candidate normative successor; no effect until protected successor admission and programme adoption",
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
        "Version `0.2.0` is a normative successor candidate to the protected `0.1.1`",
        "Programme adoption of `0.2.0`\nis a later, separate, exact, programme-owned decision.",
    ):
        if required not in current_text:
            raise DocumentarySuccessorError(
                f"missing 0.2.0 bounded-execution-continuity field: {required}"
            )

    adr_text = adr.read_text(encoding="utf-8")
    if "**Status:** Accepted" not in adr_text:
        raise DocumentarySuccessorError("ADR-0001 current status is not accepted")
    if "Human Steward approval is **pending**" in adr_text:
        raise DocumentarySuccessorError("ADR-0001 retains stale pending approval text")
    for stale_assertion in (
        "This ADR becomes accepted only after:",
        "Activate `GI-AMEND-0001`",
        "Accept this ADR and admit GCL-GHOS",
        "selection pending exact-packet admission",
    ):
        if stale_assertion in adr_text:
            raise DocumentarySuccessorError(
                f"ADR-0001 retains stale prospective status: {stale_assertion}"
            )

    readme_text = readme.read_text(encoding="utf-8")
    for required in (
        "Version `0.1.1` remains the currently admitted and selected",
        "A `0.2.0` normative successor is currently candidate-only.",
        "do not admit or adopt that successor.",
    ):
        if required not in readme_text:
            raise DocumentarySuccessorError(
                f"README successor projection is incomplete: {required}"
            )
    for forbidden in (
        "Version `0.2.0` is admitted",
        "Version `0.2.0` is the currently admitted",
        "0.2.0 adoption is active",
    ):
        if forbidden in readme_text:
            raise DocumentarySuccessorError(
                f"README prematurely activates 0.2.0: {forbidden}"
            )


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"GCL-GHOS successor validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print("GCL-GHOS 0.2.0 bounded execution continuity candidate validation passed")
