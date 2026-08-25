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

[`GCL-GHOS-00`](standards/GCL-GHOS-00.md) is the GitHub Constitutional
Operating System. Version `0.1.1` remains the version selected by the existing
MATH-PROGRAMME adoption record. Its exact admitted source is preserved at
[`standards/history/GCL-GHOS-00-0.1.1.md`](standards/history/GCL-GHOS-00-0.1.1.md),
with the admitted `0.1.0` source retained as the earlier historical predecessor.

Version `0.2.0` is the reviewed normative successor adding bounded execution
continuity for recoverable operational failures. Its standards-layer admission
authority is exclusively
[`admissions/GCL-GHOS-00-0.2.0.json`](admissions/GCL-GHOS-00-0.2.0.json),
which becomes effective only through protected merge of that exact record. The
reviewed standard source remains byte-identical to PR #52 head
`f416092f67c91ea4843fea12abe54c34b12242e5`. MATH-PROGRAMME adoption of
`0.2.0` remains a separate later gate; admission does not silently update any
programme adoption record.

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
