# GCL-CEX-01: Campaign Execution and Frontier Control

**Version:** 0.1.0  
**Status:** Candidate normative standard; no cross-programme effect until protected admission and programme adoption  
**Constitutional source:** `grandchallenge/INTELLECT/CONSTITUTION.md`  
**Compatible operating standard:** `GCL-GHOS-00`  
**Registry:** `grandchallenge/gcl-standards`  
**Council issue:** `grandchallenge/gcl-standards#81`  
**Initial pilot:** `BSD-001` in `grandchallenge/MATHSOLVE`  
**Scope:** Governed research campaigns executed by humans or agents across Grand Challenge repositories

## 1. Purpose

This standard makes campaign execution durable, cold-startable, and mechanically checkable.

A capable independent agent that has not seen prior conversations SHALL be able to enter a campaign from protected repository state, identify the exact current frontier, determine the bounded operation it may perform, distinguish mathematical progress from maintenance activity, execute within authority, and leave evidence that another independent agent can verify.

This standard is subordinate to the INTELLECT Constitution, effective amendments and directives, programme-owned policy, domain authority, repository protection, and MATHCERT mathematical certification. It does not create constitutional authority, certify mathematics, or enlarge agent permissions.

## 2. Governing principle

Operational authority SHALL reside in protected, machine-readable repository records and exact-revision evidence.

Chat transcripts, assistant memory, mutable issue summaries, and oral or informal descriptions MAY supply context. They SHALL NOT be the sole operational authority for current campaign state, claim state, permissions, protected identities, or frontier transitions.

Every governed campaign SHALL expose one canonical cold-start path from protected state.

## 3. Required records

A conforming campaign SHALL maintain the following record classes.

### 3.1 Campaign state

`CAMPAIGN_STATE` identifies:

- stable campaign identifier and title;
- constitutional, programme, work, source, and certification authorities;
- exact protected input identities required by the active lane;
- selected target and its current claim status;
- current bounded operation;
- current theorem, experiment, engineering, or evidentiary frontier;
- known-false or explicitly unrepaired conditions;
- prohibited promotions;
- cold-start entry points;
- candidate frontier transition, if any.

There SHALL be exactly one canonical campaign-state record for an active campaign within its authoritative work repository or programme-owned registry.

### 3.2 Operation contract

Every bounded operation SHALL have an `OPERATION` contract before admission review begins.

The contract SHALL identify:

- campaign and operation identifiers;
- governing issue or equivalent work record;
- exact protected base and all material provider anchors;
- the single current frontier the operation is authorized to retire, falsify, or refine into a precise blocker;
- acceptable dispositions;
- mutation scope and prohibited authorities;
- completion gates;
- governed artifacts;
- claim firewalls;
- freeze and preflight surfaces;
- completion-receipt surface;
- successor-package policy;
- legitimate stopping-boundary classes;
- recoverable events that are not stopping conditions.

An Executor SHALL NOT silently broaden this contract during realization.

### 3.3 Content freeze

Before exact-head admission review, governed candidate content SHALL be frozen by content identity.

The freeze SHALL bind:

- campaign and operation identity;
- protected base;
- exact content identities for all governed artifacts;
- invalidation conditions.

A governed-artifact change invalidates the freeze and requires a new freeze record. A candidate-head change invalidates all prior exact-head reviews and checks even when governed content is unchanged.

The freeze is evidentiary only. It does not approve, merge, certify, or promote claims.

### 3.4 Completion receipt

A completed operation SHALL leave a durable receipt bound to protected reality.

The receipt SHALL identify at least:

- final candidate head;
- protected merge identity;
- protected readback identity;
- exact-head Adversary record;
- exact-head Referee record;
- required checks and their exact subject identity;
- retired or falsified frontier;
- established disposition;
- preserved negative facts and claim firewalls;
- next frontier, if any.

The receipt MAY be a protected repository artifact, an immutable or append-only programme record, or a durable issue record when programme policy admits that surface.

A runtime failure after a valid protected transition SHALL NOT cause the system to fabricate a cleaner history or repeat an already valid transition. Recovery SHALL bind the actual protected transition and repair documentary readback around it.

## 4. Frontier disposition taxonomy

Campaign activity SHALL distinguish material frontier movement from operational work.

The standard dispositions are:

