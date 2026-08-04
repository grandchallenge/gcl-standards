from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECONCILIATION = ROOT / "deviations/GCL-GHOS-INTELLECT-PROFILE-RECONCILIATION-001.json"
MODULUS_OVERLAY = ROOT / "deviations/GCL-GHOS-SETTINGS-READBACK-001.modulus-closure-overlay.json"
EXPECTED_OPEN_ROWS = {"QUANTUM-P1-001", "QUANTUM-P2-001"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_overlay_binding(reconciliation: dict, overlay: dict) -> None:
    if reconciliation["base_records"].get("modulus_closure_overlay") != {
        "path": "deviations/GCL-GHOS-SETTINGS-READBACK-001.modulus-closure-overlay.json",
        "merge_commit": "4884001459e1346aebd21e44c49a8ab2c695d09b",
    }:
        raise ValueError("MODULUS closure-overlay binding drift")
    open_rows = {
        row.get("id")
        for row in overlay.get("open_rows", [])
        if isinstance(row, dict)
    }
    if open_rows != EXPECTED_OPEN_ROWS:
        raise ValueError("post-MODULUS open-row state drift")
    if set(reconciliation["carried_open_rows"]) != EXPECTED_OPEN_ROWS:
        raise ValueError("INTELLECT carried-row state drift")
    if reconciliation["open_priority_counts"] != {
        "P0": 0,
        "P1": 1,
        "P2": 1,
        "P3": 0,
    }:
        raise ValueError("INTELLECT post-closure priority count drift")


class IntellectPhaseBOverlayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reconciliation = load(RECONCILIATION)
        self.overlay = load(MODULUS_OVERLAY)

    def test_exact_overlay_binding_validates(self) -> None:
        validate_overlay_binding(self.reconciliation, self.overlay)

    def test_rejects_reintroduced_modulus_row(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["carried_open_rows"].append("MODULUS-P1-001")
        with self.assertRaises(ValueError):
            validate_overlay_binding(value, self.overlay)

    def test_rejects_stale_priority_counts(self) -> None:
        value = copy.deepcopy(self.reconciliation)
        value["open_priority_counts"]["P1"] = 2
        with self.assertRaises(ValueError):
            validate_overlay_binding(value, self.overlay)


if __name__ == "__main__":
    unittest.main()
