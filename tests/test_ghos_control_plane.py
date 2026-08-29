from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


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
        base_authority = MODULE.resolve_effective_authority(projection=cls.projection)
        cls.authority = MODULE.apply_propagation_barrier(
            base_authority, MODULE.load_json(MODULE.PROPAGATION_PATH)
        )

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
        state = self.reduced()
        old = state["subjects"][0]["head_sha"]
        state["gates"] = [{
            "gate_id": "DIAGNOSTIC-A", "kind": "CHECK", "required": True,
            "disposition": "SETTLED", "observed_status": "PASSED",
            "subject": {**state["subjects"][0]}, "evidence_id": "run-A",
            "observation_id": "job-A", "observed_at": "2026-08-28T12:00:00Z",
            "validity_rule": "EXACT_HEAD", "invalidation_triggers": ["CANDIDATE_HEAD_CHANGED"],
        }]
        MODULE._mutate_subject(state, {"repository": state["subjects"][0]["repository"],
            "identifier": state["subjects"][0]["identifier"], "old_head": old, "new_head": "e" * 40})
        self.assertEqual(state["gates"][0]["observed_status"], "STALE")

    def test_t10_unauthorized_transition_fails_closed(self):
        executor = MODULE.Executor("impostor", "other-session", "IMPLEMENTER", "BOUNDED_CONVERSATIONAL",
            ("durable_compare_and_swap", "git_write", "exact_git_readback"))
        with self.assertRaisesRegex(MODULE.TransitionRejected, "durable role assignment"):
            MODULE.TransactionController(self.catalog).authorize(
                self.reduced(), "RECONCILE_CURRENT_VERSION_PROJECTION", executor
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
        with patch.dict("os.environ", {"GHOS_MATH_PROGRAMME_REPO": str(ROOT)}, clear=True):
            with self.assertRaisesRegex(MODULE.AuthorityContradiction, "configuration is incomplete"):
                MODULE.validate_propagation_manifest(manifest, self.authority)
        configured_math = os.environ.get("GHOS_MATH_PROGRAMME_REPO")
        configured_profile = os.environ.get("GHOS_ORG_PROFILE_REPO")
        if configured_math and configured_profile:
            math_root, profile_root = configured_math, configured_profile
        else:
            workspace = next(
                candidate for candidate in ROOT.parents
                if (candidate / "MATH-PROGRAMME").exists() and (candidate / ".github").exists()
            )
            math_root, profile_root = str(workspace / "MATH-PROGRAMME"), str(workspace / ".github")
        with patch.dict("os.environ", {
            "GHOS_MATH_PROGRAMME_REPO": math_root,
            "GHOS_ORG_PROFILE_REPO": profile_root,
        }, clear=False):
            MODULE.validate_propagation_manifest(manifest, self.authority)
        self.assertFalse(manifest["all_derived_current_coherent"])
        self.assertTrue(any(x["status"] == "STALE" for x in manifest["consumers"]))
        codes = {x["code"] for x in self.authority["contradictions"]}
        self.assertIn("ACTIVE_VERSION_PROPAGATION_INCOMPLETE", codes)
        after_local_repair = copy.deepcopy(self.authority)
        after_local_repair["contradictions"] = [
            item for item in after_local_repair["contradictions"]
            if item["code"] != "STALE_CURRENT_PROJECTION"
        ]
        state = self.reduced()
        state["authority"] = after_local_repair
        state["domain_phase"] = "INTEGRATION"
        state["lifecycle_state"] = "READY"
        permitted, selected, _ = MODULE.derive_permitted_transitions(state, self.catalog)
        self.assertNotIn("EXECUTE_AUTHORIZED_INTEGRATION", permitted)
        self.assertEqual(selected, "RECONCILE_ACTIVE_VERSION_PROPAGATION")
        false_coherent = copy.deepcopy(manifest)
        for consumer in false_coherent["consumers"]:
            if consumer["authority_class"] == "DERIVED_CURRENT":
                consumer["observed_version"] = "0.2.0"
                consumer["status"] = "COHERENT"
        false_coherent["all_derived_current_coherent"] = True
        false_coherent["external_reconciliation_complete"] = True
        with self.assertRaisesRegex(MODULE.AuthorityContradiction, "not derived from exact content"):
            MODULE.validate_propagation_manifest(false_coherent, self.authority)
        substituted = copy.deepcopy(manifest)
        target = next(x for x in substituted["consumers"] if x["consumer_id"] == "GCL_README")
        target["exact_source"] = copy.deepcopy(substituted["adoption_source"])
        target["observed_version"] = "0.2.0"
        target["status"] = "COHERENT"
        with self.assertRaisesRegex(MODULE.AuthorityContradiction, "exact-source substitution"):
            MODULE.validate_propagation_manifest(substituted, self.authority)
        observed, status = MODULE.derive_text_consumer_status(
            "GCL_README",
            "Version `0.3.0` is current authority. Version `0.2.0` is historical.\n",
            "0.2.0",
        )
        self.assertEqual((observed, status), ("0.3.0", "STALE"))
        observed, status = MODULE.derive_text_consumer_status(
            "MATH_PROGRAMME_RECOVERY_GUIDE",
            "This document mentions 0.2.0 but makes no typed current-authority assertion.\n",
            "0.2.0",
        )
        self.assertEqual((observed, status), (None, "STALE"))
        for text in (
            "Version `0.2.0` is current authority. Version `0.3.0` is current authority.\n",
            "Version `0.3.0` is current authority. Version `0.2.0` is current authority.\n",
        ):
            self.assertEqual(
                MODULE.derive_text_consumer_status("GCL_README", text, "0.2.0"),
                (None, "STALE"),
            )
        for text in (
            "`GCL-GHOS-00` 0.2.0 is current authority. `GCL-GHOS-00` 0.3.0 is current authority.\n",
            "`GCL-GHOS-00` 0.3.0 is current authority. `GCL-GHOS-00` 0.2.0 is current authority.\n",
        ):
            self.assertEqual(
                MODULE.derive_text_consumer_status("MATH_PROGRAMME_RECOVERY_GUIDE", text, "0.2.0"),
                (None, "STALE"),
            )
        self.assertEqual(
            MODULE.derive_text_consumer_status(
                "GCL_STANDARD_FRONT_MATTER",
                "**Version:** 0.2.0\n**Version:** 0.3.0\n**Status:** Admitted\n",
                "0.2.0",
            ),
            (None, "STALE"),
        )
        self.assertEqual(
            MODULE.derive_text_consumer_status(
                "ORGANIZATION_PUBLIC_PROFILE",
                "`GCL-GHOS-00` `0.2.0` is the admitted version selected\n"
                "`GCL-GHOS-00` `0.3.0` is the admitted version selected\n",
                "0.2.0",
            ),
            (None, "STALE"),
        )

    def test_t14_capability_topology_mismatch_requires_decomposition(self):
        candidate = copy.deepcopy(self.admission)
        candidate["work_graph"]["bounded_transition_count"] = 999
        candidate["work_graph"]["has_external_wait"] = True
        candidate["available_executor_classes"] = ["BOUNDED_CONVERSATIONAL"]
        result = MODULE.admit_work_package(candidate)
        self.assertEqual(result["topology"], "MULTI_SESSION_RESUMABLE")
        self.assertEqual(result["disposition"], "DECOMPOSITION_REQUIRED")

    def test_ledger_cannot_close_without_catalog_permitted_terminal_transition(self):
        state = self.reduced()
        event = {"event_type": "WORK_PACKAGE_CLOSED", "payload": {
            "terminal_transition": "CLOSE_WORK_PACKAGE", "terminal_evidence": ["forged"]}}
        with self.assertRaisesRegex(MODULE.LedgerError, "closure is not reducer-permitted"):
            MODULE._apply_event(state, event, self.admission, self.catalog)

    def test_ledger_cannot_prepare_unknown_transition(self):
        state = self.reduced()
        assignment = next(x for x in state["roles"] if x["role"] == "IMPLEMENTER")
        executor = MODULE.Executor(assignment["actor_id"], assignment["session_id"], "IMPLEMENTER",
            "MULTI_SESSION_WORKER", ("durable_compare_and_swap", "git_write", "exact_git_readback"))
        transaction = MODULE.TransactionController(self.catalog).prepare(state,
            "RECONCILE_CURRENT_VERSION_PROJECTION", executor, transaction_id="TX-1",
            idempotency_key="KEY-1", expires_at="2026-08-28T13:00:00Z", now="2026-08-28T12:00:00Z")
        transaction["transition_id"] = "MADE_UP"
        event = {"event_type": "TRANSACTION_PREPARED", "payload": {"transaction": transaction}}
        with self.assertRaisesRegex(MODULE.TransitionRejected, "unknown or duplicate"):
            MODULE._apply_event(state, event, self.admission, self.catalog)

    def test_forged_settled_gate_cannot_enter_state(self):
        state = self.reduced()
        gate = {"gate_id": "FORGED", "kind": "REVIEW", "required": True,
            "subject": {**state["subjects"][0], "head_sha": "d" * 40}, "evidence_id": "claim",
            "observed_status": "APPROVED", "observation_id": "claim", "observed_at": "2026-08-28T12:00:00Z",
            "validity_rule": "EXACT_HEAD", "invalidation_triggers": [], "disposition": "SETTLED"}
        with self.assertRaisesRegex(MODULE.LedgerError, "local digest-addressed"):
            MODULE._upsert_gate(state, gate)

    def test_direct_subject_mutation_event_is_rejected(self):
        state = self.reduced()
        subject = state["subjects"][0]
        event = {"event_type": "SUBJECT_MUTATED", "payload": {
            "repository": subject["repository"], "identifier": subject["identifier"],
            "old_head": subject["head_sha"], "new_head": "f" * 40}}
        with self.assertRaisesRegex(MODULE.LedgerError, "committed transaction effect"):
            MODULE._apply_event(state, event, self.admission, self.catalog)

    def test_expired_executor_claim_cannot_prepare_transaction(self):
        state = self.reduced()
        assignment = next(x for x in state["roles"] if x["role"] == "IMPLEMENTER")
        executor = MODULE.Executor(assignment["actor_id"], assignment["session_id"], "IMPLEMENTER",
            "MULTI_SESSION_WORKER", ("durable_compare_and_swap", "git_write", "exact_git_readback"))
        transaction = MODULE.TransactionController(self.catalog).prepare(state,
            "RECONCILE_CURRENT_VERSION_PROJECTION", executor, transaction_id="TX-EXPIRED",
            idempotency_key="KEY-EXPIRED", expires_at="2026-08-28T12:01:00Z", now="2026-08-28T12:00:00Z")
        event = {"event_type": "TRANSACTION_PREPARED", "occurred_at": "2026-08-29T12:00:00Z",
            "payload": {"transaction": transaction}}
        with self.assertRaisesRegex(MODULE.LedgerError, "inactive or expired"):
            MODULE._apply_event(state, event, self.admission, self.catalog)

    def test_transaction_cutoff_states_are_unambiguous(self):
        state = self.reduced()
        assignment = next(x for x in state["roles"] if x["role"] == "IMPLEMENTER")
        executor = MODULE.Executor(assignment["actor_id"], assignment["session_id"], "IMPLEMENTER",
            "MULTI_SESSION_WORKER", ("durable_compare_and_swap", "git_write", "exact_git_readback"))
        transaction = MODULE.TransactionController(self.catalog).prepare(state,
            "RECONCILE_CURRENT_VERSION_PROJECTION", executor, transaction_id="TX-CUTOFF",
            idempotency_key="KEY-CUTOFF", expires_at="2026-08-28T13:00:00Z", now="2026-08-28T12:00:00Z")
        MODULE._apply_event(state, {"event_type": "TRANSACTION_PREPARED", "occurred_at": "2026-08-28T12:00:01Z",
            "payload": {"transaction": transaction}}, self.admission, self.catalog)
        self.assertEqual(state["open_transaction"]["state"], "PREPARED")
        MODULE._apply_event(state, {"event_type": "TRANSACTION_APPLYING", "occurred_at": "2026-08-28T12:00:02Z",
            "payload": {"transaction_id": "TX-CUTOFF", "attempt_id": "ATTEMPT-1"}}, self.admission, self.catalog)
        self.assertEqual(state["open_transaction"]["state"], "APPLYING")
        MODULE._apply_event(state, {"event_type": "TRANSACTION_RECONCILING", "occurred_at": "2026-08-28T12:00:03Z",
            "payload": {"transaction_id": "TX-CUTOFF", "observed_side_effects": ["partial"]}}, self.admission, self.catalog)
        self.assertEqual(state["open_transaction"]["state"], "RECONCILING")

    def test_missing_reviewers_do_not_settle_role_separation(self):
        state = self.reduced()
        self.assertNotIn("ROLE_SEPARATION", MODULE._gate_kinds_settled(state))

    def test_stale_external_result_cannot_complete_another_wait(self):
        state = self.reduced()
        subject = state["subjects"][0]
        wait = {"wait_id": "WAIT-B", "provider": "github", "repository": subject["repository"],
            "object_kind": "WORKFLOW_RUN", "object_id": "RUN-B", "subject_head": subject["head_sha"],
            "expected_terminal_observations": ["SUCCESS"], "wake_condition": "terminal",
            "latest_observation_id": None, "latest_status": "PENDING", "observed_at": None,
            "poll_policy": "EXTERNAL_WAKE", "next_eligible_observation_at": "2026-08-28T12:00:00Z",
            "backoff_attempt": 0, "deadline": None, "controller_class": "ANY_REPLACEMENT_EXECUTOR",
            "wake_mechanism": "provider event", "outcome_transitions": {"SUCCESS": "REQUEST_EXACT_HEAD_REVIEW"}}
        MODULE._apply_event(state, {"event_type": "EXTERNAL_WAIT_OPENED", "payload": {"wait": wait}},
            self.admission, self.catalog)
        stale = {"event_type": "EXTERNAL_WAIT_OBSERVED", "payload": {"wait_id": "WAIT-B",
            "object_id": "RUN-A", "subject_head": subject["head_sha"], "observation_id": "OLD-RUN-A",
            "status": "SUCCESS", "observed_at": "2026-08-28T12:01:00Z"}}
        with self.assertRaisesRegex(MODULE.LedgerError, "another object"):
            MODULE._apply_event(state, stale, self.admission, self.catalog)

    def test_role_cannot_complete_without_matching_dispatch_and_record(self):
        state = self.reduced()
        event = {"event_type": "ROLE_RESULT_RECORDED", "payload": {"role": "ADVERSARY",
            "actor_id": "invented", "session_id": "invented", "result_path": "missing.json",
            "result_digest": "0" * 64}}
        with self.assertRaisesRegex(MODULE.LedgerError, "dispatched assignment"):
            MODULE._apply_event(state, event, self.admission, self.catalog)

    def test_transaction_state_cannot_regress_or_commit_from_prepared(self):
        state = self.reduced()
        assignment = next(x for x in state["roles"] if x["role"] == "IMPLEMENTER")
        executor = MODULE.Executor(assignment["actor_id"], assignment["session_id"], "IMPLEMENTER",
            "MULTI_SESSION_WORKER", ("durable_compare_and_swap", "git_write", "exact_git_readback"))
        transaction = MODULE.TransactionController(self.catalog).prepare(state,
            "RECONCILE_CURRENT_VERSION_PROJECTION", executor, transaction_id="TX-ORDER",
            idempotency_key="KEY-ORDER", expires_at="2026-08-28T13:00:00Z", now="2026-08-28T12:00:00Z")
        MODULE._apply_event(state, {"event_type": "TRANSACTION_PREPARED", "occurred_at": "2026-08-28T12:00:01Z",
            "payload": {"transaction": transaction}}, self.admission, self.catalog)
        with self.assertRaisesRegex(MODULE.LedgerError, "cannot commit before"):
            MODULE._apply_event(state, {"event_type": "TRANSACTION_COMMITTED", "occurred_at": "2026-08-28T12:00:02Z", "payload": {
                "transaction_id": "TX-ORDER", "evidence": ["self"],
                "effects": [{"kind": "PHASE_CHANGED", "phase": "VALIDATION"}]}}, self.admission, self.catalog)
        MODULE._apply_event(state, {"event_type": "TRANSACTION_RECONCILING", "occurred_at": "2026-08-28T12:00:02Z", "payload": {
            "transaction_id": "TX-ORDER", "observed_side_effects": []}}, self.admission, self.catalog)
        with self.assertRaisesRegex(MODULE.LedgerError, "only from PREPARED"):
            MODULE._apply_event(state, {"event_type": "TRANSACTION_APPLYING", "occurred_at": "2026-08-28T12:00:03Z", "payload": {
                "transaction_id": "TX-ORDER", "attempt_id": "LATE"}}, self.admission, self.catalog)

    def test_observation_time_is_compared_as_an_instant(self):
        self.assertEqual(MODULE.instant("2026-08-28T12:00:00Z"), MODULE.instant("2026-08-28T05:00:00-07:00"))

    def test_expired_lease_rejects_later_transaction_events(self):
        state = self.reduced()
        assignment = next(x for x in state["roles"] if x["role"] == "IMPLEMENTER")
        executor = MODULE.Executor(assignment["actor_id"], assignment["session_id"], "IMPLEMENTER",
            "MULTI_SESSION_WORKER", ("durable_compare_and_swap", "git_write", "exact_git_readback"))
        transaction = MODULE.TransactionController(self.catalog).prepare(state,
            "RECONCILE_CURRENT_VERSION_PROJECTION", executor, transaction_id="TX-LEASE",
            idempotency_key="KEY-LEASE", expires_at="2026-08-28T12:01:00Z", now="2026-08-28T12:00:00Z")
        MODULE._apply_event(state, {"event_type": "TRANSACTION_PREPARED", "occurred_at": "2026-08-28T12:00:01Z",
            "payload": {"transaction": transaction}}, self.admission, self.catalog)
        with self.assertRaisesRegex(MODULE.LedgerError, "outside the active executor lease"):
            MODULE._apply_event(state, {"event_type": "TRANSACTION_APPLYING", "occurred_at": "2026-08-29T12:00:00Z",
                "payload": {"transaction_id": "TX-LEASE", "attempt_id": "TOO-LATE"}}, self.admission, self.catalog)

    def test_unrelated_repository_file_is_not_commit_evidence(self):
        import hashlib
        state = self.reduced()
        assignment = next(x for x in state["roles"] if x["role"] == "IMPLEMENTER")
        executor = MODULE.Executor(assignment["actor_id"], assignment["session_id"], "IMPLEMENTER",
            "MULTI_SESSION_WORKER", ("durable_compare_and_swap", "git_write", "exact_git_readback"))
        transaction = MODULE.TransactionController(self.catalog).prepare(state,
            "RECONCILE_CURRENT_VERSION_PROJECTION", executor, transaction_id="TX-EVIDENCE",
            idempotency_key="KEY-EVIDENCE", expires_at="2026-08-28T13:00:00Z", now="2026-08-28T12:00:00Z")
        MODULE._apply_event(state, {"event_type": "TRANSACTION_PREPARED", "occurred_at": "2026-08-28T12:00:01Z",
            "payload": {"transaction": transaction}}, self.admission, self.catalog)
        MODULE._apply_event(state, {"event_type": "TRANSACTION_APPLYING", "occurred_at": "2026-08-28T12:00:02Z",
            "payload": {"transaction_id": "TX-EVIDENCE", "attempt_id": "ATTEMPT"}}, self.admission, self.catalog)
        path = ROOT / "schemas" / "ghos_control_plane.schema.json"
        ref = f"file:schemas/ghos_control_plane.schema.json#sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"
        with self.assertRaisesRegex(MODULE.LedgerError, "exact outcome"):
            MODULE._apply_event(state, {"event_type": "TRANSACTION_COMMITTED", "occurred_at": "2026-08-28T12:00:03Z",
                "payload": {"transaction_id": "TX-EVIDENCE", "evidence": [ref],
                "effects": [{"kind": "PHASE_CHANGED", "phase": "VALIDATION"}]}}, self.admission, self.catalog)

    def test_cold_replacement_can_take_over_expired_transaction_and_abort(self):
        state = self.reduced()
        implementer = next(x for x in state["roles"] if x["role"] == "IMPLEMENTER")
        executor = MODULE.Executor(implementer["actor_id"], implementer["session_id"], "IMPLEMENTER",
            "MULTI_SESSION_WORKER", ("durable_compare_and_swap", "git_write", "exact_git_readback"))
        transaction = MODULE.TransactionController(self.catalog).prepare(state,
            "RECONCILE_CURRENT_VERSION_PROJECTION", executor, transaction_id="TX-TAKEOVER",
            idempotency_key="KEY-TAKEOVER", expires_at="2026-08-28T12:01:00Z", now="2026-08-28T12:00:00Z")
        MODULE._apply_event(state, {"event_type": "TRANSACTION_PREPARED", "occurred_at": "2026-08-28T12:00:01Z",
            "payload": {"transaction": transaction}}, self.admission, self.catalog)
        MODULE._apply_event(state, {"event_type": "ROLE_DISPATCHED", "occurred_at": "2026-08-28T12:02:00Z",
            "payload": {"role": "HARNESS_COORDINATOR", "actor_id": "replacement", "session_id": "fresh-session"}},
            self.admission, self.catalog)
        replacement = {"executor_id": "replacement", "session_id": "fresh-session",
            "role": "HARNESS_COORDINATOR", "executor_class": "MULTI_SESSION_WORKER",
            "capabilities": ["durable_compare_and_swap", "authoritative_effect_probe"],
            "acquired_at": "2026-08-28T12:02:00Z", "expires_at": "2026-08-28T13:02:00Z", "status": "ACTIVE"}
        with self.assertRaisesRegex(MODULE.LedgerError, "exact expired prior claim"):
            MODULE._apply_event(state, {"event_type": "TRANSACTION_CLAIM_REPLACED", "occurred_at": "2026-08-28T12:02:01Z",
                "payload": {"transaction_id": "TX-TAKEOVER", "prior_claim_digest": "0" * 64,
                    "executor_claim": replacement}}, self.admission, self.catalog)
        MODULE._apply_event(state, {"event_type": "TRANSACTION_CLAIM_REPLACED", "occurred_at": "2026-08-28T12:02:01Z",
            "payload": {"transaction_id": "TX-TAKEOVER", "prior_claim_digest": MODULE.digest(transaction["executor_claim"]),
                "executor_claim": replacement}}, self.admission, self.catalog)
        self.assertEqual(state["open_transaction"]["state"], "RECONCILING")
        commit_effects = [{"kind": "PHASE_CHANGED", "phase": "VALIDATION"}]
        commit_evidence = {"record_type": "TRANSACTION_OUTCOME_EVIDENCE", "transaction_id": "TX-TAKEOVER",
            "transition_id": transaction["transition_id"], "subjects": transaction["subjects"],
            "effect_probes": transaction["effect_probes"], "observed_outcome": "COMMITTED", "effects": commit_effects}
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", dir=ROOT, delete=False) as handle:
            json.dump(commit_evidence, handle, sort_keys=True, separators=(",", ":"))
            commit_path = Path(handle.name)
        try:
            import hashlib
            commit_ref = f"file:{commit_path.relative_to(ROOT).as_posix()}#sha256:{hashlib.sha256(commit_path.read_bytes()).hexdigest()}"
            with self.assertRaisesRegex(MODULE.LedgerError, "cannot commit the original transition"):
                MODULE._apply_event(state, {"event_type": "TRANSACTION_COMMITTED", "occurred_at": "2026-08-28T12:02:02Z",
                    "payload": {"transaction_id": "TX-TAKEOVER", "evidence": [commit_ref], "effects": commit_effects}},
                    self.admission, self.catalog)
        finally:
            commit_path.unlink(missing_ok=True)
        evidence = {"record_type": "TRANSACTION_OUTCOME_EVIDENCE", "transaction_id": "TX-TAKEOVER",
            "transition_id": transaction["transition_id"], "subjects": transaction["subjects"],
            "effect_probes": transaction["effect_probes"], "observed_outcome": "ABORTED", "effects": []}
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", dir=ROOT, delete=False) as handle:
            json.dump(evidence, handle, sort_keys=True, separators=(",", ":"))
            evidence_path = Path(handle.name)
        try:
            import hashlib
            ref = f"file:{evidence_path.relative_to(ROOT).as_posix()}#sha256:{hashlib.sha256(evidence_path.read_bytes()).hexdigest()}"
            MODULE._apply_event(state, {"event_type": "TRANSACTION_ABORTED", "occurred_at": "2026-08-28T12:02:03Z",
                "payload": {"transaction_id": "TX-TAKEOVER", "evidence": [ref]}}, self.admission, self.catalog)
        finally:
            evidence_path.unlink(missing_ok=True)
        self.assertIsNone(state["open_transaction"])
        self.assertEqual(state["lifecycle_state"], "READY")

    def test_candidate_artifacts_and_closed_schemas_validate(self):
        MODULE.validate()


if __name__ == "__main__":
    unittest.main()
