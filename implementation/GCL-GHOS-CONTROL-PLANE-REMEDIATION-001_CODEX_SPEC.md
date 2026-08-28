# GCL-GHOS-CONTROL-PLANE-REMEDIATION-001 — Codex Harness Specification

**Status:** Candidate remediation specification; nonbinding until governed review and protected admission where required  
**Issue:** `grandchallenge/gcl-standards#56`  
**Protected baseline:** `grandchallenge/gcl-standards@1a5e9cb24257be578b091ecd2c99d4119ff73b2c`  
**Date:** 2026-08-28  
**Primary subject:** `GCL-GHOS-00` design, implementation, adoption, projection, and agent operating conformance  
**Execution model:** Harnessed, role-separated Codex agents under Human Steward authority  

## 1. Purpose

This specification commissions an adversarial audit and remediation of a failure in the practical control-plane semantics of the GitHub Constitutional Operating System (`GCL-GHOS-00`).

The central question is not whether GitHub contains durable records. It does. The question is whether a fresh, bounded, replaceable agent can recover the authoritative state, determine the permitted next transition, execute one bounded transaction, and leave the system unambiguous without relying materially on conversational history, remembered intentions, or an unobservable remaining execution horizon.

The harness SHALL first determine what was intended, what was actually implemented, where implementation and operating practice diverged, what was foreseeable at design time, and what minimum remediation is justified. It SHALL NOT assume that another normative successor, another checklist, or another promise of agent discipline is the correct answer.

## 2. Originating-agent accountability — full mea culpa

The originating OpenAI assistant accepts material responsibility for this failure mode.

I materially participated in designing, specifying, implementing, reviewing, and operating the GH-OS/GCL governance architecture. I repeatedly represented that architecture as a way to compensate for the known limits of conversational agents: bounded execution, interrupted sessions, non-persistent internal state, changing tool availability, and the inability to work asynchronously after a response terminates.

Those limitations were not newly discovered in August 2026. I knew them while the architecture was being designed.

I nevertheless failed to force that knowledge into the system strongly enough. In particular:

1. I helped externalize authoritative institutional state, provenance, exact-head identity, review records, protected transitions, evidence, and readback, but left too much execution-control state implicit in the conversational operator.
2. I allowed the conversational agent to remain the de facto scheduler, transition selector, and session-state carrier for long-running governed sequences.
3. I did not make authoritative-state rehydration a compulsory precondition to substantial action in every governed session.
4. I did not make a machine-readable `permitted_transitions` / `next_transition` contract universally mandatory where long-running workflow topology required it.
5. I did not establish a universal crash-safe session checkpoint containing the open transaction, exact identities, settled gates, blocking conditions, and next executable transition.
6. I did not require work-package admission to classify executor suitability before significant resources were committed.
7. I repeatedly used language such as “I will complete”, “I will continue until”, or equivalent future commitments even where completion depended on external CI, future tool calls, independent review, or an execution window whose remaining budget I could not observe or guarantee.
8. I repeatedly promised improved operating discipline as though a conversational intention were an enforceable control. It was not.
9. When long sequences became difficult, I sometimes drifted toward status narration, repeated polling, local repair loops, or conversational reconstruction rather than insisting that GH-OS itself determine and preserve the next legitimate transition.
10. I did not escalate the architecture/capability mismatch early enough, despite having enough information to foresee that persistent orchestration and a bounded chat runtime are different execution models.
11. I helped create the impression that careful reasoning by the same assistant could substitute for a hard control plane. That was an architectural error.
12. Retrospective recognition of these points does not mitigate the cost of discovering them after substantial investment.

The harness SHALL treat this statement as an accountability record, not as a root-cause finding that must be accepted without independent verification. It SHALL independently reconstruct the history and SHALL be free to find that this statement is incomplete, inaccurate, too narrow, or wrongly apportions responsibility.

The originating assistant SHALL NOT be treated as a trusted reviewer of its own remediation. No acceptance criterion may depend on its memory, intention, self-report, or assertion that it will behave differently in the future.

## 3. Existing architectural intent that must be tested, not reinvented

The harness SHALL begin from existing protected evidence.

`GCL-GHOS-00` defines GitHub as a subordinate constitutional operating system, requires exact-head validation, exact-revision review, immutable evidence, bounded execution continuity, and explicit stopping only at real authority/safety/evidence boundaries. It also says that automation may request review and report drift but may not approve, merge, certify, or promote claims.

