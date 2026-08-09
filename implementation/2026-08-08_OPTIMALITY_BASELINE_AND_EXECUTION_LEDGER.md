# Optimality Baseline and Execution Ledger

Operation: `GCL-OPT-BASELINE-001`
Recorded at: `2026-08-09T01:58:07Z`
Local date: `2026-08-08` (`America/Vancouver`)
Status: `open_phase_1_and_2`
Scope: semantic coherence, governance and security, and the weekly operating scorecard

## Purpose and boundary

This is the first execution ledger for moving Grand Challenge Labs toward
maximum trustworthy progress per unit of Human Steward attention. It records
the observed baseline, assigns each Phase 1 and Phase 2 gap to a repository,
and defines the issue and pull-request order required to close those gaps.

Phases 3 through 6 are deliberately deferred. Their content may be revised
after the semantic, governance, and security baseline is coherent.

This ledger is an operational planning and evidence-index artifact. It does
not amend the Constitution, accept an ADR, admit or adopt a standard, establish
an AETHER production fact, certify mathematics, promote a claim, or authorize
organization-wide conformance.

## Exact snapshot

| Repository | Protected `main` observed at |
| --- | --- |
| `grandchallenge/INTELLECT` | `70a0a74502e0480d387d740027e48751286e4bfe` |
| `grandchallenge/gcl-standards` | `ba449fab234741a278ee8a2d7120ae69b3c9df1e` |
| `grandchallenge/MATH-PROGRAMME` | `f38dfe5ffc212dadb70ecc5fec0bdf48366e3a35` |
| `grandchallenge/.github` | `5879ff573fdce5f8483518bca0cdef9b5663da87` |
| `grandchallenge/AETHER` | `dd92467d78abb64d176cf8eec7d963c5c6efd342` |

At the snapshot:

- the organization had 38 open issues and 4 open pull requests;
- all 13 public repositories had a protected default branch;
- 12 of 13 repositories had an active immutable-release-tag ruleset;
- AETHER used strict classic branch protection rather than repository
  rulesets;
- organization-wide two-factor authentication enforcement was disabled;
- the organization had two owners, `fyremael` and `jimsteeg`;
- `jimsteeg` appeared in the owner-authenticated `2fa_disabled` membership
  readback;
- the installed GCL administrative Apps were `gcl-council-clerk` and
  `gcl-release-trust`; the `chatgpt-codex-connector` App was also installed;
- configured organization, repository, and environment secret-name readback
  found App credentials and found no personal administrative-token secret;
- the latest `gcl-standards` protected head had successful remote policy,
  security, standards, and CodeQL checks.

Secret-name and App-installation readback cannot prove that no unrecorded
break-glass or off-platform credential exists. That residual boundary remains
an explicit audit item.

## Status precedence rule

Current status shall be resolved by subject and authority, not by whichever
document was edited most recently:

1. The effective INTELLECT constitutional schedule and effective amendment
   record determine constitutional status.
2. The exact `gcl-standards` admission record selected by the current status
   projection determines standard admission status.
3. The exact programme-adoption record selected by the current status
   projection determines programme adoption status.
4. A successor admission, adoption, or coherence receipt may supersede a prior
   current-state projection only by naming the predecessor and exact commits.
5. READMEs, status pages, ADR summaries, standard front matter, profiles, and
   organization pages are descriptive projections. They must agree with the
   applicable records above or identify themselves as an explicitly dated
   historical snapshot.

An immutable historical record is not silently rewritten. If its content was
correct at the time but is misleading as current-tense text, the repair must
either time-scope the assertion or publish a successor exact record. A
coherence receipt proves cross-record agreement; it does not create the
underlying authority.

## Phase 1: semantic coherence baseline

The following eight current-tense assertions conflict with the effective,
admitted, or active records selected by the precedence rule.

| ID | Repository and surface | Observed assertion | Superior current record | Owner |
| --- | --- | --- | --- | --- |
| `SC-01` | `INTELLECT/README.md` | Authority binding and GCL-GHOS reconciliation are proposed | Active constitutional schedule and effective amendment | INTELLECT |
| `SC-02` | `INTELLECT/docs/STATUS.md` | GI-AMEND-0001 is proposed and approvals are absent | Active schedule with complete receipt and effective timestamp | INTELLECT |
| `SC-03` | `INTELLECT/AMENDMENTS/0001-commentary-and-gcl-ghos.md` metadata | GCL-GHOS is candidate and not admitted | Exact GCL-GHOS admission record | INTELLECT, with gcl-standards reference |
| `SC-04` | `INTELLECT/governance/constitutional_authority_schedule.json` | Operating-standard projection remains `candidate` | Later subordinate admission and programme adoption | INTELLECT |
| `SC-05` | `gcl-standards/README.md` | GCL-GHOS is the candidate operating system | Exact admission record | gcl-standards |
| `SC-06` | `gcl-standards/decisions/ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md` | ADR-0001 is proposed and approvals are pending | Admission record identifies ADR-0001 as accepted | gcl-standards |
| `SC-07` | `gcl-standards/standards/GCL-GHOS-00.md` | Standard front matter says `Candidate` | Exact admission record says `admitted` | gcl-standards |
| `SC-08` | `gcl-standards/admissions/GCL-GHOS-00-0.1.0.json` | Next gate is not started and programme adoption is incomplete | Active MATH-PROGRAMME adoption record | gcl-standards |

