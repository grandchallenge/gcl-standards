# GCL-HIH-00 v0.1.1; Exact-Artifact Public Release Authorization Packet

**Packet identifier:** GCL-HIH-00-PUBLIC-RELEASE-011
**Prepared:** 2026-10-20
**Status:** PREPARED FOR HUMAN STEWARD DECISION; NOT AUTHORIZED; NOT RELEASED
**Council docket:** https://github.com/grandchallenge/gcl-standards/issues/103
**Original Council acceptance:** https://github.com/grandchallenge/gcl-standards/issues/103#issuecomment-6279230502
**Editorial successor review:** https://github.com/grandchallenge/gcl-standards/issues/103#issuecomment-6290234825
**Source correction:** https://github.com/grandchallenge/gcl-standards/pull/107
**Successor admission:** https://github.com/grandchallenge/gcl-standards/pull/108

## Decision requested

The Human Steward must decide **AUTHORIZE**, **REVISE** or **DECLINE** the exact v0.1.1 formal external GitHub Release described here. GCL's effective authority schedule identifies `fyremael` as ordinary Human Steward. An authentic, attributable exact-packet decision must be recorded before any tag or release action. An assistant, Council recommendation, CI result, protected merge, or request to prepare the release cannot substitute for reserved authorization.

The previously prepared [v0.1.0 release packet](RELEASE_PACKET.md) is preserved separately as unexecuted historical evidence; it does not authorize v0.1.1 publication.

## Exact release subject

**Repository:** `grandchallenge/gcl-standards`.
**Admitted version:** `GCL-HIH-00@0.1.1`, optional standards-layer convention.
**Proposed release tag:** `gcl-hih-00-v0.1.1`.
**Exact tag target:** `a4f3544aafdfde0c8095fec7371cb776ea0b5703`, the protected v0.1.1 successor-admission merge.
**Public release title:** *Human Intellectual Heritage Acknowledgment and AI Participation Disclosure, GCL-HIH-00 v0.1.1*.
**Channel:** Formal GitHub Release, distinct from the already-public source files.

| Exact artifact at the tag target | Git blob SHA-1 |
| --- | --- |
| `standards/GCL-HIH-00.md` | `a64c68459ca0f3ed8c586fd53f5ce6b8351ba535` |
| `templates/AI_PARTICIPATION_DISCLOSURE.md` | `52e9d9cc667ad5b492d1ebae112360c157f11361` |
| `admissions/GCL-HIH-00-0.1.1.json` | `ae3d7a76d9a3f0c885a50da9e9215fa89663e3b9` |
| `status/GCL-HIH-00-current.json` | `c697caa5d6c3f78dea331b65871d416a631aa865` |
| `standards/history/GCL-HIH-00-0.1.0.md` | `7f381080b7dd98a7f922274a9693bbc7ead0f40c` |
| `templates/history/AI_PARTICIPATION_DISCLOSURE-0.1.0.md` | `4b5577a396214e3090e969808bf601ab035413de` |

The editorial successor corrects status labels only; the full and short acknowledgments, accountable-authorship clause and substantive disclosure fields remain unchanged. Source visibility is not a formal GitHub Release.

## Approved-format preparation materials

- [Exact release notes](RELEASE_NOTES-0.1.1.md) provide the proposed publication wording.
- [Release manifest](RELEASE_MANIFEST-0.1.1.json) records exact Git blobs, SHA-256 digests and file sizes of the source artifacts and release notes.
- Source archive is GitHub-generated from the pinned tag; no fictitious executable/SBOM is proposed for these text-only materials.
- The release notes and manifest are separate protected-main preparation artifacts; **they are not part of the earlier source-admission tag tree**. Their own integrity is protected and separately verifiable after this preparation PR merges.

**Rights:** The registry's `LICENSE` is MIT, Copyright 2026 Grand Challenge Labs. Retain that notice. Publication does not license third-party works, model-training datasets, individually identifiable authors' materials, or AI weights; it does not establish rights clearance, consent, compensation or specific training examples. It cannot replace identifiable attribution, direct citations, verification, or publication policy compliance.

**Institutional scope:** Optional acknowledgement and factual AI participation disclosure; no organisation-wide mandate, automatic programme adoption, mathematical certification or constitutional promotion.

## Authorization and controlled publication procedure

1. Re-read the live INTELLECT Constitution, Article X and effective `GI-STEWARD-0003` schedule; verify the identity and authority of the actual Human Steward. Review this packet from its final protected commit.
2. Confirm the protected v0.1.1 admission, Council editorial review, current registry status and exact source/tree identities. Run `python ci/verify_hih_release.py --offline` against the preparation commit and inspect its checks. The source hashes at target commit must match this packet and manifest. Any change to the packet, tag, title, notes or rights/claim language requires a fresh review/decision.
3. Check GitHub live for an existing `gcl-hih-00-v0.1.1` tag or GitHub Release. Stop and reconcile a pre-existing or unexpected identity. Never force-rewrite a tag.
4. **Obtain and record the authentic Human Steward decision** `AUTHORIZE`, `REVISE` or `DECLINE` on this exact version, packet, target, title, release-note bytes and GitHub channel. Record an attributable URL in Council issue #103. Silence, previous high-level approval, or this preparation request does not constitute consent.
5. Only upon `AUTHORIZE`, create the tag at the pinned protected target and publish a single GitHub Release with the exact title and notes. Publication tools should read back uncertain responses before any new attempt. No draft release or tag is created by this preparation.
6. Verify the actual published release URL, tag target, rendered notes, source artifacts, and licensing. Record a durable publication receipt with exact GitHub response, source tree and manifest identities.
7. Reconcile `status/GCL-HIH-00-current.json`, registry README, and Council issue #103 on a separate protected PR. No broader programme adoption is inferred.

**Suggested exact Human Steward decision once this packet is protected and reviewed:**

> AUTHORIZE formal publication of GCL-HIH-00 v0.1.1 through a GitHub Release in grandchallenge/gcl-standards, with tag gcl-hih-00-v0.1.1 pointing to protected commit a4f3544aafdfde0c8095fec7371cb776ea0b5703, using the exact protected GCL-HIH-00-PUBLIC-RELEASE-011 packet and its linked release notes and manifest.

The text above is a *template for a future authentic decision*, not authorization already given.

## Disposition

**STANDARDS ADMITTED; FORMAL PUBLIC RELEASE PREPARED BUT ON HOLD.**

Human Steward exact-publication authorization: **NOT RECORDED**.
Tag: **NOT CREATED**. GitHub Release: **NOT CREATED**.
Programme-specific adoption: **NOT ASSERTED**.

**Next obligation:** exact-packet Human Steward decision; only then may release execution and public-status reconciliation proceed.
