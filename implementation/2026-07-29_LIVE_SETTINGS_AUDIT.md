# Live GitHub settings audit

Date: 2026-07-29  
Scope: ten public governed repositories in `grandchallenge`  
Result: PASS for controls that can be activated with the current membership

This is a read-back record of GitHub state, not a mathematical certificate and
not an adoption of proposed ADR-0001. The API sweep read repository metadata,
custom-property values, active rulesets, security configuration, default-branch
trees, and exact heads. Ruleset digests are SHA-256 hashes of the compact update
payload: name, target, enforcement, bypass actors, conditions, and rules.

## Organization controls

- Base repository permission is `read`.
- Repository creation, deletion, transfer, visibility changes, team creation,
  and App installation are owner-only.
- Actions permits organization-local and GitHub-owned Actions plus only:
  `leanprover/*`, `ossf/*`, `raven-actions/actionlint@*`,
  `azohra/shell-linter@*`, `release-drafter/release-drafter@*`, and
  `zulip/github-actions-zulip@*`.
- Every Action reference must also use a full commit SHA.
- Default `GITHUB_TOKEN` permissions are read-only and workflow tokens cannot
  approve pull requests.
- Six organization custom properties exist: `authority_scope`,
  `claim_promotion_role`, `constitutional_profile`, `public_programme`,
  `risk_tier`, and `workflow_profile`.

The third-party allowlist does not authorize mutable refs. Provider pull
requests demonstrated the two independent controls: the SHA-pinned actions
failed at workflow startup before their named repositories were admitted, then
succeeded under the unchanged full-SHA requirement.

## Repository identities and properties

| Repository | Exact head | Profile | Authority scope | Claim role | Risk | Workflow |
| --- | --- | --- | --- | --- | --- | --- |
| MATH-PROGRAMME | `813f53ea28e1d941cc16c8f3da517c0dcfdc08a5` | Programme | mathematics-programme | programme-policy | critical | governance |
| MATHFORGE | `533f6ff532d047975faa1950a9ed60806afceb5f` | Forge | candidate-discovery | none | high | mathematics |
| MATHSOLVE | `6c2e3e6d9c7d2b30fa0f8e0129a3b7eeaf9494af` | Solve | work-execution | none | high | mathematics |
| MATHCERT | `3c36f63b8552b30d49e976997ad164304e8e787f` | Cert | certification | mathcert-only | critical | mathematics |
| INTELLECT | `7919b3daf16e063db18b0ee48ebad22549643728` | Provider | provider | none | high | provider |
| GLOSS | `bee1dfcc7d5c8a012863be3ab779fd3fb2466a5b` | Provider | provider | none | standard | provider |
| .github | `0957c09297f9d625b9225a234f5c29a2200318b4` | Community | community | none | high | community |
| gcl-standards | `7d1628d6d947a5cc3954ff33a841e416a2ea25cb` | Standards | cross-programme | none | critical | governance |
| lean-action | `83acf3a9f4994b48ecc32f41c8da9475042d10cc` | Provider | provider | none | critical | provider |
| upload-pages-artifact | `1976f492c26a307fdc9c381f8e86cd26932ed1ca` | Provider | provider | none | critical | provider |

Every repository has `public_programme: true`.

## Ruleset read-back

