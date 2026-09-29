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
Operating System. Version `0.2.0` is current authority for the bounded
MATH-PROGRAMME pilot through the active protected adoption record. The exact
`0.1.1` admitted source is preserved as predecessor history at
[`standards/history/GCL-GHOS-00-0.1.1.md`](standards/history/GCL-GHOS-00-0.1.1.md),
with the admitted `0.1.0` source retained as the earlier historical predecessor.

Version `0.2.0` is the reviewed normative successor adding bounded execution
continuity for recoverable operational failures. Its standards-layer admission
authority is exclusively
[`admissions/GCL-GHOS-00-0.2.0.json`](admissions/GCL-GHOS-00-0.2.0.json),
which became effective through protected merge of that exact record. The
reviewed standard source remains byte-identical to PR #52 head
`f416092f67c91ea4843fea12abe54c34b12242e5`. MATH-PROGRAMME actively adopts
`0.2.0` at protected commit `1a5e9cb24257be578b091ecd2c99d4119ff73b2c`
for its recorded bounded pilot scope. This does not establish organization-wide
conformance or widen any claim authority.

### GCL-CEX-01

[`GCL-CEX-01`](standards/GCL-CEX-01.md) is the candidate Campaign Execution and
Frontier Control standard version `0.1.0`. It defines the cold-start campaign
state, bounded operation contract, theorem/frontier disposition taxonomy,
content freeze, deterministic preflight, exact-head evidence invalidation,
completion receipt, and bounded operation-lease model required for independent
agents to assist a campaign without relying on conversational history.

Its machine-readable contracts are:

- [`schemas/gcl_campaign_state.schema.json`](schemas/gcl_campaign_state.schema.json);
- [`schemas/gcl_operation_contract.schema.json`](schemas/gcl_operation_contract.schema.json);
- [`schemas/gcl_content_freeze.schema.json`](schemas/gcl_content_freeze.schema.json);
- [`schemas/gcl_completion_receipt.schema.json`](schemas/gcl_completion_receipt.schema.json).

The first live bootstrap is BSD-001 WP60S in `grandchallenge/MATHSOLVE` PR #246.
Current registry status is recorded in
[`status/GCL-CEX-01-current.json`](status/GCL-CEX-01-current.json). Candidate
custody does not admit the standard, create organization-wide conformance, or
change mathematical or constitutional authority. Protected standard admission
and programme adoption remain separate gates.


### GCL-CC-00

[`GCL-CC-00`](standards/GCL-CC-00.md) is the candidate Core Clarity Campaign
Control standard version `0.1.0`. It requires operational state and declared
campaign state to remain one protected system, makes operational/presentational
drift a blocking defect, requires explicit external-agent and competition
lifecycles, and forbids remediation stacking without migration and retirement.

Its compact rule is: **state intelligibility is a correctness invariant**.
A campaign is not complete until protected reality, canonical machine state,
the human-readable view, supersession state, and the deterministic next action
agree.

Current registry status is recorded in
[`status/GCL-CC-00-current.json`](status/GCL-CC-00-current.json). Candidate
custody does not admit the standard, establish organization-wide conformance,
certify mathematics, or authorize competition submission.

### GCL-ID-00

[`GCL-ID-00`](standards/GCL-ID-00.md) is the admitted Identifiability
Preflight and Symmetry-Kernel Doctrine version `0.1.0`. It requires inverse,
reconstruction, calibration, and latent-recovery work to state the observation
contract, characterize observation-preserving equivalence, identify the
recoverable quotient or partial target, and separate structural
non-identifiability from conditioning, finite-data limits, model mismatch, and
optimization failure.

The compact rule is: before solving an inverse problem, characterize what the
observation map has already transformed away. The doctrine does not assume every
problem has a linear kernel or group symmetry; the invariant object is the
observation-preserving equivalence class.

A non-authoritative starting record is provided at
[`templates/identifiability_preflight.yaml`](templates/identifiability_preflight.yaml).
The motivating protected example is VGSE-ENG-WP06. Current registry status is
recorded in
[`status/GCL-ID-00-current.json`](status/GCL-ID-00-current.json). Standards-layer
admission is bound by [`admissions/GCL-ID-00-0.1.0.json`](admissions/GCL-ID-00-0.1.0.json).
MATH-PROGRAMME has adopted this version at protected commit
`64ad90b3108f476225cc1ca5a2889e71b3719cc8`; the exact downstream adoption
record is `governance/GCL-ID-00-ADOPTION.json` with Git blob
`c56c8cf70a6caeaaf6c5306eb37b071fc9588c89`. Programme adoption creates no
mathematical, constitutional, certification, or organization-wide conformance
authority.

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

The protected workflow surface uses mandatory execution routing. See the
[`GH-OS execution routing guide`](implementation/GCL-GHOS-CONTROL-PLANE-REMEDIATION-001/EXECUTION_ROUTING_GUIDE.md)
for the enforcement diagram, topology rules, operator procedure, and failure
interpretation.

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