- `CLOSED`: the named frontier was retired by admitted evidence;
- `BLOCKED`: a new irreducible mathematical, experimental, engineering, source, authority, or evidentiary dependency was identified precisely;
- `FALSIFIED`: the proposed route or claim was shown not to work within its stated scope;
- `RECONNAISSANCE`: useful information was obtained, but the named frontier did not move;
- `MAINTENANCE`: infrastructure, documentation, routing, formatting, CI, or administrative work was completed without frontier movement.

Only `CLOSED`, `BLOCKED`, or `FALSIFIED` constitute theorem- or frontier-level movement.

A successor mathematical or research package SHALL NOT be created merely because a maintenance or reconnaissance operation ended. A successor package requires either a material disposition above or an explicit programme-owned exception explaining why further decomposition is necessary.

Package count, issue count, commit count, test count, review count, and CI volume SHALL NOT be reported as substitutes for frontier movement.

## 5. One operation, one material objective

A bounded operation SHOULD target one material frontier.

Supporting source reads, repairs, routing changes, workflow registration, formatting, CI recovery, and handoff maintenance SHALL normally remain inside that operation when they do not create a new authority or materially different research question.

A new provider operation is justified when independent source admission or provenance is itself a governed dependency that changes what downstream work may lawfully claim. Routine source tracing SHOULD NOT create a separate provider package.

## 6. Cold-start protocol for independent agents

A conforming repository SHALL permit an outside agent to begin with only:

- repository identity; and
- campaign or operation identifier.

The agent SHALL then:

1. re-fetch live protected authority and work heads;
2. read the canonical `CAMPAIGN_STATE`;
3. read the active `OPERATION` contract;
4. compare live protected state with exact protected identities in the contract;
5. reject stale evidence and reconcile material drift before mutation;
6. read the named frontier, claim ledger, provider records, and direct predecessor artifacts;
7. perform only the bounded work authorized by the operation;
8. run deterministic preflight before expensive CI or admission review;
9. freeze governed content;
10. obtain exact-head non-authoring/read-only review required by superior policy;
11. run affected CI and repository-required checks;
12. perform protected mutation only when authorized gates are satisfied;
13. read back protected state;
14. publish the completion receipt;
15. update canonical campaign state to the next admitted frontier.

The cold-start path SHOULD be shorter than the historical record. A new agent SHALL NOT be required to reconstruct the campaign from all predecessor issues or chats when canonical state already identifies the relevant dependency slice.

## 7. Deterministic preflight

Every adopted campaign profile SHALL provide a cheap deterministic preflight before reviewer effort or expensive CI.

Preflight SHALL, where applicable, verify:

- campaign/operation identity coherence;
- exact protected base and provider bindings;
- current frontier equals the operation objective;
- candidate disposition is permitted;
- completion-gate completeness;
- known-false facts remain in the claim firewall;
- claim ledger and frontier records agree;
- stale candidate/protected language is absent from canonical handoffs;
- required workflows exist and are registered in GH-OS routing;
- governed artifacts exist;
- frozen content identities match repository contents;
- no prohibited successor package has appeared before disposition;
- the completion-receipt surface is declared.

Preflight failure is a candidate defect, not a mathematical disposition. Repair requires a fresh freeze when governed content changes and fresh exact-head evidence whenever the head changes.

## 8. Content freeze and admission cycle

Campaigns SHOULD minimize admission churn by completing candidate content and execution mechanics before exact-head review.

The default sequence is:

`realization -> preflight -> content freeze -> Adversary -> Referee -> affected CI -> protected mutation -> protected readback -> receipt`.

Review SHALL bind the exact candidate head. CI evidence SHALL bind the exact candidate head or protected merge as declared by the applicable gate.

If a review uncovers a defect, the candidate MAY be repaired within the bounded operation. The repair creates a new head; prior exact-head reviews and checks are stale and SHALL NOT be reused as current evidence.

## 9. Separation of roles and independent assistance

This standard supports outside independent agents without granting campaign ownership.

Agents SHOULD receive bounded operation leases, not ownership of an entire campaign. An operation lease identifies:

- operation identifier;
- exact base;
- permitted repositories and mutations;
- expiration or staleness condition;
- evidence obligations;
- protected-state mutation authority, if any.

Multiple agents MAY assist the same campaign through separate source, verification, adversarial, formalization, implementation, or review operations when their contracts do not create conflicting authority.

