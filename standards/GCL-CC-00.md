# GCL-CC-00: Core Clarity Campaign Control

**Version:** 0.1.0  
**Status:** Candidate normative standard; no cross-programme effect until protected admission and programme adoption  
**Constitutional source:** `grandchallenge/INTELLECT/CONSTITUTION.md`  
**Compatible operating standards:** `GCL-GHOS-00`, `GCL-CEX-01`  
**Registry:** `grandchallenge/gcl-standards`  
**Council issue:** `grandchallenge/gcl-standards#95`  
**Scope:** Governed Grand Challenge Labs campaigns and long-horizon worksets

## 1. Purpose

CORE CLARITY is a correctness requirement.

Operational state and declared campaign state SHALL be one protected system. A campaign SHALL NOT be considered complete, coherent, or resumable merely because its underlying implementation, proof, workflow, source lock, agent dispatch, certification action, or submission action succeeded.

A competent zero-context reader SHALL be able to determine the current campaign state, active obligations, completed obligations, external-agent state, certification state, competition or external-submission state, and next permitted actions from one canonical protected control-plane surface, with every material assertion traceable to protected evidence.

## 2. Governing invariant

Every governed campaign SHALL maintain one canonical campaign-control record.

That record SHALL bind, directly or by exact protected reference:

- the campaign identity;
- all active work lanes or hill/problem slots;
- exact source/provider state;
- exact operative work state;
- active and completed bounded operations;
- external-agent lifecycle state;
- certification lifecycle state;
- competition, publication, or external-submission lifecycle state when applicable;
- known blockers and unresolved obligations;
- superseded state;
- the exact next permitted action;
- the protected repository identities from which each material state assertion is derived.

Operational or presentational drift SHALL be a blocking defect.

When drift is detected, discretionary substantive campaign advancement SHALL stop until the control plane is reconciled.

## 3. Completion contract

A governed task SHALL NOT be declared complete until all applicable completion conditions are satisfied:

1. the operative mutation is protected;
2. required checks pass;
3. protected-main readback confirms the intended state;
4. the canonical campaign state is updated;
5. the human-readable campaign view agrees with the canonical state;
6. superseded or obsolete state is explicitly retired, marked superseded, or bound as historical;
7. the next permitted action is unambiguous.

If a conversation, agent session, connector, runtime, or orchestration surface terminates before these conditions are satisfied, the task SHALL remain incomplete in protected state.

## 4. Authority and restart discipline

Conversation history, assistant memory, issue prose, and informal summaries MAY provide context. They SHALL NOT be authoritative campaign state.

After any interrupted, truncated, lost, or replaced conversational session, an executor SHALL:

1. read the canonical protected campaign state;
2. verify its protected identities;
3. inspect incomplete operation records and completion receipts;
4. reconcile durable external events since the recorded checkpoint;
5. continue exactly one authorized next operation.

An executor SHALL NOT reconstruct current campaign authority from conversational memory when protected canonical state exists.

## 5. Operational and control planes

Every campaign mutation SHALL preserve agreement between:

### 5.1 Operational plane

Examples include:

- source locks;
- work packages;
- exact candidates;
- leases;
- external returns;
- intake receipts;
- adjudication records;
- certification records;
- competition or publication submissions.

### 5.2 Control plane

The control plane SHALL include:

- the canonical machine-readable campaign state;
- the human-readable campaign view;
- bounded-operation checkpoint or successor state where applicable;
- completion/readback receipts;
- deterministic next-action state.

A protected mutation that changes material operational state without reconciling the control plane SHALL create a blocking drift state.

A subsequent substantive operation SHALL NOT begin while such drift remains unresolved.

## 6. Human-readable campaign view

A governed campaign SHALL expose one human-readable current-state view derived from, or mechanically validated against, the canonical machine-readable campaign record.

The human-readable view SHALL NOT constitute a second independently maintained source of truth.

Historical documents MAY remain immutable. When their current-state assertions are stale, they SHALL carry an explicit supersession marker or SHALL be listed in a canonical supersession registry that identifies the replacement authority.

## 7. External-agent lifecycle

External-agent work SHALL distinguish at least these lifecycle states:

`PREPARED -> LEASED -> LAUNCHED -> RETURNED -> CAPTURED -> ADJUDICATING -> ACCEPTED | REJECTED | SUPERSEDED -> CLOSED`

A campaign MAY use more specific substates, including `LEASED_NOT_LAUNCHED`, but SHALL NOT collapse distinct lifecycle stages into one ambiguous label.

In particular:

- `LEASED` SHALL NOT imply `LAUNCHED`;
- `LAUNCHED` SHALL NOT imply `RETURNED`;
- `RETURNED` SHALL NOT imply `CAPTURED`;
- `CAPTURED` SHALL NOT imply mathematical or substantive acceptance;
- intake receipt SHALL NOT imply adjudication;
- adjudication SHALL NOT imply MATHCERT certification unless MATHCERT issues that effect through an admitted route.

