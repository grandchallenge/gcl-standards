# GCL Codex Execution Memorandum  
## CMDG P3-M Finite-Stage Recovery + HoTT Scout

**Status:** Adopted programme direction  
**Date:** 2026-08-20  
**Audience:** GCL Codex team  
**Authority:** Human Steward decision in this thread  
**Protected predecessor:** `b08ea9fdd40136e6ffebf9834ea7531784bcc22f`  
**Predecessor PR:** MATH-PROGRAMME #601  
**Predecessor result:** CMDG CM4 P3-L — global weighted kernel-functional bridge

---

## 1. Decision

The programme will **not** govern P3-M as an equivalence-transport or HoTT bridge.

P3-M will instead be governed as the direct **finite-stage recovery attack** on the remaining coefficient-object solidity boundary.

HoTT remains a legitimate GCL research direction, but it is not presently justified as the principal destination of the CMDG lane. It will therefore proceed only as a **small, independent, falsifiable scouting programme**. It must demonstrate concrete reduction of mathematical or coherence complexity before receiving larger resources or becoming an architectural dependency.

This distinction is binding:

> **CMDG P3-M pursues the strongest unresolved mathematical consequence unlocked by P3-L. HoTT scouts whether a different foundation produces measurable advantage. Neither programme is to be bent merely to make the other appear necessary.**

---

# Part I — CMDG P3-M

## 2. Canonical successor

Recommended control identifier:

**`CMDG-CM4-P3-M-FINITE-STAGE-RECOVERY-001`**

Recommended short title:

**P3-M — finite-stage recovery from finite coordinate dependence**

Protected predecessor:

`b08ea9fdd40136e6ffebf9834ea7531784bcc22f`

That protected merge contains P3-L and is now the sole admissible mathematical predecessor for this lane. PR #601 is merged, and protected `main` points to that signed merge.

---

## 3. Governing mathematical question

P3-M has one question:

> Given a solid-side coefficient morphism  
> \[
> h:(\operatorname{profiniteSolid}R)(X)\to C,
> \]
> does the protected P3-L finite-coordinate dependence theorem force \(h\) to arise from one finite discrete quotient of \(X\)?

More concretely, prove or refute that for every such \(h\), there exist

\[
j:\operatorname{DiscreteQuotient}(X)
\]

and

\[
g_Q:\operatorname{LowerHom}(X_j)
\]

such that

\[
h=\operatorname{finiteStageExtension}(X,j,g_Q).
\]

This is already formalized in the protected source as:

`CoefficientFiniteStageMappingOut`.

P3-G proves that this proposition is equivalent to the remaining mapping-out injectivity theorem and, through the existing reduction, to solidity of the coefficient object.

Therefore P3-M is not speculative infrastructure. It attacks the exact terminal obstruction already isolated by the programme.

---

## 4. Why P3-L materially changes the attack

Before P3-L, the programme knew that the desired finite-stage property was equivalent to solidity, but lacked a sufficiently strong mechanism for forcing arbitrary solid-side morphisms into a finite quotient.

P3-L now constructs, from every solid-side coefficient morphism \(h\), an additive product functional

\[
L_h :
(\operatorname{IntegralBasisIndex}X\to\mathbb Z)
\to_+\mathbb Z
\]

and proves that it depends on only finitely many basis coordinates.

The protected theorem is:

`kernelProductFunctional_finite_coordinate_dependence`.

It supplies a finite set \(I\) such that

\[
a|_I=b|_I
\quad\Longrightarrow\quad
L_h(a)=L_h(b).
\]

The corresponding finite-coordinate kernel theorem is also protected.

The principal P3-M research hypothesis is therefore:

\[
\boxed{
\text{finite dependence of }L_h
\Longrightarrow
\text{finite stage for }h
}
\]

The work is to determine whether that implication can actually be proved.

---

# Part II — Required mathematical decomposition

## 5. Intended proof chain

Codex should treat the following as the preferred attack order, not as assumed truths:

\[
\text{P3-L finite coordinate set } I
\]

\[
\Downarrow
\]

\[
\text{finite amount of Nöbeling / basis information determines }L_h
\]

\[
\Downarrow
\]

\[
\text{construct or identify a finite quotient }j\text{ capturing that information}
\]

\[
\Downarrow
\]

\[
\text{construct candidate }g_Q
\]

\[
\Downarrow
\]

\[
\text{show }h\text{ and }\operatorname{finiteStageExtension}(X,j,g_Q)
\text{ agree at the one-point component}
\]

\[
\Downarrow
\]

\[
\texttt{coefficient_hom_ext_point}
\]

\[
\Downarrow
\]

