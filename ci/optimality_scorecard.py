from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "optimality_scorecard.schema.json"


class OptimalityScorecardError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise OptimalityScorecardError(f"scorecard must be an object: {path}")
    return value


def validate_scorecard(scorecard: dict[str, Any], *, root: Path = ROOT) -> None:
    schema = load_json(root / "schemas" / "optimality_scorecard.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        scorecard,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )
    deviation_ids = {item["id"] for item in scorecard["deviations"]}
    for name, metric in scorecard["metrics"].items():
        if "unknown" in metric and metric["unknown"]["deviation_id"] not in deviation_ids:
            raise OptimalityScorecardError(
                f"unknown metric lacks an owned deviation: {name}"
            )
    if any(value is not False for value in scorecard["claim_boundaries"].values()):
        raise OptimalityScorecardError("scorecard widens prohibited claim authority")


def validate_schema(*, root: Path = ROOT) -> None:
    schema = load_json(root / "schemas" / "optimality_scorecard.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)


if __name__ == "__main__":
    validate_schema()
    print("optimality scorecard schema validated")