When launch itself is not durably evidenced, campaign state SHALL say so explicitly.

## 8. Competition and external-submission lifecycle

Competition, benchmark, publication, or other external-submission work SHALL distinguish at least:

`CANDIDATE -> LOCALLY_VERIFIED -> CERT_PENDING -> CERTIFIED -> SUBMISSION_READY -> SUBMITTED -> ACCEPTED | REJECTED`

Campaign state SHALL explicitly record when a candidate is `NOT_SUBMITTED`.

Local evaluator success, public evaluator replay, CI success, source validation, or internal certification intake SHALL NOT be described as an official submission or official competition result.

A submission state SHALL identify the exact submitted artifact and durable external receipt when one exists.

## 9. Remediation discipline

A remediation SHALL either:

1. repair the defective mechanism in place; or
2. supersede it through an explicit migration.

A remediation SHALL identify:

- the defect;
- affected artifacts;
- replacement or repair;
- migration rule;
- superseded artifacts;
- retirement status;
- completion test.

A remediation SHALL NOT create an unbounded parallel mechanism, compatibility shim, duplicate state surface, or "temporary" authority without an explicit migration and retirement rule.

A new remediation SHALL NOT be layered over an unresolved remediation unless the new bounded operation explicitly absorbs the predecessor defect and closes or supersedes it.

## 10. Drift enforcement

An adopted campaign profile SHALL mechanically check, where applicable, that:

- every active operational lane appears in canonical campaign state;
- every protected external-agent lease appears with its exact lifecycle state;
- every captured external result has an intake state and adjudication state;
- every source-locked target has the same exact identity across provider, work, and campaign state;
- every certification intake or disposition appears in campaign state;
- every competition or external submission has an explicit state;
- no `SUBMITTED` state exists without a durable receipt;
- no human-readable campaign view contradicts the canonical machine state;
- no canonical current-state assertion depends on a superseded protected identity;
- stale predecessor records are explicitly superseded;
- the declared next action is deterministic;
- substantive advancement is blocked when campaign-control freshness fails.

Drift detection SHALL fail closed for campaign advancement. It SHALL NOT fabricate, infer, or promote missing mathematical, certification, or competition state.

## 11. Cross-repository campaigns

For a campaign spanning provider, solver, certification, programme, or other repositories, the canonical campaign-control record SHALL live in the programme-owned registry or another explicitly designated authority.

Domain repositories SHALL remain authoritative for their own artifacts. The canonical campaign-control record SHALL reference their exact protected identities rather than silently copying or reinterpreting domain authority.

Cross-repository updates need not be transactionally simultaneous. However, after a material downstream protected transition:

1. canonical campaign state SHALL be reconciled before the next discretionary substantive campaign operation;
2. the unreconciled interval SHALL be represented as control-plane drift;
3. campaign preflight SHALL reject further discretionary advancement until reconciliation succeeds.

## 12. Bounded reconciliation

A reconciliation operation SHALL be bounded and auditable.

It SHALL:

- bind the exact protected states being reconciled;
- identify every detected inconsistency;
- select one replacement authority for each stale or duplicate current-state surface;
- migrate current live state into the canonical record;
- explicitly mark stale records superseded;
- preserve historical provenance;
- perform required readback;
- emit a completion receipt;
- leave a deterministic next action.

A reconciliation SHALL NOT silently rewrite historical evidence to make history appear cleaner than it was.

## 13. Relationship to GCL-CEX-01

GCL-CEX-01 governs bounded campaign execution, frontier control, operation contracts, freezes, exact-head evidence, and completion receipts.

GCL-CC-00 adds a stricter cross-operation invariant: the resolved operational state and the declared campaign-control state SHALL remain coherent at campaign boundaries.

Where both are adopted, a GCL-CEX-01 operation is not complete for campaign purposes until the GCL-CC-00 completion contract is satisfied.

## 14. Claim boundaries

This standard governs state coherence, lifecycle clarity, remediation, and campaign control.

It SHALL NOT:

- establish mathematical truth;
- certify mathematical claims;
- create constitutional authority;
- authorize publication or competition submission;
- enlarge repository mutation authority;
- create autonomous permission escalation;
- replace MATHCERT as mathematics certification authority.

## 15. Conformance statement

A campaign conforms to GCL-CC-00 only when:

- one canonical protected campaign-control record exists;
- one human-readable view is derived from or mechanically checked against it;
- operational/presentational drift is mechanically detectable;
- drift blocks further discretionary substantive advancement;
- lifecycle states are explicit;
- stale current-state records are superseded;
- bounded reconciliation leaves protected readback and completion evidence.

Documentation that merely states CORE CLARITY principles is not conformance.
