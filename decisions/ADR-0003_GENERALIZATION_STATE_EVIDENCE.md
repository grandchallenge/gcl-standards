# ADR-0003: Propose the Generalization-State Evidence Doctrine

**Date:** 2026-10-03  
**Status:** Proposed for exact-head Council review  
**Standard:** GCL-GS-00 version 0.1.0  
**Governing issue:** #98

## Context

GCL training and mechanism programmes increasingly compare architectures, optimizers, curricula, checkpoint trajectories, and reconstruction of learned capability.

arXiv:2609.33150v1 reports that language-model generalization behaviour can reverse across nearby pre-training checkpoints while conventional loss and capability trajectories remain comparatively smooth. The reported behaviour makes an existing methodological ambiguity operationally important: failure to express a computation can reflect non-acquisition, structural loss, changed accessibility/control, or behavioural suppression.

Without an explicit doctrine, GCL programmes can accidentally collapse those cases and over-interpret terminal checkpoints.

## Decision

Propose GCL-GS-00 as a candidate cross-programme methodological standard.

The standard's core distinction is:

**acquisition ≠ persistence ≠ accessibility/control ≠ behavioural expression.**

It also requires checkpoint-series evidence for trajectory claims, recovery/intervention tests when making persistence claims where feasible, explicit transition methodology, and a firewall against universal scalar diagnostics or unproven causal explanations.

## Alternatives considered

### Endpoint-only evaluation

Rejected as a general evidence rule for mechanism trajectories because endpoint comparisons cannot identify intervening reversals.

### Adopt the paper's capacity-allocation explanation

Rejected as premature. The paper motivates the research question but does not establish that explanation as a universal causal mechanism.

### Create a new standalone GCL programme only

Rejected at this stage. The issue is cross-cutting across curriculum, diagnostics, optimization, architecture, and reconstruction work. A methodological standard plus programme-specific experiments is the smaller durable intervention.

## Consequences

If admitted and adopted, affected programmes must sharpen the evidence behind claims that mechanisms were learned, lost, retained, or stabilized.

This may increase checkpoint-storage and diagnostic costs. It should reduce false monotonicity claims and make recovery, hysteresis, and state occupancy first-class experimental questions.

## Authority boundary

This ADR proposes a candidate standard only. It does not admit the standard, amend the Constitution, authorize organization-wide conformance, certify any scientific claim, or require programme adoption before the protected admission process is complete.
