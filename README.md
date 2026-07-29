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
- `programme-adoption/` records exact programme adoption decisions.
- `deprecations/` records compatibility and retirement boundaries.
- `decisions/` contains one canonical file per cross-programme ADR.

The first candidate standard is
[`GCL-GHOS-00`](standards/GCL-GHOS-00.md), the GitHub Constitutional Operating
System. Its current status is `candidate`; no programme is bound until its
adoption record identifies an accepted revision and immutable commit. Its
constitutional reconciliation also depends on proposed INTELLECT amendment
`GI-AMEND-0001`; neither proposal may be treated as ratified by merge or CI.

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
