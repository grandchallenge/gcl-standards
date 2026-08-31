# GH-OS control-plane requirements

**Work package:** `GCL-GHOS-CONTROL-PLANE-REMEDIATION-001`  
**Role:** `CONTROL_PLANE_DESIGNER`  
**Fixed design-input commit:** `78d456ffa2e050caea7429732f3e4709cb2e66d9`  
**Input set at that commit:** `ARCHAEOLOGY_REPORT.md`, `FAILURE_AUDIT.md`, `DEFECT_LEDGER.json`, and `FINDINGS_RECONCILIATION.md`  
**Authority status:** candidate requirements for governed review; not an admitted standard, programme adoption, authorization, or conformance claim

## 1. Disposition and scope

The minimum justified remediation is enforcement machinery under the already-admitted `GCL-GHOS-00` `0.2.0` bounded-execution-continuity invariant, plus immediate repair of the current-version propagation and validation defect. No normative successor is assumed.

The machinery SHALL make a governed work package resumable and transition-deterministic across permanent loss of an agent, while preserving the existing authority order and all reserved Human Steward, Council, MATHCERT, production, publication, and claim boundaries. It SHALL be piloted only within the existing MATH-PROGRAMME adoption scope. A later cross-programme mandate requires its own governed determination of whether a normative successor is necessary.

These requirements do not authorize implementation, protected mutation, approval, merge, certification, activation, or claim promotion.

## 2. Required outcomes

For every admitted work package whose topology is not a single bounded atomic action, a fresh conforming executor with repository access and no chat transcript SHALL be able to:

1. resolve the controlling authority and exact work-package state;
2. determine whether a transaction is open, complete, aborted, or in reconciliation;
3. derive the finite set of permitted transitions from versioned policy and durable facts;
4. select the sole mandatory transition, apply a recorded deterministic selection rule, or stop at an explicitly named choice/authority boundary;
5. verify that its capabilities and role are suitable for that transition;
6. execute at most one bounded mutating transaction under write-ahead semantics;
7. leave a durable record from which replacement is unambiguous; and
8. distinguish an external wait from a halt or reserved decision.

Two conforming reducers given the same policy version, state-log head, and authoritative observations SHALL produce the same permitted transition set and selection result. Free-form prose MAY explain the result but SHALL NOT determine it.

## 3. Authority and evidence precedence

The control plane SHALL implement, not reinterpret, the admitted precedence order:

1. compact Constitution;
2. effective constitutional amendments;
3. INTELLECT constitutional schedules;
4. admitted cross-programme standards;
5. active programme adoption records;
6. repository profiles and programme-local delegated policy;
7. exact candidate and external platform facts;
8. generated current-status projections and other descriptive surfaces;
9. mutable issues, pull-request prose, comments, Projects, dashboards, and chat.

Within a tier, exact protected identity and later valid supersession prevail. Historical records remain immutable facts about their own transaction; for example, an admission record's historical `next_gate: not_started` SHALL NOT be rewritten after later adoption.

If superior sources conflict, are ambiguous, or cannot be resolved exactly, the transition resolver SHALL emit a blocking contradiction and no authority-bearing transition. If a subordinate projection conflicts with a single resolvable superior selection, the resolver SHALL identify the authoritative value and the stale source, permit only non-authority-expanding reconciliation work, and block any transition that relies on the stale projection.

Control-plane state is operational evidence, not a new source of constitutional, programme, certification, merge, publication, production, or claim authority.

## 4. Work-package admission and capability topology

Before substantial execution, the work graph SHALL be classified from observable requirements, not executor confidence.

### 4.1 Execution topology

- `BOUNDED_ATOMIC`: one bounded transition, no external wait, no cross-session lease, and rollback or exact reconciliation is available.
- `MULTI_SESSION_RESUMABLE`: multiple bounded transitions or external waits are permitted because durable state is sufficient for replacement after every transaction.
- `PERSISTENT_CONTROLLER_REQUIRED`: correctness depends on uninterrupted monitoring, deadlines or leases shorter than safe handoff, autonomous wakeups, or coordination that cannot be reduced to durable bounded transitions.
- `HUMAN_DECISION_REQUIRED`: at least one next transition is reserved to a named human authority. This is an authority gate that MAY coexist with any execution topology; it is not treated as a mutually exclusive scheduling class.

### 4.2 Capability requirements

Admission SHALL record required capabilities as facts, including as applicable:

- durable read and compare-and-swap write access to the control ledger;
- exact Git and external-object readback;
- permission to perform each proposed mutation without protected bypass;
- persistent wake/scheduling support;
- maximum safe handoff latency and lease support;
- idempotency or authoritative effect-probe support;
- repository and network reachability; and
- role eligibility and separation constraints.