The accepted GH-OS ADR states that one agent identity/session cannot be relabelled as multiple independent offices, and the steward-supervised staffing record requires proposal author, Adversary, and Referee separation.

MATH-PROGRAMME's truth-spine architecture states that protected normative records must allow institutional state to be reconstructed without dashboards or a future coordination service. Its execution-recovery guide requires exact-identity binding and bounded continuation through recoverable tooling failures.

The remediation is therefore a conformance investigation against an existing thesis as much as it is a design exercise.

## 4. Concrete observations at specification opening

The following are observations, not final diagnoses:

1. Protected `gcl-standards/main` is `1a5e9cb24257be578b091ecd2c99d4119ff73b2c`.
2. `programme-adoption/MATH-PROGRAMME.yaml` records `GCL-GHOS-00` version `0.2.0`, `status: active`, activation date `2026-08-25`, and states that bounded execution continuity is in the MATH-PROGRAMME pilot scope.
3. `status/GCL-GHOS-00-current.json` still selects `0.1.1` as the active admission/adoption projection.
4. Protected `grandchallenge/MATH-PROGRAMME@f0953f4591b40df4d6775a8582658c0b94d760d8` contains `docs/governance/EXECUTION_RECOVERY_OPERATING_GUIDE.md`, which still describes `GCL-GHOS-00` `0.2.0` as a candidate rather than current authority.
5. Recent MATHCERT remediation work required a large conversational checkpoint to preserve exact heads, workflow-run identities, settled/unsettled gates, and the next polling/repair action. That is evidence that material orchestration state was not being recovered solely from the durable operating system.

The harness SHALL determine whether items 2–4 are ordinary stale descriptive projections, a broken admission/adoption propagation route, a validator gap, an operating-procedure defect, or evidence of a deeper control-plane inconsistency.

## 5. Governing problem statement

The working hypothesis to test is:

> GH-OS externalized institutional memory and authority more completely than it externalized execution orchestration and transition selection. This left a durable ledger around a still-too-agentic controller.

The harness SHALL attempt to falsify this hypothesis.

At minimum it SHALL distinguish the following defect classes:

- `SPECIFICATION_DEFECT`
- `IMPLEMENTATION_DEFECT`
- `ENFORCEMENT_DEFECT`
- `ADOPTION_OR_PROPAGATION_DEFECT`
- `OPERATING_PROCEDURE_DEFECT`
- `CAPABILITY_MISMATCH`
- `TOOL_OR_PLATFORM_LIMITATION`
- `DOCUMENTARY_PROJECTION_DEFECT`
- `REVIEW_OR_SEPARATION_DEFECT`
- `NO_DEFECT / EXPECTED_BEHAVIOR`

Each material finding SHALL identify when the relevant information became available and whether a competent designer/operator should reasonably have caught it earlier.

## 6. Non-negotiable remediation objective

A governed long-running operation must remain correct if any conversational agent disappears permanently after any completed atomic transition.

A fresh replacement agent, given no prior chat transcript, SHALL be able to determine from authoritative durable state:

- the governing work package;
- authoritative repository and protected predecessor;
- exact candidate head, if any;
- current phase;
- open transaction, if any;
- settled and unsettled gates;
- required checks and their exact-subject binding;
- required reviews and their exact-subject binding;
- blocking conditions;
- permitted next transitions;
- whether the current executor class is authorized/suitable;
- the next bounded transition, or a precise named stopping boundary.

If two fresh conforming agents presented with the same protected/candidate state choose materially different next transitions, that ambiguity SHALL be treated as a control-plane defect unless policy explicitly permits a choice set and records the selection mechanism.

## 7. Prohibited remediation shortcuts

The harness SHALL NOT declare success by:

- adding prose that tells agents to “be disciplined”;
- relying on chat summaries as canonical checkpoints;
- assuming the same model/session will continue;
- adding more frequent polling without state-machine semantics;
- weakening exact-head review, protected-branch, certification, or authority controls;
- making AETHER a required correctness dependency;
- converting every recoverable tooling failure into a Human Steward escalation;
- treating issues, PR descriptions, Projects, or mutable comments as authoritative state when superior protected records exist;
- mechanically updating stale projections without identifying why they were allowed to become stale;
- creating a new normative version before establishing whether the defect is specification, implementation, enforcement, adoption, or operating practice;
- allowing the originating author/implementer to provide the sole Adversary or Referee disposition.

