from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_gcl_rc_chronology_cure",
    ROOT / "ci" / "validate_gcl_rc_chronology_cure.py",
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ChronologyCureTests(unittest.TestCase):
    def record(self) -> dict[str, object]:
        return json.loads(
            (
                ROOT
                / "implementation"
                / "GCL-RC-CHRONOLOGY-CURE-001.json"
            ).read_text(encoding="utf-8")
        )

    def test_ratified_record_validates(self) -> None:
        validator.validate_record(self.record())

    def test_cannot_invent_pre_merge_authorization(self) -> None:
        broken = copy.deepcopy(self.record())
        broken["subject"]["pre_merge_steward_authorization_present"] = True
        with self.assertRaises(Exception):
            validator.validate_record(broken)

    def test_cannot_treat_prospective_comment_as_cure(self) -> None:
        broken = copy.deepcopy(self.record())
        broken["retrospective_ratification"] = {
            "required": True,
            "comment_id": 5160945680,
            "author": "fyremael",
            "recorded_at": "2026-08-02T23:52:26Z",
        }
        with self.assertRaises(Exception):
            validator.validate_record(broken)

    def test_ratification_comment_id_is_exact(self) -> None:
        broken = copy.deepcopy(self.record())
        broken["retrospective_ratification"]["comment_id"] = 5161001757
        with self.assertRaises(ValueError):
            validator.validate_record(broken)

    def test_ratification_timestamp_is_exact(self) -> None:
        broken = copy.deepcopy(self.record())
        broken["retrospective_ratification"]["recorded_at"] = "2026-08-03T00:07:13Z"
        with self.assertRaises(ValueError):
            validator.validate_record(broken)

    def test_pending_record_rejects_partial_ratification(self) -> None:
        broken = copy.deepcopy(self.record())
        broken["state"] = "ratification_pending"
        broken["retrospective_ratification"] = {
            "required": True,
            "comment_id": 999,
            "author": None,
            "recorded_at": None,
        }
        with self.assertRaises(ValueError):
            validator.validate_record(broken)

    def test_comment_identity_is_exact(self) -> None:
        broken = copy.deepcopy(self.record())
        broken["post_merge_comments"][1]["created_at"] = "2026-08-02T23:35:00Z"
        with self.assertRaises(Exception):
            validator.validate_record(broken)

    def test_candidate_boundary_cannot_inflate(self) -> None:
        broken = copy.deepcopy(self.record())
        broken["preserved_boundaries"]["any_programme_conformant"] = True
        with self.assertRaises(Exception):
            validator.validate_record(broken)

    def test_revert_is_not_falsely_required(self) -> None:
        broken = copy.deepcopy(self.record())
        broken["preserved_boundaries"]["revert_required"] = True
        with self.assertRaises(Exception):
            validator.validate_record(broken)


if __name__ == "__main__":
    unittest.main()
