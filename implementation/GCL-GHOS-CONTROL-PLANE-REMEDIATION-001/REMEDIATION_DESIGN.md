# GH-OS control-plane remediation design

**Work package:** `GCL-GHOS-CONTROL-PLANE-REMEDIATION-001`  
**Role:** `CONTROL_PLANE_DESIGNER`  
**Fixed design-input commit:** `78d456ffa2e050caea7429732f3e4709cb2e66d9`  
**Design basis:** the four fixed audit inputs at that commit, the protected harness specification, `GCL-GHOS-00`, ADR-0001, current admission/adoption/status records, and reachable validators/tests  
**Candidate-evidence boundary:** MATH-PROGRAMME PR #702 was inspected only as untrusted pre-existing candidate evidence; it is not a design authority  
**Status:** candidate design for independent governed review

## 1. Design disposition

**GO:** implement a MATH-PROGRAMME-scoped control-plane conformance layer that enforces the already-intended `0.2.0` bounded-continuity and authority-precedence invariants.

**GO first:** repair active-version resolution and propagation so the authoritative `0.2.0` programme adoption cannot coexist with validators that positively require `0.1.1` as current.

**NO GO:** do not declare a normative GH-OS successor, organization-wide conformance, or PR #702 acceptance from this design. Do not merge PR #702 as the full remediation without redesign and fresh exact-head review against T1-T14.

The minimum design has two independent but ordered remedies:

1. **Current-state coherence:** one authority resolver derives current version/status from the exact active adoption and admitted standard; all current projections and validators consume it or fail closed.
2. **Execution continuity:** a durable append-only control ledger, deterministic reducer, capability admission, and write-ahead transaction protocol make multi-session work replaceable after every transition and reconcilable after interruption inside a mutation.

The first closes the demonstrated immediate defect. The second closes the systemic requirements/enforcement gap. Either alone is insufficient.

## 2. Evidence-derived constraints

The design preserves these established facts:

- `GCL-GHOS-00` `0.2.0` is correctly admitted and actively adopted for the MATH-PROGRAMME pilot.
- The `0.1.1` current-status projection and stale prose are subordinate contradictions, not a competing selection.
- Existing controls preserve exact authority/evidence identities well, but separately validate incompatible snapshots.
- The immediate failure was incomplete propagation plus a false-green current-status validator.
- General interruption recovery, transaction state, deterministic transition derivation, and executor classification were not literal `0.2.0` implementation requirements; they are missing conformance machinery and a requirements gap.
- GitHub persistence did not fail. The architecture must accommodate bounded conversational executors.
- Shared GitHub account evidence cannot establish physical human/agent actor separation; the design records attributable role/session evidence and reports residual ambiguity.
- No mathematical, certification, constitutional, production, publication, deployment, or commercial authority may be widened.

## 3. Architecture

### 3.1 Authority resolver

The resolver accepts exact protected records and returns one typed `EffectiveAuthority` object:

- constitutional schedule and amendment;
- admitted standard selected by the programme;
- active programme adoption;
- programme-local policy/profile;
- authority-precedence trace; and
- contradiction list with exact source identities.

Resolution is not “latest filename wins.” It follows the admitted precedence order and explicit lineage. More than one active adoption, an adoption that does not bind an admitted source, or unresolved superior-tier disagreement yields `AUTHORITY_CONTRADICTION` and no authority-bearing transition.

A stale lower projection yields both the authoritative selection and `PROJECTION_RECONCILIATION_REQUIRED`. Only reconciliation, diagnostic, and other non-authority-expanding transitions remain permitted until affected reliance is safe.

### 3.2 Propagation manifest and generated current view

Every change to active adoption declares a versioned propagation manifest. Each consumer is classified:

- `AUTHORITATIVE`: admission/adoption record; never generated from a projection;
- `DERIVED_CURRENT`: status JSON, README current-status section, standard front-matter projection, programme guide current-authority statement, public status, and validators that interpret “current”; or
- `HISTORICAL`: immutable admission history, old evidence, and statements explicitly scoped to their historical time.

One generated `EffectiveAuthority` fixture feeds current-selection schemas, status validation, and current-version tests. Version-specific admission validators remain exact historical validators and no longer assert that their version is currently active. The current-status validator compares the live adoption path to the selected projection before validating descriptive evidence.

This avoids rewriting immutable history and removes independent hard-coded current versions. Cross-repository consumers either resolve the authoritative record directly or are staged behind a propagation barrier. An activation-changing transaction is not closed until protected readback shows every required derived-current consumer coherent.

### 3.3 Work-package admission controller

Before substantial work, a pure admission function consumes the work graph and capability declaration and emits:

