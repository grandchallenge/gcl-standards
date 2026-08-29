from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "ghos_control_plane.schema.json"
DEFECT_SCHEMA_PATH = ROOT / "schemas" / "ghos_defect_ledger.schema.json"
PACKET = ROOT / "implementation" / "GCL-GHOS-CONTROL-PLANE-REMEDIATION-001"
CONTROL_DIR = PACKET / "control-plane"
CATALOG_PATH = CONTROL_DIR / "transition-catalog.json"
ADMISSION_PATH = CONTROL_DIR / "candidate-work-package-admission.json"
LEDGER_PATH = CONTROL_DIR / "candidate-harness-ledger.json"
STATE_PATH = CONTROL_DIR / "candidate-harness-state.json"
PROPAGATION_PATH = CONTROL_DIR / "active-version-propagation-manifest.json"

CLAIM_BOUNDARIES = {
    "constitutional": False,
    "merge": False,
    "certification": False,
    "production": False,
    "publication": False,
    "mathematical_claim": False,
    "claim_promotion": False,
    "commercial": False,
}
AUTHORITY_EXPANDING_EFFECTS = {"MERGE", "PROTECTED_MUTATION", "AUTHORIZATION_RECORD"}
OPEN_TRANSACTION_STATES = {"PREPARED", "APPLYING", "RECONCILING"}
SETTLED_GATE_STATUSES = {"PASSED", "APPROVED", "AUTHORIZED"}
EVENT_PAYLOAD_KEYS = {
    "WORK_PACKAGE_ADMITTED": {"admission_path", "admission_digest"},
    "ROLE_DISPATCHED": {"role", "actor_id", "session_id"},
    "ROLE_RESULT_RECORDED": {"role", "actor_id", "session_id", "result_path", "result_digest"},
    "GATE_OBSERVED": {"gate"},
    "EXTERNAL_WAIT_OPENED": {"wait"},
    "EXTERNAL_WAIT_OBSERVED": {"wait_id", "object_id", "subject_head", "observation_id", "status", "observed_at"},
    "TRANSACTION_PREPARED": {"transaction"},
    "TRANSACTION_APPLYING": {"transaction_id", "attempt_id"},
    "TRANSACTION_RECONCILING": {"transaction_id", "observed_side_effects"},
    "TRANSACTION_COMMITTED": {"transaction_id", "evidence", "effects"},
    "TRANSACTION_ABORTED": {"transaction_id", "evidence"},
    "SUBJECT_MUTATED": {"repository", "identifier", "old_head", "new_head"},
    "BOUNDARY_DECLARED": {"category", "evidence", "needed"},
    "WORK_PACKAGE_CLOSED": {"terminal_transition", "terminal_evidence"},
}


class ControlPlaneError(ValueError):
    pass


class AuthorityContradiction(ControlPlaneError):
    pass


class LedgerError(ControlPlaneError):
    pass


class TransitionRejected(ControlPlaneError):
    pass


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ControlPlaneError("timestamp must include an offset")
    return parsed.astimezone(timezone.utc)


def verified_local_file(relative_path: str, expected_sha256: str) -> bytes:
    candidate = (ROOT / relative_path).resolve()
    if ROOT.resolve() not in candidate.parents or not candidate.is_file():
        raise LedgerError("digest-addressed record is unavailable")
    contents = candidate.read_bytes()
    if hashlib.sha256(contents).hexdigest() != expected_sha256:
        raise LedgerError("digest-addressed record content mismatch")
    return contents


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ControlPlaneError(f"record must be an object: {path}")
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ControlPlaneError(f"record must be an object: {path}")
    return value


