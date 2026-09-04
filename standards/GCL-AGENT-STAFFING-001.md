# GCL-AGENT-STAFFING-001: Functional Multi-Role Agent Staffing

**Version:** 1.0.0  
**Status:** Candidate; activation is conditional on protected selection of `GI-STEWARD-0003`  
**Registry:** `grandchallenge/gcl-standards`  
**Superior authority:** `grandchallenge/INTELLECT`  
**Review schema:** `schemas/multi_role_review.schema.json`  
**Adoption schema:** `schemas/repository_staffing_adoption.schema.json`

## 1. Purpose

This standard defines separation of governance functions by inspectable work,
not by multiplying people, accounts, models, conversations, or approval clicks.
A single Codex system MAY staff multiple non-reserved roles when each role is a
distinct logical audit pass over an exact subject and material evidence set.

This candidate creates no authority before its superior directive is effective
and this version is admitted on a protected branch.

## 2. Work classification

- `routine_bounded` changes preserve public contracts and authority boundaries.
- `substantive` changes affect a public contract, authority boundary, or material
  result but do not exercise a reserved power.
- `reserved` changes exercise Human Steward, mathematical-certification,
  destructive, safety-critical, credential, public-commitment, irreversible
  resource, production-semantic, or corpus-admission authority.

Automation MAY implement, audit, merge through satisfied protected controls,
and perform readback for routine and non-reserved substantive work. A blanket
human approval or GitHub approval requirement MUST NOT be imposed on those
classes. Repository contracts MAY require additional evidence proportionate to
risk, but MUST NOT claim that a different system, invocation, task, model,
account, or human intrinsically creates independence.

Reserved work stops at one consolidated decision by its named authority.
Automation MAY prepare, faithfully record, and mechanically execute that
decision. It MUST NOT manufacture or infer it.

## 3. Logical-pass contract

Every governed review exposes `reviewer_system_id`, unique `logical_pass_id`,
role, criteria, exact subject, mode, finding, evidence, and unresolved
obligations. The same `reviewer_system_id` MAY appear in several non-reserved
roles. When an authoring system later acts as Adversary or Referee, its mode MUST
be `non_authoring_read_only`: it may inspect and issue a finding but may not
mutate the governed subject during that pass.

A logical pass is an audit phase, not a runtime-session identity. Findings are
invalidated only when the exact subject or material evidence changes. Distinct
roles that answer different questions require distinct pass identifiers and
non-duplicated analyses.

## 4. Reserved boundaries

- **INTELLECT:** constitutional promulgation and changes to reserved office
  powers retain Human Steward authorization.
- **MATHCERT:** one system may perform preparatory roles, but no system may
  certify a mathematical claim for which it supplied the sole construction or
  verification evidence.
- **TROVE-CURATA:** destructive disposal and corpus admission retain their
  declared authority gates.
- **AETHER:** production-semantic activation and autonomous permission
  escalation remain reserved.
- **All repositories:** credential expansion, destructive organization
  operations, safety-critical deployment, external public commitments, and
  irreversible resource commitments remain reserved unless separately amended.

These exceptions constrain authority and outcomes. They do not reinstate a
blanket identity-multiplication or routine approval chain.

## 5. Fail-closed semantics

Conformance validation MUST reject duplicate pass identifiers, missing role
criteria, mutation during a read-only pass, stale subject or evidence bindings,
fabricated reserved authorization, classification downgrade, and any assertion
that green CI or numerical evidence supplies mathematical certification.

Repository adoption is explicit and digest-addressed. Drift in this standard,
its superior authority selection, or a repository head makes an adoption record
stale until regenerated. Conformance grants no new mathematical, scientific,
production, safety, deployment, commercial, credential, or destructive power.
