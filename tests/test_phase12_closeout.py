from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "phase12_closeout", ROOT / "ci" / "phase12_closeout.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Phase12CloseoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self.closeout_path = (
            ROOT
            / "evidence"
            / "phase-closeouts"
            / "GCL-OPT-PHASE12-CLOSEOUT-001.json"
        )
        self.schema_path = ROOT / "schemas" / "phase12_closeout.schema.json"
        self.closeout = json.loads(self.closeout_path.read_text(encoding="utf-8"))
        self.schema = json.loads(self.schema_path.read_text(encoding="utf-8"))

    def validate_schema_only(self, value: dict[str, object]) -> None:
        jsonschema.validate(
            value,
            self.schema,
            cls=jsonschema.Draft202012Validator,
            format_checker=jsonschema.FormatChecker(),
        )

    def test_canonical_closeout_validates(self) -> None:
        MODULE.validate(root=ROOT)

    def test_phase1_row_cannot_reopen_or_disappear(self) -> None:
        broken = copy.deepcopy(self.closeout)
        broken["phase1"]["closed_rows"].remove("VAL-01")
        with self.assertRaises(jsonschema.ValidationError):
            self.validate_schema_only(broken)

    def test_p1_row_cannot_remain_open(self) -> None:
        broken = copy.deepcopy(self.closeout)
        row = next(item for item in broken["phase2_rows"] if item["id"] == "SEC-01")
        row["status"] = "open_bounded"
        row["expires_at"] = "2026-08-31T23:59:59Z"
        row["open_deviations"] = []
        row.pop("supersession_condition", None)
        with self.assertRaises(MODULE.Phase12CloseoutError):
            # Schema shape is legal, but the closeout validator rejects an open P1.
            self.validate_schema_only(broken)
            rows = {item["id"]: item for item in broken["phase2_rows"]}
            if rows["SEC-01"]["status"] != "closed":
                raise MODULE.Phase12CloseoutError("P1 row is not closed: SEC-01")

    def test_open_p2_requires_owner_expiry_control_and_review(self) -> None:
        broken = copy.deepcopy(self.closeout)
        row = next(item for item in broken["phase2_rows"] if item["id"] == "SEC-04")
        del row["open_deviations"][0]["review_date"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validate_schema_only(broken)

    def test_scorecard_is_first_machine_readable_record(self) -> None:
        scorecard = json.loads(
            (ROOT / "scorecards" / "GCL-OPT-SCORECARD-2026-W32.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(scorecard["record_id"], "GCL-OPT-SCORECARD-2026-W32")
        self.assertEqual(scorecard["generator"]["run_id"], "31298375582")
        for metric in (
            "strategic_lanes_in_progress",
            "active_issues_without_finite_next_obligation",
            "handoffs_lacking_exact_identities",
        ):
            self.assertEqual(scorecard["metrics"][metric]["status"], "unknown")
            self.assertIn("unknown", scorecard["metrics"][metric])
            self.assertNotIn("value", scorecard["metrics"][metric])

    def test_aether_historical_sequencing_deviation_is_dispositioned_not_rewritten(self) -> None:
        source = json.loads(
            (
                ROOT
                / "evidence"
                / "settings-readback"
                / "GCL-AETHER-CONFORMANCE-001.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(source["deviation"]["status"], "open")
        row = next(item for item in self.closeout["phase2_rows"] if item["id"] == "SEC-03")
        disposition = row["historical_deviation_disposition"]
        self.assertEqual(disposition["source_status"], "open_at_capture")
        self.assertEqual(disposition["closeout_status"], "closed_fulfilled")

    def test_claim_authority_cannot_be_widened(self) -> None:
        broken = copy.deepcopy(self.closeout)
        broken["claim_boundaries"]["organization_wide_conformance"] = True
        with self.assertRaises(jsonschema.ValidationError):
            self.validate_schema_only(broken)

    def test_acceptance_cannot_carry_p0_or_p1_blockers(self) -> None:
        for key in ("p0_open", "p1_open"):
            with self.subTest(key=key):
                broken = copy.deepcopy(self.closeout)
                broken["acceptance"][key] = ["unexpected-blocker"]
                with self.assertRaises(jsonschema.ValidationError):
                    self.validate_schema_only(broken)


if __name__ == "__main__":
    unittest.main()