| Repository | Ruleset ID | Ruleset digest | Required checks |
| --- | ---: | --- | --- |
| MATH-PROGRAMME | 17137629 | `a6bedf9d912b96435b6e007d71de244cffb3ea497dacab384d5bc09706ef0d45` | `validate-json`; three exact Lean/evidence replays; `policy / policy`; `security / action-policy` |
| MATHFORGE | 17137626 | `42b41b21a64aff53a4bdd62eb3d6c7a4ec8d7b5dbb507674e96752c5604c4151` | `reconnaissance`; `policy / policy`; `security / action-policy` |
| MATHSOLVE | 17137627 | `fa6890f8123b943532ac2bb90d44123734c8d91014351b4b362d3f88fcf1217e` | `ledgers`; `policy / policy`; `security / action-policy` |
| MATHCERT | 17137628 | `e5954469c652d999aade9461c00c17645e7cdd906290ce51160bbf122321295b` | `certify`; `policy / policy`; `security / action-policy` |
| INTELLECT | 19964077 | `7b81234002e821f3c13d3c996b80a8adf3eced9f2a9d6f6dd1747b8370bbe10b` | Python 3.11 and 3.12 tests; `policy / policy`; `security / action-policy` |
| GLOSS | 19964070 | `c205a37356e2da56feb0b2f01514fd2470ae4f1e031bac720120a83a4a9ab2d5` | `package-contracts`; `lean-stable`; `policy / policy`; `security / action-policy` |
| .github | 17137624 | `58e5d4dadac4409888d1580de03d68eb396c45a47aeb9dc834f7f84843dc96c0` | `policy / policy`; `security / action-policy` |
| gcl-standards | 19962512 | `2eec4ac051bedd64cb1bf4cc5b9443df3b4a546a9308a91cfabf8aea9c037559` | `standards-policy`; `policy / policy`; `security / action-policy` |
| lean-action | 19965519 | `30e4ddf39f1a4e4866bae831a4595449c498e5eb3a47e93c0d9cfdff1bcc1a33` | `policy / policy`; `security / action-policy` |
| upload-pages-artifact | 19965833 | `30e4ddf39f1a4e4866bae831a4595449c498e5eb3a47e93c0d9cfdff1bcc1a33` | `policy / policy`; `security / action-policy` |

Every listed ruleset is active on the default branch, uses strict status checks,
requires a pull request and resolved conversations, dismisses stale reviews,
blocks force pushes and deletion, and has zero bypass actors. Every repository
also has one active immutable-tag ruleset.

## Common repository controls

The read-back was identical across all ten repositories:

- Wiki disabled;
- branch auto-deletion enabled;
- merge commits and squash merges enabled;
- rebase merges disabled;
- auto-merge enabled;
- secret scanning and push protection enabled;
- Dependabot security updates enabled;
- private vulnerability reporting enabled;
- `CODEOWNERS`, `SECURITY.md`, `SUPPORT.md`, `CITATION.cff`, `AGENTS.md`,
  `.github/dependabot.yml`, `.github/release.yml`,
  `.devcontainer/devcontainer.json`, and
  `.github/workflows/gcl-conformance.yml` present.

CodeQL default setup is configured on the eight repositories containing
supported Python or Actions-analyzable code. The two shell/composite provider
forks have no supported CodeQL language; their shared Action policy, upstream
test matrices, ShellCheck/actionlint where applicable, secret scanning, and
push protection remain active.

## App-backed administrative evidence

`gcl-release-trust` protected run
<https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30450610588>
used a short-lived installation token to apply and read back the four
administrative rulesets at exact head
`813f53ea28e1d941cc16c8f3da517c0dcfdc08a5`.

- evidence artifact: `8723362498`;
- artifact SHA-256:
  `b6f153fda1ce0d80742828aa6ede7a51c0070e908babdc924df1fe6aef65a3da`;
- canonical evidence SHA-256:
  `acd7e9c3ea10e9c03ea5dc81a0b84918d7241fea886426d2304e168b10c936f8`;
- exact-head Programme policy:
  <https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30450487344>;
- exact-head Pages publication:
  <https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30450675046>;
- live and admitted index SHA-256:
  `9a54a3831d6fb0922b1e21a792c246051d1d8f078621fac5da5e87cdd59535c7`.

## Portfolio reconciliation

The App-backed Council Clerk reconciliation
<https://github.com/grandchallenge/.github/actions/runs/30451002957>
ran at exact `.github` head
`0957c09297f9d625b9225a234f5c29a2200318b4` and reported
`missing_before: 0`. Evidence artifact `8723478494` has SHA-256
`168cd591b9f1d15fd3027ab59ebfd4d705218865b72e252b7f79e9c9c137ddd1`.
The App changed no claim status.

## Controls awaiting real human or plan prerequisites

The current single-member organization cannot truthfully enable independent
approval, CODEOWNER approval, last-push approval, Referee environment review,
self-review prevention, a second recovery owner, the #108/#109 fixed-revision
trial, or merge queues. Secure-methods-only 2FA awaits removal of SMS from the
owner account. Organization-wide rulesets await GitHub Team. Two consecutive
weekly drift-free observations necessarily remain future evidence.

These are activation prerequisites, not unexplained technical drift. They
remain tracked in
<https://github.com/grandchallenge/gcl-standards/issues/4>.