The July 31 organization-profile snapshot is dated and therefore is not one of
the eight contradictions. It must nevertheless be refreshed after upstream
coherence closes so the public front door names the effective amendment,
admitted standard, active pilot adoption, and remaining organization-wide
nonconformance without implying certification or production authority.

### Required repair shape

- Preserve the admitted `0.1.0` blobs and their Git identities as historical
  evidence.
- Publish `GCL-GHOS-00` version `0.1.1` as a documentary-status successor with
  unchanged normative clauses, admitted status metadata, predecessor identity,
  and a fresh exact admission record.
- Update the MATH-PROGRAMME adoption record to the admitted successor version
  and retain the prior adoption identity in its lineage.
- Time-scope or reconcile the INTELLECT descriptive metadata without changing
  the substantive constitutional articles.
- Add one current-status projection that selects the exact constitutional,
  admission, and adoption records.
- Add adversarial validation for at least:
  - effective amendment plus current status page saying `proposed`;
  - admitted selected standard plus current front matter saying `candidate`;
  - active selected programme adoption plus selected admission saying its
    adoption gate is `not_started`;
  - a descriptive projection that points to an unselected historical record;
  - a successor record that omits its predecessor or exact commit;
  - any projection that widens mathematical, certification, production,
    deployment, novelty, or commercial authority.
- Publish one exact-revision coherence receipt after every coordinated repair
  has landed on protected `main`.

### Validation portability gap

On the Windows checkout with `core.autocrlf=true`, `python ci/validate.py`
passed, while the 116-test unit suite reported five failures because several
validators recompute Git blob IDs from CRLF-transformed worktree bytes. The
same protected head had successful remote checks and its repository tree still
contained the admitted blob IDs.

`VAL-01` is therefore a validator-portability gap, not evidence that protected
`main` changed the admitted source blobs. The Phase 1 validator work must hash
canonical Git content or obtain the blob identity from Git, and must include
LF and CRLF adversarial fixtures.

Phase 1 exits only when all eight contradiction rows are closed, `VAL-01` is
closed, local validation passes under the supported Windows checkout, remote
checks pass at exact heads, and the coherence receipt binds the protected merge
commits.

## Phase 2: governance and security baseline

| ID | Present state | Required disposition | Owner | Priority |
| --- | --- | --- | --- | --- |
| `SEC-01` | Organization 2FA enforcement is off; one of two owners is returned by `filter=2fa_disabled` | The affected owner enables an accepted 2FA method, owner readback returns no disabled member, the Human Steward enables organization enforcement, and an exact readback receipt is admitted | `.github`, Human Steward, affected owner | P1 |
| `SEC-02` | All 13 default branches are protected; GLOSS, QUANTUM-TECHNOLOGIES, `lean-action`, and `upload-pages-artifact` already have main and immutable-tag rulesets | Retain as conformant evidence; do not reopen the already completed repair | gcl-standards | closed |
| `SEC-03` | AETHER has strict classic main protection and an admitted repository profile, but no repository ruleset or immutable-tag ruleset and no admitted AETHER-specific post-repair readback | Add governed repository surfaces and required contexts, migrate to a no-bypass main ruleset and immutable tags without a protection gap, then admit exact readback evidence | AETHER and gcl-standards | P1 |
| `SEC-04` | Council Clerk and release administration are App-backed; no personal-token secret was found in the configured GitHub secret surfaces | Publish an owner-authenticated credential inventory covering App ownership, installation scope, rotations, expiry, revocation, and any break-glass credential; create a deviation for anything not App-backed | `.github` | P2 |
| `GOV-01` | `gcl-standards#14` is open and described as future work under GI-STEWARD-0001 | Treat the Human Steward's instruction to begin this work as satisfying the issue trigger; adopt the minimum steady-state human model below through an exact INTELLECT record | INTELLECT and gcl-standards | P1 |
| `DEV-01` | The most recent admitted settings overlay has zero open rows, but it predates the AETHER conformance addition and does not authorize organization-wide conformance | Add exact rows for `SEC-01`, `SEC-03`, `SEC-04`, and `GOV-01`, each with owner, closure condition, expiry or supersession condition, compensating control, and review date | gcl-standards | P1 |

