# Grand Challenge Labs Standards

`gcl-standards` is the versioned registry and publication repository for
standards shared across Grand Challenge Labs programmes. It holds standards
admitted through constitutional process; custody of their text does not make
this repository the source of constitutional power.

It does not determine mathematical truth. Programme repositories adopt pinned
standard versions, and MATHCERT remains the only mathematics pillar that can
adjudicate a claim through an accepted certification route.

## Authority

- The compact Constitution in `grandchallenge/INTELLECT` and effective
  amendments are superior to every artifact in this repository.
- INTELLECT owns constitutional policy and gates; AETHER owns production
  semantic order, provenance, replay, and proof traces.
- `standards/` contains admitted or candidate cross-programme operating
  standards.
- `schemas/` contains machine-readable contracts.
- `templates/` contains non-authoritative starting points.
- `fixtures/` contains validation examples and repository profiles.
- `programme-adoption/` records exact programme adoption decisions and
  unresolved adoption obligations.
- `deprecations/` records compatibility and retirement boundaries.
- `decisions/` contains one canonical file per cross-programme ADR.

## Shared standards

### GCL-GHOS-00

[`GCL-GHOS-00`](standards/GCL-GHOS-00.md) is the admitted GitHub Constitutional
Operating System. The exact admitted `0.1.0` source remains preserved at
[`standards/history/GCL-GHOS-00-0.1.0.md`](standards/history/GCL-GHOS-00-0.1.0.md).
Version `0.1.1` is a documentary-only successor whose selected status is
resolved from its protected admission record. Programme adoption is recorded
separately against that immutable admission identity. Merge, CI, registry
custody, or front matter alone does not admit or adopt it.

### GCL-RC-00

[`GCL-RC-00`](standards/GCL-RC-00.md) is the candidate Regret Contract Standard
version 1.0.0. Its Draft 2020-12 schema is
[`schemas/regret_contract.schema.json`](schemas/regret_contract.schema.json),
and its reusable example is
[`templates/regret_contract.yaml`](templates/regret_contract.yaml).

The migration is source-locked to `fyremael/MODULUS` pull request #1 at exact
head `641ba766fe8eec613a01cd4726841b1d4e93ad78`. `modulus.online` remains the
candidate reference implementation. The adoption frontier and unresolved work
for MODULUS, KIBO/KOOP, AETHER, SPINDLE/SPLICE, Tricorder, and adaptive-beta are
recorded in
[`programme-adoption/REGRET-CONTRACT-1.0.0.yaml`](programme-adoption/REGRET-CONTRACT-1.0.0.yaml).
Canonical custody does not activate the standard or establish programme
conformance.

## Validation

```bash
python ci/validate.py
python -m unittest discover -s tests -p "test_*.py"
```

## Constitutional boundary

GitHub provides workflow, review, evidence, publication, and indexing
capabilities. Repositories are authoring, integration, and publication
surfaces. AETHER remains the production semantic authority. Issues own next
actions; Projects index them; Discussions are deliberative; Actions produce
evidence; releases publish already-admitted artifacts. None of those states
amends the Constitution or certifies mathematics.
