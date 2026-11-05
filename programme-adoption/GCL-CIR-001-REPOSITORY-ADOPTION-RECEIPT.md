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

## Open substantive admission obligations

| Repository | PR / dependency | State and next permitted action |
| --- | --- | --- |
| INTELLECT | [#134](https://github.com/grandchallenge/INTELLECT/pull/134) | `OPEN / REVIEW_REQUIRED`. Candidate exact-head CI green, nine regression tests executed; await genuinely eligible protected approval, merge and protected-main readback. Do not impersonate a reviewer or bypass protection. |
| MATHCERT | [#357](https://github.com/grandchallenge/MATHCERT/pull/357) | `OPEN / REVIEW_REQUIRED`. Staged passive source, frozen test inventory and manifest; exact-head Cert checks/conformance green. Obtain protected approval, merge and readback. |
| MATHCERT execution | [#358](https://github.com/grandchallenge/MATHCERT/pull/358) | Mandated `platform/certification/*` branch; only workflow path modified; platform scope preflight PASS. CI intentionally stops because source test file from #357 is absent on `main`. Once #357 merges, rebase/replay #358 and obtain its own protected review, merge and executed-test proof. Preserve full Lean/certification scope. |

The two MATHCERT PRs are **one two-stage repository adoption**, not two independent repositories. No claim of full organization-wide completion is valid while these remain unmerged.

## Other repository disposition

- `GCT-EXECUTIVE` and `gcl-public-web-preview`: no Python `test_*.py` inventory in the inspected protected tree. `NOT_APPLICABLE_PYTHON_V1`; this is **not** a claim that all other-language tests or deployment gates are covered.
- `upload-pages-artifact` and `lean-action`: organization forks excluded from the initial first-party repository adoption set; their upstream/third-party release and security requirements remain unchanged.

## Non-drift closure rule

A worker may mark `GCL-CIR-001_ORG_ADOPTION_CLOSED` only when both INTELLECT and MATHCERT have exact-head native test execution, all required protected reviews, protected merges and main readbacks, and the final repository applicability inventory is rechecked. Record the final receipt with exact merged commits and CI workflow/job IDs. A reviewer delay or platform denial must be named explicitly, not converted into success. Do not bypass a failed test, omit required CI, or relax certification boundaries. The continuing hourly `GCL CI Routing Closure` task should reconcile this receipt against **live** protected state and advance only newly eligible work.