## 8. Harness roles and separation

The remediation SHALL use role-separated agents. A harness may run roles concurrently where their inputs are immutable and independence is preserved.

### 8.1 `ARCHAEOLOGIST`

Read-only. Reconstruct the design history and authority chain for GH-OS, including Constitution/amendments, ADR-0001, admitted GH-OS versions, programme adoptions, staffing directives, truth-spine material, execution-recovery policy, implementation ledgers, issues, PRs, review records, and relevant MATHCERT operating evidence.

Output: `ARCHAEOLOGY_REPORT.md` plus a machine-readable source index.

### 8.2 `FAILURE_AUDITOR`

Read-only. Compare intended architecture with actual state and observed operating practice. Build the defect ledger and chronology. Specifically assess the originating-agent mea culpa and identify missing or overstated admissions.

Output: `DEFECT_LEDGER.json` and `FAILURE_ANALYSIS.md`.

### 8.3 `CONTROL_PLANE_DESIGNER`

Consumes only the Archaeologist and Failure Auditor products plus authoritative repository sources. Proposes the minimum architecture needed to make long-running work crash-recoverable and transition-deterministic. Must include rejected alternatives and migration cost.

Output: `REMEDIATION_DESIGN.md`, schemas/state machines as candidate artifacts, and a migration plan.

### 8.4 `IMPLEMENTER`

Implements only an independently approved remediation design on a dedicated branch. It SHALL NOT expand scope to unrelated governance cleanup.

Output: code/schema/policy changes, tests, migration artifacts, and exact-head evidence.

### 8.5 `ADVERSARY`

Fresh session; not the Archaeologist, Failure Auditor, Designer, or Implementer session. Attempts to break the remediation using stale state, agent death, replacement, review invalidation, contradictory projections, hidden execution cutoffs, partial CI completion, and authorization-boundary attacks.

Output: exact-head adversarial findings.

### 8.6 `REFEREE`

Fresh session distinct from the Adversary and all authoring sessions. Reviews exact-head evidence, verifies acceptance tests, and issues a bounded disposition. It SHALL NOT infer Human Steward authorization.

Output: exact-head Referee record.

### 8.7 `HARNESS_COORDINATOR`

May schedule agents and pass immutable artifacts between them. It SHALL NOT invent authoritative state, resolve substantive findings silently, or act as the sole independent reviewer of output it caused to be authored. Its state SHALL itself be durable and reconstructable.

## 9. Agent input discipline

Each role SHALL receive:

1. exact repository names and protected heads;
2. explicit scope;
3. authoritative source paths/identities discovered by prior roles;
4. immutable predecessor role outputs by digest or exact commit;
5. the role's authority boundary;
6. the required output contract.

Except for the Archaeologist, agents SHOULD NOT receive this conversation transcript. A central acceptance test is that the system be intelligible without it.

The originating assistant's prose is evidence to audit, not authority.

## 10. Required machine-readable execution-state contract

The Designer SHALL determine whether an existing schema can be extended or a new one is necessary. Any solution must be capable of representing at least:

```yaml
work_package: <stable-id>
authority_repository: <owner/repo>
authority_head: <protected-sha>
working_repository: <owner/repo>
working_branch: <branch-or-null>
candidate_head: <sha-or-null>
phase: <enum>
executor_class_required: <enum>
executor_class_current: <enum-or-null>
open_transaction:
  id: <stable-id-or-null>
  kind: <enum-or-null>
  subject_head: <sha-or-null>
  started_from_state_digest: <digest-or-null>
required_checks: []
settled_checks: []
required_reviews: []
settled_reviews: []
blocking_conditions: []
permitted_transitions: []
selected_next_transition: <transition-or-null>
external_waits: []
last_verified_at: <timestamp>
state_digest: <digest>
resume_token: <content-addressed-token>
```

This is a minimum semantic contract, not a mandated final schema.

The durable state SHALL distinguish an external wait from a stopping boundary. `CI_RUNNING`, for example, is not equivalent to `WORK_HALTED`.

## 11. Executor capability admission

