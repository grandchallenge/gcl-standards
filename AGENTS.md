# Agent Instructions

- Preserve the authority boundaries in `standards/GCL-GHOS-00.md`.
- Never infer mathematical certification from CI, issue, Project, Discussion,
  release, or package state.
- Treat `programme-adoption/` as explicit, commit-addressed adoption records.
- Update schemas, fixtures, and adversarial tests together.
- Automation may propose changes through pull requests; it may not approve,
  merge, certify, or promote a claim.
- Run `python ci/validate.py` and the unit-test suite before proposing changes.
