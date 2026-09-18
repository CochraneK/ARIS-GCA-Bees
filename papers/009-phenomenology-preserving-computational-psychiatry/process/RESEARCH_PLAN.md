# ARIS4C009 · Research plan

## Working title

**The Fidelity Frontier in Computational Psychiatry: Quantifying Psychopathology Without Collapsing Lived Experience**

## 1. Problem

Psychiatry repeatedly compresses rich lived phenomena into lower-dimensional representations:

[
experience ightarrow interview code ightarrow symptom score ightarrow latent dimension ightarrow computational parameter ightarrow diagnosis
]

Each transformation may be useful. None is lossless.

Current computational psychiatry is strong at formalization but still faces problems of task reliability, construct validity and ecological translation. Phenomenological psychopathology is strong at the structure of first-person experience but is difficult to scale and formalize. The central opportunity is to stop asking which tradition should replace the other and instead measure the information lost and gained at each translation.

## 2. Primary contribution

ARIS4C009 proposes a **phenomenology-preserving computational psychiatry** with four separable objectives:

1. preserve first-person structure;
2. establish construct and cross-modal validity;
3. achieve longitudinal prediction and intervention usefulness;
4. control acquisition and representation burden.

The key empirical object is the **fidelity frontier**: the non-dominated set of psychiatric representations under these competing objectives.

## 3. Research questions

### RQ1 — Representation loss

How much source-level meaning and structure is lost by different psychiatric representations?

### RQ2 — Domain fragility

Which experiential domains are most vulnerable to compression?

Candidate domains include:

- minimal self / mineness;
- agency;
- self-other boundary;
- body;
- time;
- space;
- atmosphere / salience / familiarity;
- language;
- meaning;
- affect;
- social relation;
- existential orientation.

### RQ3 — Fidelity versus prediction

Do models with similar predictive accuracy differ in phenomenological fidelity?

### RQ4 — Fidelity versus burden

What representation yields the best preservation under realistic interview, annotation and participant-burden constraints?

### RQ5 — Idiographic structure

How much clinically relevant information is lost when person-specific dynamics are replaced by group-level parameters?

### RQ6 — Cross-level mapping

Which phenomenological dimensions show reproducible relationships with behavior, computational parameters, EEG/fMRI or physiology without treating those third-person measurements as definitions of the experience?

## 4. Recommended paper sequence

### Paper 009A — The fidelity benchmark

This should be the first executable paper.

**Design:** same source episodes, multiple representations, blinded reconstruction.

Representations:

- full source record;
- structured phenomenological episode graph;
- specialist phenomenological coding;
- questionnaire/self-report abstraction;
- conventional symptom scale abstraction;
- low-dimensional latent vector;
- optional LLM-assisted structured abstraction.

Primary outcomes:

- semantic fidelity;
- relational fidelity;
- context fidelity;
- temporal fidelity;
- participant-confirmed fidelity;
- acquisition and annotation burden.

This paper can establish the core methodological contribution without claiming a neural mechanism.

### Paper 009B — Cross-level neurophenomenology

Add:

- self-referential task behavior;
- source monitoring;
- salience / uncertainty tasks;
- EEG/ERP;
- optional fMRI.

Test whether phenomenological dimensions predict independent neural or behavioral variation beyond conventional symptom totals.

### Paper 009C — Longitudinal person-specific dynamics

Collect:

- periodic deep interviews;
- EMA;
- sleep / activity / mobility where consented;
- life events and context;
- treatment/intervention timing.

Compare linear and nonlinear state-space models with person-specific and hierarchical variants.

### Paper 009D — Perturbation / intervention validation

Use treatment or micro-randomized ecological interventions to test whether inferred dynamic states predict response to perturbation.

## 5. Phase 1 sample and data design

### Population

Start with schizophrenia-spectrum / early psychosis because phenomenological tools and prior neurophenomenology are comparatively mature.

Include a clinically relevant comparison group where feasible.

Do not assume the framework is schizophrenia-specific.

### Minimum source record

For each focal episode:

- verbatim or high-quality transcript;
- interviewer prompts;
- temporal context;
- participant clarification;
- ambiguity markers;
- medication / sleep / substance / acute-context notes when relevant and ethically appropriate;
- rater confidence;
- provenance pointer.

### Instruments

Candidate set:

- EASE;
- EAWE;
- STEP;
- PANSS or a contemporary conventional symptom measure;
- selected dimensional / transdiagnostic measures.

Instrument selection should be preregistered and minimized to avoid burden inflation.

## 6. Gold standard problem

There is no perfect gold standard for lived experience.

Therefore use **multi-anchor adjudication** rather than one privileged label:

- raw source evidence;
- trained phenomenological raters;
- independent adjudication;
- participant clarification;
- repeated assessment where appropriate.

Disagreement is data.

Store:

- rater A interpretation;
- rater B interpretation;
- adjudicated interpretation;
- uncertainty;
- unresolved alternatives.

## 7. Benchmark experiment

For each episode, generate representations (Z_1 ... Z_K).

Blinded evaluators receive only one representation and answer a preregistered query bank about the original episode.

Compare each representation to answers generated from the richest source record under adjudication.

Key outcome:

[
D_k = d(X, Z_k)
]

where (d) is multidimensional and source-grounded.

