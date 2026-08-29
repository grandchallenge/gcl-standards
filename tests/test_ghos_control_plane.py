from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ghos_control_plane", ROOT / "ci" / "ghos_control_plane.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class GhosControlPlaneAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = MODULE.load_json(MODULE.CATALOG_PATH)
        cls.admission = MODULE.load_json(MODULE.ADMISSION_PATH)
        cls.ledger = MODULE.load_json(MODULE.LEDGER_PATH)
        cls.projection = MODULE.load_json(ROOT / "status" / "GCL-GHOS-00-current.json")
        cls.authority = MODULE.resolve_effective_authority(projection=cls.projection)

    def reduced(self):
        return MODULE.reduce_ledger(
            self.ledger, self.catalog, self.authority, self.admission
        )

    def test_t01_cold_resume_is_byte_deterministic(self):
        first = self.reduced()
        second = self.reduced()
        self.assertEqual(MODULE.canonical_bytes(first), MODULE.canonical_bytes(second))
        self.assertEqual(first["selected_transition"], "RECONCILE_CURRENT_VERSION_PROJECTION")

    def test_t02_agent_replacement_does_not_change_transition(self):
        state = self.reduced()
        replacement = copy.deepcopy(state)
        replacement["roles"][1]["actor_id"] = "replacement-executor"
        MODULE.derive_permitted_transitions(replacement, self.catalog)
        self.assertEqual(state["permitted_transitions"], replacement["permitted_transitions"])

    def test_t03_stale_chat_loses_to_protected_authority(self):
        result = MODULE.resolve_effective_authority(
            projection=self.projection, conversational_version="0.1.1"
        )
        self.assertEqual(result["version"], "0.2.0")
        self.assertIn("STALE_CONVERSATIONAL_INSTRUCTION", {x["code"] for x in result["contradictions"]})

    def test_t04_cutoff_corrupting_any_ledger_boundary_fails_closed(self):
        corrupt = copy.deepcopy(self.ledger)
        corrupt["ledger_head_digest"] = "0" * 64
        with self.assertRaisesRegex(MODULE.LedgerError, "ledger head digest mismatch"):
            MODULE.validate_event_sequence(corrupt)

    def test_t05_interrupted_mutation_requires_probe_or_boundary(self):
        transaction = {
            "intended_effects": ["VALIDATION"],
            "replay_class": "REPLAY_AFTER_ABSENCE_PROBE",
        }
        controller = MODULE.TransactionController(self.catalog)
        self.assertEqual(controller.reconcile(transaction, []), "REPLAY_AFTER_ABSENCE_PROBE")
        self.assertEqual(controller.reconcile(transaction, ["partial"]), "RECONCILIATION_BOUNDARY")
        self.assertEqual(controller.reconcile(transaction, ["VALIDATION"]), "COMMIT_OBSERVED_SUCCESS")

    def test_t06_stale_review_is_invalidated_on_head_change(self):
        state = self.reduced()
        old = state["subjects"][0]["head_sha"]
        state["gates"] = [{
            "gate_id": "REVIEW-A", "kind": "REVIEW", "disposition": "SETTLED",
            "observed_status": "APPROVED", "subject": {"head_sha": old},
        }]
        MODULE._mutate_subject(state, {
            "repository": state["subjects"][0]["repository"],
            "identifier": state["subjects"][0]["identifier"],
            "old_head": old, "new_head": "f" * 40,
        })
        self.assertEqual(state["gates"][0]["disposition"], "INVALIDATED")

    def test_t07_projection_contradiction_names_the_authoritative_record(self):
        item = self.authority["contradictions"][0]
        self.assertEqual(item["authoritative_source"], "programme-adoption/MATH-PROGRAMME.yaml")
        self.assertEqual((item["observed_value"], item["authoritative_value"]), ("0.1.1", "0.2.0"))

    def test_t08_async_observation_must_name_recorded_wait(self):
        state = self.reduced()
        event = {"event_type": "EXTERNAL_WAIT_OBSERVED", "payload": {
            "wait_id": "UNKNOWN", "observation_id": "OBS-1", "status": "SUCCESS",
            "observed_at": "2026-08-28T12:00:00Z",
        }}
        with self.assertRaisesRegex(MODULE.LedgerError, "unknown wait"):
            MODULE._apply_event(state, event, self.admission)

    def test_t09_superseded_diagnostic_is_invalidated_with_subject(self):
        self.test_t06_stale_review_is_invalidated_on_head_change()

    def test_t10_unauthorized_transition_fails_closed(self):
        executor = MODULE.Executor("x", "s", "IMPLEMENTER", "BOUNDED_CONVERSATIONAL", ("durable_read",))
        with self.assertRaisesRegex(MODULE.TransitionRejected, "not reducer-permitted"):
            MODULE.TransactionController(self.catalog).authorize(
                self.reduced(), "EXECUTE_AUTHORIZED_INTEGRATION", executor
            )

    def test_t11_loss_of_summaries_changes_no_input_or_digest(self):
        state = self.reduced()
        self.assertNotIn("conversation", MODULE.canonical_bytes(state).decode("utf-8").lower())
        self.assertEqual(state["state_digest"], MODULE.state_digest(state))

    def test_t12_coordinator_death_leaves_reconstructible_role_graph(self):
        state = self.reduced()
        coordinator = next(x for x in state["roles"] if x["role"] == "HARNESS_COORDINATOR")
        self.assertEqual(coordinator["status"], "PENDING")
        self.assertEqual(self.reduced()["roles"], state["roles"])

    def test_t13_active_version_manifest_blocks_stale_consumers(self):
        manifest = MODULE.load_json(MODULE.PROPAGATION_PATH)
        MODULE.validate_propagation_manifest(manifest, self.authority)
        self.assertFalse(manifest["all_derived_current_coherent"])
        self.assertTrue(any(x["status"] == "STALE" for x in manifest["consumers"]))

    def test_t14_capability_topology_mismatch_requires_decomposition(self):
        candidate = copy.deepcopy(self.admission)
        candidate["work_graph"]["requires_autonomous_wake"] = True
        candidate["available_executor_classes"] = ["BOUNDED_CONVERSATIONAL"]
        result = MODULE.admit_work_package(candidate)
        self.assertEqual(result["topology"], "PERSISTENT_CONTROLLER_REQUIRED")
        self.assertEqual(result["disposition"], "DECOMPOSITION_REQUIRED")

    def test_candidate_artifacts_and_closed_schemas_validate(self):
        MODULE.validate()


if __name__ == "__main__":
    unittest.main()
