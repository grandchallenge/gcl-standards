from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from optimality_scorecard import validate_scorecard


ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT_PATH = ROOT / "evidence" / "phase-closeouts" / "GCL-OPT-PHASE12-CLOSEOUT-001.json"
SCHEMA_PATH = ROOT / "schemas" / "phase12_closeout.schema.json"
COHERENCE_PATH = ROOT / "evidence" / "coherence-reviews" / "GCL-STATUS-COHERENCE-001-coherence.json"
AETHER_PATH = ROOT / "evidence" / "settings-readback" / "GCL-AETHER-CONFORMANCE-001.json"
SCORECARD_PATH = ROOT / "scorecards" / "GCL-OPT-SCORECARD-2026-W32.json"


class Phase12CloseoutError(ValueError):
    pass


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Phase12CloseoutError(f"record must be an object: {path}")
    return value


def validate(*, root: Path = ROOT) -> None:
    schema = _load(root / "schemas" / "phase12_closeout.schema.json")
    closeout = _load(
        root / "evidence" / "phase-closeouts" / "GCL-OPT-PHASE12-CLOSEOUT-001.json"
    )
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        closeout,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    expected_phase1 = {
        "SC-01",
        "SC-02",
        "SC-03",
        "SC-04",
        "SC-05",
        "SC-06",
        "SC-07",
        "SC-08",
        "VAL-01",
    }
    if set(closeout["phase1"]["closed_rows"]) != expected_phase1:
        raise Phase12CloseoutError("Phase 1 closeout row set drift")

    coherence = _load(
        root
        / "evidence"
        / "coherence-reviews"
        / "GCL-STATUS-COHERENCE-001-coherence.json"
    )
    if coherence.get("status") != "coherent":
        raise Phase12CloseoutError("Phase 1 coherence is not closed")
    contradictions = coherence.get("contradictions", {})
    if contradictions.get("open_count") != 0:
        raise Phase12CloseoutError("Phase 1 coherence retains open contradictions")
    if set(contradictions.get("closed_ids", [])) != expected_phase1:
        raise Phase12CloseoutError("Phase 1 coherence receipt row set drift")

    rows = {item["id"]: item for item in closeout["phase2_rows"]}
    if set(rows) != {"SEC-01", "SEC-03", "SEC-04", "GOV-01"}:
        raise Phase12CloseoutError("Phase 2 deviation row set drift")
    for identifier in ("SEC-01", "SEC-03", "GOV-01"):
        if rows[identifier]["priority"] != "P1" or rows[identifier]["status"] != "closed":
            raise Phase12CloseoutError(f"P1 row is not closed: {identifier}")
    if rows["SEC-04"]["priority"] != "P2" or rows["SEC-04"]["status"] != "open_bounded":
        raise Phase12CloseoutError("SEC-04 must remain a bounded P2 remainder")

    open_p2 = rows["SEC-04"].get("open_deviations", [])
    if {item["id"] for item in open_p2} != {
        "GCL-HUMAN-CLI-ADMIN-SCOPE-001",
        "GCL-CLERK-CONTENTS-SCOPE-001",
    }:
        raise Phase12CloseoutError("credential P2 remainder set drift")
    for item in open_p2:
        for key in ("owner", "expires_at", "compensating_control", "review_date"):
            if not item.get(key):
                raise Phase12CloseoutError(
                    f"open P2 deviation lacks {key}: {item.get('id')}"
                )

    aether = _load(
        root / "evidence" / "settings-readback" / "GCL-AETHER-CONFORMANCE-001.json"
    )
    if aether.get("protected_main_sha") != closeout["protected_heads"]["grandchallenge/AETHER"]:
        raise Phase12CloseoutError("AETHER closeout head does not match admitted readback")
    if aether.get("verifier", {}).get("status") != "passed" or aether.get("verifier", {}).get("blockers"):
        raise Phase12CloseoutError("AETHER readback is not zero-blocker verified")
    if not aether.get("default_branch_protection", {}).get("classic_absent"):
        raise Phase12CloseoutError("AETHER classic protection retirement is not read back")
    if any(item.get("bypass_actors") for item in aether.get("rulesets", [])):
        raise Phase12CloseoutError("AETHER closeout permits a ruleset bypass")

    scorecard = _load(root / "scorecards" / "GCL-OPT-SCORECARD-2026-W32.json")
    validate_scorecard(scorecard, root=root)
    scorecard_ref = closeout["weekly_scorecard"]
    if scorecard.get("record_id") != scorecard_ref["record_id"]:
        raise Phase12CloseoutError("scorecard record identity drift")
    if scorecard.get("generator", {}).get("run_id") != scorecard_ref["generator_workflow_run"]:
        raise Phase12CloseoutError("scorecard generator run drift")

    acceptance = closeout["acceptance"]
    if acceptance["p0_open"] or acceptance["p1_open"]:
        raise Phase12CloseoutError("Phase 1-2 closeout retains a P0/P1 blocker")
    if set(acceptance["p2_open"]) != {
        "SEC-04/GCL-HUMAN-CLI-ADMIN-SCOPE-001",
        "SEC-04/GCL-CLERK-CONTENTS-SCOPE-001",
    }:
        raise Phase12CloseoutError("declared P2 remainder set drift")
    if any(closeout["claim_boundaries"].values()):
        raise Phase12CloseoutError("Phase 1-2 closeout widens prohibited authority")


if __name__ == "__main__":
    validate()
    print("Phase 1-2 closeout validated")
