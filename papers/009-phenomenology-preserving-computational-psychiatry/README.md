# ARIS4C009 · The Fidelity Frontier in Computational Psychiatry

**Status:** research design / pre-ARIS deepening

## Canonical question

> How much can psychopathological experience be compressed into quantitative representations before clinically and phenomenologically important structure is irreversibly lost, and what modeling architecture best preserves that structure while remaining mechanistically informative and predictively useful?

The project joins computational psychiatry with phenomenological psychopathology, but it does **not** assume that one should be reduced to the other.

The core proposal is to treat every psychiatric representation — narrative, interview code, scale score, latent dimension, computational parameter, biomarker, diagnosis — as a **lossy representation** of a richer evidential record. The scientific target is therefore not merely prediction accuracy. It is the trade-off between what a representation costs and what it destroys.

## Epistemic boundary

The project does not claim direct access to a patient's complete subjective reality or to a single hidden psychiatric "ground truth."

Instead, it distinguishes:

1. the unobserved lived state;
2. the richest obtainable first-person and contextual record;
3. structured phenomenological representations;
4. symptom and dimensional representations;
5. computational and biological models;
6. categorical labels.

The raw record is evidence, not reality itself. The model is a view over evidence, not a replacement for the person.

## Core architecture

For person *i* at time *t*, let the archived evidence be:

```
X_it = {
  interview narrative,
  episode context,
  participant clarification,
  EMA,
  behavior,
  clinician observation,
  optional passive sensing,
  optional EEG/fMRI/physiology
}
```

Representations of increasing compression are:

```
Z0 = provenance-preserved source archive
Z1 = structured phenomenological episode graph
Z2 = EASE / EAWE / STEP-like phenomenological dimensions
Z3 = symptom / HiTOP-like dimensions
Z4 = computational latent parameters
Z5 = diagnosis or coarse clinical class
```

No downstream representation deletes the upstream layer.

## The key distinction

**Phenomenological fidelity is not the same thing as validity.**

A representation may predict relapse while badly misrepresenting what a particular experience meant. Conversely, a highly faithful narrative representation may have little predictive utility.

ARIS4C009 therefore keeps at least four evaluation families separate:

- **phenomenological fidelity** — how well a representation preserves the meaning, context, temporal structure, relations and participant-endorsed character of an episode;
- **construct / cross-modal validity** — whether it coheres with independent behavior, neurophysiology or theoretically relevant measures;
- **predictive / intervention utility** — whether it forecasts future states or responses to perturbation;
- **burden / compression** — data volume, interview time, annotation cost, dimensionality and participant burden.

The target is a **Pareto frontier**, not a single magic score.

## Main hypotheses

### H1 · Compression has a measurable fidelity cost

Moving from rich contextual records toward self-report scales, symptom totals and diagnoses will produce monotonic average information loss, but the loss will be highly non-uniform across phenomenological domains.

### H2 · Context-sensitive phenomena are disproportionately fragile

Experiences involving mineness, agency, self-world boundary, atmosphere, temporality and subtle forms of self-disturbance will suffer larger distortion when converted into decontextualized self-report items than more behaviorally concrete phenomena.

### H3 · Structured phenomenology occupies a useful middle layer

Phenomenological interviews and structured episode graphs will preserve substantially more source-level meaning than conventional symptom scales while remaining formal enough for statistical and computational modeling.

### H4 · Predictive accuracy and fidelity can dissociate

Representations with similar held-out prediction may have substantially different source-level fidelity. Therefore predictive performance alone cannot identify the scientifically preferable representation.

### H5 · Person-specific dynamics matter

Idiographic state-space models will recover clinically important temporal and contextual structure that is hidden by cross-sectional group averages, while hierarchical priors can still pool information across people.

### H6 · No single computational ontology should be privileged a priori

Active inference, predictive processing, reinforcement learning, dynamical systems, network models and other formalisms should compete at the mechanism layer. A theory is supported when it explains data across levels without requiring phenomenology to be rewritten in its vocabulary.

## First empirical target

The cleanest first paper is **not** an fMRI mega-study.

It is a representation benchmark in which the *same underlying interviews/episodes* are encoded at multiple levels and evaluated for information loss.

A strong initial design would compare:

- full phenomenological interview record;
- structured phenomenological graph;
- trained-rater EASE/EAWE/STEP coding;
- self-report approximation;
- conventional symptom coding;
- low-dimensional latent representation;
- optional LLM-generated structured representation under blinded evaluation.

This directly tests the fidelity frontier before adding expensive neural data.

## Why psychosis is the best first domain

The schizophrenia/psychosis literature currently offers unusually mature tools for linking detailed experience to quantification:

- EASE for anomalous self-experience;
- EAWE for world experience;
- STEP for time and space;
- PANSS and related conventional symptom scales;
- a developing neurophenomenology of self-disturbance;
- computational work on belief updating, salience, uncertainty and active inference.

Psychosis is therefore a benchmark domain, not the assumed final ontology of psychopathology.

## Long-term program

The research program can expand in stages:

1. **Fidelity benchmark** — quantify loss across representations.
2. **Cross-level validation** — connect retained phenomenological structure to behavior and neurophysiology.
3. **Longitudinal dynamics** — combine periodic deep interviews with EMA and passive sensing.
4. **Idiographic generative models** — fit person-specific latent-state dynamics with hierarchical pooling.
5. **Intervention perturbation tests** — ask whether models predict how experience changes after treatment or environmental perturbation.
6. **Transdiagnostic generalization** — test depression, bipolar disorder, anxiety, OCD, trauma and other domains without assuming psychosis-derived phenomenology transfers unchanged.

## Interpretation boundary

A computational parameter is not a person.
A diagnosis is not a latent state.
A brain correlate is not automatically an explanation.
A self-report item is not automatically a faithful version of a phenomenological interview.
A highly predictive model is not necessarily the least distorted model.

The scientific goal is to make these losses visible and testable.