### Important anti-leakage rule

No evaluator who generated a compressed representation can evaluate its fidelity.

If LLMs are used:

- freeze model/version;
- use identical prompt templates;
- separate extraction from evaluation;
- keep human-only evaluation as the primary endpoint;
- report stochastic variability across repeated model runs.

## 8. Sample size logic

Do not power the study on the number of patients alone.

The unit structure is hierarchical:

- participants;
- episodes;
- questions/relations;
- raters.

Use simulation-based power for mixed-effects comparisons of representation type.

Primary target should be the smallest representation effect considered scientifically meaningful, not a generic (p<.05).

## 9. Statistical model

Example semantic-fidelity model:

[
accuracy_{iqrk} sim representation_k + domain_q + representation_k 	imes domain_q + (1|person_i)+(1|episode_{ir})+(1|rater)
]

For probabilistic judgments use hierarchical logistic or ordinal models.

For relation retention use edge-level hierarchical models.

For participant ratings use ordinal mixed models.

Report posterior distributions or confidence intervals for pairwise representation contrasts and domain-specific loss.

## 10. Pareto analysis

For each representation calculate:

- fidelity vector;
- reliability;
- validity vector;
- predictive utility where available;
- burden vector.

Construct Pareto fronts under:

1. research use;
2. screening use;
3. mechanistic study;
4. longitudinal monitoring.

Different use cases may rationally choose different points on the frontier.

The paper should **not** report a universal winner.

## 11. Longitudinal extension

### Observations

Deep interview: monthly / milestone-based.

EMA: several brief samples per day in intensive bursts or sustained lower-frequency sampling.

Passive sensing: only variables with clear hypotheses and explicit consent.

### Models

Baselines:

- persistence;
- person mean;
- linear autoregression;
- VAR;
- Kalman filter.

Advanced:

- switching state-space;
- PLRNN;
- Gaussian-process SSM;
- hierarchical Bayesian nonlinear dynamics;
- Transformer as a prediction comparator.

### Evaluation

Forward-only validation.

Never randomly shuffle time points across train and test.

Compare:

- forecast error;
- calibration;
- transition detection;
- intervention-response prediction;
- interpretability;
- fidelity to deep-interview anchors.

## 12. Mechanistic model competition

Active inference is a candidate, not the ontology.

For any proposed mechanism:

1. specify the phenomenological phenomenon without computational jargon;
2. specify competing models;
3. derive discriminating predictions;
4. test parameter recovery;
5. test falsifiable behavioral / neural predictions;
6. check whether the mechanism adds information beyond phenomenological dimensions and conventional symptoms.

Candidate families:

- active inference / predictive processing;
- reinforcement learning;
- drift diffusion / sequential sampling;
- dynamical systems;
- symptom / experience networks;
- control theory;
- information-theoretic models.

## 13. Cross-cultural and language requirement

Phenomenological coding may not be measurement invariant across language and culture.

The framework must retain:

- original language;
- translated text;
- translation uncertainty;
- culture-specific interpretation notes.

A later multi-site study should explicitly test whether the fidelity frontier shifts across languages.

Machine translation must not silently become the source record.

## 14. Ethics

The framework creates unusually rich psychiatric records.

Requirements:

- data minimization despite methodological richness;
- tiered access;
- de-identification;
- explicit consent for passive sensing;
- clear separation of research inference from clinical diagnosis;
- no covert monitoring;
- no use of computational scores as autonomous treatment decisions;
- careful handling of participant access to derived models.

The source-preservation principle does **not** mean indiscriminate retention of identifiable raw data.

## 15. Literature anchors

The current literature already supplies important bridge components:

- computational phenomenology via generative modeling;
- phenomenological psychopathology as a translational resource;
- EASE / EAWE / STEP measurement traditions;
- neurophenomenological self-disorder studies;
- spatiotemporal psychopathology;
- computational psychiatry reliability critiques;
- digital phenotyping and EMA;
- nonlinear state-space forecasting of mental-health trajectories;
- idiographic dynamic psychopathology.

What is missing is a common benchmark where the amount of information destroyed by each representational translation is itself an explicit outcome.

## 16. Strong falsification

A serious framework needs failure conditions.

Abandon or substantially revise the central thesis if:

- simple self-report preserves specialist phenomenological information with negligible loss;
- richer representation yields no reproducible fidelity advantage;
- fidelity metrics cannot be rated reliably;
- participant-confirmed fidelity is unrelated to supposedly source-faithful representations;
- additional phenomenological information contributes neither explanatory nor predictive value across repeated datasets;
- the apparent advantage is only a function of representation length;
- results collapse under cross-site replication.

## 17. Immediate ARIS deliverables

- literature matrix with direct DOI/PMID anchors;
- formal fidelity metric specification;
- novelty audit;
- simulation / engineering benchmark of the Pareto machinery;
- preregistration-ready 009A protocol;
- data dictionary for episode-level phenomenology;
- analysis skeleton for hierarchical fidelity models.

## 18. Current recommended scope

Keep the first empirical paper narrow:

> **How much phenomenological information is lost when the same psychopathological experiences are encoded as expert phenomenology, self-report, conventional symptoms and low-dimensional quantitative representations?**

Do not begin with a claim to build a complete digital twin of psychiatric reality.

Establish the measurement theorem first.
