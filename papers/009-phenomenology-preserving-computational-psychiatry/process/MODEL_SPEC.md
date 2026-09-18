# ARIS4C009 · Model specification

## 1. Objects being modeled

Let (H_{it}) denote the lived mental state of person (i) at time (t). (H) is not directly observable and is not treated as a measurable ground truth.

Let (X_{it}) denote the richest ethically and practically obtainable evidential record:

[
X_{it} = (N_{it}, C_{it}, P_{it}, E_{it}, B_{it}, O_{it}, S_{it}, G_{it})
]

where:

- (N): narrative / interview material;
- (C): contextual information;
- (P): participant clarification or confirmation;
- (E): ecological momentary assessment;
- (B): behavior / task data;
- (O): clinician or observer information;
- (S): passive sensor streams;
- (G): physiology / EEG / imaging, when available.

The central rule is:

[
H 
eq X
]

and no analysis claims otherwise.

## 2. Representation ladder

Define a family of transformations:

[
Z^{(k)} = f_k(X)
]

where (k) indexes representational schemes rather than an assumed ontological hierarchy.

Candidate schemes:

- **R0 — source archive:** transcript/audio-derived record + context + provenance;
- **R1 — episode graph:** entities, experiential dimensions, relations, temporal order, uncertainty, contextual qualifiers and direct source pointers;
- **R2 — phenomenological instrument representation:** EASE, EAWE, STEP and related trained-rater codes;
- **R3 — conventional clinical / dimensional representation:** PANSS, symptom factors, HiTOP-like dimensions;
- **R4 — computational representation:** model parameters and latent dynamical states;
- **R5 — categorical representation:** DSM/ICD-style diagnosis or other coarse class.

The ladder is not assumed to be strictly ordered in usefulness.

## 3. Phenomenological fidelity vector

No single scalar can certify fidelity. Report a vector:

[
F(Z) = (F_{sem}, F_{rel}, F_{ctx}, F_{temp}, F_{pers})
]

### 3.1 Semantic fidelity (F_{sem})

Construct a preregistered query bank (Q) over each source episode.

Examples:

- Did the participant experience a loss of agency?
- Was the experience endorsed as literal, metaphorical or uncertain?
- Did it occur before or after a specific event?
- Was the experience frightening, neutral or compelling?
- Was it attributed to medication, sleep deprivation, another person or no identified cause?

Independent raters answer (Q) using either the source archive or a compressed representation.

For categorical questions:

[
F_{sem}=1-rac{1}{|Q|}sum_q mathbb{1}[a_q^{source}
eq a_q^{repr}]
]

For probabilistic answers, use proper scoring rules such as Brier or log loss and normalize to ([0,1]).

### 3.2 Relational fidelity (F_{rel})

Represent an episode as a labeled graph (G_X=(V,E)) containing phenomenological entities and relations:

- self ↔ thought;
- self ↔ body;
- self ↔ other;
- event ↔ meaning;
- temporal precedence;
- causal attribution;
- certainty;
- context;
- modality.

Compare source-derived and representation-derived graphs with a preregistered graph distance, weighted so that clinically meaningful relation types are not overwhelmed by trivial node counts.

Possible starting metrics:

- normalized graph edit distance;
- relation-level precision / recall / F1;
- weighted edge Jaccard similarity.

### 3.3 Context fidelity (F_{ctx})

Context loss is operationalized as the increase in misclassification or interpretive disagreement after contextual qualifiers are removed.

For an episode (j):

[
D_{ctx,j} = L(y_j,hat y_j^{compressed})-L(y_j,hat y_j^{context})
]

where (y_j) is an expert-adjudicated interpretation and (L) is a preregistered loss.

This directly tests whether ordinary experiences, medication effects, psychotic phenomena and subtle self-disorders are conflated by compression.

### 3.4 Temporal fidelity (F_{temp})

Measure preservation of:

- event order;
- duration;
- recurrence;
- state transitions;
- lead/lag relationships;
- episodic versus trait-like character.

For repeated observations, compare transition matrices or event sequences rather than only marginal symptom totals.

### 3.5 Participant fidelity (F_{pers})

After blinded reconstruction, participants judge whether a representation preserves what they meant.

Use structured ratings and discrepancy interviews.

This is not treated as infallible ground truth. It is one indispensable constraint among several.

## 4. Reliability is separate from fidelity

A measure can be highly reliable and faithfully reproduce the same distortion.

