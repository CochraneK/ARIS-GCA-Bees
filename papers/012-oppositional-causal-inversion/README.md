# ARIS4C012 · When Opposites Become Causes

**Status:** research design / prior-art audit in progress  
**ARIS provenance:** v0.4.26 · `951654847b015585385b2448c5667dcd04e7b56b`

## Working title

**When Opposites Become Causes: An Indexed Cross-Domain Framework for Oppositional Causal Inversion**

## Motivating puzzle

George Orwell's *Nineteen Eighty-Four* compresses three apparent contradictions into slogans:

- war is peace;
- freedom is slavery;
- ignorance is strength.

ARIS4C012 does **not** ask whether these slogans are literally true, endorse them, or treat them as universal political laws. A literal identity such as `X = not-X` at the same actor, level, time, and construct definition is ordinarily a contradiction.

The scientific question is narrower and testable:

> Under what identifiable boundary conditions can increasing a construct X causally increase a prespecified functional opposite O(X) after the actor, level, time horizon, construct, feedback state, or capacity regime changes?

The Orwell triad is therefore a **stress test for a general causal framework**, not the result to be proved.

## Core correction: restore the missing indices

A slogan may look logically impossible because it suppresses indices.

Instead of:

`War = Peace`

test relations such as:

`War/external-threat_(between groups,t0) -> cohesion/cooperation_(within group,t1)`

Instead of:

`Freedom = Slavery`

test:

`formal choice/flexibility_(t0) -> burden/norm escalation -> effective autonomy_(t1) decreases`

Instead of:

`Ignorance = Strength`

separate at least two distinct mechanisms:

1. `information restriction_B -> coordination capacity_B decreases -> relative power_A increases`;
2. `selective information use_A -> variance/overfitting decreases -> decision robustness_A increases` under specific environments.

These are empirical causal claims, not semantic identities.

## Proposed construct

### Oppositional Causal Inversion (OCI)

Let `X_i` be a construct indexed by actor, level, time, operational definition, and environment. Let `O(X)_j` be a **prespecified functional opposite** under a different index `j`.

An OCI candidate exists when:

1. `X` and `O(X)` are defined before outcome inspection;
2. increasing `X_i` is estimated to causally increase `O(X)_j`, directly or through a documented mediator/feedback path;
3. the index switch `i -> j` is explicit;
4. the result survives a same-index contradiction check and plausible confounding/selection alternatives;
5. boundary conditions are reported.

This definition deliberately excludes mere wordplay, correlation, post-hoc relabelling, and cases where the claimed "opposite" is invented after observing the result.

## Six candidate inversion families

1. **Actor-switch inversion** — X for actor A produces O(X) for actor B.
2. **Level-switch inversion** — X between groups produces O(X) within groups, or vice versa.
3. **Temporal inversion** — X improves its target in the short run but generates O(X) over a longer horizon.
4. **Construct-switch inversion** — formal or nominal X increases while effective/substantive X decreases.
5. **Feedback/equilibrium inversion** — individually rational increases in X alter the environment and feed back into O(X).
6. **Capacity/nonlinearity inversion** — additional X is beneficial below a threshold but harmful above it because of overload, noise, variance, congestion, or complexity.

A case may receive multiple labels.

## Why the three Orwellian cases are scientifically unequal

### War -> peace

The strongest nearby evidence does **not** justify "war creates peace" as a general claim.

Relevant mechanisms include:
- deterrence can prevent crises or attacks under particular credibility, capability, and interest conditions;
- intergroup competition can increase intragroup cooperation;
- external conflict can sometimes generate rally effects;
- diversionary-war evidence is conditional and historically mixed.

The project therefore separates **war**, **threat**, **competition**, **deterrence**, **internal cohesion**, **regime support**, and **absence of violence**. They are not interchangeable.

### Freedom -> dependence / reduced effective autonomy

This is a promising construct-switch and feedback family.

Relevant mechanisms include:
- choice overload under high complexity, difficulty, and preference uncertainty;
- the autonomy paradox in mobile work, where short-run flexibility contributed to norms of continual availability;
- algorithmic or institutional delegation that can increase nominal options while increasing dependence.

Crucial falsifier: a large self-determination-theory literature finds autonomy and autonomous motivation are generally associated with beneficial outcomes. Therefore OCI predicts **conditional reversal**, not a global negative effect of freedom.

### Ignorance -> strength

At least three different hypotheses must remain separate:
- **adaptive filtering:** less information can improve prediction under bias-variance/ecological conditions;
- **rational inattention:** finite processing capacity makes selective attention potentially optimal;
- **power asymmetry:** restricting another actor's information/coordination can increase one's relative control.

Deliberate ignorance and information avoidance are not automatically beneficial. The framework must distinguish strategic filtering from harmful avoidance, deception, censorship, or denial.

## Closest neighboring theories

OCI must establish incremental value relative to:

- paradox theory;
- unintended/perverse consequences;
- boomerang and iatrogenic effects;
- counterfinality;
- security dilemma;
- choice overload;
- ecological rationality / less-is-more effects;
- rational inattention;
- deliberate ignorance;
- externality and equilibrium feedback models.

The broad idea that interventions can backfire is **not novel**. After explicit audit against Merton, Boudon, complex-systems intervention work, rebound typologies, paradox theory, and related literatures, the remaining provisional novelty is narrower: a **prespecified functional-opposition test + indexed causal representation + independent construct-validation protocol** for distinguishing opposite-producing effects from generic unintended consequences.

## Primary empirical program

ARIS4C012 should begin as a **theory + systematic evidence map**, not a pooled meta-analysis of incommensurable outcomes.

The first empirical deliverables are:

1. a preregistered ontology of inversion mechanisms;
2. a broad literature search using neutral terms such as paradox, backfire, boomerang, unintended consequence, self-defeating, less-is-more, overload, security dilemma, counterfinality, and iatrogenic;
3. double-coded candidate papers across multiple disciplines;
4. a corpus-level estimate of which inversion mechanisms and index switches actually recur;
5. domain-specific quantitative syntheses only where interventions and outcomes are sufficiently comparable.

## Hard falsification rules

The unified theory weakens if:

- most apparent cases disappear once actor/level/time/construct indices are made explicit;
- "opposites" cannot be prespecified reliably by independent coders;
- candidate effects are mostly correlational or depend on post-hoc semantic reframing;
- effects fail replication or vanish under stronger identification;
- no mechanism taxonomy generalizes across domains;
- the Orwell triad requires three unrelated explanations with no reusable structure;
- positive main effects dominate and reversals occur only as rare anomalies without predictable moderators.

A null result is informative: it would show that rhetorical paradoxes are better treated as domain-specific phenomena than as a general causal class.

## Current state

**DESIGN INITIALISED / NOVELTY PROVISIONAL.**

A live seed search confirms strong adjacent literatures and several credible conditional mechanisms, but no claim of a new general theory is locked yet. The next gate is a systematic closest-prior-work audit plus a reproducible evidence-map search.

## Novelty narrowed after umbrella-theory audit

The project explicitly rejects any claim to have discovered a general science of unintended consequences. See `process/NOVELTY_AUDIT.md`. OCI survives only if its narrower indexed representation is independently reliable and adds value beyond existing paradox/backfire/unintended-consequence frameworks.
