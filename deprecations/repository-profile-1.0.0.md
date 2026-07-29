# Repository profile 1.0.0 field deprecation

**Status:** Proposed with GCL-GHOS 0.1.0 candidate reconciliation
**Superseded contract:** `repository_profile.schema.json` version 1.0.0
**Replacement:** version 1.1.0
**Affected adopters:** all repository profile fixtures
**Compatibility window:** until GCL-GHOS adoption and live profile migration

## Reason

Version 1.0.0 used `canonical_policy_source` to point at
`grandchallenge/gcl-standards`. That name collapsed constitutional law and
subordinate operating policy, and could be read as granting the registry power
it does not possess.

Version 1.1.0 separates:

- `constitutional_source`, fixed to the compact INTELLECT Constitution; and
- `operating_policy_source`, fixed to the candidate GCL-GHOS revision.

It also adds the `constitutional` repository profile and applies it to
INTELLECT.

## Migration

Candidate fixtures migrate immediately for review. Live GitHub custom
properties and repository settings must not be changed on the authority of
this record alone. They migrate only after `GI-AMEND-0001` and GCL-GHOS are
accepted at exact commits.

There is no silent compatibility alias: accepting an object that still uses
`canonical_policy_source` would preserve the authority ambiguity this change
is intended to remove.
