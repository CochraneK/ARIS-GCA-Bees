# ARIS4C009 · Model specification

## 1. Separate the unobserved state, acquisition process and encoding process

Let (H_{it}) denote the lived mental state of person (i) at time (t).

(H) is not directly observable and is never treated as empirical ground truth.

For acquisition method (m):

[
X^{(m)}_{it}=A_m(H_{it},C_{it},I^{(m)}_{it})+epsilon^{(m)}_{it}
]

where:

- (A_m) = elicitation/acquisition method;
- (C) = relevant context;
- (I^{(m)}) = interaction/process features such as interviewer probing, item wording, response format and rapport;
- (epsilon^{(m)}) = acquisition noise/omission.

Examples of (m):

- phenomenological interview;
- participant self-report;
- conventional symptom interview;
- EMA;
- behavioral task;
- passive sensing;
- EEG/fMRI/physiology.

For representation method (k):

[
Z^{(m,k)}_{it}=E_k(X^{(m)}_{it})+eta^{(m,k)}_{it}
]

where (E_k) maps evidence into a coded/quantitative representation and (eta) denotes encoding error or omission.

This decomposition is central:

[
	ext{observed difference} 
eq 	ext{encoding loss alone}
]

when both (A_m) and (E_k) change.

## 2. Two distinct empirical benchmarks

### 2.1 009A1 · Same-source encoding benchmark

Fix one source record (X^{(m_0)}), initially a rich phenomenological interview record.

Generate multiple encodings from that same source:

- **R0:** rich source record;
- **R1:** structured phenomenological episode graph;
- **R2:** trained-rater phenomenological codes;
- **R3P:** questionnaire-format projection from the same source;
- **R4P:** conventional symptom-code projection from the same source;
- **R5:** low-dimensional quantitative/latent representation;
- **R6 exploratory:** frozen LLM-assisted structured representation.

R3P and R4P are **projections**, not actual participant-completed measures.

009A1 estimates encoding/representation loss conditional on one acquisition method.

### 2.2 009A2 · Acquisition benchmark

Collect genuinely different (X^{(m)}) from the same participant using multiple acquisition methods.

Examples:

- EASE/EAWE/STEP-style interview;
- participant-completed self-report;
- conventional symptom assessment;
- EMA.

009A2 estimates acquisition/process divergence and cannot assume one method is a neutral readout of (H).

Order, interval, symptom/state change, practice, priming and interviewer effects must be recorded and modeled.

## 3. Source-grounded fidelity vector

For 009A1, report:

[
F(Z)=(F_{sem},F_{rel},F_{ctx},F_{temp},F_{pers})
]

### 3.1 Semantic fidelity

Use an independently constructed, preregistered query bank.

For categorical questions:

[
F_{sem}^{strict}=rac{1}{|Q|}sum_q I(hat y_q=y_q)
]

When adjudication is uncertain, use admissible answer sets or probability distributions and proper scoring rules.

### 3.2 Relational fidelity

Represent source episodes as relation graphs and compare reconstruction using:

- edge precision;
- edge recall;
- edge F1;
- relation-type confusion.

Graph-edit distance is secondary.

### 3.3 Context fidelity

Use context-ablation contrasts:

[
D_{ctx}=L(hat y_{without context},y)-L(hat y_{with context},y)
]

### 3.4 Temporal fidelity

Measure event-order concordance, duration, recurrence and transition preservation.

### 3.5 Participant-endorsed fidelity

Where feasible, participants evaluate whether blinded reconstructions preserve intended meaning.

Participant endorsement is a constraint, not infallible ground truth.

## 4. Reliability is separate from fidelity

A representation can reliably reproduce the same distortion.

Report separately:

- inter-rater reliability;
- test-retest reliability where appropriate;
- parameter recovery;
- fidelity vector.

## 5. Intended-use validity

Modern validity logic is use-dependent.

Define:

[
V_{use}(Z,u)
]

where (u) may be:

- rich description;
- screening;
- diagnosis;
- mechanism;
- prediction;
- monitoring;
- intervention selection.

A measure is not declared invalid simply because it omits information irrelevant to its intended use.

Therefore:

- source-reconstruction fidelity is one empirical property;
- intended-use validity is another;
- omissions count as "distortion" only when preservation is part of the target representation claim or shared task.

## 6. Purpose-conditioned utility

For use (u):

[
U(Z,u)
]

may include:

- diagnostic discrimination;
- future-state prediction;
- relapse forecasting;
- functional outcome prediction;
- participant-valued outcomes;
- intervention-response prediction.

Prediction of administrative labels alone is insufficient for broad mechanistic claims.

## 7. Burden / rate

Define:

[
C(Z)=(C_{bits},C_{time},C_{participant},C_{expert},C_{compute})
]

Keep acquisition burden and encoding burden distinct.

A 3-hour interview plus 5-minute coding is not cost-equivalent to a 5-minute questionnaire plus no expert coding.

## 8. Use-conditioned fidelity frontier

For representation (Z) and use (u):

[
M(Z,u)={F(Z),R(Z),V_{use}(Z,u),U(Z,u),C(Z)}
]

A representation is dominated only within an explicitly specified comparison set/use case.

No universal winner is declared.

## 9. Rate-distortion formulation

For 009A1:

[
R(D)=min_{p(z|x):mathbb{E}[d(X,hat X)]le D} I(X;Z)
]

The distortion function (d) is built from preregistered semantic, relational, contextual and temporal reconstruction losses.

This formulation applies to **encoding of a fixed source**. It must not be used to claim that differences between independently acquired interview and self-report records are purely compression effects.

## 10. Dynamic generative layer

For later longitudinal work:

[
s_{i,t+1}=f_i(s_{it},e_{it},u_{it})+epsilon_{it}
]

[
y_{it}=g_i(s_{it})+eta_{it}
]

Candidate models include:

- VAR/dynamic networks;
- switching state-space models;
- hierarchical Bayesian state-space models;
- PLRNN/nonlinear state-space models;
- Gaussian-process state-space models;
- active-inference/POMDP models where justified;
- sequence models as predictive comparators.

## 11. Idiographic + population hierarchy

Use partial pooling:

[
	heta_i sim mathcal{N}(mu_	heta,Sigma_	heta)
]

Compare fully pooled, diagnosis-stratified, hierarchical transdiagnostic and person-specific models.

## 12. Strong falsification

The central program is weakened if:

- coarse same-source projections preserve source semantics and relations as well as richer encodings at much lower burden;
- richer representations add no reproducible value beyond verbosity;
- fidelity metrics remain unreliable after calibration;
- participant meaning checks systematically conflict with source-derived fidelity;
- findings depend mainly on evaluator theoretical background;
- the apparent "loss" disappears once acquisition and encoding are properly separated;
- intended-use validity favors simpler tools for the use case despite their lower narrative fidelity.

## 13. Non-negotiable safeguards

- every derived code retains source provenance where ethically possible;
- uncertainty remains explicit;
- no forced assignment under genuine ambiguity;
- no synthetic/LLM output is presented as participant evidence;
- brain data do not adjudicate subjective meaning by themselves;
- diagnosis is not treated as a failed narrative representation;
- actual self-report is not conflated with a source-derived questionnaire-format projection.
