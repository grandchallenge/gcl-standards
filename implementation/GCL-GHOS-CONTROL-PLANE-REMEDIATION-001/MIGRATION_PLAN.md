# GH-OS control-plane migration plan

**Work package:** `GCL-GHOS-CONTROL-PLANE-REMEDIATION-001`  
**Role:** `CONTROL_PLANE_DESIGNER`  
**Fixed design-input commit:** `78d456ffa2e050caea7429732f3e4709cb2e66d9`  
**Status:** executed; protected reconciliation and successor-control pilot complete
**Target:** MATH-PROGRAMME pilot conformance under admitted `GCL-GHOS-00` `0.2.0`

## 1. Migration disposition

Closeout readback: the current-version reconciliation, external guide/profile
propagation, protected control-store enforcement, and successor-ref replacement
pilot are complete. The active-work inventory is recorded in
`ACTIVE_WORK_MIGRATION_INVENTORY.json`. No active item requires a persistent
controller at this readback; future topology changes remain subject to
capability admission.

Proceed in two gates: repair current-version coherence first, then pilot the durable control plane. Do not combine the coherence cure, generic control-plane implementation, migration of every active work package, and any normative-successor proposal into one review subject.

There is no justification for a programme-wide or organization-wide shutdown. A targeted hold is required for work whose correctness currently depends on missing control state.

### Continue

- read-only evidence gathering and exact-state reconstruction;
- bounded atomic work with no external wait and a safe reconciliation route;
- already-authorized diagnostics and non-destructive replay;
- unrelated mathematical work that does not rely on the contradictory GH-OS projection; and
- preparation of candidate remediation artifacts without protected mutation.

### Pause at the next atomic boundary

- new long-running governed work that has not passed topology/capability admission;
- multi-session work whose open transaction, exact gates, waits, or next transition exist only in chat;
- irreversible or authority-bearing transitions that rely on the stale `0.1.1` projection;
- merge, terminal closure, or completion claims where exact-head reviews/checks/readback cannot be reconstructed durably; and
- any work classified `PERSISTENT_CONTROLLER_REQUIRED` when no persistent controller is assigned.

Paused work may be rehydrated and inventoried. It resumes only after a durable provisional state is created and validated or after decomposition into bounded atomic work.

PR #702 should remain unmerged as a claimed full solution. Its useful prototype elements may be rebased into the independently approved design, but its existing exact-head approval does not apply to changed bytes.

## 2. Migration principles

1. Preserve immutable admissions, historical receipts, and historical `next_gate` values.
2. Resolve authority before updating projections; never make a projection the source of current authority.
3. Separate current-version repair from transaction-control rollout so each failure mode has a clear acceptance oracle.
4. Keep control-ledger updates off candidate code branches.
5. Migrate active work by exact inventory and explicit state reconstruction; do not fabricate missing completion evidence.
6. Fail closed on authority-bearing actions, not on authorized diagnosis or reconciliation.
7. Require exact-head fresh review after every design or implementation change.
8. Preserve an exit path: the pilot can be removed without rewriting authoritative programme records if it fails acceptance.

## 3. Phase 0 — immediate containment and authoritative coherence

### Objective

Remove the false-current split before relying on GH-OS current projections.

### Candidate change set

In separately governed implementation work:

- introduce one effective-authority resolver anchored to `programme-adoption/MATH-PROGRAMME.yaml` and `admissions/GCL-GHOS-00-0.2.0.json`;
- change current-selection schemas from independent `0.1.1` constants to validation of the resolver's exact `0.2.0` selection;
- update `status/GCL-GHOS-00-current.json` as a derived projection of that selection;
- classify immutable `0.1.1` admission/receipt evidence as historical rather than current;
- remove validator clauses that require README/ADR/front matter to describe `0.1.1` as current or reject active `0.2.0` wording;
- correct the MATH-PROGRAMME recovery guide's current-authority statement through its own protected route;
- add a propagation manifest covering every current-version consumer; and
- add a hostile fixture proving superior `0.2.0` adoption plus subordinate `0.1.1` projection fails with exact-source diagnostics.

ADR-0001 may retain historically scoped `0.1.1` successor text, but any unqualified “current” wording must be corrected or explicitly marked historical. The `0.2.0` admission record remains unchanged.

### Exit criteria

- one resolver identifies `0.2.0` as the active MATH-PROGRAMME selection;
- all derived-current consumers agree or validation fails closed;
- historical validators still verify immutable `0.1.1` and `0.2.0` identities without asserting current status;
- no test positively requires a superseded current assertion;
- cross-repository guide/status evidence is exact-source bound; and
- protected readback records zero open current-version contradictions.

### Cost

**Medium, bounded.** Expected scope is two governed repositories, one resolver/propagation manifest, the existing current-selection schemas/status record, several validators/tests, and current-status prose. Review cost is dominated by exact cross-repository evidence and protected readback, not code volume.

## 4. Phase 1 — control-plane kernel

### Objective

Implement the smallest reusable machinery required for deterministic resume and interrupted-transaction reconciliation.

### Candidate components