- execution topology: `BOUNDED_ATOMIC`, `MULTI_SESSION_RESUMABLE`, or `PERSISTENT_CONTROLLER_REQUIRED`;
- reserved `HUMAN_DECISION_REQUIRED` transition points;
- required executor capabilities;
- required decomposition, if any;
- role graph and separation constraints; and
- an admission disposition and evidence trace.

`HUMAN_DECISION_REQUIRED` is modeled as a gate rather than a competing scheduling category. A workflow may be multi-session resumable and still contain a reserved Human Steward transition.

Admission fails before material mutation if a persistent controller is required but unavailable, if a mutation cannot be reconciled after interruption, or if role separation cannot be represented. A bounded conversational executor is admitted only for one bounded transition at a time.

### 3.4 Control ledger

Each non-atomic work package receives a dedicated append-only control ledger, stored outside the candidate code branch. The preferred implementation is a work-package-specific Git ref under a ruleset that prohibits force updates/deletion and permits only compare-and-swap appends by the scoped control writer.

The ledger contains:

- an immutable admission event;
- append-only transaction, observation, invalidation, wait, role, and terminal events;
- a hash-linked sequence;
- a canonical snapshot derived by a deterministic reducer; and
- an exact ledger-head commit used for compare-and-swap.

Keeping the ledger off the candidate branch is necessary: routine wait/checkpoint updates must not create a new candidate head and invalidate the checks or reviews they are recording. Direct ledger write authority is narrowly scoped and conveys no pull-request merge, protected-main mutation, approval, certification, or claim authority.

A single shared coordination branch is not preferred because unrelated work packages would contend on one head. One mutable JSON file without immutable events is insufficient because it cannot prove whether an interrupted update overwrote or omitted a transition.

### 3.5 Transition catalog and deterministic reducer

Transitions are versioned data/code entries, not free-form next-action prose. Each transition defines:

- input phases/states;
- authority, gate, role, and capability preconditions;
- exact subject selectors;
- whether it is read-only, mutating, reserved-human, or persistent-controller work;
- prepared intent and idempotency class;
- authoritative effect probes;
- postconditions;
- review/check invalidation rules;
- wait outcomes;
- failure/reconciliation behavior; and
- legal successor phases.

The reducer consumes the catalog digest, authority resolution, ledger events, and exact observations. It outputs the canonical state digest, gate dispositions, permitted transition IDs, and either one selected transition, an explicit policy-defined choice set, a wait observation transition, or a named stopping boundary.

Operator-written `next_action` is not trusted. If mirrored for readability, validation recomputes it and rejects disagreement.

### 3.6 Transaction coordinator

The coordinator implements a write-ahead saga because GitHub mutations and Git ledger writes cannot be one distributed atomic commit.

```text
rehydrate -> admit executor -> PREPARED -> recheck -> APPLYING
                                      -> RECONCILING -> COMMITTED -> reduce
                                                      -> ABORTED
                                                      -> BLOCKED
```

`PREPARED` records the exact mutation, source state digest, idempotency key, preconditions, executor claim, expected effects, and probes before any side effect. `COMMITTED` is legal only after authoritative readback proves the postconditions. A command return, action dispatch response, or chat statement is never completion evidence.

An executor claim prevents concurrent mutation and has a bounded expiry. Takeover after death is a recorded reconciliation transition, never silent lease theft. Compare-and-swap on ledger head rejects competing updates.

Replay classes are explicit:

- `READ_ONLY_REPEATABLE`;
- `IDEMPOTENT_BY_KEY`;
- `REPLAY_AFTER_ABSENCE_PROBE`;
- `COMPENSATABLE_WITH_AUTHORITY`; or
- `NON_REPLAYABLE_REQUIRES_RECONCILIATION`.

No mutating transition may be admitted without an effect probe and one of these dispositions.

### 3.7 Evidence and wait adapters

Provider adapters normalize exact external observations without becoming authority. For GitHub they bind repository, PR, head, check suite/run/check/job/review identifiers, observed status, and observation timestamp.

An async wait is a first-class state with a stable ID, exact objects, wake condition, bounded backoff, next observation time, and outcome transitions. A persistent wake mechanism is required only when policy requires autonomous or deadline-bounded continuation. Otherwise any fresh executor may perform the next bounded observation transaction after the recorded eligibility time.

This prevents broad rediscovery and repeated matrix polling while preserving the distinction between `WAITING_EXTERNAL` and `BLOCKED`.

### 3.8 Review and role guard

Review gates bind exact head/tree/base and reviewed artifact set to review record, reviewer identity, recorded role/session, and disposition. Candidate mutation emits invalidation events before a new transition can use old approval or checks. `H1` evidence remains historical but cannot settle `H2` gates.

The role guard proves only what durable evidence supports. It validates distinct recorded role/session identifiers and non-author review identity where required. Shared-account ambiguity is retained as an attribution limitation rather than converted into a false physical-actor claim.