Therefore report separately:

- inter-rater reliability;
- test-retest reliability when theoretically appropriate;
- parameter recovery for computational models;
- fidelity vector (F).

Do not use reliability as a substitute for meaning preservation.

## 5. Construct and cross-modal validity

Define:

[
V(Z) = (V_{conv},V_{disc},V_{beh},V_{neuro},V_{interv})
]

for convergent, discriminant, behavioral, neural and intervention validity.

These variables **must not** be folded into the definition of phenomenological fidelity.

A neural correlate can constrain a model without proving that a compressed description captured the experience correctly.

## 6. Predictive utility

For longitudinal data:

[
U_{pred}(Z)= -L(Y_{t+h},hat Y_{t+h}|Z_{le t})
]

Evaluate with rolling-origin or forward-chaining validation.

Targets should include multiple clinically meaningful outcomes:

- future first-person states;
- functional change;
- relapse / crisis indicators;
- intervention response;
- participant-valued outcomes.

Prediction of administrative diagnosis alone is insufficient.

## 7. Burden / representation rate

Define a burden vector rather than only file size:

[
C(Z)=(C_{bits},C_{time},C_{participant},C_{expert},C_{compute})
]

where components quantify:

- description length / dimensionality;
- acquisition time;
- participant burden;
- expert annotation time;
- computational cost.

This prevents a 3-hour specialist interview and a 2-minute questionnaire from being treated as equally costly.

## 8. Fidelity frontier

For representation (Z), retain the multi-objective tuple:

[
M(Z)={F(Z),V(Z),U_{pred}(Z),C(Z)}
]

A representation is dominated if another representation has:

- no lower fidelity;
- no worse validity;
- no worse prediction;
- no greater burden;

with at least one strict improvement.

The remaining representations form the empirical **fidelity frontier**.

No overall winner should be declared unless a use case supplies explicit, preregistered utility weights.

## 9. Rate-distortion formulation

A restricted information-theoretic version can be studied as:

[
R(D)=min_{p(z|x):mathbb{E}[d(X,hat X)]le D} I(X;Z)
]

But (d) must not default to generic token overlap or mean-squared error.

For psychopathology, (d) should be built from the preregistered fidelity components above.

A perception-aware extension can compare source and reconstructed distributions, but distributional similarity must not replace person-level semantic fidelity.

## 10. Dynamic generative layer

For longitudinal modeling, define latent state (s_{it}):

[
s_{i,t+1}=f_i(s_{it},e_{it},u_{it})+epsilon_{it}
]

[
y_{it}=g_i(s_{it})+eta_{it}
]

where:

- (e): environmental/contextual input;
- (u): intervention or perturbation;
- (y): multimodal observations.

Candidate models:

- VAR / dynamic network baseline;
- Kalman / switching state-space models;
- hierarchical Bayesian state-space models;
- PLRNN / nonlinear state-space models;
- Gaussian-process state-space models;
- active-inference / POMDP models where justified;
- sequence models as predictive comparators.

The mechanistic model is selected by predictive adequacy, parameter recovery, cross-level constraint and interpretability — not by theoretical fashion.

## 11. Idiographic + population hierarchy

Use partial pooling:

[
	heta_i sim mathcal{N}(mu_	heta,Sigma_	heta)
]

Each person receives individual parameters while the population informs priors.

Compare:

1. fully pooled;
2. diagnosis-stratified;
3. hierarchical transdiagnostic;
4. person-specific models.

The empirical question is how much individual structure is lost by each pooling level.

## 12. Falsification criteria

The central proposal is weakened if:

- coarse representations preserve source semantics and relations as well as richer ones at much lower burden;
- participant-confirmed phenomenological detail adds no incremental prediction, construct validity or intervention information;
- fidelity metrics fail to show acceptable inter-rater reliability;
- the frontier is unstable across sites, languages or raters;
- richer representations merely encode verbosity without preserving reproducible structure;
- person-specific models do not outperform appropriately regularized population models in held-out longitudinal data.

## 13. Non-negotiable safeguards

- immutable provenance pointers from every code back to source;
- uncertainty stored explicitly;
- no forced assignment when evidence is ambiguous;
- no deletion of source layer after coding;
- no diagnosis inferred from a single computational parameter;
- no claim that brain data adjudicate subjective meaning on their own;
- no synthetic or LLM-generated material presented as participant evidence.