The current executor SHALL present an identity, session or instance identity, executor class, capabilities, and role. Capability satisfaction SHALL be mechanically compared with transition requirements. Capability never supplies authority.

A conversational executor MAY perform a bounded transition in `MULTI_SESSION_RESUMABLE` work only when the ledger is current, the transition can be reconciled after interruption, and no continued presence is required. It SHALL NOT be the sole scheduler for `PERSISTENT_CONTROLLER_REQUIRED` work. Such work must be decomposed or assigned to a persistent controller before admission.

### 4.3 Mandatory workflow routing

Protected policy SHALL enumerate the complete repository workflow surface. Each
workflow SHALL have one routing record whose observed unattended, wake, wait,
reuse, and write-capability features are derived from workflow bytes. Missing or
stale records SHALL fail closed. Any non-bounded topology SHALL either identify
an admitted persistent controller with a durable wake mechanism and state store,
or identify a complete decomposition into registered non-persistent workflows.
Adding a workflow without adding valid routing is prohibited by the same check.

## 5. Durable execution-state contract

The final schema need not copy the harness example. It SHALL contain the following semantic groups because each is needed to resolve a demonstrated ambiguity.

### 5.1 Envelope and concurrency

- schema identifier and version;
- stable work-package identifier and control-ledger identifier;
- monotonically increasing event sequence or generation;
- previous event/state digest and current canonical state digest;
- exact ledger ref and ledger commit identity;
- reducer/transition-catalog identifier and digest; and
- creation and last-observation timestamps as evidence freshness data, never as authority.

The state digest is the resume token. A second independently authored opaque resume token is unnecessary and SHALL NOT be required.

### 5.2 Governing authority

- authority repository and exact protected baseline;
- governing issue/work-package record;
- applicable standard admission and programme adoption references with exact commits/blobs;
- repository/programme policy references;
- declared authority-precedence profile; and
- fixed false claim/authority boundaries.

### 5.3 Work subjects and phase

- each working repository, branch/ref, protected base, candidate head, pull request, artifact, and digest material to the operation;
- current lifecycle phase and terminal condition identifier;
- work-graph node and dependency state; and
- role assignments and separation constraints for author, implementer, Adversary, Referee, coordinator, and reserved decision maker.

Null identities are allowed only when the phase makes the object inapplicable. A PR-, review-, check-, or workflow-bound transition SHALL carry its exact candidate subject.

### 5.4 Gates and evidence

Each required gate SHALL have:

- stable gate identifier and kind;
- required/optional status;
- exact subject selector, including head/tree/base/digest as applicable;
- authoritative evidence object identity;
- observed status and observation identity/time;
- validity rule and invalidation triggers; and
- settled/unsettled/invalidated disposition.

Required checks and reviews are gate instances, not unstructured lists. “Green” or “approved” without exact-subject identity is invalid.

### 5.5 Transition decision

- reducer input digest;
- finite permitted transition identifiers derived from the transition catalog;
- selected transition identifier or null;
- selection-rule identifier and its inputs;
- explicit reason when a policy-permitted choice set remains;
- required executor capabilities and authorized actor/role for each transition; and
- named stopping boundary when no transition is executable.

The stored permitted set is a checkable reducer output, not an operator-authored grant. Validation SHALL recompute it and reject mismatch.

### 5.6 External waits

Each wait SHALL have a stable `wait_id` and:

- provider, repository, object kind, immutable object identifier, and exact subject head/digest;
- expected terminal observations and wake condition;
- latest observation identity, status, and timestamp;
- bounded poll policy, next eligible observation time, and backoff state;
- deadline or `null` when policy has none;
- owning controller class and wake mechanism; and
- transition to run for each recognized terminal observation.

“Wait”, “wait for CI”, a URL alone, or a mutable check name without run/check identity is insufficient. A wait is not a blocker. It becomes a named boundary only when an applicable boundary rule is satisfied.

### 5.7 Open transaction and executor claim

At most one mutating transaction may be open for a work package. It SHALL record:

- stable transaction and transition identifiers;
- state `PREPARED`, `APPLYING`, `RECONCILING`, `COMMITTED`, `ABORTED`, or `BLOCKED`;
- idempotency key and replay classification;
- starting generation/state digest and exact subject identities;
- preconditions and intended effects;
- authorized actor role and executor claim: executor/session identity, capability class, acquired time, expiry, and release/supersession state;
- authoritative effect probes and expected observations;
- attempt identities and observed side effects;
- postconditions and exact evidence; and
- review/check invalidations caused by the transition.

No free-form “last action” field may substitute for this transaction record.