\[
h=\operatorname{finiteStageExtension}(X,j,g_Q)
\]

\[
\Downarrow
\]

\[
\texttt{CoefficientFiniteStageMappingOut}
\]

\[
\Downarrow
\]

\[
\texttt{CoefficientMappingOutInjectivity}
\]

\[
\Downarrow
\]

\[
\operatorname{CondensedMod.IsSolid}(R,C).
\]

The existing `coefficient_hom_ext_point` theorem is especially important: equality of coefficient morphisms is reducible to equality at the one-point component.

That sharply localizes what P3-M actually has to reconstruct.

---

## 6. First research subproblem

Before writing substantial new infrastructure, Codex should attack this question directly:

> Given the finite set  
> \[
> I:\operatorname{Finset}(\operatorname{IntegralBasisIndex}X)
> \]
> produced by `kernelProductFunctional_finite_coordinate_dependence`, can one construct a single `DiscreteQuotient X` on which all basis information indexed by \(I\) simultaneously descends?

This is the first true mathematical discriminator.

If yes, the next task is to bind that finite quotient to the value of the one-point component of \(h\).

If no, Codex must determine **why not**. In particular, it must distinguish:

- inability to construct the quotient with currently exposed APIs;
- a missing compatibility theorem between basis indices and finite quotients;
- an actual mathematical failure of finite-coordinate dependence to imply finite-stage dependence;
- a need for stronger information than the scalar product functional retains.

Do not silently add structure until this distinction has been made.

---

## 7. Second research subproblem

Assuming a suitable finite quotient \(j\) can be produced, determine whether the corresponding lower-side morphism \(g_Q\) can be reconstructed.

The desired object type is already fixed by P3-G:

\[
g_Q :
\operatorname{LowerHom}(X.\mathrm{diagram.obj}\,j).
\]

Existing infrastructure already knows how to turn such a \(g_Q\) into

`finiteStageExtension X j gQ`

and proves that its precomposition with solidification gives the corresponding lower-side finite-stage morphism.

P3-M therefore should avoid rebuilding this machinery.

The new information must enter only in the reverse direction:

\[
h
\rightsquigarrow
I
\rightsquigarrow
j
\rightsquigarrow
g_Q.
\]

---

## 8. Third research subproblem

The final comparison should preferably use the already-protected point-extensionality theorem rather than attempting full natural-transformation equality directly.

Target:

\[
h_{\ast}
=
\bigl(\operatorname{finiteStageExtension}(X,j,g_Q)\bigr)_{\ast}
\]

at

\[
\operatorname{CompHaus.of} PUnit.
\]

Then invoke:

`coefficient_hom_ext_point`.

This avoids unnecessarily reopening the full condensed-object naturality problem.

---

# Part III — Authorized P3-M scope

## 9. Authorized work

P3-M may introduce only mathematics directly required to establish or falsify the finite-stage recovery implication.

Authorized categories include:

1. finite-support/basis-to-finite-quotient bridge lemmas;
2. simultaneous finite quotient domination for finitely many relevant basis data;
3. reconstruction of a lower-side finite-stage morphism;
4. one-point evaluation identities;
5. kernel-product-functional separation lemmas;
6. a theorem deriving `CoefficientFiniteStageMappingOut` from the protected P3-L result;
7. once that theorem exists, application of the already-protected equivalence to obtain mapping-out injectivity;
8. only after injectivity is established, the existing terminal equivalence may yield coefficient-object solidity.

The lane should reuse protected declarations wherever possible rather than reproving them.

---

## 10. Explicit exclusions

Until mathematically forced, P3-M does **not** authorize:

- general HoTT machinery;
- univalence;
- Cubical Agda;
- equivalence-as-equality principles;
- generic equivalence-transport infrastructure;
- new foundations;
- higher inductive types;
- arbitrary categorical abstraction unrelated to the blocker;
- rewriting P2/P3 predecessor APIs;
- broad refactors of CMDG formal files;
- weakening exact-head replay requirements;
- assuming `CoefficientFiniteStageMappingOut`;
- assuming `CoefficientMappingOutInjectivity`;
- assuming `CondensedMod.IsSolid` for the coefficient object;
- declaring P3 complete before the terminal theorem has actually replayed.

No theorem may be admitted simply because it is equivalent to the desired result.

---

# Part IV — Fail-closed research discipline

## 11. Codex operating rule

P3-M is a **research lane**, not a theorem-production quota.

Codex must be willing to terminate with a precise negative result.

A legitimate P3-M outcome is:

> P3-L finite-coordinate dependence does not, with the information currently retained by `kernelProductFunctional`, determine a finite-stage factorization of \(h\).

