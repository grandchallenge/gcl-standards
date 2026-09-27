from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from gcl_id import (  # noqa: E402
    ADMISSION,
    GCLIDError,
    _load_json,
    validate,
    validate_admission_record,
)


class GCLIDTests(unittest.TestCase):
    def test_current_admission_is_well_formed(self) -> None:
        validate()

    def test_current_programme_adoption_projection_is_effective(self) -> None:
        from gcl_id import STATUS

        status = _load_json(STATUS)
        self.assertEqual(status["programme_adoption"]["status"], "effective")
        self.assertEqual(
            status["programme_adoption"]["protected_commit"],
            "64ad90b3108f476225cc1ca5a2889e71b3719cc8",
        )
        self.assertTrue(status["claim_boundaries"]["programme_adoption_complete"])

    def test_duplicate_logical_pass_is_rejected(self) -> None:
        record = copy.deepcopy(_load_json(ADMISSION))
        record["source_reviews"]["referee"]["logical_pass_id"] = record["source_reviews"]["adversary"]["logical_pass_id"]
        with self.assertRaisesRegex(GCLIDError, "distinct logical passes"):
            validate_admission_record(record)

    def test_duplicate_review_record_is_rejected(self) -> None:
        record = copy.deepcopy(_load_json(ADMISSION))
        record["source_reviews"]["referee"]["record_ref"] = record["source_reviews"]["adversary"]["record_ref"]
        with self.assertRaisesRegex(GCLIDError, "distinct durable records"):
            validate_admission_record(record)

    def test_authority_inflation_is_rejected(self) -> None:
        record = copy.deepcopy(_load_json(ADMISSION))
        record["claim_boundaries"]["mathematical_claim_authorized"] = True
        with self.assertRaises(Exception):
            validate_admission_record(record)

    def test_review_subject_drift_is_rejected(self) -> None:
        record = copy.deepcopy(_load_json(ADMISSION))
        record["source_reviews"]["referee"]["candidate_head"] = "0" * 40
        with self.assertRaises(Exception):
            validate_admission_record(record)


if __name__ == "__main__":
    unittest.main()
