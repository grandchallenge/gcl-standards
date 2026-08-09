from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "optimality_scorecard", ROOT / "ci" / "optimality_scorecard.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def metric(*, value: float | None = None, unknown: bool = False) -> dict[str, object]:
    item: dict[str, object] = {
        "unit": "count",
        "status": "unknown" if unknown else "observed",
        "target": {"operator": "eq", "value": 0},
        "evidence_references": [],
        "measurement_window": {
            "start": "2026-08-02T00:00:00Z",
            "end": "2026-08-09T00:00:00Z",
        },
        "exclusions": [],
        "exact_source_heads": [],
    }
    if unknown:
        item["unknown"] = {"reason": "registry not admitted", "deviation_id": "DEV-1"}
    else:
        item["value"] = 0 if value is None else value
    return item


def canonical() -> dict[str, object]:
    names = (
        "status_contradictions",
        "unprotected_default_branches",
        "human_actions_per_governed_decision",
        "strategic_lanes_in_progress",
        "active_issues_without_finite_next_obligation",
        "handoffs_lacking_exact_identities",
        "median_pr_decision_time_hours",
        "reproducible_governed_lifecycle",
        "github_inferred_mathematical_claims",
    )
    metrics = {name: metric() for name in names}
    for name in (
        "strategic_lanes_in_progress",
        "active_issues_without_finite_next_obligation",
        "handoffs_lacking_exact_identities",
    ):
        metrics[name] = metric(unknown=True)
    return {
        "$schema": "../schemas/optimality_scorecard.schema.json",
        "schema_version": "1.0.0",
        "record_id": "GCL-OPT-SCORECARD-2026-W32",
        "generated_at": "2026-08-09T00:00:00Z",
        "measurement_window": {
            "start": "2026-08-02T00:00:00Z",
            "end": "2026-08-09T00:00:00Z",
        },
        "generator": {
            "repository": "grandchallenge/.github",
            "workflow": ".github/workflows/weekly-optimality-scorecard.yml",
            "run_id": "1",
            "app_slug": "gcl-council-clerk",
        },
        "metrics": metrics,
        "deviations": [
            {
                "id": "DEV-1",
                "owner": "fyremael",
                "expires_at": "2026-09-01T00:00:00Z",
                "compensating_control": "report unknown",
                "next_review": "2026-08-16T00:00:00Z",
                "evidence": ["https://example.test/deviation"],
            }
        ],
        "claim_boundaries": {
            "organization_wide_conformance_authorized": False,
            "production_claim_authorized": False,
            "mathematical_claim_authorized": False,
            "certification_claim_authorized": False,
            "novelty_claim_authorized": False,
            "deployment_claim_authorized": False,
            "commercial_claim_authorized": False,
        },
    }


class OptimalityScorecardTests(unittest.TestCase):
    def test_canonical_record_and_schema_validate(self) -> None:
        MODULE.validate_schema()
        MODULE.validate_scorecard(canonical())

    def test_unknown_cannot_be_coerced_to_zero(self) -> None:
        broken = copy.deepcopy(canonical())
        item = broken["metrics"]["strategic_lanes_in_progress"]
        item["value"] = 0
        with self.assertRaises(MODULE.jsonschema.ValidationError):
            MODULE.validate_scorecard(broken)

    def test_unknown_requires_owned_deviation(self) -> None:
        broken = copy.deepcopy(canonical())
        broken["metrics"]["handoffs_lacking_exact_identities"]["unknown"][
            "deviation_id"
        ] = "MISSING"
        with self.assertRaisesRegex(
            MODULE.OptimalityScorecardError, "lacks an owned deviation"
        ):
            MODULE.validate_scorecard(broken)

    def test_claim_authority_inflation_is_rejected(self) -> None:
        broken = copy.deepcopy(canonical())
        broken["claim_boundaries"]["mathematical_claim_authorized"] = True
        with self.assertRaises(MODULE.jsonschema.ValidationError):
            MODULE.validate_scorecard(broken)


if __name__ == "__main__":
    unittest.main()
