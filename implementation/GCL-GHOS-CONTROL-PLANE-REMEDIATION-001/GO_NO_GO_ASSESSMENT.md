# GH-OS Go / No-Go Assessment

## Current disposition

`GO_WITH_RESTRICTED_EXECUTOR_TOPOLOGY`

GH-OS can now support interruptible and replaceable agent execution when the
work is admitted to a compatible topology and all workflow state is carried by
the protected control store. A bounded conversational executor may execute one
bounded transaction or resume a multi-session ledger; it may not be admitted as
the sole controller of persistent unattended work. Such work must be decomposed
or assigned an admitted persistent controller.

## Exit evidence

The implementation, server-reachable store validator, and event-boundary repair
were admitted through protected main. The `0.1.1`/`0.2.0` contradiction and all
declared local and external current projections were reconciled and read back.
The first live pilot was preserved as failed evidence. Its successor ref then
demonstrated direct-push rejection, cold asynchronous-wait recovery, exact prior
prefix validation, a deliberately expired transaction, replacement of the dead
executor claim, evidence-bound abort, and deterministic recovery to `READY`
with no open transaction. Exact identities are in `PILOT_EVIDENCE.json`.

## Cost and project-value assessment

The shared control-plane repair is smaller than retiring or replacing GH-OS and
preserves useful exact-identity, authority, and provenance controls. The audit
therefore does not justify closing an active project on cost grounds. It does
justify pausing only the incompatible controller assignment, not the underlying
project, and minimizing volunteer work to one later exact-head human disposition
where the governing route requires it.
