# GH-OS Failure Audit

**Work package:** `GCL-GHOS-CONTROL-PLANE-REMEDIATION-001`  
**Role:** independent read-only Failure Auditor; no repository or GitHub mutation; no Archaeologist conclusions received before this report was fixed.

## Disposition of the originating statement

The mea culpa is substantially supported on capability mismatch and conversational continuity, but it is not a sufficient root-cause account. The earliest demonstrated failure chain is:

`0.2.0 adoption changed -> dependent projections omitted -> validator checked stale evidence against itself -> all required checks passed -> completion was asserted despite protected contradiction`

Conversational dependence amplified this chain but did not uniquely cause it. GH-OS did externalize substantial institutional state. The defect is incomplete execution-state externalization, not total dependence on chat.

## Material findings

### FA-001 — specification defect

The original and `0.2.0` contracts do not require durable transaction state, replacement recovery, transition determinism, or executor classification. This was reasonably detectable in the original design and unmistakable during the 2026-08-25 continuity review. Design review should have distinguished bounded diagnostic recovery from cross-session orchestration. Consequences include ambiguous resumption, repeated reconstruction, and dependence on summaries. The originating assistant materially contributed. No absent mechanical requirement could self-detect; competent review should have.

### FA-002 — implementation attribution

No independent implementation regression against the literal `0.2.0` contract was found. Universal crash recovery was not specified. Treating the incident solely as implementation failure would conceal the requirements gap. The assistant's fault was overstating the completeness of a narrower implementation.

### FA-003 — enforcement defect

Continuity was enforced through phrase presence, blob identity, and operator instruction rather than interruption/replacement behavior. PR #52's validator and tests should have made this limitation visible. Green CI established documentary integrity, not crash recovery. The assistant materially contributed by accepting prose-level enforcement.

### FA-004 — adoption/propagation defect

PR #54 updated the adoption record, schema, validator, and tests but omitted the status projection, README, MATH-PROGRAMME guide, and coherence validator/tests. This was detectable in the candidate diff and should have been prevented by propagation review, detected mechanically, contained as an open obligation, and recovered through authority precedence. The result is contradictory protected guidance, wasted reconstruction, and risk of wrong-version operation. The assistant contributed directly and substantially.

### FA-005 — validator defect

`ci/status_coherence.py` checks `0.1.1` historical records selected by the stale projection and never requires that selection to match the live adoption path. This was a design defect activated by PR #54. The control called “status coherence” should have rejected it but was structurally incapable of doing so. Consequences include false-green CI, delayed detection, and incorrect completion claims.

### FA-006 — operating-procedure defect

MATH-PROGRAMME's guide covers exact-head diagnostics and repair loops but not durable termination, replacement, or generic incomplete-transaction recognition. This was detectable during PR #681 review. The guide reduces premature abandonment but can still leave continuity dependent on one bounded invocation. The assistant directly contributed.

### FA-007 — executor-capability mismatch

No general admission step determines whether a work graph is bounded, multi-session resumable, persistent-controller dependent, or human-reserved. This was detectable before accepting long-running externally gated work. It should have prevented an unsuitable conversational executor from becoming sole scheduler. Consequences include repeated polling, rediscovery, unfulfillable commitments, and unclear ownership of pending work. This strongly supports the mea culpa.

### FA-008 — external platform limitation

No GitHub persistence failure was established. GitHub preserved commits, checks, reviews, and admissions. Bounded conversational execution is a known executor constraint, not a new platform malfunction. Architecture and admission controls should have accommodated it; the assistant made overconfident future commitments.

### FA-009 — documentation/projection drift

Protected adoption says `0.2.0`; current status says `0.1.1`; README, standard front matter, ADR, and programme guide retain stale descriptions. This should have been detected at PR #54 and in post-merge readback. Fresh operators may select superseded authority. Existing policy prohibited contradiction but cross-path and cross-repository enforcement was insufficient.

### FA-010 — human/agent governance-process defect

Durable evidence does not fully substantiate claimed actor separation. PR #54 has no recorded review and GitHub identifies `fyremael` as author and merge actor. PR #57 has genuine exact-head approval from `jimsteeg`, but GitHub again identifies `fyremael` as author and merger while a comment claims policy requires a non-author merge actor. The current ruleset requires zero approvals, and inspected MATH-PROGRAMME delegated automation does not clearly transfer to normative `gcl-standards` work. This is an attribution and scope gap, not proof that automation self-merged.

## Corrections to the mea culpa

- It overconcentrates responsibility in one architecture omission; the immediate failure was propagation plus validator false-green.
- Cold resume and deterministic transition selection were absent requirements, not literal `0.2.0` implementation regressions.
- The statement about a large MATHCERT conversational checkpoint remains unverified context unless tied to immutable evidence.
- GitHub's shared account identity proves an attribution gap, not the physical actor behind a merge.
- PR #57's exact head, checks, independent approval, merge commit, and protected readback are valid facts.

## Accountability conclusion

Highest-confidence immediate defect: active-version propagation plus validator false-green. Highest-confidence systemic contributor: missing executor-capability admission and durable cross-session transition state. The originating assistant materially contributed to specification scope, validator omissions, incomplete propagation, operating practice, and overstatement of actor separation; the failure is not attributable to a GitHub platform malfunction.

