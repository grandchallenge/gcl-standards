# GCL-CIR-001 — Cross-repository declarative CI impact routing

**Version:** 1.0.0  
**Status:** proposed cross-repository engineering standard, effective only upon each protected repository's explicit admission.  
**Authority:** subordinate engineering contract; does not amend INTELLECT's Constitution, substitute for MATHCERT certification, grant production access, or weaken protected check contexts.

## Purpose

Ensure that new research components and tests are automatically discovered within declared ownership namespaces, that their actual executing check is named, and that dependency changes reach downstream consumers without requiring edits to a central classifier. Prevent new unowned tests, overlapping ownership, unknown checks, dangling dependencies, dependency cycles, and stale legacy inventories from silently entering source.

Adoption must preserve existing CI and formally admitted replay boundaries. The initial portable implementation is an **enforcement-and-observation adapter**: it may select candidate checks for diagnostics but does not suppress established workflow jobs. A repository may enable reduced execution only through a separate evidence-backed protected policy change with a fail-closed status aggregator and full sentinels.

## Canonical files

- `reference/gcl_component_routing.py`: standard-library-only reference engine, suitable for vendoring at `ci/gcl_component_routing.py`.
- `governance/ci_routing_baseline.json`: repository ID, recognized CI check identifiers and real test discovery glob patterns, and a frozen inventory of pre-existing unowned tests.
- `governance/ci_components/<component_id>.json`: one component declaration per file. Every declaration has `contract_id`, `version`, `component_id`, `owner`, `paths` with exact/prefix/test-prefix arrays, `depends_on`, and nonempty `checks`.
- `tests/test_gcl_component_routing.py` (or native equivalent): a test automatically executed under a pre-existing required workflow. It must invoke `validate(ROOT)`, not merely import the implementation.

## Executable invariants

1. A newly introduced `test_*.py` under `tests/` or `ci/` is either owned by exactly one declared component or explicitly present in the frozen pre-adoption inventory. The baseline is fixed and cannot grow implicitly.
2. Every declared test has at least one selected check whose test-discovery glob matches that exact path; naming a check without discovery coverage fails.
3. Dependency edges point from consumers to producers. Changing an upstream producer selects its own check obligations and the checks of all downstream consumers. Changing only the consumer does not automatically replay its producers.
4. A missing/ambiguous owner, malformed component, unknown check, unsafe path, control-plane capture, missing dependency, cyclic graph, or stale baseline is a hard validation error. Unknown changed paths select the complete registered check catalog for diagnostics, not an empty test set.
5. Existing branch protection, formal proof replay, certified-result independence, credential authority and GHOS workflow routing retain precedence. A green CI result is not mathematical certification.

## Repository onboarding

Read local `AGENTS.md`, protected workflows, mandatory check contexts and runtime setup. Pin a release of this standard by exact protected commit, copy the reference engine and create repository-specific declarations. Take the initial legacy inventory from an exact protected tree; do not invent entries or auto-enroll future test files. Integrate the validation test with the *existing* CI execution path. Do not add or alter an autonomous workflow merely to adopt the contract.

Run positive and hostile unit tests, verify that a genuine newly added test is discovered by an actual CI job, then merge through repository protection. Read back the exact source blobs and record the protected merge identity and test-run evidence. Only then mark that repository `ENFORCED`. For partially supported languages or unusual CI, record `SHADOW` or `NOT_ADOPTED` explicitly rather than claiming universal coverage.

## Cross-repository drift control

Each adopter pins the standard's exact source commit and records the local vendored engine blob, ownership manifest and native CI evidence. A change to the published standard does not silently mutate adopters; migration requires new protected PRs and independent exact-head replay for each affected repository. Repository names, proof/CI roles and local test globs are never inferred. Reconcile against live protected state instead of copying stale context.

There is no automatic right to reduce CI on an unfamiliar repository: the portable adapter starts in `ENFORCE_DISCOVERY_PRESERVE_EXISTING_CI` mode. For MATH-PROGRAMME, the existing admitted `MP-POLICY-IMPACT-GATING-001` remains authoritative; GCL-CIR-001 is a cross-repository interoperability contract rather than a replacement implementation.

## Acceptance and closure

A repository is fully onboarded when (a) protected policy permits the bounded change, (b) its manifests cover an introduced positive test and reject an unknown one, (c) the existing CI actually executes those tests, (d) all required checks pass at the exact candidate head, (e) protected merge and protected-main readback succeed, and (f) any exceptions are recorded by exact identity. Never claim that a repository with merely staged manifests is operational.
