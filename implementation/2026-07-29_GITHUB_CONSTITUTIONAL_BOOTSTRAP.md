# GitHub constitutional bootstrap ledger

Date: 2026-07-29  
Operator: `fyremael`  
Status: technical bootstrap complete; Steward-supervised agent review pending

This ledger records operational installation evidence. It does not adopt
ADR-0001, certify mathematics, or change a claim disposition.

## Authority and commons

- `gcl-standards` bootstrap: `dc3951cc560f946591f78f6d2b2f1621a130e1df`
- constitutional team ownership: `c5604226b306a1b6fe104757a3852ded5cba2bb9`
- ratification issue: <https://github.com/grandchallenge/gcl-standards/issues/3>
- human-control activation issue:
  <https://github.com/grandchallenge/gcl-standards/issues/4>
- organization commons integration:
  <https://github.com/grandchallenge/.github/pull/6>
- nonbinding Discussions notice:
  <https://github.com/orgs/grandchallenge/discussions/7>
- public portfolio: <https://github.com/orgs/grandchallenge/projects/1>

Organization Discussions use `.github` as their source. Categories are
Announcements, Ask the Council, Research Proposals, RFC Deliberation,
Reproducibility Help, and Show-and-Tell.

## Repository migrations

| Repository | Contract PR | Merge commit |
| --- | --- | --- |
| MATH-PROGRAMME | [#131](https://github.com/grandchallenge/MATH-PROGRAMME/pull/131) | `bbe1872d838e5855061724c1a60f837a0767250c` |
| MATHFORGE | [#26](https://github.com/grandchallenge/MATHFORGE/pull/26) | `3f416cba0b80fae40c6c421a059c6b2c48028657` |
| MATHSOLVE | [#78](https://github.com/grandchallenge/MATHSOLVE/pull/78) | `1da78f09ce7e3c12105ed56fb694d64bbc824517` |
| MATHCERT | [#33](https://github.com/grandchallenge/MATHCERT/pull/33) | `ccdf51f2bd2c2fdbb6aa28a00a45c8b44cd9c294` |
| INTELLECT | [#10](https://github.com/grandchallenge/INTELLECT/pull/10) | `e58a2f49b4cbcb1aeebb556bffcb87ab657ec8b8` |
| GLOSS | [#3](https://github.com/grandchallenge/GLOSS/pull/3) | `715d21e632e977d1ac818f2b2c9a0d1f562ecd7e` |

Each migrated repository has an explicit authority boundary, team CODEOWNERS,
grouped Actions dependency updates, release configuration, a Codespaces
definition, and a SHA-pinned call to the shared conformance workflow.

## Apps and automation

- `gcl-council-clerk`, App ID `4423674`, installation `149809110`, installed
  organization-wide with metadata read and checks, issues, pull requests, and
  organization Projects write.
- Council Clerk reconciliation workflow:
  <https://github.com/grandchallenge/.github/actions/runs/30444536385>
- `gcl-release-trust`, App ID `4423678`, installation `149809343`, installed
  only on MATH-PROGRAMME, MATHCERT, MATHSOLVE, and INTELLECT with
  administration write, Actions read, Issues write, and metadata read.

Both Apps are webhook-free. They mint short-lived installation tokens from
repository or protected-environment secrets. Neither App has review-approval
authority, a ruleset bypass, or a protected-branch write path.

### Release Trust proof

- ruleset-native administration change:
  <https://github.com/grandchallenge/MATH-PROGRAMME/pull/135>
- exact-head Programme policy before administration:
  <https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30446169969>
- exact-head Pages publication:
  <https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30446339153>
- protected `mode: apply`, `close_child_issues: true` run:
  <https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30446399649>
- release-trust evidence artifact: `8721612194`
- artifact SHA-256:
  `719c28ea73b69cfcb07049988ab48f231c235160e8c2b01f48761b49623ac33e`
- canonical evidence SHA-256:
  `a3cfeea6a58de0e193015b96fd5929567bae9a3ee2aca68efe52795474669a85`
- App-only verify run after removal of the temporary human PAT:
  <https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30446476966>
- admitted audit:
  <https://github.com/grandchallenge/MATH-PROGRAMME/pull/136>
- exact-head Programme policy after audit merge:
  <https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30446915861>
- exact-head Pages publication after audit merge:
  <https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30447093527>

The authoritative Programme audit records
`operational_release_complete: true`, no remaining blockers, and a `CLOSE`
umbrella disposition. MATH-PROGRAMME issue #6 remains closed with the refreshed
evidence chain.

## Live controls

- Base repository permission: read.
- Member repository creation, deletion, transfer, visibility changes, team
  creation, and App installation: owner-only.
- Actions: organization-local and GitHub-owned plus only `leanprover/*`,
  `ossf/*`, `raven-actions/actionlint@*`, `azohra/shell-linter@*`,
  `release-drafter/release-drafter@*`, and
  `zulip/github-actions-zulip@*`; full commit SHA policy enabled.
- Default `GITHUB_TOKEN`: read-only and cannot approve pull requests.
- One active repository main ruleset per profile, with no bypass actors,
  strict required checks, pull requests, resolved conversations, stale-review
  dismissal, no force pushes, and no deletion.
- Active immutable-tag rulesets and immutable Releases on every governed
  repository.
- Wikis disabled, merged branches auto-deleted, rebase merges disabled.
- Secret scanning, push protection, vulnerability alerts, security updates,
  private vulnerability reporting, and CodeQL default setup enabled.
- Protected admission environments use protected branches and disallow admin
  bypass.
- The Grand Challenge Portfolio has saved Portfolio, Promotion Queue, Council
  Review, Certification, Blocked Work, Overdue Review, Releases, and Security
  views. Their filters consume organization issue fields or governed labels.

The organization-owned forks `grandchallenge/lean-action` and
`grandchallenge/upload-pages-artifact` exist solely to pin nested composite
Action dependencies that upstream still references by mutable version tags.
Governance consumes their exact commits.

The final live read-back, ruleset digests, exact heads, custom properties,
security settings, merge settings, and contract-file inventory are recorded in
[the live settings audit](2026-07-29_LIVE_SETTINGS_AUDIT.md).

## Temporary staffing override

`GI-STEWARD-0001` makes the Human Steward the only required human during
bootstrap and permits agents to staff every other office. The additional-human
controls below remain inactive, but their absence is no longer an activation
blocker:

1. independent approval, CODEOWNER review, and last-push approval;
2. Referee environment approval with self-review prevention;
3. a second recovery owner and two independent contributors;
4. MATH-PROGRAMME and MATHCERT merge queues;
5. an additional-human fixed-revision review for Programme issue 108 / PR 109;
6. secure-methods-only organization 2FA (the current owner must first remove
   SMS 2FA);
7. Team-plan organization rulesets.

Future human onboarding is tracked in
[issue 4](https://github.com/grandchallenge/gcl-standards/issues/4). No
bootstrap record may describe these deferred controls as active. The active
bootstrap review path instead requires distinct non-author agent findings and
Human Steward authorization.

GitHub Projects custom charts currently do not expose the organization issue
fields as grouping axes. Promotion Gate and Next Review therefore remain
truthfully represented by filtered views; no proxy chart is published as gate
distribution, review latency, blocked age, or evidence freshness.

## Completion criterion

After the Steward-supervised agent staffing changes are admitted, two
consecutive weekly Council Clerk, policy, security, project, and release-trust
runs must report no unexplained drift. Only then may the Council accept a
completion PR that references exact run IDs and evidence digests.
