# GCL-GS-00: Generalization-State Evidence Doctrine

**Version:** 0.1.0  
**Status:** Candidate normative standard; no cross-programme effect until protected admission and programme adoption  
**Registry:** grandchallenge/gcl-standards  
**Council issue:** grandchallenge/gcl-standards#98  
**Scope:** Training-state, checkpoint-selection, learned-mechanism, curriculum-control, capability-persistence, and generalization-dynamics claims

## 1. Purpose

GCL work SHALL NOT infer monotone improvement of learned computational mechanisms solely from smoother loss, more training, a later checkpoint, or better endpoint benchmark performance.

When a work package makes a claim about what a model has learned, retained, lost, or can generalize, it SHALL distinguish, where material:

1. **acquisition** — whether a computation was learned;
2. **persistence** — whether relevant computational substrate remains present;
3. **accessibility/control** — whether the computation can still be recruited under a declared condition or bounded intervention;
4. **behavioural expression** — whether the computation controls the observed answer under the declared evaluation.

The compact operational rule is:

> **Treat checkpoints as potentially distinct computational states. Separate acquisition, persistence, accessibility, and expression before making mechanism claims.**

## 2. Motivating evidence

The immediate motivating source is:

Jiaxin Wen, Zhengxuan Wu, Dawn Song, Lijie Chen, *Generalization Dynamics of LM Pre-training*, arXiv:2609.33150v1, submitted 2026-09-27.

Exact version URI:

https://arxiv.org/abs/2609.33150v1

The paper reports non-monotone generalization behaviour across nearby language-model pre-training checkpoints, including abrupt reversals on several behavioural probes while conventional loss and benchmark trajectories remain comparatively smooth. It also reports downstream differences after post-training from different pre-training checkpoints and a preliminary data-selection intervention that stabilizes one target behavioural mode.

These observations motivate this doctrine. They do not establish a universal causal mechanism.

## 3. Core distinctions

### GS-1: Acquisition

Evidence that a behaviour is expressed at time t MAY support that a compatible computation is available at t, subject to the evaluation contract.

Failure to express the behaviour at time t SHALL NOT by itself establish that the computation was never acquired.

### GS-2: Persistence

A claim that a computation persists across checkpoints requires evidence stronger than behavioural similarity.

Useful evidence MAY include parameter-path localization, representation correspondence, circuit/path continuity, causal substitution, recoverability, or another declared structural bridge.

### GS-3: Accessibility and control

A computation may persist while losing behavioural control.

Work SHALL distinguish a latent or recoverable computation from one that is currently selected, routed, attended, or otherwise dominant.

### GS-4: Behavioural expression

Expression is evaluation-conditional.

The work SHALL state the prompt, task, scoring rule, decoding rule, seed structure, and other conditions needed to interpret the observed behaviour.

A change in expression is not automatically a change in underlying mechanism.

## 4. Checkpoint-series requirement

When the research question concerns training dynamics rather than endpoint quality, the work SHOULD evaluate a checkpoint series dense enough to detect reversals at the timescale being claimed.

A comparison of only the initial and final checkpoint SHALL NOT support a claim that the intervening mechanism trajectory was monotone.

Checkpoint spacing, token count or compute coordinate, and any interpolation or averaging procedure SHALL be disclosed.

## 5. Transition evidence

A claimed training-state transition SHOULD include:

- the behavioural or mechanistic state definition;
- at least one pre-transition and one post-transition checkpoint;
- replication or uncertainty treatment appropriate to the probe;
- soft-score evidence when a hard threshold could manufacture an apparent discontinuity;
- a statement of whether ordinary loss or benchmark metrics changed concurrently;
- competing explanations that remain open.

A transition label such as G → P or P → G is a shorthand for a declared regime definition, not an ontological statement that there are only two model states.

## 6. Mechanism-evidence ladder

GCL work SHOULD classify evidence at the strongest supported level:

- BEHAVIOURAL_STATE_CHANGE;
- REPRESENTATIONAL_CHANGE_SUPPORTED;
- ACCESSIBILITY_SHIFT_SUPPORTED;
- MECHANISM_PERSISTENCE_SUPPORTED;
- MECHANISM_CHANGE_SUPPORTED;
- CAUSAL_MECHANISM_ESTABLISHED;
- UNRESOLVED.

A behavioural transition SHALL NOT be promoted directly to CAUSAL_MECHANISM_ESTABLISHED without an appropriate causal bridge.

## 7. Recovery tests

