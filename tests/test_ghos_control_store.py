from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for name in ("ghos_control_plane", "ghos_control_store"):
    spec = importlib.util.spec_from_file_location(name, ROOT / "ci" / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
STORE = sys.modules["ghos_control_store"]
CONTROL = sys.modules["ghos_control_plane"]


class ProtectedControlStoreTests(unittest.TestCase):
    def fixture(self, directory: Path) -> None:
        source = ROOT / "implementation" / "GCL-GHOS-CONTROL-PLANE-REMEDIATION-001" / "control-plane"
        admission = json.loads((source / "candidate-work-package-admission.json").read_text())
        ledger = json.loads((source / "candidate-harness-ledger.json").read_text())
        ledger["storage_status"] = "PROTECTED_CONTROL_REF"
        ledger["candidate_branch_notice"] = None
        directory.mkdir(parents=True)
        (directory / "admission.json").write_text(json.dumps(admission), encoding="utf-8")
        (directory / "ledger.json").write_text(json.dumps(ledger), encoding="utf-8")
        store = {
            "work_package": ledger["work_package"],
            "repository": "grandchallenge/gcl-standards",
            "ref": STORE.CONTROL_REF,
            "ruleset_id": STORE.CONTROL_RULESET_ID,
            "ruleset_url": f"https://github.com/grandchallenge/gcl-standards/rules/{STORE.CONTROL_RULESET_ID}",
            "deletion_prohibited": True,
            "non_fast_forward_prohibited": True,
            "claim_boundaries": copy.deepcopy(CONTROL.CLAIM_BOUNDARIES),
        }
        (directory / "store.json").write_text(json.dumps(store), encoding="utf-8")

    def test_valid_protected_store_reduces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "control"
            self.fixture(directory)
            state = STORE.validate_control_directory(directory)
            self.assertEqual(state["work_package"], "GCL-GHOS-CONTROL-PLANE-REMEDIATION-001")

    def test_invalid_append_is_rejected_before_integration(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "control"
            self.fixture(directory)
            ledger = json.loads((directory / "ledger.json").read_text())
            ledger["events"][0]["event_digest"] = "0" * 64
            (directory / "ledger.json").write_text(json.dumps(ledger), encoding="utf-8")
            with self.assertRaisesRegex(CONTROL.LedgerError, "event digest mismatch"):
                STORE.validate_control_directory(directory)

    def test_store_protection_and_claims_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "control"
            self.fixture(directory)
            store = json.loads((directory / "store.json").read_text())
            store["non_fast_forward_prohibited"] = False
            (directory / "store.json").write_text(json.dumps(store), encoding="utf-8")
            with self.assertRaisesRegex(STORE.ControlStoreError, "append-only"):
                STORE.validate_control_directory(directory)

    def test_append_must_preserve_exact_prior_prefix_and_store(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "control"
            self.fixture(directory)
            admission = json.loads((directory / "admission.json").read_text())
            base_ledger = json.loads((directory / "ledger.json").read_text())
            store = json.loads((directory / "store.json").read_text())
            rewritten = copy.deepcopy(base_ledger)
            rewritten["events"][0]["payload"]["admission_path"] = "substituted.json"
            rewritten["events"][0]["event_digest"] = CONTROL.event_digest(rewritten["events"][0])
            rewritten["ledger_head_digest"] = rewritten["events"][0]["event_digest"]
            rewritten["events"].append(copy.deepcopy(rewritten["events"][0]))
            (directory / "ledger.json").write_text(json.dumps(rewritten), encoding="utf-8")
            with self.assertRaisesRegex(STORE.ControlStoreError, "rewrites prior"):
                STORE.validate_append_prefix(
                    directory, base_admission=admission, base_ledger=base_ledger, base_store=store
                )

    def test_append_rejects_admission_or_ruleset_substitution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "control"
            self.fixture(directory)
            admission = json.loads((directory / "admission.json").read_text())
            ledger = json.loads((directory / "ledger.json").read_text())
            store = json.loads((directory / "store.json").read_text())
            ledger["events"].append(copy.deepcopy(ledger["events"][0]))
            (directory / "ledger.json").write_text(json.dumps(ledger), encoding="utf-8")
            changed_store = copy.deepcopy(store)
            changed_store["ruleset_id"] = 1
            (directory / "store.json").write_text(json.dumps(changed_store), encoding="utf-8")
            with self.assertRaisesRegex(STORE.ControlStoreError, "admission/store identity"):
                STORE.validate_append_prefix(
                    directory, base_admission=admission, base_ledger=json.loads((directory / "ledger.json").read_text()), base_store=store
                )
            (directory / "store.json").write_text(json.dumps(store), encoding="utf-8")
            changed_admission = copy.deepcopy(admission)
            changed_admission["human_decision_required"] = not admission["human_decision_required"]
            (directory / "admission.json").write_text(json.dumps(changed_admission), encoding="utf-8")
            with self.assertRaisesRegex(STORE.ControlStoreError, "admission/store identity"):
                STORE.validate_append_prefix(
                    directory, base_admission=admission, base_ledger=json.loads((directory / "ledger.json").read_text()), base_store=store
                )

    def test_target_control_ref_fails_on_zero_match(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with mock.patch.dict("os.environ", {
                "GHOS_CONTROL_TARGET_REF": STORE.CONTROL_REF,
                "GHOS_CONTROL_BASE_SHA": "a" * 40,
            }, clear=False):
                with self.assertRaisesRegex(STORE.ControlStoreError, "deleted, renamed, or duplicated"):
                    STORE.validate(root=Path(temporary))


if __name__ == "__main__":
    unittest.main()
