# ADR-0001: Establish the GitHub Constitutional Operating System

**Date:** 2026-07-29  
**Status:** Proposed for independent Council review  
**Owner:** Amanuensis with Security and Referee review

## Context

Grand Challenge repositories already use Issues, Projects, Actions, Pages,
releases, rulesets, environments, and cross-repository evidence. Their
authority boundaries are expressed in several mathematics-specific documents
but not in one cross-programme operating contract.

The live baseline found a single organization member, no enforced
organization two-factor authentication, an unassigned Council team, disabled
Discussions and code-security features, a sparse stale Project, duplicated
branch-protection mechanisms, and a human-bound administrative token.

## Decision

Adopt `GCL-GHOS-00` as the candidate cross-programme contract and validate the
implementation through a mathematics pilot before organization-wide
activation.

`gcl-standards` owns cross-programme standards. `MATH-PROGRAMME` retains
mathematics-specific authority and records the exact cross-programme revision
it adopts.

## Non-negotiable boundaries

- GitHub automation cannot certify mathematics.
- Project and Discussion state cannot replace repository artifacts.
- Independent Referee review cannot be simulated by a bot or the author.
- Candidate standards are not binding until an exact revision is admitted.

## Activation conditions

This ADR becomes accepted only after:

1. at least two independent contributors join the organization;
2. a non-author Referee reviews the exact candidate revision;
3. validation and settings-readback evidence pass;
4. the mathematics pilot records its adoption commit;
5. no critical exception remains.

## Alternatives rejected

- Expanding MATH-PROGRAMME into the authority for unrelated programmes would
  collapse the mathematics-specific and cross-programme policy boundaries.
- Treating GitHub settings as self-documenting would omit semantic decisions,
  exceptions, and authoritative integrated versions.
- Treating automated council checks as independent review would contradict the
  Referee boundary.