Where a previously expressed capability disappears, a work package SHOULD test whether it can be restored by a declared bounded intervention class when such a test is technically feasible.

Let Delta be the allowed intervention class and C(delta) its declared cost.

A recovery quantity MAY be defined by

R_Delta(theta,q) = inf over delta in Delta of C(delta)

subject to restoration of the target behaviour or capability on probe q.

The intervention class, restoration criterion, and cost SHALL be explicit.

A low recovery cost supports accessibility or persistence only relative to the declared intervention contract. It does not prove identity of the recovered mechanism.

## 8. State occupancy and transition summaries

For a declared regime G and checkpoint set {theta_t}, work MAY report quantities such as

O_G = (1/T) sum_t 1[theta_t in G]

and a transition count or rate over declared checkpoint spacing.

These quantities are comparative summaries.

They SHALL NOT be represented as universal scalar measures of intelligence or generalization.

## 9. Scalar-diagnostic firewall

No single effective-rank, Fisher, sharpness, gradient-cosine, spectral, activation, entropy, or related scalar statistic SHALL be treated as a universal generalization-state detector without independent evidence across models, tasks, and transitions.

Best-layer, best-head, best-metric, or best-checkpoint retrospective selection SHALL be disclosed.

Prospective or held-out transition prediction is preferred when the research claim is predictive.

## 10. Curriculum and data-control claims

When data selection or curriculum control is claimed to stabilize a desirable regime, the work SHALL distinguish:

- the probe used to define the regime;
- the data-selection mechanism;
- the target model and checkpoint;
- whether control transfers to other probes or tasks;
- whether the effect persists after the control intervention ends;
- whether ordinary capability or loss is traded off;
- whether the effect is reproducible across seeds or training replicas.

Control of one probe SHALL NOT be generalized to broad capability without separate evidence.

## 11. Architecture and optimizer comparisons

When an architecture or optimizer is claimed to improve transferable computation, terminal loss or endpoint capability alone SHOULD NOT be the sole evidence where checkpoint dynamics are feasible to measure.

Comparisons MAY include:

- desirable-state occupancy;
- transition frequency;
- transition predictability;
- recovery cost;
- hysteresis or path dependence;
- post-training transfer from selected checkpoints.

These metrics remain conditional on their declared probes and sampling contracts.

## 12. Hysteresis and path dependence

Where training-control surfaces permit, work SHOULD test whether nominally similar final conditions reached through different training histories produce distinguishable states.

A path-dependence claim requires a declared comparison of histories and final evaluation conditions.

The mere fact that two independent runs differ does not establish hysteresis.

## 13. Capacity-allocation claim boundary

The motivating paper proposes competition between shallow and generalizable circuits for bounded model capacity as an explanation of mode-hopping.

GCL MAY investigate this hypothesis.

GCL SHALL NOT treat it as doctrine unless independently supported by mechanism-level evidence.

Alternative explanations, including routing changes, representational reorganization, optimizer-state dynamics, data-window effects, evaluation sensitivity, or other causes, remain open.

## 14. Relation to existing GCL research

This doctrine is intended to support, without predetermining results in:

- Minimal Curricula and Reasoning Bases;
- Learning Progress as a Search Operator;
- CPS and optimizer-state dynamics;
- K-DIAGNOSTICS and spectral/operator diagnostics;
- the Residual and capability reconstruction;
- nGPT/RUNT and geometry-constrained architectures;
- Muon-like, manifold, and MODULUS-derived optimization;
- optionality/correction-capacity research.

Programme adoption MAY define stronger domain-specific requirements.

## 15. Claim boundary

GCL-GS-00 is a methodological and evidentiary standard.

It does not establish:

- that mode-hopping occurs in every model family;
- that any specific checkpoint is superior;
- that a particular circuit is present;
- that capacity allocation causes a transition;
- that a recovery intervention reconstructs the same mechanism;
- that a scalar diagnostic is universal;
- mathematical certification;
- constitutional authority;
- organization-wide conformance merely by being present in this registry.

Candidate text becomes normative only through applicable protected admission and programme-adoption processes.

## 16. Conformance statement

A work package conforms to GCL-GS-00 only when its training-state or learned-mechanism claims state the checkpoint/evaluation contract, distinguish acquisition from persistence, accessibility, and expression where material, avoid endpoint-only monotonicity inference, disclose transition and selection methodology, preserve causal claim boundaries, and identify unresolved competing explanations.

Documentation that merely uses the phrase “generalization state” without these distinctions is not conformance.