### 5.8 Terminal and blocking state

A terminal state SHALL contain the terminal transition, terminal-condition evidence, protected readback where required, and no open transaction or wait. A blocked state SHALL name one allowed boundary category, exact evidence, the authority or condition needed, and the non-mutating transitions still permitted. Conversation length, agent disappearance, ordinary running CI, and one failed diagnostic surface are never boundary categories.

## 6. Transaction semantics

Every mutating transition SHALL use the following protocol:

1. **Rehydrate:** resolve superior authority, exact subjects, gates, ledger head, and reducer output.
2. **Admit executor:** verify role, authority prerequisite, capabilities, and absence of conflicting unexpired executor claim.
3. **Prepare:** compare-and-swap an append-only `PREPARED` event containing the complete intended mutation, idempotency key, preconditions, effect probes, and executor claim.
4. **Recheck:** immediately re-read material external identities. Drift aborts before mutation.
5. **Apply once:** perform only the prepared bounded mutation.
6. **Observe:** use authoritative readback/effect probes; a command response or chat assertion is not a postcondition.
7. **Commit or reconcile:** append `COMMITTED` only when postconditions are observed. Otherwise leave `RECONCILING`, append `ABORTED`, or append `BLOCKED` with exact evidence.
8. **Reduce:** derive the next state, invalidate subject-dependent gates, and compare-and-swap the new state/log head.

Ledger writes SHALL be append-only and compare-and-swap against the observed parent. Competing writers must lose cleanly, rehydrate, and never overwrite history. Force updates and deletion of active ledger history are prohibited.

External systems and Git cannot provide one distributed atomic transaction. The required semantic is therefore write-ahead intent plus deterministic reconciliation, not a false claim of cross-system atomicity.

### 6.1 Interruption behavior

- Interruption before `PREPARED`: no transaction exists; replacement derives the same transition.
- Interruption after `PREPARED` but before mutation: replacement probes for the effect; if absent and preconditions remain true, it may replay according to the recorded replay class.
- Interruption during/after mutation but before `COMMITTED`: replacement enters `RECONCILING`, probes exact effects, and may commit observed success, safely replay an idempotent absent effect, compensate only when explicitly authorized, or block. It SHALL NOT infer success from partial side effects.
- Interruption after `COMMITTED`: replacement reduces from the committed event; it SHALL NOT repeat the mutation.
- An unexpired executor claim prevents concurrent mutation. Expiry permits takeover only through a recorded reconciliation transition.

## 7. Review and check invalidation

Review validity SHALL bind at minimum to repository, pull request or packet, exact candidate head/tree, applicable base, reviewed artifact/digest set, reviewer identity, reviewer session/role, review record identifier, and disposition.

Any mutation that changes a bound subject SHALL invalidate the review before another authority-bearing transition is derived. Head `H1` approval cannot authorize `H2`. Carry-forward is forbidden unless superior policy defines an explicit unchanged-subject rule whose predicate is mechanically proven and recorded; no such general rule is assumed here.

Check and diagnostic evidence SHALL likewise bind to exact head/run/job/artifact. A repair that produces a new head invalidates prior-head check settlement and diagnostics as current evidence, while preserving them as history.

## 8. Active-version coherence and propagation

The authoritative current GH-OS selection for a programme SHALL be resolved from the active programme adoption and its exact admitted standard. Current-status schemas, validators, README/front matter, and programme-local guides SHALL consume that resolved selection or be classified explicitly as historical. They SHALL NOT each hard-code an independent “current” version.

An adoption-changing transaction SHALL declare a propagation manifest containing every current-version consumer, its repository/path, authority class (`AUTHORITATIVE`, `DERIVED_CURRENT`, or `HISTORICAL`), expected value, and reconciliation status. Completion requires:

- one unambiguous active adoption;
- exact admission/adoption linkage;
- every `DERIVED_CURRENT` consumer updated or generated from the resolved selection;
- cross-repository exact-source validation;
- no validator that positively requires a superseded current assertion; and
- protected readback of the authoritative selection and required projections.

Cross-repository publication is a saga, not an atomic commit. Consumers SHOULD avoid embedding mutable current-version claims when they can resolve the authoritative adoption directly. Where a staged update is unavoidable, the activation transaction remains incomplete and authority-bearing downstream transitions fail closed until the propagation manifest is settled. Historical records are not rewritten.

The present `0.2.0` adoption is controlling for the MATH-PROGRAMME pilot under existing precedence. The `0.1.1` status projection and stale prose are contradictions to reconcile, not alternate authority and not grounds to rewrite immutable admission history.

## 9. Control-ledger storage requirements

