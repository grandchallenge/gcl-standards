# Regret Contract migration audit

Date: 2026-08-02  
Work package: `GCL-RC-MIGRATION-001`  
Source issue: `grandchallenge/.github#4`  
Protected base: `06658ff8181e47e3c6152708cab34321c7b6b20f`

## Audit result

The original issue contained one completed bootstrap obligation and one orphaned
migration obligation.

Completed before this work package:

- `grandchallenge/gcl-standards` exists;
- `standards/`, `schemas/`, `templates/`, `fixtures/`, `programme-adoption/`,
  `deprecations/`, and `decisions/` are established;
- schema-validation CI exists;
- CODEOWNERS and Council-office routing exist;
- semantic-versioning and deprecation machinery exist.

Not completed before this work package:

- the Regret Contract standard, schema, and template were absent;
- no canonical source lock named the MODULUS draft head and blobs;
- no adoption-status record covered MODULUS, KIBO/KOOP, AETHER,
  SPINDLE/SPLICE, Tricorder, and adaptive-beta work;
- `gcl-standards#3` had drifted to the unrelated `GCL-GHOS-00` decision and
  could not truthfully ratify the Regret Contract migration.

## Migration package

This branch adds:

- `standards/GCL-RC-00.md`;
- `schemas/regret_contract.schema.json`;
- `templates/regret_contract.yaml`;
- `programme-adoption/REGRET-CONTRACT-1.0.0.yaml`;
- `decisions/ADR-0002_REGRET_CONTRACT_STANDARD.md`;
- fail-closed validator and mutation tests;
- README discovery and authority wording.

The source lock is MODULUS pull request #1 at
`641ba766fe8eec613a01cd4726841b1d4e93ad78`. The source PR remains draft and
unmerged. This package therefore records a canonical candidate and does not
claim that MODULUS or any downstream programme is conformant.

## Closure sequence

1. Validate and independently review the exact `gcl-standards` candidate.
2. Obtain explicit Human Steward authorization naming its exact head.
3. Protected-merge the candidate and record the merge identity.
4. Update MODULUS pull request #1 so its documentation and schema metadata point
   to the admitted `gcl-standards` version and exact commit while retaining
   `modulus.online` as the reference implementation.
5. Validate the MODULUS exact head.
6. Record the complete authority chain on `.github#4` and close it as completed.

Downstream implementation work remains governed by WP-RC-02 through WP-RC-06
and is not collapsed into this authority-migration closeout.

## Claim boundary

This audit and migration do not establish regret bounds beyond the declared
assumptions, controller optimality, neural-network convergence, deployment
safety, mathematical certification, novelty, priority, product, or commercial
claims.
