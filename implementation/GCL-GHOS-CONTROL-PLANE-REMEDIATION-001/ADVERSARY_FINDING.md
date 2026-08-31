# Adversary Finding

- Reviewed exact revision: `39d4af2b78beb95afd49ebb2b925656d1148f444`
- Reviewed tree: `31155534544907bce7e987b76d45884754e9bb43`
- Reviewer role: distinct non-author Adversary session
- Disposition: `PASS`
- Scope: technical and adversarial conformance only

The Adversary returned changes requested across multiple exact revisions. The
resolved findings covered direct ledger bypass, fabricated closure and gates,
unbound executor identity, incomplete topology admission, stale asynchronous
observations, invalid role completion, non-monotonic transactions, expired
leases, unrelated commit evidence, stranded post-expiry recovery, recovery
authority widening, non-exact claim replacement, ambiguous typed authority
claims, acceptance records carrying unattested semantic fields, and clean-runner
availability of exact external propagation consumers.

At the reviewed revision, 29 control-plane adversarial tests and repository
validation passed. The final review verified fail-closed parsing of multiple
authority claims and an acceptance execution manifest restricted to exact
scenario-to-test bindings. The validator rejects extra scenario result fields,
requires complete T01-T14 coverage, binds the mapping to the acceptance packet,
and executes every mapped test. No blocking ordinary correctness finding
remained. The workflow now checks out the exact external consumer commits into
distinct paths and exposes both roots at job scope to validation and tests.
Configured paths fail closed unless both are Git checkouts, and the controller
still binds repository, commit, path, authority class, content, and declared
blob identity. All live PR checks passed on the reviewed head.

This finding conveys no approval, authorization, merge, activation,
certification, publication, production, claim-promotion, or protected-state
authority.

## Final closeout pass

- Reviewed exact revision: `9eed42dc2559d2b58e3ef7f59a68545f27223f1c`
- Reviewed tree: `f1ed33b23201806aff8116335841f2bd0e1a0039`
- Disposition: `PASS`

The distinct Adversary independently matched the failed and successor control
refs, ruleset, repair and pilot PR identities, seven-event recovery ledger,
typed abort evidence, terminal reducer state, coherence merges, and complete
live open-PR inventory. It found no evidence mismatch or authority overclaim.
The absence of dedicated schemas for the two closeout summary JSON files was
recorded as nonblocking hardening because their cited identities were directly
verified and the summaries confer no authority.