### Minimum human-governance model

- One named Human Steward remains the accountable authorization point.
- The second owner is security-compliant recovery capacity and may be assigned
  bounded human-office eligibility, but is not a mandatory approver for every
  ordinary governed decision.
- Distinct non-author agent Adversary and Referee sessions perform the two
  independent substantive reviews for one exact packet.
- Automation assembles, hashes, validates, and publishes the packet and
  role-specific findings. It never signs, approves, merges, ratifies,
  certifies, activates, or infers approval.
- The Human Steward performs one authenticated, role-bound authorization on
  the current packet. Routine merge operations are implementation actions and
  must not be misreported as additional substantive approvals.
- Account recovery, Steward replacement, organization deletion, and similarly
  irreversible authority changes require a separately declared recovery
  procedure; they are not silently treated as ordinary one-action decisions.
- No human is asked to transcribe a SHA, digest, or checklist by hand.

Phase 2 exits only after 2FA enforcement reads back active without owner
eviction, AETHER has an exact admitted conformance readback, the credential
inventory has no unowned or unbounded credential, issue #14 is closed by the
effective human-governance record, all remaining deviations are owned and
bounded, and organization-wide conformance remains false unless separately
authorized.

## Weekly operating scorecard

Unknown is a valid baseline result. It must not be coerced to zero.

| Measure | Snapshot value | Target | Evidence boundary / next measurement owner |
| --- | ---: | ---: | --- |
| Status contradictions | 8 | 0 | Rows `SC-01` through `SC-08`; gcl-standards owns the cross-record validator |
| Unprotected default branches | 0 of 13 | 0 | Live branch ruleset or classic-protection readback; `.github` and gcl-standards |
| Human actions per governed decision | 1 in the latest constitutional activation sample; not yet generalized | 1 | Council Clerk receipt plus authenticated Steward action; `.github` |
| Strategic lanes in progress | unknown; no canonical active-lane registry | at most 3 | Deferred portfolio-definition work in MATH-PROGRAMME; do not infer from issue count |
| Active issues without a finite next obligation | unknown; 38 total open issues | 0 | Requires an admitted issue-classification and next-obligation audit; repository owners |
| Handoffs lacking exact identities | unknown | 0 | Requires a cross-pillar handoff inventory; MATH-PROGRAMME, MATHSOLVE, and MATHCERT |
| Median PR decision time | 0.31 hours for 164 human-authored PRs closed from `2026-08-02T01:58:07Z` through `2026-08-09T01:58:07Z`; p95 8.43 hours | less than 48 hours | GitHub search timestamps; excludes bot-authored PRs but does not prove review quality |
| Reproducible governed lifecycle | 0 production demonstrations | 1, then continuous replay | INTELLECT reports the live AETHER cycle as not yet verified; later integration phase |
| Mathematical claims inferred from GitHub state | 0 known in the sampled authoritative records | 0 | Claim-boundary validators and spot audit; not a blanket certification of all prose |

Supporting Phase 2 indicators:

| Indicator | Snapshot | Target |
| --- | ---: | ---: |
| Organization members with 2FA enabled | 1 of 2 | 2 of 2 before enforcement |
| Organization 2FA enforcement | off | on |
| Immutable-release-tag rulesets | 12 of 13 | 13 of 13 after AETHER migration |
| Detected personal administrative-token secrets | 0 | 0, with owner-authenticated inventory |
| Open owned P0/P1/P2 deviation rows covering the new baseline | 0, because the prior overlay predates these gaps | one row per live gap, then 0 after closure |

Each weekly record must state its exact UTC timestamp, source commit or API
identity, measurement window, exclusions, unknown values, and whether the
result is observed, derived, or unverified. Scorecard improvement never
changes constitutional, production, or mathematical status.

## Exact Phase 1 and Phase 2 issue/PR sequence

No issue, pull request, approval, setting change, or merge is created merely by
this ledger. The following is the required execution order after this baseline
is accepted.