Operational state SHALL be stored outside the candidate code branch so that checkpoint updates do not change the reviewed candidate head or recursively invalidate checks/reviews. The minimum topology is a work-package-specific append-only Git ref or equivalently protected durable ledger with:

- no force update or deletion;
- compare-and-swap writes;
- immutable event payloads and hash linkage;
- a canonical derived snapshot reproducible from events;
- schema and semantic validation before accepting a new event;
- exact links to, but no duplication of authority from, protected records; and
- bounded write permission that grants neither merge nor protected-main authority.

Mutable issue bodies/comments, Projects, Actions artifacts with retention limits, and chat MAY mirror or index the ledger but SHALL NOT be the sole resume surface.

## 10. Acceptance architecture for T1-T14

Acceptance SHALL combine closed-schema tests, semantic reducer tests, a crash-injection scenario runner, exact Git/external-object fixtures, and a reproducible no-chat replacement run. A test that merely searches for required phrases is insufficient.

| Test | Required architecture and oracle |
| --- | --- |
| T1 cold resume | Start a clean process with only ledger/policy/repository access; reducer reconstructs the expected phase, transaction state, and transition ID. |
| T2 model/session replacement | Two independent executor sessions consume identical inputs; machine reducer outputs are byte-identical or the same policy-authorized choice set. |
| T3 stale-chat attack | Inject conflicting chat as lowest-precedence input; resolver reports it stale and leaves the authoritative transition unchanged. |
| T4 cutoff at every boundary | Crash after every committed scenario event for branch mutation, CI launch/partial settlement, review request/approval, authorization, merge, and readback; replay reaches the expected state without duplicate mutation. |
| T5 cutoff inside transaction | Crash at each prepare/apply/observe/commit fault point; effect probes distinguish absent, partial, and complete effects and never infer completion. |
| T6 stale review invalidation | Bind approval to `H1`, mutate to `H2`, and prove review gate becomes invalid before merge/authorization derivation. |
| T7 projection contradiction | Fixture superior `0.2.0` adoption and subordinate `0.1.1` projection; validator identifies both exact sources, resolves precedence, and blocks reliance on the projection. |
| T8 external CI wait | Persist exact run/check identities and wake policy, terminate executor, then resume directly at one bounded observation transition without broad discovery. |
| T9 failed CI repair loop | Commit repair to `H2`; reducer invalidates `H1` diagnostics/checks and rejects them as current settlement. |
| T10 unauthorized transition | Remove each required authority/role gate in turn; reducer emits no merge, certification, promotion, protected mutation, or authority-expansion transition. |
| T11 conversational silence | Run the complete representative scenario with chat/private memory unavailable; all required inputs resolve from authorized durable sources. |
| T12 coordinator death | Crash coordinator between every role dispatch/result event; replacement reconstructs role graph, exact input digests, pending roles, and separation constraints. |
| T13 active-version coherence | Exercise current adoption, admission, generated projections, programme guide, and validator reachability across repositories; agreement passes and any contradiction fails closed. |
| T14 capability mismatch | Submit persistent-monitoring/deadline fixtures without a persistent controller; admission rejects them or emits a required decomposition transition before substantial work. |

Every scenario SHALL assert the exact transition ID, state digest, open-transaction state, gate invalidations, and prohibited authority outcomes. T1-T14 evidence SHALL bind to the exact implementation head reviewed by the Adversary and Referee.

## 11. Non-functional and governance requirements

- The reducer and validators SHALL be deterministic, offline-testable for fixtures, and independent of AETHER at correctness time.
- Live evidence acquisition MAY use GitHub APIs, but cached observations SHALL retain exact object identities and freshness.
- The control plane SHALL minimize broad polling through recorded wake conditions and bounded backoff.
- Schema validity alone is insufficient; semantic hostile-mutation tests and end-to-end interruption tests are mandatory.
- Proposal author, Implementer, Adversary, and Referee session separation SHALL be recorded and validated. The control plane SHALL report attribution gaps rather than claim physical identity it cannot prove.
- Green CI means only that the declared control-plane contract passed for the exact tested subject. It does not grant authority.

## 12. Normative-successor decision gate

Implementation SHOULD proceed first as MATH-PROGRAMME-scoped subordinate conformance machinery. A new GH-OS normative successor is justified only if governed review finds that either:

1. `0.2.0` cannot reasonably support mandatory durable transaction state and executor-topology admission as enforcement of bounded continuity; or
2. organization-wide adoption requires changing the cross-programme duties rather than supplying a programme-local implementation profile.

Until that finding exists, calling the remediation `0.3.0`, changing the standard's normative body, or claiming organization-wide conformance is out of scope.
