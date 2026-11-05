# GCL-CIR-001 Cross-Repository Adoption Receipt

**Snapshot:** 2026-11-05 UTC. **Scope:** active, non-fork repositories of `grandchallenge`. **Contract:** [GCL-CIR-001](../standards/GCL-CIR-001.md) v1.0.0. **Canonical source:** protected-merged standards PR [#114](https://github.com/grandchallenge/gcl-standards/pull/114), exact candidate `cab9749f74e55cf4126b98a372984d35974189a1` (merged 2026-11-05T03:45:04Z).

This ledger is a **versioned evidence receipt**, not permission to skip live GitHub checks. The exact PR head, protected merge, required CI and on-main file readback govern the current state. Refresh after every successful admission; never treat staged source or green PR CI alone as `ADMITTED`.

## Admitted protected implementations

| Repository | PR | Protected merge UTC | Authority / scope |
| --- | ---: | --- | --- |
| gcl-standards | [114](https://github.com/grandchallenge/gcl-standards/pull/114) | 03:45:04 | Canonical published standard/reference |
| MATHFORGE | [526](https://github.com/grandchallenge/MATHFORGE/pull/526) | 03:47:33 | Native Forge test discovery |
| MATHSOLVE | [1188](https://github.com/grandchallenge/MATHSOLVE/pull/1188) | 03:47:38 | Native Solve checks |
| AETHER | [158](https://github.com/grandchallenge/AETHER/pull/158) | 05:35:00 | Python CI only; Rust/Go and product integration preserved |
| GLOSS | [13](https://github.com/grandchallenge/GLOSS/pull/13) | 05:35:05 | Package-contract execution; Lean unchanged |
| QUANTUM-TECHNOLOGIES | [126](https://github.com/grandchallenge/QUANTUM-TECHNOLOGIES/pull/126) | 07:09:29 | QTR validation; 315 tests pass |
| BUTTERFLY | [18](https://github.com/grandchallenge/BUTTERFLY/pull/18) | 07:09:35 | Pytest/quality/governance/smoke; canonical MANIFEST refreshed |
| TROVE-CURATA | [7](https://github.com/grandchallenge/TROVE-CURATA/pull/7) | 07:22:37 | Existing 3.11/3.12 acceptance; no corpus admission |
| MODULUS | [33](https://github.com/grandchallenge/MODULUS/pull/33) | 07:32:21 | Native 3.10/3.11/3.12 pytest |
| GSD | [3](https://github.com/grandchallenge/GSD/pull/3) | 07:32:48 | Evaluator test lane, no GPU experiment promotion |
| CONTROL | [57](https://github.com/grandchallenge/CONTROL/pull/57) | 08:25:24 | Source-and-security; no deployed-runtime claim |
| ADAPTIVE-INTELLIGENCE-ATLAS | [447](https://github.com/grandchallenge/ADAPTIVE-INTELLIGENCE-ATLAS/pull/447) | 08:31:40 | Atlas validation; editorial authority unchanged |
| COMPUTATIONAL-DIFFICULTY-ATLAS | [62](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/pull/62) | 08:32:05 | Native operational test checks; editorial authority unchanged |
| .github | [115](https://github.com/grandchallenge/.github/pull/115) | 08:40:49 | Shared constitutional-review tests and scoped path triggers |
| INTELLECT | [134](https://github.com/grandchallenge/INTELLECT/pull/134) | 12:21:56 | Native 3.11/3.12 CI, nine GCL-CIR-001 routing tests, code scanning, policy and routing enforcement; protected merge `1c22839042da4b98fb8a979bc20edc0b3002f78e` |
| MATHCERT | [357](https://github.com/grandchallenge/MATHCERT/pull/357), [358](https://github.com/grandchallenge/MATHCERT/pull/358) | 12:15:09, 12:39:12 | Passive routing engine and manifest admitted first at `f6b72807d5ab82b33ed73b74604d1bcdf06e2662`; workflow execution admitted after dependent replay at `7a97ac1131d5a80840d59c3f172499e92e29e182`; Lean/certification scope preserved |

All times above refer to 2026-11-05 UTC. The protected `main` component-manifest or engine was read back in each admission transaction; original exact-head CI evidence belongs to the linked PR. These are CI engineering adoptions, not mathematical result certification or protected state promotion.

## Existing native implementation

- `MATH-PROGRAMME`: protected-admitted `MP-POLICY-IMPACT-GATING-001` with declarative component routing (PRs #3127, #3128, #3129), exact-head OAI26 and negative-test execution proof. This is the authoritative native implementation, **not replaced** by the portable adapter.

## Final cross-repository admission closure

**Disposition:** `GCL-CIR-001_ORG_ADOPTION_CLOSED` for the Python v1.0.0 applicability set, evidenced as of 2026-11-05 UTC. **17 of 17 applicable non-fork repositories admitted**, counting MATH-PROGRAMME's existing protected native implementation. MATHCERT #357 and #358 form one two-stage adoption, not two repository counts.

- **INTELLECT:** PR #134 approved by eligible reviewer `jimsteeg` at 12:14:23Z; exact candidate `f9955d433fef390a232a1dce13328f2c81994878`; protected squash merge `1c22839042da4b98fb8a979bc20edc0b3002f78e` at 12:21:56Z, matching protected `main` readback. Original CI: Python 3.11 job `126956490702`, Python 3.12 job `126956490524`, routing enforcement job `126956492645`, policy job `126956492970`, and validation job `126956490997`; all SUCCESS. Protected-main engine `ci/gcl_component_routing.py` blob `c8ca0e9209835d96cf4c61c3986db33fca656739`.
- **MATHCERT source:** PR #357 approved by `jimsteeg` at 12:14:37Z; exact candidate `d9442a979c95be548c1966b1d27563ced6ad308d`; protected squash merge `f6b72807d5ab82b33ed73b74604d1bcdf06e2662` at 12:15:09Z. Original certify job `126989883761` and policy/routing/code-scanning checks SUCCESS. Protected-main engine `ci/gcl_component_routing.py` blob `c8ca0e9209835d96cf4c61c3986db33fca656739`.
- **MATHCERT execution:** PR #358 approved by `jimsteeg` at 12:14:54Z. Following #357 admission, exact candidate `f940d28f5dfb1c6ce2f410d94c96d890342e022f` integrated the protected source dependency. Cert workflow run `42028008138`, job `127246986119`, SUCCESS, explicitly executed all nine `test_gcl_component_routing.py` tests, in addition to the existing certification checks. Conformance and routing checks SUCCESS; merge state CLEAN; review APPROVED. Protected squash merge `7a97ac1131d5a80840d59c3f172499e92e29e182` at 12:39:12Z, matching protected MATHCERT `main` readback. Protected-main `.github/workflows/ci.yml` blob `db95d6584deb95beb1a6490f7a03d1d3423f517f` includes the explicit invoking test command.
- **Inventory recheck:** live `gh repo list grandchallenge --limit 100` returned 21 repositories: 19 active non-forks and 2 forks. Of 19 non-forks, 17 are applicable and admitted, and `GCT-EXECUTIVE` plus `gcl-public-web-preview` remain `NOT_APPLICABLE_PYTHON_V1`. The forks `upload-pages-artifact` and `lean-action` remain excluded. This is Python-v1 adoption closure only, not other-language CI or scientific certification.

All new admissions were made through GitHub's enforced protected review and merge controls, with source and execution kept distinct in MATHCERT. The earlier #358 failed check belongs to its obsolete pre-dependency head; the new exact-head replay passed. This closure does not widen certification or security authority.

## Other repository disposition

- `GCT-EXECUTIVE` and `gcl-public-web-preview`: no Python `test_*.py` inventory in the inspected protected tree. `NOT_APPLICABLE_PYTHON_V1`; this is **not** a claim that all other-language tests or deployment gates are covered.
- `upload-pages-artifact` and `lean-action`: organization forks excluded from the initial first-party repository adoption set; their upstream/third-party release and security requirements remain unchanged.

## Non-drift closure rule

A worker may mark `GCL-CIR-001_ORG_ADOPTION_CLOSED` only when both INTELLECT and MATHCERT have exact-head native test execution, all required protected reviews, protected merges and main readbacks, and the final repository applicability inventory is rechecked. Record the final receipt with exact merged commits and CI workflow/job IDs. A reviewer delay or platform denial must be named explicitly, not converted into success. Do not bypass a failed test, omit required CI, or relax certification boundaries. The continuing hourly `GCL CI Routing Closure` task should reconcile this receipt against **live** protected state and advance only newly eligible work.
