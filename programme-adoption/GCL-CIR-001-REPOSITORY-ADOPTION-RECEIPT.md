# GCL-CIR-001 Cross-Repository Adoption Receipt

**Snapshot:** 2026-11-05 UTC. **Scope:** active, non-fork repositories of `grandchallenge`. **Contract:** [GCL-CIR-001](../standards/GCL-CIR-001.md) v1.0.0. **Canonical source:** protected-merged standards PR [#114](https://github.com/grandchallenge/gcl-standards/pull/114), exact candidate `cab9749f74e55cf4126b98a372984d35974189a1` (merged 2026-11-05T03:45:04Z).

This ledger is an **immutable-as-of evidence snapshot**, not permission to skip live GitHub checks. The exact PR head, protected merge, required CI and on-main file readback govern the current state. Refresh after every successful admission; never treat staged source or green PR CI alone as `ADMITTED`.

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

All times above refer to 2026-11-05 UTC. The protected `main` component-manifest or engine was read back in each admission transaction; original exact-head CI evidence belongs to the linked PR. These are CI engineering adoptions, not mathematical result certification or protected state promotion.

## Existing native implementation

- `MATH-PROGRAMME`: protected-admitted `MP-POLICY-IMPACT-GATING-001` with declarative component routing (PRs #3127, #3128, #3129), exact-head OAI26 and negative-test execution proof. This is the authoritative native implementation, **not replaced** by the portable adapter.

## Final substantive admissions — protected and verified

**Disposition: `GCL-CIR-001_ORG_ADOPTION_CLOSED` (2026-11-05 UTC).** The last two applicable repositories were admitted through three protected PRs. The source and execution changes in MATHCERT are one two-stage adoption, not two repositories.

| Repository / stage | PR | Approved reviewer | Exact candidate head | Protected merge UTC | Protected merge SHA | Required CI evidence |
| --- | --- | --- | --- | --- | --- | --- |
| INTELLECT source | [#134](https://github.com/grandchallenge/INTELLECT/pull/134) | jimsteeg, 12:14:23 UTC | `f9955d433fef390a232a1dce13328f2c81994878` | 12:21:56 | `1c22839042da4b98fb8a979bc20edc0b3002f78e` | [CI Python 3.11/3.12](https://github.com/grandchallenge/INTELLECT/actions/runs/41939540499); [validation](https://github.com/grandchallenge/INTELLECT/actions/runs/41939540584); nine routing tests executed |
| MATHCERT source | [#357](https://github.com/grandchallenge/MATHCERT/pull/357) | jimsteeg, 12:14:37 UTC | `d9442a979c95be548c1966b1d27563ced6ad308d` | 12:15:09 | `f6b72807d5ab82b33ed73b74604d1bcdf06e2662` | [Cert checks, job 126989883761](https://github.com/grandchallenge/MATHCERT/actions/runs/41949365091/job/126989883761) |
| MATHCERT executing workflow | [#358](https://github.com/grandchallenge/MATHCERT/pull/358) | jimsteeg, 12:14:54 UTC; still APPROVED on updated head | `f940d28f5dfb1c6ce2f410d94c96d890342e022f` | 12:39:12 | `7a97ac1131d5a80840d59c3f172499e92e29e182` | [Cert checks, job 127246986119](https://github.com/grandchallenge/MATHCERT/actions/runs/42028008138/job/127246986119): nine `test_gcl_component_routing.py` tests executed and passed, plus existing cert checks |

The explicit dependency sequence was preserved: #357 protected-merged before #358's head was updated to consume its source. The first #358 certification check failed because that source test was absent; the refreshed exact head ran all nine new routing tests successfully and its required checks completed green. No failed check was waived. Full Lean/certification scope was preserved.

**Protected readback:** INTELLECT `main=1c22839042da4b98fb8a979bc20edc0b3002f78e`; MATHCERT `main=7a97ac1131d5a80840d59c3f172499e92e29e182`. All three PRs returned `MERGED` with these exact protected merge commits, and #358 returned `APPROVED`, `CLEAN`, and successful certification before admission.

**Applicability inventory rechecked on 2026-11-05 UTC:** 21 organization repositories observed, comprising 19 active non-fork repositories and two forks. Of the 19 first-party repositories, 17 have applicable Python-v1 implementations (16 portable including the canonical standards repository, plus MATH-PROGRAMME's pre-existing native implementation); GCT-EXECUTIVE and gcl-public-web-preview remain `NOT_APPLICABLE_PYTHON_V1`. The two forks remain excluded. This closes the declared Python-v1 CI-routing adoption scope only; it does not certify all other-language CI, mathematical claims, deployments or future repositories.

## Other repository disposition

- `GCT-EXECUTIVE` and `gcl-public-web-preview`: no Python `test_*.py` inventory in the inspected protected tree. `NOT_APPLICABLE_PYTHON_V1`; this is **not** a claim that all other-language tests or deployment gates are covered.
- `upload-pages-artifact` and `lean-action`: organization forks excluded from the initial first-party repository adoption set; their upstream/third-party release and security requirements remain unchanged.

## Non-drift closure rule

A worker may mark `GCL-CIR-001_ORG_ADOPTION_CLOSED` only when both INTELLECT and MATHCERT have exact-head native test execution, all required protected reviews, protected merges and main readbacks, and the final repository applicability inventory is rechecked. Record the final receipt with exact merged commits and CI workflow/job IDs. A reviewer delay or platform denial must be named explicitly, not converted into success. Do not bypass a failed test, omit required CI, or relax certification boundaries. The continuing hourly `GCL CI Routing Closure` task should reconcile this receipt against **live** protected state and advance only newly eligible work.
