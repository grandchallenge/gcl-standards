# ADR-0002: Establish the GCL Regret Contract Standard

**Date:** 2026-08-02  
**Status:** Proposed for exact-head Council review  
**Standard:** `GCL-RC-00` version `1.0.0`  
**Owner:** Amanuensis with Referee and Security review

## Context

Adaptive controllers are currently described separately across MODULUS, KIBO,
AETHER, SPINDLE/SPLICE, Tricorder, and optimizer-control work. The candidate
packet in `fyremael/MODULUS` pull request #1 provides a common declaration and
evaluation contract but was staged there only because `gcl-standards` did not
then exist.

## Decision

Register `GCL-RC-00` and its Draft 2020-12 schema in `gcl-standards`. Preserve
`modulus.online` as the candidate reference implementation. Require each
programme to adopt an admitted standard revision through an exact commit and to
record unresolved obligations before claiming conformance.

## Source identity

The migration is bound to MODULUS pull request #1 at exact head
`641ba766fe8eec613a01cd4726841b1d4e93ad78`. Source path and blob identities are
recorded in `programme-adoption/REGRET-CONTRACT-1.0.0.yaml` and validated by CI.

## Non-negotiable boundaries

- Registry custody and green CI do not activate the standard.
- The open MODULUS candidate is not silently treated as merged or admitted.
- A regret guarantee is only as broad as its declared feedback, bounded-loss,
  geometry, and comparator assumptions.
- Conformance does not prove convergence, safety, end-task improvement,
  governance soundness, novelty, or priority.
- Hard governance and safety eligibility constraints remain outside and prior
  to any regret-minimizing router.
- Programme-local copies must not become competing canonical schemas.

## Activation conditions

This ADR becomes accepted only after:

1. exact-head validation of the canonical standard, schema, template, source
   lock, and adoption ledger;
2. a non-author exact-head review;
3. explicit Human Steward authorization naming the exact candidate head;
4. protected merge into `gcl-standards`;
5. a protected MODULUS revision that links to the admitted standards commit
   while retaining the reference implementation; and
6. a post-merge closeout record on `grandchallenge/.github#4`.

Downstream implementations in KIBO/KOOP, AETHER, SPINDLE/SPLICE, Tricorder, and
adaptive-beta work remain separate work packages. Their incompleteness does not
block migration closure because the adoption ledger records them as planned and
preserves their unresolved obligations.

## Alternatives rejected

- Leaving the standard solely in MODULUS would preserve competing custody and
  make cross-programme versioning ambiguous.
- Treating `GCL-GHOS-00` ratification as the Regret Contract decision would
  conflate unrelated constitutional-operating and adaptive-control standards.
- Requiring every downstream implementation before canonical migration would
  make the authority repair depend on research completion.