If that happens, the next control must characterize the missing invariant rather than patch around the failure.

Possible missing information could include higher-rank pairings, vector-valued evaluations, compatibility across multiple selectors, or additional naturality data. Those are hypotheses to investigate, not assumptions.

---

## 12. Escalation rule

New mathematical machinery may be introduced only when a concrete failed proof attempt establishes that it is needed.

The pattern should be:

\[
\text{exact target}
\rightarrow
\text{minimal attempted lemma}
\rightarrow
\text{exact obstruction}
\rightarrow
\text{minimal successor construction}.
\]

Not:

\[
\text{large speculative abstraction}
\rightarrow
\text{hope it becomes useful}.
\]

This principle should remain particularly strict after the substantial infrastructure already accumulated through P2-E and P3-C–P3-L.

---

# Part V — P3-M certification ladder

## 13. Expected formal sequence

The precise theorem names may change, but the logical ladder should resemble:

```text
finite coordinate kernel
    ↓
finite coordinate dependence
    ↓
finite basis data jointly descend to one quotient
    ↓
finite quotient captures product functional
    ↓
candidate lower morphism gQ
    ↓
one-point finite-stage equality
    ↓
coefficient_hom_ext_point
    ↓
CoefficientFiniteStageMappingOut
    ↓
CoefficientMappingOutInjectivity
    ↓
CoefficientResidualHomTheorem
    ↓
CondensedMod.IsSolid R coefficientObject
```

The first two are already protected P3-L results.

The existing P3-G source already proves the terminal equivalences among finite-stage mapping out, injectivity, the residual Hom theorem, and solidity.

Codex should not reopen those equivalences unless an exact compiler incompatibility requires a local repair.

---

## 14. Acceptance criteria

A successful P3-M lane requires all of the following:

- predecessor exactly descended from protected `b08ea9fdd40136e6ffebf9834ea7531784bcc22f`;
- no unauthorized predecessor mutation;
- exact pinned Lean/mathlib environment;
- existing protected P2-E through P3-L replay green;
- new P3-M theorem replay green;
- terminal protected characterization replay green;
- no proof placeholders;
- no `sorryAx`;
- explicit `#print axioms` readback on substantive new declarations;
- downstream protected replay where applicable;
- exact-head independent non-author review;
- protected merge;
- signed protected-main readback.

If P3-M does not reach solidity, the PR description must state exactly where the implication stops.

---

# Part VI — Resource policy for P3-M

## 15. Resource allocation

Within the formal-mathematics effort, P3-M receives the principal allocation.

Recommended working allocation:

| Activity | Share of formal-mathematics attention |
|---|---:|
| P3-M finite-stage recovery | 60–70% |
| HoTT scout | ~10% |
| Diagnostic/supporting formal work | remainder |

This is not a company-wide resource allocation. It applies to the relevant formal-mathematics capacity.

The reason is expected information gain: P3-M either closes a long-standing terminal obstruction or identifies precisely why the newly protected finite-dependence theorem is insufficient.

Both outcomes materially advance the programme.

---

# Part VII — HoTT policy

## 16. HoTT is retained, but demoted from presumed destination to testable hypothesis

The programme should maintain a separate control:

**`GCL-HOTT-SCOUT-001`**

Its purpose is not to “start the HoTT programme.”

Its purpose is to answer:

> Does a univalent or cubical formulation materially reduce coherence burden, representation dependence, or proof complexity for a mathematical construction that GCL already understands?

The scout must be independent of CMDG P3-M.

P3-M must not depend on it.

---

## 17. HoTT scout experimental design

Choose one bounded construction with all of the following properties:

- already understood formally in Lean;
- has at least two equivalent presentations;
- requires nontrivial transport or coherence bookkeeping;
- small enough to reproduce independently;
- has a clear quantitative or qualitative comparison criterion.

Then reproduce the relevant structure in a genuinely HoTT/cubical setting.

The most plausible environment for the experiment is Cubical Agda, because the scout is specifically intended to test computational path transport/univalence rather than merely imitate HoTT vocabulary inside ordinary Lean.

But the tool choice belongs to the scout control, not CMDG.

---

## 18. HoTT success criteria

The scout is successful only if it demonstrates a material advantage such as:

- substantially fewer coherence lemmas;
- elimination of repeated transport bureaucracy;
- substantially cleaner equivalence-invariant APIs;
- useful computational behavior of transport;
- a construction that is difficult or unnatural in the existing foundation but natural under univalence;
- a convincing route to synthetic higher-categorical mathematics relevant to GCL.

Merely proving the same theorem twice does not count.

---

## 19. HoTT failure criteria

The scout should be stopped or deprioritized if:

- proof complexity merely moves into cubical infrastructure;
- interoperability dominates the work;
- the mathematical objects remain entirely set-level;
- explicit Lean equivalences are already adequate;
- higher paths do not participate materially;
- no measurable coherence burden is removed;
- tooling/friction outweighs foundational benefit.

A failed scout is a useful result.

It tells us not to divert the main formal programme.

---

# Part VIII — Conditions for HoTT promotion

## 20. HoTT must earn architectural status

No `GCL-HOTT` production programme should be created merely because the scout succeeds technically.

Promotion requires evidence that the same higher-structural advantage recurs across more than one relevant construction.

A reasonable promotion threshold would require at least:

1. one successful bounded scout;
2. a second independent construction showing the same advantage;
3. a clear interoperability boundary with the main GCL formal stack;
4. identified mathematics where higher coherence is a genuine bottleneck;
5. an explicit cost model for maintaining two foundational ecosystems;
6. governance rules for transporting claims between them.

Only then should GCL consider HoTT a first-class architectural component.

---

# Part IX — Relationship to the previously proposed equivalence-transport fixture

## 21. `GCL-EQUIV-TRANSPORT-001` remains useful, but is not P3-M

The proposed fixture remains conceptually valid:

> Given two independently produced artifacts, a declared observational boundary, and an equivalence certificate, determine exactly which certified claims transport.

That problem remains relevant to GCL governance.

But it should not consume the CMDG successor slot.

Its future role is better understood as a governance/semantic fixture that may eventually interact with HoTT if the HoTT scout demonstrates real benefit.

It remains separate from the finite-stage recovery theorem.

---

# Part X — Strategic rationale

## 22. Why this allocation is preferable

P3-M sits at a rare research position:

- substantial prerequisite mathematics has already been certified;
- the remaining obstruction is explicitly named;
- its equivalence to the desired solidity theorem is already formalized;
- P3-L has introduced a genuinely new theorem that may attack that obstruction;
- failure would itself identify the missing mathematical information.

That is high-value research territory.

By comparison, building an ordinary equivalence-transport layer now would have a much higher probability of success but much lower information gain.

The programme should prefer the question whose answer is unknown.

---

# Part XI — Instructions to Codex

## 23. Immediate execution directive

The Codex team should proceed under the following directive:

> Treat protected merge `b08ea9fdd40136e6ffebf9834ea7531784bcc22f` as the fixed predecessor.
>
> Open no HoTT-dependent CMDG successor.
>
> Define P3-M solely as a finite-stage recovery attack.
>
> Begin by determining whether the finite coordinate set produced by `kernelProductFunctional_finite_coordinate_dependence` can be realized through one finite discrete quotient of the profinite source in a way strong enough to recover the one-point component of the original solid-side coefficient morphism.
>
> Reuse `coefficient_hom_ext_point` as the preferred terminal extensionality mechanism.
>
> Introduce no new general abstraction until a concrete failure requires it.
>
> Fail closed if the P3-L functional has discarded information necessary to reconstruct the morphism.
>
> Do not assert mapping-out injectivity or solidity until they follow from an exact-certified finite-stage theorem.
>
> Separately establish `GCL-HOTT-SCOUT-001` as a non-production research experiment. It carries no authority over CMDG and receives no architectural status unless it demonstrates a material reduction in real coherence/proof burden.

---

# Part XII — Decision record

## 24. Durable programme statement

The following should be treated as the canonical memorialization:

> **GCL Decision — CMDG P3-M / HoTT Resource Direction**
>
> Following protection of CMDG CM4 P3-L, GCL will exploit the newly certified finite-coordinate-dependence theorem against the exact unresolved coefficient finite-stage mapping-out boundary.
>
> P3-M is therefore governed as **finite-stage recovery**, not as equivalence transport.
>
> Its objective is to determine whether finite dependence of the kernel product functional forces every solid-side coefficient morphism to descend from one finite profinite quotient. A successful proof closes the already-formalized chain from finite-stage mapping out to mapping-out injectivity and coefficient-object solidity.
>
> GCL will not presume HoTT to be the destination of this lane. HoTT remains a separate, small, falsifiable scouting programme. Its purpose is to measure whether univalence, path-based transport, or higher structure materially reduce coherence or proof complexity on bounded constructions relevant to GCL.
>
> HoTT will receive broader architectural status only if repeated experiments establish an advantage sufficient to justify the foundational and interoperability costs.
>
> The governing principle is:
>
> **Exploit the strongest live mathematical frontier first. Require alternative foundations to demonstrate that they solve an actual problem better before reorganizing the programme around them.**

That should be the Codex team's operative planning record going forward.