- closed schemas for work-package admission, ledger events, derived snapshot, typed gates, waits, executor claims, and transactions;
- a versioned transition catalog;
- deterministic authority resolver and state reducer;
- append-only hash-chain validation and compare-and-swap writer;
- capability/topology admission;
- write-ahead transaction and reconciliation engine;
- Git/GitHub exact-observation adapter;
- review/check invalidation rules; and
- workflow reachability from the protected policy CI entry point.

Use a work-package-specific control ref with force/deletion prohibition. If repository rules cannot enforce that storage topology, stop at a protected-state/design boundary and select an equivalently durable append-only store; do not silently fall back to issue comments or candidate-branch checkpoint files.

### Exit criteria

- reducer outputs are deterministic for fixed inputs;
- competing ledger writers fail compare-and-swap without history loss;
- each mutating transition has write-ahead intent, replay class, and authoritative effect probe;
- interruption at every prepare/apply/observe/commit fault point is unambiguous;
- stale review/check evidence is mechanically invalidated; and
- schemas and semantic hostile-mutation tests agree.

### Cost

**Medium-high.** This is new enforcement code and test infrastructure, but it is intentionally limited to Git/GitHub and the MATH-PROGRAMME pilot. A generic distributed workflow engine, UI, and AETHER integration are excluded.

## 5. Phase 2 — T1-T14 conformance harness

### Objective

Demonstrate behavior, not phrase presence.

### Work

- create a stateful scenario runner with deterministic fake GitHub objects and fault injection;
- encode branch mutation, CI dispatch/settlement, review, authorization, merge, and readback scenarios;
- crash the executor before and after every material event;
- run fresh-process/no-chat resume and coordinator replacement;
- inject stale conversation, stale reviews, stale diagnostics, version contradictions, unauthorized transitions, and capability mismatch;
- record exact expected transition IDs, state digests, invalidations, and prohibited authority outcomes; and
- prove the harness is invoked by governed CI.

T1-T14 mapping and oracles are defined in `CONTROL_PLANE_REQUIREMENTS.md`. A single hand-written live checkpoint does not satisfy this phase.

### Exit criteria

- all T1-T14 scenarios pass on the exact candidate head;
- the test packet records transition-catalog and fixture digests;
- a fresh process can resume without chat/private memory;
- coordinator death does not lose the role graph or pending work; and
- no passing test infers approval, certification, merge authority, or claim status.

### Cost

**Medium-high.** Crash matrix size, not schema construction, is the principal cost. Keep fixtures representative and combinatorial state bounded by transition type.

## 6. Phase 3 — one shadow-mode pilot

### Objective

Validate the control plane against a real multi-session governed workflow without making it the sole authority-bearing executor.

### Selection criteria

Choose one active MATH-PROGRAMME work package that:

- has external CI waits and candidate-head changes;
- does not require uninterrupted sub-minute response;
- has clear issue/PR/check/review identities;
- has no unresolved ambiguity in its governing authority; and
- can be safely mirrored without changing mathematical or certification status.

Do not choose a workflow whose current state cannot be reconstructed. Such a workflow first needs a governed reconciliation record with unknowns left explicit.

### Shadow operation

- create and protect the work-package control ref;
- admit topology and capabilities;
- reconstruct initial state from exact evidence and label inferred/unknown facts;
- run the reducer in parallel with existing authorized operations;
- compare every predicted transition and gate invalidation with observed action;
- inject at least one planned executor replacement and one interrupted non-authority-bearing mutation in a sandbox/fixture route; and
- retain discrepancy events rather than editing history.

### Exit criteria

- no transition depends materially on chat;
- no candidate/check/review identity is lost or silently carried forward;
- replacement resumes directly from ledger state;
- observation volume and operator burden are acceptable; and
- discrepancies are zero or dispositioned before authority-bearing cutover.

### Cost

**Medium per first pilot; low-medium thereafter.** Initial cost includes evidence reconstruction and storage/ruleset setup. Subsequent work packages should require an admission record and initial state rather than new machinery.

## 7. Phase 4 — guarded pilot cutover

### Objective

Make the control plane mandatory for the selected MATH-PROGRAMME workflow class only.

### Cutover gates

- successful shadow pilot;
- exact-head Adversary findings resolved or explicitly accepted by the proper authority;
- distinct-session Referee disposition on the same head;
- any required Human Steward authorization bound to that exact head;
- protected integration and policy-workflow reachability;
- protected-main readback; and
- a rollback procedure tested against non-authority state.

At cutover, work-package admission blocks new multi-session workflow execution unless a valid control ledger exists. Existing bounded atomic work remains outside the ledger unless its topology changes.

### Rollback

Rollback may disable admission of new controlled work and revert the scoped enforcement integration through the governed route. It SHALL NOT delete ledger history, rewrite authority records, revalidate stale reviews, or mark open work complete. Existing ledgers become retained evidence and work returns to a named hold until another safe controller is admitted.

### Cost

**Medium governance cost, low code delta after pilot.** Independent review and protected readback are mandatory.

## 8. Phase 5 — active-work migration

### Inventory

For each active governed work package, record:

- governing authority and issue;
- repositories, branches, PRs, protected bases, and exact heads;
- open/last mutation and whether its effect is provable;
- required and settled gates with exact subjects;
- external waits and exact objects;
- role assignments and reserved decisions;
- topology/capability classification; and
- next reducer-derived transition or named boundary.

### Migration classes

- **A — bounded atomic:** no control ledger required unless scope changes.
- **B — reconstructable multi-session:** create an admission event and initial snapshot from exact evidence; resume after validation.
- **C — interrupted/ambiguous transaction:** create a reconciliation transaction; perform read-only effect probes; do not assert completion until resolved.
- **D — persistent controller required:** assign controller or decompose; remain paused.
- **E — human decision required:** preserve durable state and present one exact, role-specific action to the named authority.

Unknowns remain explicit. A migration record cannot retroactively manufacture a transaction intent, review, authorization, or terminal receipt.

### Cost

**Variable by active-work count.** Class A is negligible; Class B is a bounded evidence inventory; Class C can be expensive because side effects must be reconciled; Class D may require infrastructure and is intentionally not hidden inside the minimum pilot.

## 9. Phase 6 — evaluate normative successor need

After at least one guarded pilot and active-work sample, produce a governed evaluation answering:

- Are durable transaction state and capability admission a reasonable enforcement interpretation of `0.2.0`, or do they add cross-programme duties?
- Can other programmes adopt the profile without changing the standard?
- Did the storage/capability model create a new authority or custody requirement?
- Are any invariants impossible to enforce programme-locally?

If the answers demonstrate a standards-level change, prepare a normative successor through exact-head Adversary, Referee, Human Steward, admission, adoption, and readback routes. Otherwise retain the implementation as a versioned programme conformance profile.

No organization-wide rollout occurs from pilot success alone.

## 10. PR #702 migration handling

Treat PR #702 as an untrusted prototype branch.

Retain, subject to fresh implementation review:

- registry discovery;
- exact candidate/run identities;
- false authority boundaries;
- policy-shard reachability;
- explicit no-chat intent; and
- recovery-guide correction.

Replace or redesign:

- mutable latest-checkpoint storage;
- state on candidate paths;
- free-form phase/action semantics;
- self-attested fresh-session safety;
- missing capability admission;
- missing write-ahead/reconciliation state;
- incomplete review/check invalidation;
- prose wait objects; and
- mutation-only tests that do not exercise T1-T14.

Any reuse creates a new candidate head. Re-run all governed checks and obtain fresh exact-head independent review. Do not carry forward the approval attached to `67823169e40947352dffc1e82b65f51bc7b6989c`.

## 11. Cost and volunteer-burden assessment

| Area | Relative cost | Burden control |
| --- | --- | --- |
| Active-version coherence cure | Medium | One resolver and propagation manifest replace repeated manual audits. |
| Ledger/reducer/transaction kernel | Medium-high | Build once; keep GitHub-only and programme-scoped. |
| T1-T14 harness | Medium-high | Reusable scenarios avoid repeated subjective agent reviews of basic semantics. |
| First shadow pilot | Medium | Choose one representative workflow and avoid authority-bearing cutover. |
| Each reconstructable work migration | Low-medium | Generate inventory from exact sources; ask humans only for reserved decisions. |
| Persistent controller, if actually required | High | Decompose where safe; do not impose this cost on resumable work. |
| Independent governed admission/readback | Medium | One exact packet and one role-specific Human Steward action where required. |

The design reduces ongoing volunteer burden by making transition selection, stale-evidence rejection, and wait resumption mechanical. It does not transfer reserved judgment to automation.

## 12. Migration risks and controls

| Risk | Control |
| --- | --- |
| Ledger becomes a new authority source | Re-resolve superior exact authority before every authority-bearing transition; fix all authority flags false. |
| Ledger update invalidates candidate review | Store ledger on a separate control ref. |
| Concurrent agents duplicate mutation | Compare-and-swap, executor claim, write-ahead intent, idempotency class, and effect probe. |
| Historical record is rewritten to look current | Classify historical consumers and preserve immutable admissions/receipts. |
| Cross-repository propagation is called atomic | Use an explicit saga/barrier and keep activation incomplete until readback. |
| Schema passes but behavior fails | Require semantic hostile mutations and crash-injection T1-T14. |
| Persistent controller becomes universal dependency | Admit it only when topology requires uninterrupted wake/lease behavior. |
| Shared account is misrepresented as actor separation | Record role/session evidence and disclose residual attribution ambiguity. |
| Migration invents missing state | Preserve unknown/ambiguous status and require reconciliation probes. |

## 13. Completion criteria

Migration is complete only for the scoped pilot when:

1. active-version contradictions are zero on protected readback;
2. the control-plane implementation passes T1-T14 at the exact reviewed head;
3. one representative workflow has completed shadow mode and guarded cutover;
4. applicable active work is classified and migrated or explicitly held;
5. independent Adversary and Referee records bind the exact implementation;
6. reserved authorization and protected integration/readback are complete where required; and
7. closure language states the exact pilot scope and preserves all claim boundaries.

This does not establish a normative successor or organization-wide conformance.