def validate_schema_instance(instance: Mapping[str, Any], *, root: Path = ROOT) -> None:
    schema = load_json(root / "schemas" / "ghos_control_plane.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        instance,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )


def source(
    repository: str,
    path: str,
    commit_sha: str,
    authority_class: str,
    git_blob_sha1: str | None = None,
) -> dict[str, Any]:
    result = {
        "repository": repository,
        "path": path,
        "commit_sha": commit_sha,
        "authority_class": authority_class,
    }
    if git_blob_sha1 is not None:
        result["git_blob_sha1"] = git_blob_sha1
    return result


def resolve_effective_authority(
    *,
    root: Path = ROOT,
    projection: Mapping[str, Any] | None = None,
    conversational_version: str | None = None,
) -> dict[str, Any]:
    adoption_path = root / "programme-adoption" / "MATH-PROGRAMME.yaml"
    adoption = load_yaml(adoption_path)
    if adoption.get("programme") != "grandchallenge/MATH-PROGRAMME":
        raise AuthorityContradiction("programme adoption repository identity drift")
    if adoption.get("standard") != "GCL-GHOS-00" or adoption.get("status") != "active":
        raise AuthorityContradiction("one active GCL-GHOS-00 adoption is required")

    version = adoption.get("standard_version")
    admission_ref = adoption.get("standard_admission")
    if not isinstance(version, str) or not isinstance(admission_ref, dict):
        raise AuthorityContradiction("active adoption lacks exact admission linkage")
    admission_relative = admission_ref.get("path")
    if not isinstance(admission_relative, str):
        raise AuthorityContradiction("active adoption lacks admission path")
    admission_path = root / admission_relative
    admission = load_json(admission_path)
    admitted_standard = admission.get("standard")
    if not isinstance(admitted_standard, dict):
        raise AuthorityContradiction("admission standard record is missing")
    if (
        admission.get("status") != "admitted"
        or admitted_standard.get("identifier") != "GCL-GHOS-00"
        or admitted_standard.get("version") != version
    ):
        raise AuthorityContradiction("adoption does not select its exact admitted record")
    admission_commit = admission_ref.get("commit_sha")
    if (
        admission_commit != adoption.get("standards_commit")
        or admission_commit != "87307a0c1fe5ff19b34bb08451e7d6281a7d5dea"
    ):
        raise AuthorityContradiction("0.2.0 exact admitted commit linkage drift")
    if admission_ref.get("operation_id") != admission.get("operation_id"):
        raise AuthorityContradiction("adoption operation does not match admission")

    adoption_source = source(
        "grandchallenge/gcl-standards",
        "programme-adoption/MATH-PROGRAMME.yaml",
        "1a5e9cb24257be578b091ecd2c99d4119ff73b2c",
        "PROGRAMME_ADOPTION",
    )
    admission_source = source(
        "grandchallenge/gcl-standards",
        admission_relative,
        admission_commit,
        "ADMITTED_STANDARD",
        admission_ref.get("admission_record_git_blob_sha1"),
    )
    contradictions: list[dict[str, str]] = []
    if projection is not None:
        projected = projection.get("selected_admission", {})
        projected_version = (
            projected.get("version") if isinstance(projected, Mapping) else None
        )
        if projected_version != version:
            contradictions.append(
                {
                    "code": "STALE_CURRENT_PROJECTION",
                    "authoritative_source": "programme-adoption/MATH-PROGRAMME.yaml",
                    "stale_source": "status/GCL-GHOS-00-current.json",
                    "authoritative_value": version,
                    "observed_value": str(projected_version),
                }
            )
    if conversational_version is not None and conversational_version != version:
        contradictions.append(
            {
                "code": "STALE_CONVERSATIONAL_INSTRUCTION",
                "authoritative_source": "programme-adoption/MATH-PROGRAMME.yaml",
                "stale_source": "conversation",
                "authoritative_value": version,
                "observed_value": conversational_version,
            }
        )
    return {
        "programme": "grandchallenge/MATH-PROGRAMME",
        "standard": "GCL-GHOS-00",
        "version": version,
        "adoption": adoption_source,
        "admission": admission_source,
        "precedence_trace": [
            source(
                "grandchallenge/INTELLECT",
                "CONSTITUTION.md",
                adoption["constitutional_source"]["amendment_commit"],
                "CONSTITUTIONAL",
            ),
            admission_source,
            adoption_source,
        ],
        "contradictions": contradictions,
    }


def classify_topology(work_graph: Mapping[str, Any]) -> str:
    if (
        work_graph.get("requires_uninterrupted_monitoring")
        or work_graph.get("requires_autonomous_wake")
        or work_graph.get("mutation_reconcilable") is False
    ):
        return "PERSISTENT_CONTROLLER_REQUIRED"
    if work_graph.get("bounded_transition_count", 1) > 1 or work_graph.get(
        "has_external_wait"
    ):
        return "MULTI_SESSION_RESUMABLE"
    return "BOUNDED_ATOMIC"


def admit_work_package(candidate: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(candidate))
    topology = classify_topology(result["work_graph"])
    result["topology"] = topology
    executor_classes = set(result["available_executor_classes"])
    compatible = {
        "BOUNDED_ATOMIC": {"BOUNDED_CONVERSATIONAL", "MULTI_SESSION_WORKER", "PERSISTENT_CONTROLLER", "HUMAN"},
        "MULTI_SESSION_RESUMABLE": {"MULTI_SESSION_WORKER", "PERSISTENT_CONTROLLER"},
        "PERSISTENT_CONTROLLER_REQUIRED": {"PERSISTENT_CONTROLLER"},
    }[topology]
    if not executor_classes.intersection(compatible):
        result["disposition"] = "DECOMPOSITION_REQUIRED"
        result["required_decomposition"] = (
            "Decompose into durable bounded transitions or assign a persistent controller."
        )
    else:
        result["disposition"] = "ADMITTED"
        result["required_decomposition"] = None
    validate_role_separation(result.get("roles", []), result.get("separation_constraints", []))
    if result.get("claim_boundaries") != CLAIM_BOUNDARIES:
        raise ControlPlaneError("work-package admission widens authority")
    return result


def validate_role_separation(
    roles: Iterable[Mapping[str, Any]], constraints: Iterable[str]
) -> None:
    by_role = {role["role"]: role for role in roles}
    for constraint in constraints:
        left, separator, right = constraint.partition("!=")
        if not separator:
            raise ControlPlaneError(f"invalid separation constraint: {constraint}")
        first = by_role.get(left)
        second = by_role.get(right)
        if not first or not second:
            continue
        if first.get("actor_id") and first.get("actor_id") == second.get("actor_id"):
            raise ControlPlaneError(f"role actor separation violated: {constraint}")
        if first.get("session_id") and first.get("session_id") == second.get("session_id"):
            raise ControlPlaneError(f"role session separation violated: {constraint}")


def event_digest(event: Mapping[str, Any]) -> str:
    body = {key: value for key, value in event.items() if key != "event_digest"}
    return digest(body)


def validate_event_payload(event: Mapping[str, Any]) -> None:
    event_type = event["event_type"]
    payload = event["payload"]
    required = EVENT_PAYLOAD_KEYS[event_type]
    if set(payload) != required:
        raise LedgerError(
            f"closed event payload mismatch for {event_type}: expected={sorted(required)} actual={sorted(payload)}"
        )


def validate_event_sequence(ledger: Mapping[str, Any]) -> str:
    previous: str | None = None
    seen_ids: set[str] = set()
    for expected_sequence, event in enumerate(ledger["events"], start=1):
        if event["sequence"] != expected_sequence:
            raise LedgerError("event sequence is not contiguous")
        if event["event_id"] in seen_ids:
            raise LedgerError("duplicate event identity")
        if event["previous_event_digest"] != previous:
            raise LedgerError("event hash link mismatch")
        validate_event_payload(event)
        computed = event_digest(event)
        if event["event_digest"] != computed:
            raise LedgerError("event digest mismatch")
        previous = computed
        seen_ids.add(event["event_id"])
    if ledger["ledger_head_digest"] != previous:
        raise LedgerError("ledger head digest mismatch")
    return previous or digest([])


def append_event(
    ledger: Mapping[str, Any], event_type: str, event_id: str, occurred_at: str, payload: Mapping[str, Any]
) -> dict[str, Any]:
    updated = copy.deepcopy(dict(ledger))
    validate_event_sequence(updated)
    event = {
        "sequence": len(updated["events"]) + 1,
        "event_id": event_id,
        "event_type": event_type,
        "occurred_at": occurred_at,
        "previous_event_digest": updated["ledger_head_digest"],
        "payload": copy.deepcopy(dict(payload)),
    }
    validate_event_payload(event)
    event["event_digest"] = event_digest(event)
    updated["events"].append(event)
    updated["ledger_head_digest"] = event["event_digest"]
    return updated


def catalog_digest(catalog: Mapping[str, Any]) -> str:
    return digest(catalog)


def _initial_state(
    work_package: str, authority: Mapping[str, Any], catalog_hash: str
) -> dict[str, Any]:
    return {
        "$schema": "../../../schemas/ghos_control_plane.schema.json",
        "record_type": "DERIVED_STATE",
        "schema_version": "1.0.0",
        "work_package": work_package,
        "generation": 0,
        "lifecycle_state": "UNADMITTED",
        "domain_phase": "ADMISSION",
        "authority": copy.deepcopy(dict(authority)),
        "subjects": [],
        "roles": [],
        "gates": [],
        "external_waits": [],
        "open_transaction": None,
        "permitted_transitions": [],
        "selected_transition": None,
        "selection_rule": "LOWEST_PRIORITY_THEN_LEXICAL",
        "stopping_boundary": None,
        "blocking_conditions": [],
        "invalidated_gate_ids": [],
        "catalog_digest": catalog_hash,
        "ledger_head_digest": "0" * 64,
        "state_digest": "0" * 64,
        "claim_boundaries": copy.deepcopy(CLAIM_BOUNDARIES),
    }


def _replace_role(state: dict[str, Any], payload: Mapping[str, Any], status: str) -> None:
    for role in state["roles"]:
        if role["role"] == payload["role"]:
            role["actor_id"] = payload["actor_id"]
            role["session_id"] = payload["session_id"]
            role["status"] = status
            if "result_digest" in payload:
                role["result_digest"] = payload["result_digest"]
            return
    raise LedgerError(f"unknown role: {payload['role']}")


def _upsert_gate(state: dict[str, Any], gate: Mapping[str, Any]) -> None:
    if gate["kind"] in {"ROLE_SEPARATION", "CAPABILITY", "AUTHORITY_COHERENCE"}:
        raise LedgerError("derived gate kind cannot be asserted by an observation event")
    if gate["disposition"] == "SETTLED":
        if not gate["evidence_id"] or not gate["observation_id"] or not gate["observed_at"]:
            raise LedgerError("settled gate requires exact evidence and observation identity")
        if gate["observed_status"] not in SETTLED_GATE_STATUSES:
            raise LedgerError("settled gate has non-settled observation")
        expected_status = {
            "CHECK": "PASSED",
            "REVIEW": "APPROVED",
            "HUMAN_AUTHORIZATION": "AUTHORIZED",
            "PROTECTED_READBACK": "PASSED",
        }.get(gate["kind"])
        if gate["observed_status"] != expected_status:
            raise LedgerError("gate kind and settled status are incompatible")
        match = re.fullmatch(r"file:([^#]+)#sha256:([0-9a-f]{64})", gate["evidence_id"])
        if not match:
            raise LedgerError("settled gate evidence must be a local digest-addressed record")
        evidence_path = (ROOT / match.group(1)).resolve()
        if ROOT.resolve() not in evidence_path.parents or not evidence_path.is_file():
            raise LedgerError("settled gate evidence record is unavailable")
        evidence_bytes = evidence_path.read_bytes()
        if hashlib.sha256(evidence_bytes).hexdigest() != match.group(2):
            raise LedgerError("settled gate evidence digest mismatch")
        try:
            evidence = json.loads(evidence_bytes)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LedgerError("settled gate evidence is not JSON") from exc
        expected_evidence = {
            "kind": gate["kind"], "subject": gate["subject"],
            "observed_status": gate["observed_status"],
            "observation_id": gate["observation_id"],
        }
        if not isinstance(evidence, dict) or any(evidence.get(key) != value for key, value in expected_evidence.items()):
            raise LedgerError("settled gate evidence does not bind the asserted observation")
        if not any(
            gate["subject"].get("repository") == subject.get("repository")
            and gate["subject"].get("head_sha") is not None
            and gate["subject"].get("head_sha") == subject.get("head_sha")
            and (
                gate["subject"].get("base_sha") is None
                or gate["subject"].get("base_sha") == subject.get("base_sha")
            )
            for subject in state["subjects"]
        ):
            raise LedgerError("gate subject is not an exact current subject")
    state["gates"] = [item for item in state["gates"] if item["gate_id"] != gate["gate_id"]]
    state["gates"].append(copy.deepcopy(dict(gate)))
    state["gates"].sort(key=lambda item: item["gate_id"])


def _mutate_subject(state: dict[str, Any], payload: Mapping[str, Any]) -> None:
    old_head = payload["old_head"]
    new_head = payload["new_head"]
    found = False
    for subject in state["subjects"]:
        if (
            subject["repository"] == payload["repository"]
            and subject["identifier"] == payload["identifier"]
        ):
            if subject["head_sha"] != old_head:
                raise LedgerError("subject mutation old head drift")
            subject["head_sha"] = new_head
            found = True
    if not found:
        raise LedgerError("subject mutation target is unknown")
    for gate in state["gates"]:
        if gate["subject"]["head_sha"] == old_head and gate["disposition"] == "SETTLED":
            gate["disposition"] = "INVALIDATED"
            gate["observed_status"] = "STALE"
            state["invalidated_gate_ids"].append(gate["gate_id"])
    state["invalidated_gate_ids"] = sorted(set(state["invalidated_gate_ids"]))


def _apply_event(
    state: dict[str, Any],
    event: Mapping[str, Any],
    admission_record: Mapping[str, Any],
    catalog: Mapping[str, Any] | None = None,
) -> None:
    kind = event["event_type"]
    payload = event["payload"]
    if kind == "WORK_PACKAGE_ADMITTED":
        admission = admission_record
        if payload["admission_digest"] != digest(admission):
            raise LedgerError("admission event digest does not match referenced record")
        state["roles"] = copy.deepcopy(admission["roles"])
        state["subjects"] = [
            {
                "repository": admission["working_repository"],
                "kind": "BRANCH",
                "identifier": admission["working_branch"],
                "head_sha": admission["protected_base"],
                "base_sha": admission["protected_base"],
                "artifact_digest": None,
            }
        ]
        if admission["disposition"] == "ADMITTED":
            state["lifecycle_state"] = "READY"
            state["domain_phase"] = "IMPLEMENTATION"
        elif admission["disposition"] == "DECOMPOSITION_REQUIRED":
            state["lifecycle_state"] = "BLOCKED"
            state["blocking_conditions"] = ["CAPABILITY_TOPOLOGY_MISMATCH"]
            state["stopping_boundary"] = "PERSISTENT_CONTROLLER_REQUIRED"
        else:
            state["lifecycle_state"] = "BLOCKED"
            state["blocking_conditions"] = ["WORK_PACKAGE_ADMISSION_REJECTED"]
            state["stopping_boundary"] = "ADMISSION_REJECTED"
    elif kind == "ROLE_DISPATCHED":
        role = next((item for item in state["roles"] if item["role"] == payload["role"]), None)
        if role is None or role["status"] != "PENDING" or role.get("actor_id") or role.get("session_id"):
            raise LedgerError("role dispatch requires one unassigned pending role")
        _replace_role(state, payload, "DISPATCHED")
    elif kind == "ROLE_RESULT_RECORDED":
        role = next((item for item in state["roles"] if item["role"] == payload["role"]), None)
        if role is None or role["status"] != "DISPATCHED" or role.get("actor_id") != payload["actor_id"] or role.get("session_id") != payload["session_id"]:
            raise LedgerError("role result does not match a dispatched assignment")
        result_bytes = verified_local_file(payload["result_path"], payload["result_digest"])
        try:
            result = json.loads(result_bytes)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LedgerError("role result record is not JSON") from exc
        if not isinstance(result, dict) or any(result.get(key) != payload[key] for key in ("role", "actor_id", "session_id")):
            raise LedgerError("role result record identity mismatch")
        _replace_role(state, payload, "COMPLETE")
    elif kind == "GATE_OBSERVED":
        _upsert_gate(state, payload["gate"])
    elif kind == "EXTERNAL_WAIT_OPENED":
        if state["open_transaction"] is not None:
            raise LedgerError("external wait cannot open during mutation")
        wait = payload["wait"]
        if not any(
            wait["repository"] == subject["repository"]
            and wait["subject_head"] == subject["head_sha"]
            for subject in state["subjects"]
        ):
            raise LedgerError("external wait is not bound to an exact current subject")
        if any(item["wait_id"] == wait["wait_id"] for item in state["external_waits"]):
            raise LedgerError("duplicate external wait identity")
        state["external_waits"].append(copy.deepcopy(wait))
        state["lifecycle_state"] = "WAITING_EXTERNAL"
    elif kind == "EXTERNAL_WAIT_OBSERVED":
        wait = next(
            (item for item in state["external_waits"] if item["wait_id"] == payload["wait_id"]),
            None,
        )
        if wait is None:
            raise LedgerError("observation references unknown wait")
        if payload["object_id"] != wait["object_id"] or payload["subject_head"] != wait["subject_head"]:
            raise LedgerError("external observation is stale or bound to another object")
        observed_at = instant(payload["observed_at"])
        if observed_at < instant(wait["next_eligible_observation_at"]):
            raise LedgerError("external observation occurred before it was eligible")
        if wait["observed_at"] is not None and observed_at <= instant(wait["observed_at"]):
            raise LedgerError("external observation time is not monotonic")
        wait["latest_observation_id"] = payload["observation_id"]
        wait["latest_status"] = payload["status"]
        wait["observed_at"] = payload["observed_at"]
        if payload["status"] in wait["expected_terminal_observations"]:
            state["external_waits"].remove(wait)
            state["lifecycle_state"] = "READY"
    elif kind == "TRANSACTION_PREPARED":
        transaction = copy.deepcopy(payload["transaction"])
        if state["open_transaction"] is not None or transaction["state"] != "PREPARED":
            raise LedgerError("at most one PREPARED mutating transaction is allowed")
        if transaction["started_state_digest"] != state["state_digest"]:
            raise LedgerError("transaction starts from stale state digest")
        if catalog is None:
            raise LedgerError("transaction preparation requires transition catalog")
        transition = transition_by_id(catalog, transaction["transition_id"])
        permitted, _, _ = derive_permitted_transitions(state, catalog)
        if transaction["transition_id"] not in permitted or transition["mode"] != "MUTATING":
            raise LedgerError("transaction transition is not reducer-permitted")
        claim = transaction["executor_claim"]
        role = next((item for item in state["roles"] if item["role"] == claim["role"]), None)
        if role is None or role.get("actor_id") != claim["executor_id"] or role.get("session_id") != claim["session_id"]:
            raise LedgerError("transaction executor is not the durable role assignment")
        if (
            claim["status"] != "ACTIVE"
            or claim["expires_at"] <= claim["acquired_at"]
            or event["occurred_at"] < claim["acquired_at"]
            or event["occurred_at"] >= claim["expires_at"]
        ):
            raise LedgerError("transaction executor claim is inactive or expired")
        if claim["role"] not in transition["required_roles"] or not set(transition["required_capabilities"]).issubset(claim["capabilities"]):
            raise LedgerError("transaction executor lacks transition authority")
        if transaction["replay_class"] != transition["replay_class"] or transaction["effect_probes"] != transition["effect_probes"]:
            raise LedgerError("transaction semantics drift from catalog")
        state["open_transaction"] = transaction
        state["lifecycle_state"] = "TRANSACTION_OPEN"
    elif kind == "TRANSACTION_APPLYING":
        transaction = state["open_transaction"]
        if transaction is None or transaction["transaction_id"] != payload["transaction_id"]:
            raise LedgerError("APPLYING references no open transaction")
        if transaction["state"] != "PREPARED":
            raise LedgerError("transaction can enter APPLYING only from PREPARED")
        transaction["state"] = "APPLYING"
        transaction["attempt_ids"].append(payload["attempt_id"])
    elif kind == "TRANSACTION_RECONCILING":
        transaction = state["open_transaction"]
        if transaction is None or transaction["transaction_id"] != payload["transaction_id"]:
            raise LedgerError("RECONCILING references no open transaction")
        if transaction["state"] not in {"PREPARED", "APPLYING"}:
            raise LedgerError("transaction can enter RECONCILING only from PREPARED or APPLYING")
        transaction["state"] = "RECONCILING"
        transaction["observed_side_effects"] = payload["observed_side_effects"]
    elif kind == "TRANSACTION_COMMITTED":
        transaction = state["open_transaction"]
        if transaction is None or transaction["transaction_id"] != payload["transaction_id"]:
            raise LedgerError("COMMITTED references no open transaction")
        if transaction["state"] not in {"APPLYING", "RECONCILING"}:
            raise LedgerError("transaction cannot commit before APPLYING or RECONCILING")
        if transaction["replay_class"] == "NON_REPLAYABLE_REQUIRES_RECONCILIATION" and transaction["state"] != "RECONCILING":
            raise LedgerError("non-replayable transaction requires reconciliation before commit")
        if not payload["evidence"]:
            raise LedgerError("transaction cannot commit without authoritative evidence")
        for evidence_ref in payload["evidence"]:
            match = re.fullmatch(r"file:([^#]+)#sha256:([0-9a-f]{64})", evidence_ref)
            if not match:
                raise LedgerError("transaction evidence must be a local digest-addressed record")
            verified_local_file(match.group(1), match.group(2))
        if catalog is None:
            raise LedgerError("transaction commit requires transition catalog")
        transition = transition_by_id(catalog, transaction["transition_id"])
        phase_effects = [effect for effect in payload["effects"] if effect["kind"] == "PHASE_CHANGED"]
        if len(phase_effects) != 1 or phase_effects[0]["phase"] != transition["successor_phase"]:
            raise LedgerError("committed phase does not match catalog successor")
        for effect in payload["effects"]:
            if effect["kind"] == "SUBJECT_MUTATED":
                _mutate_subject(state, effect)
            elif effect["kind"] == "PHASE_CHANGED":
                state["domain_phase"] = effect["phase"]
            else:
                raise LedgerError(f"unknown committed effect: {effect['kind']}")
        state["open_transaction"] = None
        state["lifecycle_state"] = "READY"
    elif kind == "TRANSACTION_ABORTED":
        transaction = state["open_transaction"]
        if transaction is None or transaction["transaction_id"] != payload["transaction_id"]:
            raise LedgerError("ABORTED references no open transaction")
        state["open_transaction"] = None
        state["lifecycle_state"] = "READY"
    elif kind == "SUBJECT_MUTATED":
        raise LedgerError("subject mutation is valid only as a committed transaction effect")
    elif kind == "BOUNDARY_DECLARED":
        state["lifecycle_state"] = "BLOCKED"
        state["blocking_conditions"] = [payload["category"]]
        state["stopping_boundary"] = payload["needed"]
    elif kind == "WORK_PACKAGE_CLOSED":
        if state["open_transaction"] or state["external_waits"]:
            raise LedgerError("terminal state cannot retain transaction or wait")
        if catalog is None:
            raise LedgerError("closure requires transition catalog")
        permitted, _, _ = derive_permitted_transitions(state, catalog)
        if payload["terminal_transition"] != "CLOSE_WORK_PACKAGE" or "CLOSE_WORK_PACKAGE" not in permitted:
            raise LedgerError("work package closure is not reducer-permitted")
        if not payload["terminal_evidence"]:
            raise LedgerError("work package closure requires exact terminal evidence")
        state["lifecycle_state"] = "TERMINAL"
        state["domain_phase"] = "CLOSED"
    else:  # pragma: no cover - schema and payload guard enumerate all kinds
        raise LedgerError(f"unsupported event type: {kind}")


def _gate_kinds_settled(state: Mapping[str, Any]) -> set[str]:
    settled = {
        gate["kind"]
        for gate in state["gates"]
        if gate["required"]
        and gate["disposition"] == "SETTLED"
        and gate["observed_status"] in SETTLED_GATE_STATUSES
    }
    review_roles = [
        next((item for item in state["roles"] if item["role"] == name), None)
        for name in ("IMPLEMENTER", "ADVERSARY", "REFEREE")
    ]
    if all(
        role is not None and role.get("actor_id") and role.get("session_id")
        and role.get("status") == "COMPLETE" and role.get("result_digest")
        for role in review_roles
    ):
        validate_role_separation(state["roles"], [
        "IMPLEMENTER!=ADVERSARY", "IMPLEMENTER!=REFEREE", "ADVERSARY!=REFEREE"
        ])
        settled.add("ROLE_SEPARATION")
    if not state["authority"]["contradictions"]:
        settled.add("AUTHORITY_COHERENCE")
    return settled


def derive_permitted_transitions(
    state: Mapping[str, Any], catalog: Mapping[str, Any]
) -> tuple[list[str], str | None, str | None]:
    settled = _gate_kinds_settled(state)
    eligible_roles = {
        role["role"]
        for role in state["roles"]
        if role["status"] in {"DISPATCHED", "COMPLETE", "RESERVED"}
    }
    permitted: list[tuple[int, str]] = []
    contradictions = state["authority"]["contradictions"]
    for transition in catalog["transitions"]:
        if (
            transition["transition_id"] == "RECONCILE_CURRENT_VERSION_PROJECTION"
            and not contradictions
        ):
            continue
        if state["domain_phase"] not in transition["input_phases"]:
            continue
        if state["lifecycle_state"] not in transition["lifecycle_states"]:
            continue
        if transition["requires_open_transaction"] != (
            state["open_transaction"] is not None
        ):
            continue
        if transition["requires_external_wait"] != bool(state["external_waits"]):
            continue
        if transition["requires_no_contradictions"] and contradictions:
            continue
        if contradictions and transition["authority_effect"] in AUTHORITY_EXPANDING_EFFECTS:
            continue
        if not set(transition["required_gate_kinds"]).issubset(settled):
            continue
        if not set(transition["required_roles"]).issubset(eligible_roles):
            continue
        permitted.append((transition["priority"], transition["transition_id"]))
    permitted.sort(key=lambda item: (item[0], item[1]))
    ids = [item[1] for item in permitted]
    if not permitted:
        return ids, None, state.get("stopping_boundary") or "NO_PERMITTED_TRANSITION"
    best_priority = permitted[0][0]
    best = [identifier for priority, identifier in permitted if priority == best_priority]
    if len(best) > 1:
        return ids, None, "POLICY_CHOICE_REQUIRED"
    return ids, best[0], None


def state_digest(state: Mapping[str, Any]) -> str:
    material = {key: value for key, value in state.items() if key != "state_digest"}
    return digest(material)


def reduce_ledger(
    ledger: Mapping[str, Any],
    catalog: Mapping[str, Any],
    authority: Mapping[str, Any],
    admission: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_event_sequence(ledger)
    expected_catalog_digest = catalog_digest(catalog)
    if ledger["catalog_digest"] != expected_catalog_digest:
        raise LedgerError("ledger transition-catalog digest mismatch")
    if admission is None:
        first_payload = ledger["events"][0]["payload"]
        admission = load_json(ROOT / first_payload["admission_path"])
    state = _initial_state(ledger["work_package"], authority, expected_catalog_digest)
    for event in ledger["events"]:
        state["state_digest"] = state_digest(state)
        _apply_event(state, event, admission, catalog)
        state["generation"] = event["sequence"]
        state["ledger_head_digest"] = event["event_digest"]
    permitted, selected, boundary = derive_permitted_transitions(state, catalog)
    state["permitted_transitions"] = permitted
    state["selected_transition"] = selected
    if boundary == "POLICY_CHOICE_REQUIRED":
        state["lifecycle_state"] = "CHOICE_REQUIRED"
    state["stopping_boundary"] = boundary
    state["state_digest"] = state_digest(state)
    if state["claim_boundaries"] != CLAIM_BOUNDARIES:
        raise LedgerError("derived state widens authority")
    validate_role_separation(state["roles"], [
        "IMPLEMENTER!=ADVERSARY",
        "IMPLEMENTER!=REFEREE",
        "ADVERSARY!=REFEREE",
    ])
    return state


def assert_stored_state(
    stored: Mapping[str, Any], recomputed: Mapping[str, Any]
) -> None:
    if canonical_bytes(stored) != canonical_bytes(recomputed):
        raise LedgerError("stored derived state does not match reducer output")
    if stored["state_digest"] != state_digest(stored):
        raise LedgerError("stored state digest mismatch")


def transition_by_id(catalog: Mapping[str, Any], transition_id: str) -> Mapping[str, Any]:
    matches = [
        transition
        for transition in catalog["transitions"]
        if transition["transition_id"] == transition_id
    ]
    if len(matches) != 1:
        raise TransitionRejected(f"unknown or duplicate transition: {transition_id}")
    return matches[0]


@dataclass(frozen=True)
class Executor:
    executor_id: str
    session_id: str
    role: str
    executor_class: str
    capabilities: tuple[str, ...]


class TransactionController:
    def __init__(self, catalog: Mapping[str, Any]):
        self.catalog = catalog

    def authorize(
        self, state: Mapping[str, Any], transition_id: str, executor: Executor
    ) -> Mapping[str, Any]:
        transition = transition_by_id(self.catalog, transition_id)
        if transition_id not in state["permitted_transitions"]:
            raise TransitionRejected("transition is not reducer-permitted")
        if executor.role not in transition["required_roles"]:
            raise TransitionRejected("executor role is not authorized")
        assignment = next((item for item in state["roles"] if item["role"] == executor.role), None)
        if assignment is None or assignment.get("actor_id") != executor.executor_id or assignment.get("session_id") != executor.session_id:
            raise TransitionRejected("executor is not the durable role assignment")
        if assignment.get("status") not in {"DISPATCHED", "COMPLETE", "RESERVED"}:
            raise TransitionRejected("durable role assignment is not active")
        missing = set(transition["required_capabilities"]) - set(executor.capabilities)
        if missing:
            raise TransitionRejected(f"executor capability mismatch: {sorted(missing)}")
        if transition["mode"] == "RESERVED_HUMAN" and executor.executor_class != "HUMAN":
            raise TransitionRejected("reserved transition requires a human executor")
        return transition

    def prepare(
        self,
        state: Mapping[str, Any],
        transition_id: str,
        executor: Executor,
        *,
        transaction_id: str,
        idempotency_key: str,
        expires_at: str,
        now: str,
    ) -> dict[str, Any]:
        transition = self.authorize(state, transition_id, executor)
        if transition["mode"] != "MUTATING":
            raise TransitionRejected("only mutating transitions use transaction prepare")
        if state["open_transaction"] is not None:
            raise TransitionRejected("another mutating transaction is open")
        return {
            "transaction_id": transaction_id,
            "transition_id": transition_id,
            "state": "PREPARED",
            "idempotency_key": idempotency_key,
            "replay_class": transition["replay_class"],
            "started_generation": state["generation"],
            "started_state_digest": state["state_digest"],
            "subjects": copy.deepcopy(state["subjects"]),
            "preconditions": ["reducer_transition_permitted", "exact_subjects_rechecked"],
            "intended_effects": [transition["successor_phase"]],
            "executor_claim": {
                "executor_id": executor.executor_id,
                "session_id": executor.session_id,
                "role": executor.role,
                "executor_class": executor.executor_class,
                "capabilities": list(executor.capabilities),
                "acquired_at": now,
                "expires_at": expires_at,
                "status": "ACTIVE",
            },
            "effect_probes": copy.deepcopy(transition["effect_probes"]),
            "attempt_ids": [],
            "observed_side_effects": [],
            "postconditions": [f"phase={transition['successor_phase']}"],
            "evidence": [],
            "invalidated_gate_ids": [],
        }

    def reconcile(
        self, transaction: Mapping[str, Any], observed_effects: Iterable[str]
    ) -> str:
        observed = set(observed_effects)
        intended = set(transaction["intended_effects"])
        if intended and intended.issubset(observed):
            return "COMMIT_OBSERVED_SUCCESS"
        if not observed and transaction["replay_class"] in {
            "IDEMPOTENT_BY_KEY",
            "REPLAY_AFTER_ABSENCE_PROBE",
        }:
            return "REPLAY_AFTER_ABSENCE_PROBE"
        return "RECONCILIATION_BOUNDARY"


def validate_propagation_manifest(
    manifest: Mapping[str, Any], authority: Mapping[str, Any]
) -> None:
    if manifest["authoritative_version"] != authority["version"]:
        raise AuthorityContradiction("propagation manifest version is stale")
    authoritative = [
        item for item in manifest["consumers"] if item["authority_class"] == "AUTHORITATIVE"
    ]
    if len(authoritative) != 2 or any(item["status"] != "COHERENT" for item in authoritative):
        raise AuthorityContradiction("admission and adoption must be coherent authoritative consumers")
    derived = [
        item for item in manifest["consumers"] if item["authority_class"] == "DERIVED_CURRENT"
    ]
    computed_local_coherence = all(
        item["status"] == "COHERENT"
        for item in derived
        if item["repository"] == "grandchallenge/gcl-standards"
    )
    if manifest["all_derived_current_coherent"] != computed_local_coherence:
        raise AuthorityContradiction("derived-current coherence summary mismatch")
    unresolved_external = any(
        item["status"] in {"STALE", "UNRESOLVED_EXTERNAL"}
        for item in derived
        if item["repository"] != "grandchallenge/gcl-standards"
    )
    if manifest["external_reconciliation_complete"] == unresolved_external:
        raise AuthorityContradiction("external reconciliation summary mismatch")
    if manifest["claim_boundaries"] != CLAIM_BOUNDARIES:
        raise AuthorityContradiction("propagation manifest widens authority")


def validate_candidate_artifacts(*, root: Path = ROOT) -> None:
    schema = load_json(root / "schemas" / "ghos_control_plane.schema.json")
    defect_schema = load_json(root / "schemas" / "ghos_defect_ledger.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator.check_schema(defect_schema)
    defect = load_json(root / "implementation" / "GCL-GHOS-CONTROL-PLANE-REMEDIATION-001" / "DEFECT_LEDGER.json")
    jsonschema.validate(defect, defect_schema, cls=jsonschema.Draft202012Validator)

    control = root / "implementation" / "GCL-GHOS-CONTROL-PLANE-REMEDIATION-001" / "control-plane"
    catalog = load_json(control / "transition-catalog.json")
    admission = load_json(control / "candidate-work-package-admission.json")
    ledger = load_json(control / "candidate-harness-ledger.json")
    stored_state = load_json(control / "candidate-harness-state.json")
    manifest = load_json(control / "active-version-propagation-manifest.json")
    for instance in (catalog, admission, ledger, stored_state, manifest):
        jsonschema.validate(
            instance,
            schema,
            cls=jsonschema.Draft202012Validator,
            format_checker=jsonschema.FormatChecker(),
        )
    admitted = admit_work_package(admission)
    if admitted != admission:
        raise ControlPlaneError("stored admission does not match topology reducer")
    projection = load_json(root / "status" / "GCL-GHOS-00-current.json")
    authority = resolve_effective_authority(root=root, projection=projection)
    contradiction_codes = {
        item["code"] for item in authority["contradictions"]
    }
    if contradiction_codes - {"STALE_CURRENT_PROJECTION"}:
        raise AuthorityContradiction("unexpected authority contradiction")
    if "STALE_CURRENT_PROJECTION" not in contradiction_codes:
        raise AuthorityContradiction(
            "baseline coherence defect disappeared without a governed transition"
        )
    validate_propagation_manifest(manifest, authority)
    reduced = reduce_ledger(ledger, catalog, authority, admission)
    assert_stored_state(stored_state, reduced)


def validate(*, root: Path = ROOT) -> None:
    validate_candidate_artifacts(root=root)


if __name__ == "__main__":
    validate()
    print("GH-OS control-plane schemas, authority, ledger, and derived state validated")
