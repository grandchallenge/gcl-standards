# Grand Challenge Labs Standards

`gcl-standards` is the versioned authority for standards shared across Grand
Challenge Labs programmes.

It does not determine mathematical truth. Programme repositories adopt pinned
standard versions, and MATHCERT remains the only mathematics pillar that can
adjudicate a claim through an accepted certification route.

## Authority

- `standards/` contains normative cross-programme standards.
- `schemas/` contains machine-readable contracts.
- `templates/` contains non-authoritative starting points.
- `fixtures/` contains validation examples and repository profiles.
- `programme-adoption/` records exact programme adoption decisions.
- `deprecations/` records compatibility and retirement boundaries.
- `decisions/` contains one canonical file per cross-programme ADR.

The first candidate standard is
[`GCL-GHOS-00`](standards/GCL-GHOS-00.md), the GitHub Constitutional Operating
System. Its current status is `candidate`; no programme is bound until its
adoption record identifies an accepted revision and immutable commit.

## Validation

```bash
python ci/validate.py
python -m unittest discover -s tests -p "test_*.py"
```

## Constitutional boundary

GitHub provides workflow, review, evidence, publication, and indexing
capabilities. Repository artifacts remain authoritative. Issues own next
actions; Projects index them; Discussions are deliberative; Actions produce
evidence; releases publish already-admitted artifacts.
