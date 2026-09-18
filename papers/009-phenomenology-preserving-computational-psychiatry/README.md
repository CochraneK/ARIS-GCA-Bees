# ARIS4C009 · The Fidelity Frontier in Computational Psychiatry

**Status:** research design / pre-ARIS deepening

## Canonical question

> How much clinically and phenomenologically important structure is lost at each stage from lived experience → elicitation → representation → computation, and which representations are most efficient for a specified scientific or clinical purpose?

The project joins computational psychiatry with phenomenological psychopathology, but it does **not** assume that one should be reduced to the other.

The core proposal is now explicitly two-stage:

1. **acquisition / elicitation:** different methods bring different parts of experience into an evidential record;
2. **encoding / compression:** the same record can then be represented at different levels of abstraction.

These two losses must not be conflated.

## Epistemic boundary

The project does not claim direct access to a patient's complete subjective reality or to a single hidden psychiatric "ground truth."

Let:

- (H) = lived state, not directly observable;
- (A_m) = acquisition method (m), such as a phenomenological interview, self-report questionnaire, conventional symptom interview or EMA;
- (X^{(m)} = A_m(H)) = the evidence produced by that method;
- (E_k) = representation/encoding method (k);
- (Z^{(m,k)} = E_k(X^{(m)})) = encoded representation.

The raw interview record is evidence, not reality itself. A model is a view over evidence, not a replacement for the person.

## Two benchmark layers

### 009A1 · Same-source encoding benchmark

Hold the source record fixed and compare how much information survives different encodings.

Examples:

- full de-identified source record;
- structured phenomenological episode graph;
- trained-rater phenomenological codes;
- questionnaire-format projection generated from the same source;
- conventional symptom-code projection generated from the same source;
- low-dimensional latent representation;
- optional frozen LLM representation.

This isolates **encoding loss**.

A source-derived questionnaire-format projection must not be called a real participant self-report.

### 009A2 · Acquisition benchmark

The same participants are assessed with genuinely different acquisition methods, for example:

- phenomenological interview;
- participant-completed self-report;
- conventional symptom interview/scale;
- EMA where relevant.

This estimates **acquisition/process differences**, but must account for order, state change, learning/carryover and interviewer effects.

009A2 is methodologically distinct from 009A1.

## The key distinction

**Phenomenological fidelity is not the same thing as reliability, validity or utility.**

A representation may predict relapse while failing to preserve what a particular experience meant. Conversely, a detailed representation may preserve meaning but add little to a specific screening task.

ARIS4C009 therefore keeps separate:

- **source-grounded fidelity** — semantic, relational, contextual, temporal and participant-endorsed preservation;
- **reliability** — reproducibility of ratings/parameters;
- **construct / cross-modal validity** — convergence and discrimination against independent evidence;
- **purpose-conditioned utility** — usefulness for a specified task;
- **burden / compression** — participant time, expert time, dimensionality and computation.

## Intended-use rule

No representation is globally "good" or "bad."

Validity and utility are evaluated conditional on an intended use (u):

[
V_{use}(Z,u)
]

Possible uses include:

- rich description;
- screening;
- diagnosis/classification;
- mechanistic modeling;
- prediction;
- longitudinal monitoring;
- intervention selection.

A diagnosis is therefore **not** judged as though its purpose were to reproduce a full narrative. Diagnosis can be included as a deliberately coarse comparison or as a use-specific representation, but low narrative fidelity is not itself proof of diagnostic invalidity.

## Fidelity frontier

For a specified use (u), compare:

[
M(Z,u)={F(Z),R(Z),V(Z,u),U(Z,u),C(Z)}
]

where (F) is fidelity, (R) reliability, (V) validity, (U) utility and (C) burden.

The target is a **use-conditioned Pareto frontier**, not a single universal ranking.

## Main hypotheses

### H1 · Same-source encoding has measurable loss

When the same source episode is encoded at lower representational bandwidth, average source-reconstruction fidelity will decline, but not uniformly across domains.

### H2 · Context-sensitive phenomena are disproportionately fragile

Agency, mineness, self-world boundary, atmosphere/salience and temporality will show larger source-reconstruction losses than more concrete factual content under aggressive encoding.

### H3 · Structured phenomenology may occupy an efficient middle region

A structured graph or trained phenomenological code may preserve more source-level structure than coarse symptom projections at lower burden than the full record.

### H4 · Acquisition and encoding losses are dissociable

Differences between an actual self-report and an interactive phenomenological interview will not be assumed to be compression effects; they may arise from elicitation, interpretation or interaction.

### H5 · Predictive accuracy and source fidelity can dissociate

Representations with similar held-out prediction may have substantially different source-grounded fidelity.

### H6 · No single computational ontology is privileged a priori

Active inference, predictive processing, reinforcement learning, dynamical systems, network models and other formalisms compete at the mechanism layer.

## Why psychosis is the first benchmark domain

The schizophrenia/psychosis literature offers unusually mature tools for linking detailed experience to quantification:

- EASE for anomalous self-experience;
- EAWE for world experience;
- STEP for time and space;
- conventional symptom measures;
- emerging neurophenomenology and computational work.

Psychosis is a benchmark domain, not the assumed final ontology of psychopathology.

## Long-term program

1. **009A1 — encoding fidelity benchmark**
2. **009A2 — acquisition-process benchmark**
3. **cross-level validation**
4. **longitudinal person-specific dynamics**
5. **intervention perturbation tests**
6. **transdiagnostic and cross-cultural generalization**

## Interpretation boundary

A computational parameter is not a person.  
A diagnosis is not a latent state.  
A brain correlate is not automatically an explanation.  
A self-report item is not automatically a faithful version of a phenomenological interview.  
A long interview is not automatically better for every purpose.  
A highly predictive model is not necessarily the least distorted model.

The scientific goal is to make these trade-offs visible and testable.