### 3.9 Conformance harness

The harness has four layers:

1. closed-schema and hostile semantic mutation tests;
2. reducer determinism and authority-precedence fixtures;
3. stateful scenario tests with crash injection at every transaction fault point; and
4. reproducible fresh-process/fresh-session runs with chat and private memory absent.

The T1-T14 matrix in `CONTROL_PLANE_REQUIREMENTS.md` is mandatory. Tests must bind exact implementation head, transition-catalog digest, fixture digest, and result. CI reachability is checked from the protected workflow entry point; a local validator that is not invoked by governed CI is not acceptance evidence.

## 4. State model

Lifecycle state and domain phase are separate. The generic lifecycle is:

- `UNADMITTED`: no capability/topology admission;
- `READY`: admitted, no transaction or wait, at least one derived transition;
- `TRANSACTION_OPEN`: one transaction in `PREPARED`, `APPLYING`, or `RECONCILING`;
- `WAITING_EXTERNAL`: no mutating transaction; exact wait objects and observation transition exist;
- `CHOICE_REQUIRED`: policy permits multiple choices and records the authorized selection mechanism;
- `BLOCKED`: a named genuine boundary is evidenced;
- `TERMINAL`: terminal condition and required readback are settled.

Domain phases such as authoring, validation, review, authorization, integration, and readback are catalog-defined. They are not arbitrary strings.

Invariants:

- at most one open mutating transaction;
- no concurrent unexpired executor claims;
- `TRANSACTION_OPEN` has write-ahead intent and probes;
- `WAITING_EXTERNAL` has exact wait identities and is not a blocker;
- `BLOCKED` names an allowed boundary and required authority/condition;
- `TERMINAL` has no open transaction/wait and carries terminal evidence;
- every state is reproducible from the event log;
- every stored transition decision matches reducer output; and
- every authority-bearing transition consumes current exact gates.

## 5. Representative transition set

The implementation should begin with the smallest transition catalog needed by the pilot:

- `ADMIT_WORK_PACKAGE`
- `DECOMPOSE_FOR_RESUMABILITY`
- `CLAIM_BOUNDED_TRANSACTION`
- `MUTATE_CANDIDATE_BRANCH`
- `DISPATCH_EXACT_HEAD_CI`
- `OBSERVE_EXTERNAL_WAIT`
- `RECONCILE_INTERRUPTED_MUTATION`
- `RECORD_CHECK_SETTLEMENT`
- `REQUEST_EXACT_HEAD_REVIEW`
- `RECORD_EXACT_HEAD_REVIEW`
- `INVALIDATE_SUPERSEDED_GATES`
- `REQUEST_RESERVED_AUTHORIZATION`
- `RECORD_RESERVED_AUTHORIZATION`
- `EXECUTE_AUTHORIZED_INTEGRATION`
- `VERIFY_PROTECTED_READBACK`
- `RECONCILE_CURRENT_VERSION_PROJECTION`
- `DECLARE_NAMED_BOUNDARY`
- `CLOSE_WORK_PACKAGE`

This is a catalog seed, not permission to perform every transition. Each repository/profile may expose only applicable transitions, and reserved transitions remain unavailable without their authority gate.

## 6. Interrupted mutation examples

### Branch update

Before push, prepare the intended old head, new commit/tree, ref, lease, and probe “does ref equal new head?” If the agent dies after push, replacement reads the ref. Exact match permits committing the transaction; old-head match permits replay subject to the recorded rule; any third head is material drift and blocks/rebases only through a new authorized transition.

### CI dispatch

Prepare workflow/ref/head and idempotency correlation. After interruption, query runs created for the exact head and correlation window/key. One matching run commits dispatch; none allows replay if policy permits; multiple ambiguous runs enter reconciliation and cannot be treated as settled evidence.

### Review

Review request is separate from review settlement. The gate stores review ID and `commit_id`. A new candidate head immediately invalidates settlement. Request delivery alone never creates approval.

### Merge/integration

Prepare exact PR head/base, required checks/reviews/authorization, merge method, and expected parentage. Immediately recheck all identities, execute only under recorded authorization, then probe PR state, merge commit, parentage, and protected-head readback. Interruption never converts a prepared merge into authorization.

## 7. PR #702 assessment

PR #702 contains useful prototype ideas:

- a registry and closed schemas;
- exact candidate/run identities;
- explicit no-chat/fresh-session intent;
- external-wait versus boundary distinction;
- claim/merge/certification boundaries fixed false;
- validator reachability through the policy shard; and
- correction of the programme guide's stale `0.2.0` statement.

Those ideas should be retained where they survive independent implementation review. The candidate is not sufficient as the remediation because:

- it stores one mutable latest checkpoint rather than an append-only, compare-and-swap transaction ledger;
- it has no write-ahead open transaction, effect probe, idempotency class, executor claim, or inside-mutation reconciliation semantics;
- `fresh_session_safe: true` and prose resume instructions are self-assertions, not demonstrated reducer properties;
- phase and action descriptions are free-form and permitted actions are operator-authored rather than derived;
- it has no capability/topology admission or persistent-controller rejection;
- it does not model authority precedence or active-version propagation;
- review/check exact-subject validity and invalidation are incomplete;
- wait object statuses and instructions are mostly prose and lack wake/backoff identity;
- updating checkpoint state on the governed candidate path risks head churn and review/check invalidation;
- tests cover schema mutations but not T1-T14 replacement, coordinator death, crash points, stale chat, or transaction replay; and
- green checks and exact-head approval establish only that candidate's declared tests passed, not architectural sufficiency.

Disposition: treat PR #702 as a prototype input. Supersede or substantially revise it after this design is independently approved; obtain fresh exact-head Adversary, Referee, and reserved authorization evidence. Its existing approval must not carry to changed bytes.

## 8. Rejected alternatives

### More operator prose or a checklist

Rejected. It repeats the demonstrated prose-level enforcement defect and cannot survive agent death or choose a transition deterministically.

### Chat summaries as checkpoints

Rejected. They are unavailable to fresh agents, mutable, lower precedence, and cannot participate in compare-and-swap or exact-subject validation.

### One mutable checkpoint JSON

Rejected as the canonical mechanism. It is useful as a derived snapshot but cannot distinguish overwrite, incomplete update, or mutation-before-checkpoint without an immutable write-ahead event history.

### State on the candidate branch

Rejected. Every wait observation changes candidate head, invalidating the checks/reviews being observed and causing recursive CI churn.

### Issue body, PR description, comment, Project, or dashboard as authority

Rejected. These may index or mirror state, but are mutable platform projections beneath protected records and lack the required transactional semantics.

### Update the checkpoint only after side effects

Rejected. Agent death between effect and checkpoint makes completion indistinguishable from non-execution. Write-ahead intent plus effect probes is required.

### Claim cross-repository atomicity

Rejected. GitHub repositories and external services do not provide a common transaction manager. A propagation barrier and reconciled saga are honest and testable.

### Make every operation use a persistent controller

Rejected as unnecessary cost and a new availability dependency. Multi-session workflows can use replaceable bounded executors when state and transaction semantics are sufficient. Persistent control is reserved for topology that actually requires it.

### Make AETHER a correctness dependency

Rejected by the harness and existing authority separation. AETHER may later consume evidence but is not required to resume or validate control-plane state.

### Escalate every wait or interruption to the Human Steward

Rejected. It increases volunteer burden and converts operational mechanics into synthetic authority gates. Human action remains only where superior policy reserves it.

### Declare `0.3.0` immediately

Rejected. The fixed findings justify enforcement of existing intent and a scoped pilot first. Normative amendment is a later governed decision if implementation exposes an actual standards-level insufficiency.

### Mechanically copy the harness field list

Rejected. Several harness fields are semantic prompts, not the final model. For example, the canonical state digest is sufficient as the resume token; executor capability belongs to admission and transaction claims; checks/reviews need typed gate instances; and free-form selected-next-transition data must be reducer-derived.

## 9. Security, failure, and authority properties

- Loss or compromise of the control ledger cannot grant authority because all authority-bearing transitions independently resolve superior exact gates.
- Rewriting ledger history is prohibited and detectable by ref rules plus hash linkage.
- A stale ledger cannot authorize mutation: rehydration compares exact live subjects and emits drift/invalidation.
- A dead coordinator leaves no hidden role graph; dispatch and result events are durable.
- A persistent controller outage pauses only workflows classified as requiring it; it does not alter authority or terminal status.
- If the reducer/catalog changes, existing work remains bound to its recorded catalog digest until an explicit migration transition validates semantic compatibility.
- Claim-boundary fields remain false constants in control-state schemas and are rechecked semantically.

## 10. Acceptance and governance route

Implementation may be recommended only after:

1. current-version coherence repair and hostile contradiction tests pass;
2. schema, reducer, ledger, transaction coordinator, and adapters pass T1-T14;
3. a representative multi-session pilot survives fresh-process and injected-crash runs;
4. CI/workflow reachability is proven on the exact candidate head;
5. an independent Adversary attacks exact-head state;
6. a distinct-session Referee issues an exact-head bounded disposition;
7. any reserved Human Steward authorization is recorded for that exact head; and
8. protected integration and readback occur through the applicable route.

Passing this route establishes only the scoped remediation disposition. It does not itself admit a standard successor or widen any authority.
