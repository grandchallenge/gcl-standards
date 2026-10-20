# HIH editorial status reconciliation; v0.1.1

**Work ID:** GCL-HIH-00-EDITORIAL-011
**Authority:** Council non-reserved exact-revision editorial review; Human Steward remains reserved for formal public representation.
**Predecessor:** v0.1.0, accepted [Council finding](https://github.com/grandchallenge/gcl-standards/issues/103#issuecomment-6279230502), protected admission [PR #105](https://github.com/grandchallenge/gcl-standards/pull/105).
**Scope:** Correct outdated candidate/draft status language in the canonical readable documents; preserve substantive acknowledgment/disclosure wording verbatim. New 0.1.1 metadata acquires standards-layer effect only on its own reviewed protected admission; does not grant programme adoption or GitHub Release authority.

## Immutable predecessor sources

- `standards/history/GCL-HIH-00-0.1.0.md`: Git blob `7f381080b7dd98a7f922274a9693bbc7ead0f40c`; exact copy of original `standards/GCL-HIH-00.md`.
- `templates/history/AI_PARTICIPATION_DISCLOSURE-0.1.0.md`: Git blob `4b5577a396214e3090e969808bf601ab035413de`; exact copy of original companion template.
- `admissions/GCL-HIH-00-0.1.0.json`, `status/GCL-HIH-00-current.json`, original Council decisions, and original v0.1.0 `RELEASE_PACKET.md` remain unchanged in the source correction. The original packet still explicitly targets its original immutable admission commit; it must not be silently reinterpreted as a v0.1.1 release authorization.

## Editorial scope and acceptance

- Front matter references authoritative registry status instead of perpetually claiming a Council candidate, unadmitted work, or a draft disclosure.
- Current canonical text identifies v0.1.1 as an editorial successor, and acknowledges that the predecessor v0.1.0 is admitted.
- Stale prospective Council-review and proposal-only statements are replaced by historical provenance and precise admissions/public-release separation.
- Both the full and short human intellectual heritage acknowledgment passages, including the accountable authorship sentence, remain textually unchanged; disclosure template fields and use guidance remain unchanged.
- Neither editorial PR integration nor admission constitutes formal external release. No release/tag is created; v0.1.0 historical bytes and optional-use status are preserved.
- `tests/test_hih_editorial_fidelity.py` provides executable regression tests for immutable predecessor Git blobs, exact acknowledgment bodies, unchanged disclosure fields, and non-stale status pointers.

**Review instructions:** Run the fidelity tests, inspect the exact successor Git blobs, apply role-scoped Adversary/Verifier/Referee review, and only then create a successor admission record on a subsequent protected PR. Public release requires a separately authorized exact-release packet.