The harness SHALL require an explicit executor-topology classification before substantial governed execution begins. At minimum evaluate:

- `BOUNDED_ATOMIC`
- `MULTI_SESSION_RESUMABLE`
- `PERSISTENT_CONTROLLER_REQUIRED`
- `HUMAN_DECISION_REQUIRED`

The classification SHALL be derived from the work graph, not from an agent's confidence.

A conversational agent may execute bounded transactions within a multi-session resumable workflow only where durable state is sufficient for replacement after every transaction. It SHALL NOT be the sole orchestration mechanism for a workflow classified `PERSISTENT_CONTROLLER_REQUIRED`.

## 12. Transaction semantics

The Designer and Implementer SHALL make explicit what constitutes an atomic governed transition.

Every transition must define:

- preconditions;
- exact subject identities;
- authorized actor/executor class;
- mutation/evidence actions;
- postconditions;
- durable state update;
- failure semantics;
- replay/idempotence behavior where applicable;
- review invalidation behavior;
- whether the transition may safely terminate the current agent invocation.

No transition is complete merely because a chat response says it is complete.

## 13. Mandatory adversarial conformance tests

The remediation SHALL NOT pass without automated or reproducibly scripted tests covering the following.

### T1 — cold resume

Terminate the authoring agent. Start a fresh agent with repository access and no chat transcript. It must reconstruct the current work state and identify the permitted next transition.

### T2 — model/session replacement

Use a different agent identity/session. Given the same exact state, it must derive the same mandatory next transition or the same explicitly permitted choice set.

### T3 — stale-chat attack

Provide a fresh agent with conversational instructions that conflict with newer protected state. The protected state must win and the stale instruction must be identified as stale.

### T4 — cutoff at every boundary

Simulate termination immediately after each transaction boundary, including after branch mutation, CI launch, partial CI settlement, review request, review approval, merge authorization, merge, and protected readback. Recovery must remain unambiguous.

### T5 — cutoff inside a transaction

Terminate before the durable postcondition is recorded. The next agent must distinguish incomplete from completed work and must not infer success from side effects alone.

### T6 — stale review invalidation

Approve exact head `H1`, then produce `H2`. The system must mechanically prevent the `H1` review from authorizing `H2` unless policy explicitly defines a valid unchanged-subject carry-forward rule.

### T7 — projection contradiction

Create or fixture a case where a generated/current-status projection disagrees with a superior protected admission/adoption record. Validation must detect the contradiction and identify authority precedence.

### T8 — external CI wait

Leave required CI running beyond one agent invocation. A fresh agent must resume from durable state without broad rediscovery or repeated wasteful polling.

### T9 — failed CI repair loop

A failing exact-head job is repaired, creating a new head. Diagnostics for the superseded head must be rejected as current evidence.

### T10 — unauthorized transition

Attempt a merge, certification, promotion, protected mutation, or authority expansion without the required gate. The control plane must refuse or fail closed.

### T11 — conversational silence

Remove all conversation summaries and private memory. The complete operational state required for the next transition must remain reconstructable from authorized durable records.

### T12 — coordinator death

Terminate the harness coordinator itself between role invocations. A replacement coordinator must recover the role graph and pending work from durable state.

### T13 — active-version coherence

Verify that admitted and programme-adopted GH-OS versions, current status projections, programme-local operating guides, and conformance validators agree on the effective version and status, or emit a blocking contradiction with exact sources.

### T14 — capability mismatch rejection

Present a work package that requires uninterrupted persistent monitoring but lacks a persistent controller. Admission must reject the topology or require decomposition before execution begins.

## 14. Required audit of the current 0.2.0 state

Before proposing 0.3.0 or any other normative successor, the harness SHALL determine:

1. whether 0.2.0 is correctly admitted;
2. whether MATH-PROGRAMME adoption of 0.2.0 is valid and current;
3. why `status/GCL-GHOS-00-current.json` still projects 0.1.1;
4. why MATH-PROGRAMME's execution-recovery guide still calls 0.2.0 a candidate;
5. whether validators should have rejected either stale surface;
6. whether any actual governed operation relied on the stale projection;
7. whether the defect is documentary only or changes permitted execution;
8. whether the existing bounded-execution-continuity language is substantively sufficient but under-enforced, or itself incomplete.

This phase SHALL produce a disposition before normative redesign begins.

