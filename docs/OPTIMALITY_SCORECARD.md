# Weekly optimality scorecard interface

The weekly scorecard is a machine-readable observation record governed by
[`schemas/optimality_scorecard.schema.json`](../schemas/optimality_scorecard.schema.json).
It is evidence and does not itself create conformance, production, mathematical,
certification, novelty, deployment, or commercial authority.

Every metric contains either a numeric `value` or an explicit `unknown` object,
plus its unit, observed/derived/unknown/unverified status, target, evidence,
measurement window, exclusions, and exact source heads. An unknown metric must
reference an owned deviation; it may never be coerced to zero.

Metric meanings are fixed as follows:

- `status_contradictions`: conflicts detected across selected current status projections.
- `unprotected_default_branches`: repositories without a compliant active ruleset or compliant classic protection.
- `human_actions_per_governed_decision`: substantive authenticated Steward authorizations; excludes merge clicks, 2FA setup, and account recovery.
- `strategic_lanes_in_progress`, `active_issues_without_finite_next_obligation`, and `handoffs_lacking_exact_identities`: unknown until authoritative registries are admitted in later phases.
- `median_pr_decision_time_hours`: creation to closure for human-authored PRs in the rolling seven-day window; bots are excluded, and external dependencies are excluded only with an explicit controlled label and linked blocker.
- `reproducible_governed_lifecycle`: admitted production demonstrations only.
- `github_inferred_mathematical_claims`: validated inference violations; zero observations never imply global mathematical correctness.

The scheduled producer may open a draft pull request. It may not write directly
to protected `main`, approve, merge, or promote a claim. Missing or forbidden
evidence is recorded as `unknown` with an owned deviation.
