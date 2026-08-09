from __future__ import annotations

import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CI_DIR = Path(__file__).resolve().parent
if str(CI_DIR) not in sys.path:
    sys.path.insert(0, str(CI_DIR))

from git_content import git_blob_sha1  # noqa: E402


HISTORICAL_STANDARD = ROOT / "standards" / "history" / "GCL-GHOS-00-0.1.0.md"
CURRENT_STANDARD = ROOT / "standards" / "GCL-GHOS-00.md"
ADR = ROOT / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"
EXPECTED_HISTORICAL_BLOB = "b93c57f1fb27bf2a017a4b90719290342424f6d5"
EXPECTED_NORMATIVE_SHA256 = (
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
    historical = root / "standards" / "history" / "GCL-GHOS-00-0.1.0.md"
    current = root / "standards" / "GCL-GHOS-00.md"
    adr = root / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md"

    if git_blob_sha1(historical, root=root) != EXPECTED_HISTORICAL_BLOB:
        raise DocumentarySuccessorError("historical 0.1.0 Git blob identity drift")

    historical_body = normative_body(historical.read_text(encoding="utf-8"))
    current_text = current.read_text(encoding="utf-8")
    current_body = normative_body(current_text)
    if historical_body != current_body:
        raise DocumentarySuccessorError("0.1.1 normative body differs from 0.1.0")
    if hashlib.sha256(current_body).hexdigest() != EXPECTED_NORMATIVE_SHA256:
        raise DocumentarySuccessorError("GCL-GHOS normative body digest drift")

    for required in (
        "**Version:** 0.1.1",
        "**Status:** Admitted documentary successor; effective only when selected by a protected admission record",
        "**Predecessor admission:** `admissions/GCL-GHOS-00-0.1.0.json`",
        "**Admission authority:** exact protected `gcl-standards` admission record",
        "**Adoption authority:** exact programme-owned adoption record",
    ):
        if required not in current_text:
            raise DocumentarySuccessorError(f"missing 0.1.1 documentary field: {required}")

    adr_text = adr.read_text(encoding="utf-8")
    if "**Status:** Accepted" not in adr_text:
        raise DocumentarySuccessorError("ADR-0001 current status is not accepted")
    if "Human Steward approval is **pending**" in adr_text:
        raise DocumentarySuccessorError("ADR-0001 retains stale pending approval text")
    for stale_assertion in (
        "This ADR becomes accepted only after:",
        "Activate `GI-AMEND-0001`",
        "Accept this ADR and admit GCL-GHOS",
    ):
        if stale_assertion in adr_text:
            raise DocumentarySuccessorError(
                f"ADR-0001 retains stale prospective status: {stale_assertion}"
            )
    for required in (
        "ADR-0001 was accepted through the protected `0.1.0` admission lineage",
        "MATH-PROGRAMME adoption follows the protected `0.1.1` admission",
        "Admit byte-identical reviewed `0.1.1` source blobs",
    ):
        if required not in adr_text:
            raise DocumentarySuccessorError(
                f"ADR-0001 successor sequence is incomplete: {required}"
            )
    if "does not itself admit `0.1.1`" not in adr_text:
        raise DocumentarySuccessorError("0.1.1 admission boundary is missing")


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"documentary successor validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print("GCL-GHOS 0.1.1 documentary successor validation passed")