| Seq. | Repository | Issue or operation | Pull request / output | Dependency and exit |
| ---: | --- | --- | --- | --- |
| 0 | `gcl-standards` | `GCL-OPT-BASELINE-001` | `[baseline] Admit Phase 1-2 optimality baseline and execution ledger` | This document only; validators and `git diff --check` must pass |
| 1 | `gcl-standards` | `[P0] GCL-STATUS-COHERENCE-001: reconcile effective, admitted, and adopted status` | Umbrella issue, no authority change | Opens only after sequence 0 is protected; owns `SC-01` through `SC-08` and `VAL-01` |
| 2A | `INTELLECT` | `GI-STATUS-PROJECTION-001: reconcile effective amendment and subordinate status` | `docs: reconcile effective constitutional status projections` | Updates README/status metadata and a time-scoped subordinate-status projection; substantive constitutional articles unchanged |
| 2B | `gcl-standards` | Child of `GCL-STATUS-COHERENCE-001` | `governance: prepare GCL-GHOS 0.1.1 documentary status successor` | Preserves exact `0.1.0`, prepares documentary-only `0.1.1`, schemas, fixtures, adversarial tests, digest equality, and the `VAL-01` portability repair; it does not yet create the admission record |
| 3 | `.github` Council Clerk | `GCL-STATUS-COHERENCE-REVIEW-001` | One digest-addressed packet covering only the exact heads of 2A and 2B | Distinct non-author agent Adversary and Referee findings; one authenticated `fyremael` Human Steward authorization; any subject-head or campaign-contract change invalidates the packet |
| 4A | `gcl-standards` | Protected source integration | Integration PR containing the exact reviewed `0.1.1` blobs and a new admission record | Admission names the reviewed source head and blob identities; a validator proves packet identity; after merge, close 2B as superseded rather than independently merging it |
| 4B | `gcl-standards` | Programme-adoption successor | Adoption PR selecting the exact protected `0.1.1` admission | Retains `0.1.0` lineage, marks the selected adoption gate complete, and preserves every nonclaim and organization-wide conformance boundary |
| 4C | `INTELLECT` | Protected constitutional projection integration | Merge the unchanged reviewed 2A head | Occurs only after the `0.1.1` admission and adoption are protected; INTELLECT remains constitutional authority and does not become standards-admission authority |
| 4D | `grandchallenge/.github` | `GCL-PUBLIC-STATUS-PROJECTION-001` | `docs: publish effective GCL authority and adoption status` | Generated from exact protected INTELLECT, admission, and adoption records; preserves GitHub's operational/evidentiary-only boundary |
| 4E | `gcl-standards` | `GCL-STATUS-COHERENCE-CLOSEOUT-001` | Final closeout PR adding the selected current-status projection and exact coherence receipt | Receipt binds the review packet, reviewed source heads, integration, adoption, INTELLECT, and public-profile merge identities; closes `SC-01` through `SC-08` and `VAL-01` |
| 5 | `.github` | `[P1] GCL-ORG-2FA-001: enforce 2FA without owner eviction` | Owner preflight, setting change, and exact readback evidence; no code PR substitutes for the setting | `jimsteeg` first enables accepted 2FA; zero disabled-member readback precedes Steward enforcement |
| 6A | `AETHER` | `[P1] GCL-AETHER-CONFORMANCE-001: migrate classic protection without a gap` | `governance: add GCL profile surfaces and conformance workflow` | Preserve existing strict contexts until replacement ruleset is active and read back |
| 6B | AETHER settings | Same issue | Active no-bypass main ruleset plus immutable-release-tag ruleset | Exact ruleset detail and required-context readback must pass before classic protection is retired |
| 6C | `gcl-standards` | `GCL-AETHER-READBACK-001` | `evidence: admit AETHER post-migration conformance readback` | Binds AETHER protected head, ruleset IDs and digests, surfaces, workflows, security settings, and claim boundaries |
| 7 | `.github` | `[P2] GCL-CREDENTIAL-BOUNDARY-001: admit App and break-glass inventory` | `security: publish bounded administrative credential inventory` | Names Apps and secret surfaces without secret values; every exception has owner, expiry, compensating control, and revocation path |
| 8A | `INTELLECT` | `GI-HUMAN-GOVERNANCE-TRANSITION-001` | `governance: adopt minimum steady-state human authorization model` | Records one-Steward authorization, second-owner recovery role, distinct agent review, escalation boundaries, effective date, and rollback |
| 8B | `gcl-standards#14` | Update and close roadmap issue | Closure comment links the effective INTELLECT record and exact readback | Issue trigger is this Human Steward instruction; closing the issue does not itself activate governance |
| 9 | `gcl-standards` | `GCL-OPT-PHASE12-CLOSEOUT-001` | `evidence: admit Phase 1-2 security, deviation, and scorecard baseline` | Adds owned deviation rows and first weekly machine-readable scorecard; all P0/P1 rows closed or explicitly blocking |

If sequence 2B changes the normative clauses rather than documentary status
only, stop and open a new substantive standards decision. It may not be
smuggled through the coherence packet.

## Completion rule

Phase 1 and Phase 2 are complete only when the protected records and live
readbacks satisfy their exit gates. A local branch, green CI, an issue closure,
a PR merge, a release, or publication of this ledger is not constitutional
activation, standard admission, programme adoption, organization-wide
conformance, an AETHER production fact, or mathematical certification.