Review remains subject to the INTELLECT separation-of-powers rules and any stronger domain-specific separation requirement.

## 10. Exact identity and stale evidence

Where exact identity matters, evidence SHALL bind the current exact artifact, revision, run, job, provider record, or protected merge.

Evidence from a superseded head SHALL NOT be reused as current exact-head evidence.

A protected-base advance is not automatically a failure. The operation SHALL determine whether the state change is immaterial, mechanically reconcilable, or materially invalidates the governing plan. Materially changed state is a legitimate stopping or re-planning boundary; ordinary `BEHIND` or recoverable synchronization state is not necessarily one.

## 11. Recovery doctrine

Within an authorized bounded operation, agents SHALL continue through reasonably available non-destructive diagnostic, repair, replay, and evidence-gathering paths.

Recoverable connector, logging, compiler, CI, environment, formatting, routing, or tooling failures are not stopping conditions by themselves.

Fail-closed behavior applies to unsupported claims, certification, promotion, protected-state mutation, and authority. It SHALL NOT be interpreted as requiring abandonment of authorized recovery or evidence gathering.

Before stopping, the executing agent SHALL name the exact boundary preventing the next authorized recovery action.

## 12. Claim firewalls

Every operation SHALL carry forward material negative facts and prohibited promotions from campaign state.

A narrower replacement theorem SHALL NOT silently promote a stronger failed hypothesis. A source audit SHALL NOT become mathematical certification. CI success SHALL NOT become mathematical truth. Repository merge SHALL NOT become certification unless the declared domain authority explicitly assigns that effect.

For mathematics campaigns, MATHCERT retains sole certification authority through its admitted routes.

## 13. Provider and cross-repository dependencies

A downstream operation MAY depend on a protected provider record in another repository.

The operation SHALL bind the exact provider repository and revision. If the provider revision changes, downstream work SHALL determine whether the change is an admitted successor, an unrelated advance, or a material invalidation.

A provider result SHALL state its downstream claim boundary and preserve stronger unproved or false conditions explicitly.

## 14. Enforcement profile

Programme adoption SHALL identify the repository paths and workflow checks that make this standard enforceable.

A conforming enforcement profile SHOULD reject admission when:

- campaign state is missing or incoherent;
- the operation contract does not target the current frontier;
- a known-false fact is omitted or promoted;
- the candidate has changed after its freeze without a new freeze;
- exact-head review refers to a stale head;
- required workflows are unregistered;
- the completion gate omits protected readback or a completion receipt;
- a successor package appears after maintenance/reconnaissance alone without an exception;
- the protected base materially changed and was not reconciled;
- the operation claims authority it does not possess.

Repositories MAY add stronger domain checks.

## 15. Minimum machine-readable profile

The registry supplies schemas for:

- campaign state;
- operation contract;
- content freeze;
- completion receipt.

Programme profiles MAY extend these schemas but SHALL preserve the core semantic fields and claim boundaries.

Repository-native Git content identities MAY be used for a freeze when the validator also emits a stronger digest over the exact frozen artifact set. SHA-256 SHOULD be used for cross-system evidence bundles and publication receipts.

## 16. Bootstrap and migration

The first pilot is BSD-001 WP60S in MATHSOLVE. The pilot is evidence for the standard; it does not by itself admit this standard organization-wide.

Migration of an active campaign SHOULD occur at a natural frontier boundary. Historical packages need not be rewritten. The new canonical campaign state SHALL identify the protected predecessor chain that remains authoritative.

Adoption SHOULD measure:

- frontier movement per operation;
- maintenance/reconnaissance ratio;
- repeated admission cycles per material closure;
- stale-evidence failures;
- preflight catches before reviewer or expensive-CI consumption;
- outside-agent cold-start success without conversational context.

## 17. Conformance statement

A campaign conforms to GCL-CEX-01 only when its adopted programme profile provides machine-readable campaign state, bounded operation contracts, deterministic preflight, content freeze, exact-head evidence invalidation, protected readback, and completion receipts.

Documentation that merely describes these concepts is not conformance.

## 18. Claim boundary

GCL-CEX-01 governs execution and evidence flow. It does not establish any mathematical theorem, scientific result, commercial claim, novelty claim, constitutional amendment, or autonomous permission escalation.
