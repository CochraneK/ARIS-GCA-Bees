# ARIS4C009A1 · Fidelity metric specification

## Purpose

009A1 operationalizes **source-grounded representation fidelity** while keeping acquisition fixed.

The central rule is:

> Representations are evaluated by reconstruction tasks generated independently from the representations.

A long source record may preserve more information, but the experiment must also ask whether its advantage survives rate and burden matching.

## 1. Scope

009A1 compares representations generated from the **same fixed source evidence**.

Primary labels:

- R0 rich source;
- R1 structured episode graph;
- R2 phenomenological code;
- R3P questionnaire-format projection;
- R4P conventional symptom-code projection;
- R5 compact quantitative representation;
- R6 exploratory frozen LLM representation.

R3P is not participant self-report.  
R4P is not an independently administered clinical interview.

Actual acquisition-method differences belong to 009A2.

## 2. Three-panel architecture

### Panel A · Query constructors

Sees source evidence only.

Constructs candidate semantic, relational, contextual and temporal questions.

### Panel B · Source adjudicators

Sees source evidence and candidate questions.

Establishes:

- answerability;
- reference answer/admissible answer set;
- uncertainty;
- criticality;
- provenance.

### Panel C · Representation evaluators

Sees one representation of an episode.

Does not see:

- source;
- competing representations;
- hypothesized ordering.

## 3. Query admissibility

A confirmatory query must:

1. be supported by source evidence;
2. be adjudicable or explicitly uncertain;
3. avoid representation-specific vocabulary unless definitions are common;
4. have frozen scoring;
5. survive redundancy screening.

## 4. Fidelity vector

[
F(R)=(F_{sem},F_{rel},F_{ctx},F_{temp},F_{pers})
]

### Semantic fidelity

For point categorical references:

[
F_{sem}^{strict}=rac{1}{Q}sum_q I(hat y_q=y_q)
]

For uncertain source references, use admissible sets or probability distributions and proper scoring rules.

### Relational fidelity

Primary:

- edge precision;
- edge recall;
- edge F1;
- relation confusion matrix.

Graph-edit distance is secondary.

### Context fidelity

For context-ablation variants:

[
D_{ctx}=L(hat y_{without},y)-L(hat y_{with},y)
]

### Temporal fidelity

Report separately:

- order concordance;
- duration error;
- recurrence classification;
- transition preservation.

### Participant-endorsed fidelity

Where feasible:

- meaning preserved;
- important omission;
- important distortion;
- unacceptable reinterpretation.

Participant endorsement is a constraint, not infallible truth.

## 5. Source uncertainty

Reference state may be:

- point answer;
- admissible set;
- probability distribution;
- unresolved;
- not answerable.

Preserving uncertainty is not an error.

## 6. Reliability gate

Reliability is not fidelity.

Report:

- percent agreement;
- Gwet AC1/AC2 for categorical adjudication;
- ICC for continuous/ordinal components;
- relation-level rater F1;
- probabilistic calibration.

Pilot thresholds are engineering gates and are frozen only after pilot calibration.

## 7. Criticality weighting

Before representation evaluation, source adjudicators may label questions low/medium/high criticality.

Report both:

- unweighted fidelity;
- preregistered criticality-weighted fidelity.

Weighted results never replace unweighted results.

## 8. Fairness to representation bandwidth

### 8.1 Raw frontier

Report observed fidelity and costs.

### 8.2 Equal-description-rate analysis

Estimate representation rate using defensible common measures such as:

- tokens/characters;
- structured-field count;
- dimensionality;
- compressed description length where justified.

Compare representations over overlapping rates.

### 8.3 Encoding-burden analysis

Since the acquisition source is fixed in 009A1, compare:

- coder/expert time;
- compute time/cost;
- storage/representation complexity.

### 8.4 Real-world total-burden analysis

For intended deployment, report:

[
C_{total}=C_{acquisition}+C_{encoding}
]

but label this a deployment comparison, not the manipulated factor in A1.

### 8.5 Controlled budget curves

Where possible, generate frozen budget variants before evaluation.

Estimate:

[
F_R(b)
]

where (b) is representation budget.

## 9. Ontology-favoritism controls

Query bank combines:

1. phenomenology-informed questions;
2. conventional clinical questions;
3. domain-general factual/relational questions;
4. participant-generated preservation questions.

Report performance by query origin.

## 10. Evaluator-background controls

Record evaluator background:

- phenomenological psychopathology;
- conventional psychiatry;
- computational psychiatry;
- psychology/neuroscience;
- trained non-specialist.

Test:

[
representation 	imes evaluator_background
]

## 11. Confidence, calibration and abstention

Allow:

> cannot infer from this representation.

Report:

- coverage;
- accuracy conditional on answer;
- Brier/proper score;
- calibration;
- overconfidence.

Sparse representations are not forced to guess.

## 12. Primary hierarchical model

[
logit(P(Y=1))=
eta_0+eta_R+eta_D+eta_{R	imes D}
+u_{participant}+u_{episode}+u_{query}+u_{evaluator}
]

Include query origin and evaluator background if preregistered.

## 13. Intended-use validity is separate

A representation may have low source fidelity but strong performance for a defined use.

For use (u):

[
V_{use}(R,u),quad U(R,u)
]

Fidelity is never silently redefined as clinical usefulness.

## 14. Minimum confirmatory output set

1. semantic reconstruction score;
2. relation F1;
3. context-ablation loss;
4. temporal-order concordance;
5. encoding burden/rate.

Participant-endorsed fidelity is key secondary output where recontact is feasible.

## 15. Metric falsification

Revise the metric architecture if:

- question origin determines results;
- reliability remains poor;
- representation differences vanish under rate matching;
- participant meaning checks systematically disagree;
- reasonable scoring rules reverse results;
- evaluator background determines ordering;
- query redundancy inflates apparent precision.
