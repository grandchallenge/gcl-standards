# GCL-GHOS-00: GitHub Constitutional Operating System

**Version:** 0.1.0  
**Status:** Candidate  
**Authority:** Grand Challenge Council  
**Owner:** Amanuensis with Security and Referee review  
**Scope:** All repositories owned by `grandchallenge`

## Purpose

This standard binds GitHub capabilities to the Grand Challenge constitutional
model without allowing platform state to replace authoritative programme
artifacts or mathematical certification.

## Authority map

| GitHub capability | Permitted authority | Forbidden inference |
| --- | --- | --- |
| Repository content | Canonical artifacts, standards, ledgers, decisions | Placement alone does not certify a claim |
| Issue | Owns the next operational action | Open or closed state is not mathematical status |
| Pull request | Reviewed integration route | Mergeability is not approval or certification |
| Actions and checks | Reproducible validation and evidence | Green CI is not mathematical truth unless the declared MATHCERT route says so |
| Project | Cross-repository index and planning view | Project fields are not an independent source of truth |
| Discussion | Nonbinding deliberation, questions, announcements | Consensus or reaction counts do not create policy |
| Environment and deployment | Human-gated publication or administration boundary | Deployment does not upgrade claim status |
| Release | Immutable publication of an already-admitted artifact | Release creation cannot admit an unsupported claim |
| Package | Content-addressed execution environment or tool | A container or package is not evidence by itself |
| Pages | Public orientation generated from canonical records | Pages must not outlive or contradict source records |

## Repository profiles

Every repository carries a validated profile with:

- constitutional role;
- authority scope;
- claim-promotion role;
- risk tier;
- required workflow profile;
- public-interface obligations;
- release policy;
- canonical policy source.

Profiles are descriptive inputs to automation. They do not grant authority.

## Work graph

Issues use organization issue types and public fields for operational metadata.
Sub-issues and issue dependencies express operational decomposition only.
Theorem dependencies remain in checked mathematical artifacts.

Every governed issue identifies:

- a stable identifier;
- owning pillar or programme;
- authoritative artifact;
- immutable upstream identity when applicable;
- claim boundary;
- evidence or certification route;
- current promotion gate;
- next finite obligation and review date.

## Council and review

Council office records remain machine-readable repository artifacts. GitHub
teams and CODEOWNERS route human review but do not substitute for office
findings.

An independent Referee decision requires a reviewer who:

1. is not the author of the reviewed revision;
2. reviews an exact commit;
3. records the disposition and evidence location;
4. cannot self-approve the protected publication environment.

Automation may request review, validate record completeness, annotate a diff,
and report drift. It may not approve, merge, certify, or promote a claim.

## Actions and automation

Workflows use:

- explicit least-privilege permissions;
- pinned runner images and action commit SHAs;
- deterministic dependency versions;
- concurrency controls;
- exact-head validation for promotion;
- immutable evidence manifests and SHA-256 digests.

Organization-owned GitHub Apps are preferred for long-lived cross-repository
automation. Personal access tokens are temporary bootstrap or break-glass
credentials only.

## Security

Public repositories enable dependency graphs, Dependabot alerts and security
updates, secret scanning and push protection, private vulnerability reporting,
and CodeQL where the language is supported.

Protected branches require pull requests, strict checks, resolved review
conversations, no force pushes, no deletion, and no bypass actors. Independent
approval and CODEOWNER enforcement activate when the required human membership
exists; the absence of reviewers must be reported as an activation blocker.

## Promotion and publication

Governance admission, certification admission, release trust administration,
and Pages publication use distinct environments.

Release assets include:

- an artifact manifest;
- checksums;
- replay instructions;
- an evidence bundle;
- an SBOM where executable dependencies exist;
- a GitHub artifact or release attestation.

Immutable releases and digest-addressed packages preserve published identity.
Mutable tags may assist readers but may not be consumed by governance.

## Drift and exceptions

Settings, rulesets, workflows, issue metadata, and release evidence are audited
against checked-in profiles. Drift creates a governed remediation issue or pull
request. Automation must not silently rewrite canonical records.

An exception identifies owner, scope, rationale, expiry, compensating control,
and Council disposition. An expired exception is blocking.

## Adoption

Adoption is explicit and commit-addressed. A programme records:

- adopted standard version;
- exact standards commit;
- adoption decision;
- unresolved deviations;
- activation date.

Candidate status does not create binding authority.