## 15. Required historical audit of originating-agent representations

The Failure Auditor SHALL inspect available repository records and conversation-derived evidence supplied as non-authoritative context to identify instances where the originating assistant:

- represented a long-running project as fully within its execution capabilities;
- promised completion across unbounded external dependencies;
- relied on future self-discipline rather than mechanical enforcement;
- failed to perform executor-capability admission;
- stopped at a recoverable boundary contrary to applicable continuity rules;
- allowed chat summaries to carry state that should have been durable;
- discovered a defect retrospectively that was reasonably foreseeable at design time.

The purpose is not punishment or rhetorical self-criticism. The purpose is to make recurrence testable and to identify which claims about agent capability must be prohibited or mechanically qualified.

## 16. Required deliverables

The harness SHALL produce, on one governed remediation branch or a clearly linked work-package branch set:

- `ARCHAEOLOGY_REPORT.md`
- `SOURCE_INDEX.json`
- `DEFECT_LEDGER.json`
- `FAILURE_ANALYSIS.md`
- `REMEDIATION_DESIGN.md`
- machine-readable execution-state schema(s), if justified;
- transition validation code, if justified;
- migration/reconciliation tooling for stale state, if justified;
- adversarial fixtures and tests for T1–T14;
- `MIGRATION_PLAN.md`
- `ADVERSARY_FINDINGS.*`
- `REFEREE_FINDINGS.*`
- exact-head test/CI evidence;
- a protected-readback/closure record if and only if the governing route later authorizes and completes protected admission.

The harness SHALL preserve negative findings. If remediation is not economically or architecturally justified, it SHALL produce a `NO_GO` recommendation rather than manufacturing a success path.

## 17. Acceptance criteria

Remediation may be recommended for governed admission only if all of the following are demonstrated:

1. A fresh agent with no chat transcript can resume representative governed work from durable state alone.
2. Exact-head state, review validity, and authority precedence are mechanically enforced.
3. An execution cutoff after any completed atomic transition produces no ambiguous workflow state.
4. An execution cutoff during a transaction cannot be mistaken for successful completion.
5. External waits are represented durably and do not require repeated broad rediscovery.
6. Executor capability/topology is checked before substantial work begins.
7. The active GH-OS version and programme adoption are coherently projected or contradictions fail closed.
8. Stale conversation cannot override newer authoritative state.
9. Proposal author, Adversary, and Referee separation is preserved.
10. No acceptance criterion depends on the originating assistant's promise to behave better.
11. No AETHER runtime is required for correctness.
12. Existing mathematical, certification, constitutional, production, publication, and commercial authority boundaries are not weakened.

## 18. Stop / escalation conditions

A harness agent SHALL stop or escalate only when it encounters a named authority, authentication, safety, protected-state, materially changed-state, substantive evidentiary, or actual recovery-exhaustion boundary.

It SHALL NOT stop merely because:

- CI is still running;
- a connector response is incomplete;
- one diagnostic surface fails;
- the current agent invocation is nearing its execution boundary;
- the conversation is long;
- a replacement agent will be needed.

If an invocation must terminate for an external execution boundary, its last substantive action SHALL be to ensure that durable state identifies the exact completed transaction, unsettled work, and next permitted transition. A prose chat summary may mirror that state but SHALL NOT be the sole continuity record.

## 19. Claim and authority boundary

This specification authorizes investigation and candidate remediation work only. It does not:

- amend the INTELLECT Constitution;
- admit a GH-OS successor;
- establish organization-wide GH-OS conformance;
- certify mathematics;
- alter MATHCERT jurisdiction;
- promote any mathematical, novelty, priority, patentability, production, deployment, mechanical, manufacturing, or commercial claim;
- authorize an agent to approve or merge its own work.

Any normative change discovered to be necessary must follow the applicable exact-head admission, Adversary, Referee, Human Steward, protected-merge, programme-adoption, and readback route.

## 20. Harness completion condition

The harness may declare the audit/remediation packet ready for governed review only when the artifacts above are exact-head bound and the adversarial test matrix has a recorded disposition.

The pre-review exit token is:

`GHOS_CONTROL_PLANE_REMEDIATION_PACKET_READY_FOR_GOVERNED_REVIEW`

This token means only that a candidate packet exists for review. It does not mean the remediation is admitted, effective, adopted, or complete.
